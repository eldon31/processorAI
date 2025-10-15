"""
Docling HybridChunker implementation for intelligent document splitting.

COPIED AND REFACTORED FROM: ottomator-agents/docling-rag-agent/ingestion/chunker.py

This module uses Docling's built-in HybridChunker which combines:
- Token-aware chunking (uses actual tokenizer)
- Document structure preservation (headings, sections, tables)
- Semantic boundary respect (paragraphs, code blocks)
- Contextualized output (chunks include heading hierarchy)

Benefits over custom chunking:
- Fast (no LLM API calls)
- Token-precise (not character-based estimates)
- Better for RAG (chunks include document context)
- Battle-tested (maintained by Docling team)
"""

import logging
import os
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from transformers import AutoTokenizer
from docling.chunking import HybridChunker
from docling_core.types.doc import DoclingDocument

logger = logging.getLogger(__name__)


class ChunkingConfig(BaseModel):
    """
    Configuration for chunking (Pydantic model for validation).
    
    REFACTORED: Changed from dataclass to Pydantic BaseModel for constitution compliance.
    """
    chunk_size: int = Field(default=2048, description="Target characters per chunk (optimized for code)")
    chunk_overlap: int = Field(default=100, description="Character overlap between chunks (reduced for code)")
    max_chunk_size: int = Field(default=4096, description="Maximum chunk size (increased for code context)")
    min_chunk_size: int = Field(default=100, ge=1, description="Minimum chunk size")
    use_semantic_splitting: bool = Field(default=True, description="Use HybridChunker")
    preserve_structure: bool = Field(default=True, description="Preserve document structure")
    max_tokens: int = Field(default=2048, description="Maximum tokens for nomic-embed-code model")

    def model_post_init(self, __context: Any) -> None:
        """Validate configuration after initialization."""
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("chunk_overlap must be less than chunk_size")


class DocumentChunk(BaseModel):
    """
    Represents a document chunk with optional embedding (Pydantic model).
    
    REFACTORED: Changed from dataclass to Pydantic BaseModel.
    Matches src/models/chunk.py interface but with flexibility for ingestion.
    """
    content: str = Field(..., min_length=1, description="Chunk text content")
    index: int = Field(..., ge=0, description="Position in document")
    start_char: int = Field(..., ge=0, description="Start character offset")
    end_char: int = Field(..., gt=0, description="End character offset")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Chunk metadata")
    token_count: Optional[int] = Field(default=None, description="Actual token count")
    embedding: Optional[List[float]] = Field(default=None, description="Optional embedding vector")

    def model_post_init(self, __context: Any) -> None:
        """Calculate token count if not provided."""
        if self.token_count is None:
            # Rough estimation: ~4 characters per token
            self.token_count = len(self.content) // 4


