"""
Relationship model with self-reference prevention and evidence tracking.

Represents a connection between two entities in the knowledge graph.
"""

from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel, Field, model_validator


class RelationshipType(str, Enum):
    """Types of relationships between entities."""

    USES = "uses"
    CREATED_BY = "created_by"
    PART_OF = "part_of"
    RELATED_TO = "related_to"
    DEPENDS_ON = "depends_on"
    IMPLEMENTS = "implements"
    MENTIONS = "mentions"
    SIMILAR_TO = "similar_to"


class Relationship(BaseModel):
    """
    Relationship model representing a connection between entities.

    Attributes:
        id: Unique relationship identifier
        source_entity_id: Source entity ID
        target_entity_id: Target entity ID
        relationship_type: Type of relationship
        confidence: Relationship confidence score (0-1)
        evidence: List of evidence strings supporting this relationship
        source_documents: Document IDs where relationship appears
        created_at: Relationship creation timestamp
        updated_at: Last update timestamp
    """

    id: str = Field(..., description="Unique relationship identifier")
    source_entity_id: str = Field(..., description="Source entity ID")
    target_entity_id: str = Field(..., description="Target entity ID")
    relationship_type: RelationshipType = Field(..., description="Relationship type")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    evidence: List[str] = Field(
        default_factory=list, description="Evidence supporting relationship"
    )
    source_documents: List[str] = Field(
        default_factory=list, description="Document IDs where relationship appears"
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation time")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update time")

    @model_validator(mode="after")
    def prevent_self_reference(self) -> "Relationship":
        """Prevent relationships where source and target are the same entity."""
        if self.source_entity_id == self.target_entity_id:
            raise ValueError(
                f"Self-reference not allowed: source_entity_id and target_entity_id "
                f"cannot both be '{self.source_entity_id}'"
            )
        return self

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "id": "rel-1",
                "source_entity_id": "ent-1",
                "target_entity_id": "ent-2",
                "relationship_type": "uses",
                "confidence": 0.85,
                "evidence": [
                    "Django uses Python for web development",
                    "Python is the underlying language for Django",
                ],
                "source_documents": ["doc-123"],
                "created_at": "2025-10-12T10:34:00Z",
                "updated_at": "2025-10-12T10:34:00Z",
            }
        }
