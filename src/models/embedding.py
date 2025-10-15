"""
Embedding model with vector dimension validation (768/1536/3072).

Represents a vector embedding for semantic search.
"""

from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, field_validator, computed_field


class Embedding(BaseModel):
    """
    Embedding model representing a vector embedding.

    Attributes:
        id: Unique embedding identifier
        chunk_id: Reference to source chunk
        vector: Embedding vector (768/1536/3072 dimensions)
        model_version: Embedding model used (e.g., text-embedding-3-small)
        created_at: Embedding generation timestamp
    """

    id: str = Field(..., description="Unique embedding identifier")
    chunk_id: str = Field(..., description="Source chunk ID")
    vector: List[float] = Field(..., description="Embedding vector")
    model_version: str = Field(..., description="Embedding model version")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Generation time")

    @computed_field
    @property
    def dimension(self) -> int:
        """Return the dimension of the embedding vector."""
        return len(self.vector)

    @field_validator("vector")
    @classmethod
    def validate_dimensions(cls, v: List[float]) -> List[float]:
        """
        Validate vector has supported dimensions (768/1536/3072).

        768: BERT-based models
        1536: OpenAI text-embedding-3-small
        3072: OpenAI text-embedding-3-large
        """
        valid_dims = [768, 1536, 3072]
        dim = len(v)
        if dim not in valid_dims:
            raise ValueError(
                f"vector dimension {dim} not supported. Must be one of {valid_dims}"
            )
        return v

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "id": "emb-1",
                "chunk_id": "chunk-1",
                "vector": [0.1] * 1536,  # 1536-dimensional vector
                "model_version": "text-embedding-3-small",
                "created_at": "2025-10-12T10:32:00Z",
            }
        }
