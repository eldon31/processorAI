"""
Ingestion package for document processing pipeline.

Provides Docling-based chunking, embedding generation, and document ingestion orchestration.
"""

from src.ingestion.processor import (
    DocumentProcessor,
    DocumentMetadata,
    ProcessedDocument,
)
from src.ingestion.chunker import (
    ChunkingConfig,
    DocumentChunk,
    DoclingHybridChunker,
    create_chunker,
)
from src.ingestion.embedder import (
    EmbeddingConfig,
    EmbeddingGenerator,
    EmbeddingCache,
    create_embedder,
)
try:
    from src.ingestion.ingest import (  # type: ignore
        IngestionConfig,
        IngestionResult,
        DocumentIngestionPipeline,
    )
except Exception:  # pragma: no cover - optional ingestion extras
    IngestionConfig = None  # type: ignore
    IngestionResult = None  # type: ignore
    DocumentIngestionPipeline = None  # type: ignore

__all__ = [
    "DocumentProcessor",
    "DocumentMetadata",
    "ProcessedDocument",
    "ChunkingConfig",
    "DocumentChunk",
    "DoclingHybridChunker",
    "create_chunker",
    "EmbeddingConfig",
    "EmbeddingGenerator",
    "EmbeddingCache",
    "create_embedder",
    "IngestionConfig",
    "IngestionResult",
    "DocumentIngestionPipeline",
]