class DoclingHybridChunker:
    """
    Docling HybridChunker wrapper for intelligent document splitting.

    This chunker uses Docling's built-in HybridChunker which:
    - Respects document structure (sections, paragraphs, tables)
    - Is token-aware (fits embedding model limits)
    - Preserves semantic coherence
    - Includes heading context in chunks
    """

    def __init__(self, config: ChunkingConfig):
        """
        Initialize chunker.

        Args:
            config: Chunking configuration (Pydantic model)
        """
        self.config = config

        # Initialize tokenizer for token-aware chunking
        # Use Nomic model tokenizer for consistency with embeddings
        model_id = os.getenv("EMBEDDING_MODEL", "nomic-ai/nomic-embed-code")
        logger.info(f"Initializing tokenizer for code chunking: {model_id}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)

        # Create HybridChunker
        self.chunker = HybridChunker(
            tokenizer=self.tokenizer,
            max_tokens=config.max_tokens,
            merge_peers=True  # Merge small adjacent chunks
        )

        logger.info(f"HybridChunker initialized (max_tokens={config.max_tokens})")

    async def chunk_document(
        self,
        content: str,
        title: str,
        source: str,
        metadata: Optional[Dict[str, Any]] = None,
        docling_doc: Optional[DoclingDocument] = None
    ) -> List[DocumentChunk]:
        """
        Chunk a document using Docling's HybridChunker.

        Args:
            content: Document content (markdown format)
            title: Document title
            source: Document source
            metadata: Additional metadata
            docling_doc: Optional pre-converted DoclingDocument (for efficiency)

        Returns:
            List of document chunks with contextualized content
        """
        if not content.strip():
            return []

        base_metadata = {
            "title": title,
            "source": source,
            "chunk_method": "hybrid",
            **(metadata or {})
        }

        # If we don't have a DoclingDocument, use fallback
        if docling_doc is None:
            logger.warning("No DoclingDocument provided, using simple chunking fallback")
            return self._simple_fallback_chunk(content, base_metadata)

        try:
            # Use HybridChunker to chunk the DoclingDocument
            chunk_iter = self.chunker.chunk(dl_doc=docling_doc)
            chunks = list(chunk_iter)

            # Convert Docling chunks to DocumentChunk Pydantic objects
            document_chunks = []
            current_pos = 0

            for i, chunk in enumerate(chunks):
                # Get contextualized text (includes heading hierarchy)
                contextualized_text = self.chunker.contextualize(chunk=chunk)

                # Count actual tokens
                token_count = len(self.tokenizer.encode(contextualized_text))

                # Create chunk metadata
                chunk_metadata = {
                    **base_metadata,
                    "total_chunks": len(chunks),
                    "token_count": token_count,
                    "has_context": True
                }

                # Estimate character positions
                start_char = current_pos
                end_char = start_char + len(contextualized_text)

                document_chunks.append(DocumentChunk(
                    content=contextualized_text.strip(),
                    index=i,
                    start_char=start_char,
                    end_char=end_char,
                    metadata=chunk_metadata,
                    token_count=token_count
                ))

                current_pos = end_char

            logger.info(f"Created {len(document_chunks)} chunks using HybridChunker")
            return document_chunks

        except Exception as e:
            logger.error(f"HybridChunker failed: {e}, falling back to simple chunking")
            return self._simple_fallback_chunk(content, base_metadata)

    def _simple_fallback_chunk(
        self,
        content: str,
        base_metadata: Dict[str, Any]
    ) -> List[DocumentChunk]:
        """
        Simple fallback chunking when HybridChunker can't be used.

        Args:
            content: Content to chunk
            base_metadata: Base metadata for chunks

        Returns:
            List of document chunks
        """
        chunks = []
        chunk_size = self.config.chunk_size
        overlap = self.config.chunk_overlap

        start = 0
        chunk_index = 0

        while start < len(content):
            end = start + chunk_size

            if end >= len(content):
                chunk_text = content[start:]
            else:
                # Try to end at sentence boundary
                chunk_end = end
                for i in range(end, max(start + self.config.min_chunk_size, end - 200), -1):
                    if i < len(content) and content[i] in '.!?\n':
                        chunk_end = i + 1
                        break
                chunk_text = content[start:chunk_end]
                end = chunk_end

            if chunk_text.strip():
                token_count = len(self.tokenizer.encode(chunk_text))

                chunks.append(DocumentChunk(
                    content=chunk_text.strip(),
                    index=chunk_index,
                    start_char=start,
                    end_char=end,
                    metadata={
                        **base_metadata,
                        "chunk_method": "simple_fallback",
                        "total_chunks": -1
                    },
                    token_count=token_count
                ))

                chunk_index += 1

            start = end - overlap

        # Update total chunks
        for chunk in chunks:
            chunk.metadata["total_chunks"] = len(chunks)

        logger.info(f"Created {len(chunks)} chunks using simple fallback")
        return chunks


def create_chunker(config: ChunkingConfig) -> DoclingHybridChunker:
    """
    Create Docling HybridChunker instance.

    Args:
        config: Chunking configuration (Pydantic model)

    Returns:
        DoclingHybridChunker instance
    """
    return DoclingHybridChunker(config)
