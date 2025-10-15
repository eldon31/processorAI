"""Pydantic configuration models for the consolidated knowledge pipeline."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from src.ingestion.chunker import ChunkingConfig


class ToolkitSettings(BaseModel):
    """Global settings for the knowledge ingestion toolkit."""

    embedding_model: str = Field(
        default=os.getenv("EMBEDDING_MODEL", "nomic-ai/nomic-embed-code"),
        description="Sentence-transformers model to use for embeddings.",
    )
    embedding_device: str = Field(
        default=os.getenv("EMBEDDING_DEVICE", "cpu"),
        description="Torch device identifier (cpu/cuda/mps).",
    )
    embedding_batch_size: int = Field(
        default=int(os.getenv("EMBEDDING_BATCH_SIZE", "8")),
        ge=1,
        le=128,
        description="Batch size when encoding chunks.",
    )
    chunk_max_tokens: int = Field(
        default=int(os.getenv("CHUNK_MAX_TOKENS", "2048")),
        ge=128,
        description="Target maximum tokens per chunk.",
    )
    chunk_overlap: int = Field(
        default=int(os.getenv("CHUNK_OVERLAP", "100")),
        ge=0,
        description="Token overlap between consecutive chunks.",
    )
    chunk_min_size: int = Field(
        default=int(os.getenv("CHUNK_MIN_SIZE", "100")),
        ge=10,
        description="Minimum characters allowed per chunk.",
    )
    qdrant_host: str = Field(default=os.getenv("QDRANT_HOST", "localhost"))
    qdrant_port: int = Field(default=int(os.getenv("QDRANT_PORT", "6333")))
    default_collection: str = Field(
        default=os.getenv("QDRANT_COLLECTION", "knowledge_base"),
        description="Fallback Qdrant collection name when none is provided by a collection config.",
    )
    enable_quantization: bool = Field(default=True, description="Whether to enable int8 quantization.")
    ingest_to_qdrant: bool = Field(
        default=True,
        description="If False, embeddings are only written to disk and not pushed to Qdrant.",
    )
    output_root: Path = Field(
        default=Path(os.getenv("TOOLKIT_OUTPUT_ROOT", "output/collections")),
        description="Folder where embedded chunk files will be written.",
    )
    download_root: Path = Field(
        default=Path(os.getenv("TOOLKIT_DOWNLOAD_ROOT", "data/downloads")),
        description="Folder where remote documents are downloaded before processing.",
    )

    def build_chunk_config(self) -> ChunkingConfig:
        """Create the default chunking configuration."""

        return ChunkingConfig(
            max_tokens=self.chunk_max_tokens,
            chunk_overlap=self.chunk_overlap,
            min_chunk_size=self.chunk_min_size,
        )


class DocumentItem(BaseModel):
    """Description of a document to ingest into the knowledge base."""

    id: str = Field(..., description="Unique identifier for the document.")
    path: Optional[Path] = Field(
        default=None,
        description="Local path to the document, relative or absolute.",
    )
    url: Optional[str] = Field(
        default=None,
        description="Optional HTTP(S) URL for downloading the document if a local path is not provided.",
    )
    category: str = Field(default="general", description="High-level category for organisation.")
    subcategory: Optional[str] = Field(default=None, description="Optional subcategory label.")
    tags: List[str] = Field(default_factory=list, description="Arbitrary tags for the document.")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata to attach.")
    ingest: bool = Field(default=True, description="Whether to push the embeddings into Qdrant.")
    output_file: Optional[str] = Field(
        default=None,
        description="Override for the output JSON filename. Defaults to '<id>_embedded.json'.",
    )
    chunk_config: Optional[ChunkingConfig] = Field(
        default=None,
        description="Optional per-document chunking overrides.",
    )

    @model_validator(mode="before")
    def _validate_location(cls, values):
        data = dict(values)
        if not data.get("path") and not data.get("url"):
            raise ValueError("A DocumentItem requires either a 'path' or a 'url'.")
        return values

    @field_validator("path", mode="before")
    def _expand_path(cls, value: Optional[Any]) -> Optional[Path]:
        if value is None:
            return None
        return Path(value).expanduser()


class CollectionConfig(BaseModel):
    """Batch definition for ingesting related documents."""

    name: str = Field(..., description="Human friendly name for the collection batch.")
    slug: Optional[str] = Field(
        default=None,
        description="Optional slug used for output folder names. Defaults to a sanitised name.",
    )
    description: Optional[str] = Field(default=None)
    qdrant_collection: Optional[str] = Field(
        default=None,
        description="Override Qdrant collection name for this batch.",
    )
    embedder_model: Optional[str] = Field(
        default=None,
        description="Override embedding model for this collection.",
    )
    chunk_config: Optional[ChunkingConfig] = Field(
        default=None,
        description="Optional shared chunking overrides for all documents in the collection.",
    )
    documents: List[DocumentItem] = Field(..., description="Documents included in the batch.")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Extra metadata inherited by documents.")

    @field_validator("documents")
    def _ensure_documents(cls, value: List[DocumentItem]) -> List[DocumentItem]:
        if not value:
            raise ValueError("CollectionConfig.documents must contain at least one DocumentItem.")
        return value

    def resolved_slug(self) -> str:
        """Return a filesystem-safe slug for the collection."""

        base = self.slug or self.name.lower().strip().replace(" ", "-")
        return "".join(c for c in base if c.isalnum() or c in {"-", "_"})
