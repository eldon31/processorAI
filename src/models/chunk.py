"""
Chunk model with character offsets, token count validation (200-500), and ChunkType enum.

Represents a semantically meaningful text segment from a document.
"""

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, field_validator


class ChunkType(str, Enum):
    """Types of text chunks."""

    TEXT = "text"
    TABLE = "table"
    CODE = "code"
    LIST = "list"
    TITLE = "title"
    PARAGRAPH = "paragraph"


class Chunk(BaseModel):
    """
    Chunk model representing a text segment from a document.

    Attributes:
        id: Unique chunk identifier
        document_id: Reference to parent document
        chunk_index: Position in document (0-based)
        text: Actual text content
        chunk_type: Type of content (text, table, code, etc.)
        char_start: Starting character offset in original document
        char_end: Ending character offset in original document
        token_count: Number of tokens (200-500 per spec)
        created_at: Chunk creation timestamp
    """

    id: str = Field(..., description="Unique chunk identifier")
    document_id: str = Field(..., description="Parent document ID")
    chunk_index: int = Field(..., ge=0, description="Position in document (0-based)")
    text: str = Field(..., min_length=1, description="Text content")
    chunk_type: ChunkType = Field(default=ChunkType.TEXT, description="Content type")
    char_start: int = Field(..., ge=0, description="Start character offset")
    char_end: int = Field(..., gt=0, description="End character offset")
    token_count: int = Field(..., ge=200, le=500, description="Token count (200-500)")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation time")

    @field_validator("char_end")
    @classmethod
    def validate_char_range(cls, v: int, info) -> int:
        """Validate that char_end > char_start."""
        char_start = info.data.get("char_start")
        if char_start is not None and v <= char_start:
            raise ValueError("char_end must be greater than char_start")
        return v

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "id": "chunk-1",
                "document_id": "doc-123",
                "chunk_index": 0,
                "text": "This is the first paragraph of the document. It contains important information about the topic.",
                "chunk_type": "paragraph",
                "char_start": 0,
                "char_end": 95,
                "token_count": 250,
                "created_at": "2025-10-12T10:31:00Z",
            }
        }
