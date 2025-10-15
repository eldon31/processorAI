"""Unified knowledge ingestion pipeline built on top of existing ingestion modules."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional
from urllib.parse import urlparse
from urllib.request import urlretrieve

import os

from src.ingestion.chunker import ChunkingConfig, DoclingHybridChunker, DocumentChunk, create_chunker
from src.ingestion.processor import DocumentProcessor
from src.config.jina_provider import EmbedderConfig, SentenceTransformerEmbedder
from src.storage.qdrant_store import QdrantStore, QdrantStoreConfig
from src.toolkit.config import CollectionConfig, DocumentItem, ToolkitSettings

logger = logging.getLogger(__name__)


@dataclass
class DocumentResult:
    """Summary of a processed document."""

    document_id: str
    collection: str
    category: str
    subcategory: Optional[str]
    local_path: Path
    chunks: int
    embeddings: int
    output_path: Path
    qdrant_ids: List[str]
    error: Optional[str] = None
    warnings: List[str] = field(default_factory=list)


@dataclass
class CollectionResult:
    """Summary of an entire collection run."""

    collection: CollectionConfig
    documents: List[DocumentResult]

    @property
    def succeeded(self) -> int:
        return sum(1 for doc in self.documents if doc.error is None)

    @property
    def failed(self) -> int:
        return sum(1 for doc in self.documents if doc.error is not None)


class KnowledgeToolkit:
    """High-level orchestrator that chains document processing, chunking, embedding, and ingestion."""

    def __init__(self, settings: Optional[ToolkitSettings] = None):
        self.settings = settings or ToolkitSettings()
        self.processor = DocumentProcessor()
        self._default_chunk_config = self.settings.build_chunk_config()
        self._chunker_cache: Dict[str, DoclingHybridChunker] = {}
        self._embedder_cache: Dict[str, SentenceTransformerEmbedder] = {}
        self._qdrant_cache: Dict[str, QdrantStore] = {}

        # Ensure folders exist up-front
        self.settings.output_root.mkdir(parents=True, exist_ok=True)
        self.settings.download_root.mkdir(parents=True, exist_ok=True)

    async def run_collections(self, collections: Iterable[CollectionConfig]) -> List[CollectionResult]:
        """Process multiple collections sequentially."""

        results: List[CollectionResult] = []
        for collection in collections:
            collection_result = await self.run_collection(collection)
            results.append(collection_result)
        return results

    async def run_collection(self, collection: CollectionConfig) -> CollectionResult:
        """Process a single collection definition."""

        logger.info("Processing collection '%s'", collection.name)
        tasks = []
        for item in collection.documents:
            tasks.append(self._process_document(collection, item))

        documents = []
        for coro in tasks:
            documents.append(await coro)

        logger.info(
            "Collection '%s' complete (%s success, %s failed)",
            collection.name,
            sum(1 for doc in documents if doc.error is None),
            sum(1 for doc in documents if doc.error is not None),
        )
        return CollectionResult(collection=collection, documents=documents)

    async def _process_document(self, collection: CollectionConfig, item: DocumentItem) -> DocumentResult:
        """Process an individual document from the collection."""

        local_path = self._resolve_local_path(item)
        logger.info("Processing document '%s' (%s)", item.id, local_path)

        try:
            processed_document = self.processor.process_file(str(local_path))
            document_metadata = processed_document.metadata.model_dump(mode="json")
            model_name = collection.embedder_model or self.settings.embedding_model
            chunker = self._get_chunker(item.chunk_config or collection.chunk_config, model_name)
            chunks = await chunker.chunk_document(
                content=processed_document.content,
                title=processed_document.metadata.title or item.id,
                source=str(local_path),
                metadata={
                    **document_metadata,
                    **collection.metadata,
                    **item.metadata,
                    "category": item.category,
                    "subcategory": item.subcategory,
                },
                docling_doc=processed_document.docling_document,
            )

            if not chunks:
                raise RuntimeError("No chunks produced for document")

            embedder = self._get_embedder(model_name)
            texts = [chunk.content for chunk in chunks]
            embeddings = await embedder.embed_documents(texts)

            if len(embeddings) != len(chunks):
                raise RuntimeError(
                    f"Embedding count mismatch (chunks={len(chunks)} embeddings={len(embeddings)})"
                )

            output_path = self._write_output(collection, item, chunks, embeddings, local_path)

            qdrant_ids: List[str] = []
            warnings: List[str] = []
            if item.ingest and self.settings.ingest_to_qdrant:
                try:
                    qdrant_store = self._get_qdrant_store(
                        collection_name=collection.qdrant_collection or self.settings.default_collection,
                        vector_size=len(embeddings[0]),
                    )
                    qdrant_ids = self._ingest_to_qdrant(
                        collection=collection,
                        item=item,
                        chunks=chunks,
                        embeddings=embeddings,
                        qdrant_store=qdrant_store,
                        document_metadata=document_metadata,
                    )
                except Exception as ingest_error:  # pylint: disable=broad-except
                    warning = f"Qdrant ingest skipped: {ingest_error}"
                    logger.warning(warning)
                    warnings.append(warning)

            return DocumentResult(
                document_id=item.id,
                collection=collection.name,
                category=item.category,
                subcategory=item.subcategory,
                local_path=local_path,
                chunks=len(chunks),
                embeddings=len(embeddings),
                output_path=output_path,
                qdrant_ids=qdrant_ids,
                warnings=warnings,
            )

        except Exception as exc:  # pylint: disable=broad-except
            logger.exception("Failed to process document '%s': %s", item.id, exc)
            return DocumentResult(
                document_id=item.id,
                collection=collection.name,
                category=item.category,
                subcategory=item.subcategory,
                local_path=local_path,
                chunks=0,
                embeddings=0,
                output_path=self._expected_output_path(collection, item),
                qdrant_ids=[],
                error=str(exc),
                warnings=[],
            )

    def _resolve_local_path(self, item: DocumentItem) -> Path:
        if item.path:
            return item.path.resolve()

        assert item.url, "DocumentItem.url should exist when path is not provided"
        parsed = urlparse(item.url)
        extension = Path(parsed.path).suffix or ".md"
        filename = f"{item.id}{extension}"
        destination = self.settings.download_root / filename
        if not destination.exists():
            logger.info("Downloading %s -> %s", item.url, destination)
            urlretrieve(item.url, destination)  # nosec - trusted manual inputs
        return destination

    def _get_chunker(
        self,
        config_override: Optional[ChunkingConfig],
        model_name: str,
    ) -> DoclingHybridChunker:
        config = config_override or self._default_chunk_config
        cache_key = f"{json.dumps(config.model_dump(), sort_keys=True)}|{model_name}"
        if cache_key not in self._chunker_cache:
            previous = os.environ.get("EMBEDDING_MODEL")
            os.environ["EMBEDDING_MODEL"] = model_name
            try:
                self._chunker_cache[cache_key] = create_chunker(config)
            finally:
                if previous is not None:
                    os.environ["EMBEDDING_MODEL"] = previous
                else:
                    os.environ.pop("EMBEDDING_MODEL", None)
        return self._chunker_cache[cache_key]

    def _get_embedder(self, model_name: str) -> SentenceTransformerEmbedder:
        cache_key = f"{model_name}:{self.settings.embedding_device}:{self.settings.embedding_batch_size}"
        if cache_key not in self._embedder_cache:
            config = EmbedderConfig(
                model_name=model_name,
                device=self.settings.embedding_device,
                batch_size=self.settings.embedding_batch_size,
            )
            self._embedder_cache[cache_key] = SentenceTransformerEmbedder(config)
        return self._embedder_cache[cache_key]

    def _get_qdrant_store(self, collection_name: str, vector_size: int) -> QdrantStore:
        if collection_name not in self._qdrant_cache:
            config = QdrantStoreConfig(
                host=self.settings.qdrant_host,
                port=self.settings.qdrant_port,
                collection_name=collection_name,
                vector_size=vector_size,
                enable_quantization=self.settings.enable_quantization,
            )
            self._qdrant_cache[collection_name] = QdrantStore(config)
        return self._qdrant_cache[collection_name]

    def _expected_output_path(self, collection: CollectionConfig, item: DocumentItem) -> Path:
        category = item.category or "general"
        subcategory = item.subcategory or "misc"
        filename = item.output_file or f"{item.id}_embedded.json"
        return self.settings.output_root / collection.resolved_slug() / category / subcategory / filename

    def _write_output(
        self,
        collection: CollectionConfig,
        item: DocumentItem,
        chunks: List[DocumentChunk],
        embeddings: List[List[float]],
        local_path: Path,
    ) -> Path:
        output_path = self._expected_output_path(collection, item)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        payload = {
            "collection": collection.name,
            "category": item.category,
            "subcategory": item.subcategory,
            "document": {
                "id": item.id,
                "source_path": str(local_path),
                "metadata": item.metadata,
                "collection_metadata": collection.metadata,
            },
            "embedding_model": collection.embedder_model or self.settings.embedding_model,
            "embedding_dimension": len(embeddings[0]) if embeddings else 0,
            "embedded_chunks": [
                {
                    "index": chunk.index,
                    "text": chunk.content,
                    "token_count": chunk.token_count,
                    "metadata": chunk.metadata,
                    "embedding": embedding,
                }
                for chunk, embedding in zip(chunks, embeddings)
            ],
        }

        with output_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False, default=str)

        logger.info("Wrote embedded chunks -> %s", output_path)
        return output_path

    def _ingest_to_qdrant(
        self,
        collection: CollectionConfig,
        item: DocumentItem,
        chunks: List[DocumentChunk],
        embeddings: List[List[float]],
        qdrant_store: QdrantStore,
        document_metadata: Dict[str, object],
    ) -> List[str]:
        ids = [f"{item.id}_chunk_{chunk.index}" for chunk in chunks]

        payloads: List[Dict[str, object]] = []
        for chunk, embedding in zip(chunks, embeddings):
            payloads.append(
                {
                    "document_id": item.id,
                    "document_title": document_metadata.get("title") or item.id,
                    "chunk_index": chunk.index,
                    "chunk_total": chunk.metadata.get("total_chunks"),
                    "category": item.category,
                    "subcategory": item.subcategory,
                    "tags": item.tags,
                    "collection": collection.name,
                    "collection_slug": collection.resolved_slug(),
                    "content": chunk.content,
                    "source_path": document_metadata.get("file_path"),
                    "source_url": item.url,
                    "metadata": {
                        **collection.metadata,
                        **item.metadata,
                        "document": document_metadata,
                    },
                }
            )

        return qdrant_store.add_embeddings(embeddings=embeddings, metadatas=payloads, ids=ids)
