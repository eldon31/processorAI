"""
Entity model with confidence score 0-1 and canonical name normalization.

Represents a named entity extracted from documents.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class EntityType(str, Enum):
    """Types of named entities."""

    PERSON = "person"
    ORGANIZATION = "organization"
    LOCATION = "location"
    TECHNOLOGY = "technology"
    CONCEPT = "concept"
    PRODUCT = "product"
    EVENT = "event"
    OTHER = "other"


class Entity(BaseModel):
    """
    Entity model representing a named entity from knowledge graph.

    Attributes:
        id: Unique entity identifier
        name: Display name of entity
        canonical_name: Normalized lowercase name for matching
        entity_type: Type of entity (person, organization, etc.)
        confidence: Extraction confidence score (0-1)
        mentions: Number of times entity appears across documents
        source_documents: List of document IDs where entity appears
        description: Optional description of entity
        created_at: Entity creation timestamp
        updated_at: Last update timestamp
    """

    id: str = Field(..., description="Unique entity identifier")
    name: str = Field(..., min_length=1, description="Entity display name")
    canonical_name: str = Field(..., min_length=1, description="Normalized name for matching")
    entity_type: EntityType = Field(..., description="Entity type")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    mentions: int = Field(default=1, ge=1, description="Number of mentions")
    source_documents: List[str] = Field(
        default_factory=list, description="Document IDs where entity appears"
    )
    description: Optional[str] = Field(default=None, description="Entity description")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation time")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update time")

    @field_validator("canonical_name", mode="before")
    @classmethod
    def normalize_canonical_name(cls, v: str) -> str:
        """Normalize canonical name to lowercase for consistent matching."""
        if isinstance(v, str):
            return v.lower().strip()
        return v

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "id": "ent-1",
                "name": "Python",
                "canonical_name": "python",
                "entity_type": "technology",
                "confidence": 0.95,
                "mentions": 15,
                "source_documents": ["doc-123", "doc-456"],
                "description": "A high-level programming language",
                "created_at": "2025-10-12T10:33:00Z",
                "updated_at": "2025-10-12T10:33:00Z",
            }
        }
