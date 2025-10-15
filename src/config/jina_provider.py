"""
Sentence-Transformers Embedding Provider

Provides local embeddings using sentence-transformers library.
No API calls needed - runs locally with batching support.

Recommended Models for Code/Documentation:
- nomic-ai/nomic-embed-code (1536 dim, BEST for code, APIs, workflows)
- jinaai/jina-embeddings-v2-base-code (768 dim, code-specific)
- sentence-transformers/all-MiniLM-L6-v2 (384 dim, fast, general purpose)
- codellama/CodeLlama-7b-Instruct-hf (4096 dim, very specialized)

For your use case (code/docs/workflows): nomic-ai/nomic-embed-code
"""

import logging
import os
from typing import List, Optional
import asyncio

from sentence_transformers import SentenceTransformer
from pydantic import BaseModel, Field
import torch

logger = logging.getLogger(__name__)


class EmbedderConfig(BaseModel):
    """Configuration for sentence-transformers embeddings."""
    
    model_name: str = Field(
        default="nomic-ai/nomic-embed-code",
        description="Sentence-transformers model name (nomic-embed-code for code/APIs)"
    )
    device: str = Field(
        default="cpu",
        description="Device to run model on (cpu/cuda/mps)"
    )
    batch_size: int = Field(
        default=32,
        description="Batch size for encoding",
        ge=1,
        le=256
    )
    normalize_embeddings: bool = Field(
        default=True,
        description="Normalize embeddings to unit length"
    )
    show_progress_bar: bool = Field(
        default=False,
        description="Show progress bar during encoding"
    )
    
    @classmethod
    def from_env(cls) -> "EmbedderConfig":
        """Create config from environment variables."""
        return cls(
            model_name=os.getenv("EMBEDDING_MODEL", "nomic-ai/nomic-embed-code"),
            device=os.getenv("EMBEDDING_DEVICE", "cpu"),
            batch_size=int(os.getenv("EMBEDDING_BATCH_SIZE", "32")),
        )


class SentenceTransformerEmbedder:
    """
    Sentence-transformers embedding client for local embeddings.
    
    Features:
    - No API calls - runs locally
    - Automatic batching for efficiency
    - GPU support (CUDA/MPS)
    - Multiple model options
    
    Usage:
        embedder = SentenceTransformerEmbedder(config)
        embeddings = await embedder.embed_texts(["text1", "text2"])
    """
    
    def __init__(self, config: Optional[EmbedderConfig] = None):
        """
        Initialize sentence-transformers embedder.
        
        Args:
            config: Optional config, defaults to env-based config
        """
        self.config = config or EmbedderConfig.from_env()
        
        # Auto-detect device if not specified
        if self.config.device == "auto":
            if torch.cuda.is_available():
                self.config.device = "cuda"
            elif torch.backends.mps.is_available():
                self.config.device = "mps"
            else:
                self.config.device = "cpu"
        
        # Load model
        logger.info(f"Loading sentence-transformers model: {self.config.model_name}")
        
        # Special handling for Nomic models (require trust_remote_code)
        if "nomic" in self.config.model_name.lower():
            self.model = SentenceTransformer(
                self.config.model_name,
                device=self.config.device,
                trust_remote_code=True  # Required for Nomic models
            )
        else:
            self.model = SentenceTransformer(
                self.config.model_name,
                device=self.config.device
            )
        
        logger.info(
            f"Embedder initialized (model={self.config.model_name}, "
            f"device={self.config.device}, dim={self.get_dimension()})"
        )
    
    async def embed_texts(
        self,
        texts: List[str],
        task: str = "search_document"  # For Nomic: "search_document" or "search_query"
    ) -> List[List[float]]:
        """
        Generate embeddings for texts using sentence-transformers.
        
        Args:
            texts: List of text strings to embed
            task: Task type for Nomic models:
                - "search_document": For documents/chunks (default)
                - "search_query": For search queries
                - "clustering": For clustering tasks
                - "classification": For classification tasks
        
        Returns:
            List of embedding vectors (one per text)
        """
        if not texts:
            return []
        
        # Run encoding in thread pool to avoid blocking event loop
        loop = asyncio.get_event_loop()
        
        # Nomic models support task prefixes for better retrieval
        if "nomic" in self.config.model_name.lower():
            # Map generic task names to Nomic prompt identifiers
            prompt_map = {
                "search_document": "document",
                "search_query": "query",
                "clustering": "document",
                "classification": "document",
            }
            prompt_name = prompt_map.get(task, "document")
            
            embeddings = await loop.run_in_executor(
                None,
                lambda: self.model.encode(
                    texts,
                    batch_size=self.config.batch_size,
                    show_progress_bar=self.config.show_progress_bar,
                    normalize_embeddings=self.config.normalize_embeddings,
                    convert_to_numpy=True,
                    prompt_name=prompt_name  # Nomic-specific
                )
            )
        else:
            # Standard sentence-transformers encoding
            embeddings = await loop.run_in_executor(
                None,
                lambda: self.model.encode(
                    texts,
                    batch_size=self.config.batch_size,
                    show_progress_bar=self.config.show_progress_bar,
                    normalize_embeddings=self.config.normalize_embeddings,
                    convert_to_numpy=True
                )
            )
        
        # Convert to list of lists
        embeddings_list = embeddings.tolist()
        
        logger.debug(
            f"Generated {len(embeddings_list)} embeddings "
            f"(dim={len(embeddings_list[0]) if embeddings_list else 0})"
        )
        
        return embeddings_list
    
    async def embed_query(self, query: str) -> List[float]:
        """
        Embed a search query.
        
        Args:
            query: Search query text
        
        Returns:
            Embedding vector for the query
        """
        embeddings = await self.embed_texts([query], task="search_query")
        return embeddings[0] if embeddings else []
    
    async def embed_documents(self, documents: List[str]) -> List[List[float]]:
        """
        Embed document chunks (alias for embed_texts).
        
        Args:
            documents: List of document text chunks
        
        Returns:
            List of embedding vectors
        """
        return await self.embed_texts(documents, task="search_document")
    
    def get_dimension(self) -> int:
        """Get embedding dimension for the current model."""
        # Get dimension from loaded model
        dimension = self.model.get_sentence_embedding_dimension()
        return int(dimension) if dimension is not None else 0
    
    async def close(self):
        """Cleanup resources (no-op for local models)."""
        pass
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


async def create_embedder(model_name: Optional[str] = None) -> SentenceTransformerEmbedder:
    """
    Factory function to create sentence-transformers embedder.
    
    Args:
        model_name: Optional model name, uses env var if not provided
    
    Returns:
        Configured SentenceTransformerEmbedder instance
    """
    if model_name:
        config = EmbedderConfig(model_name=model_name)
    else:
        config = EmbedderConfig.from_env()
    
    return SentenceTransformerEmbedder(config)
