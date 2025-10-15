"""
Document model with ProcessingStatus lifecycle and SHA-256 hash validation.

Represents an uploaded file with metadata, processing status, and validation rules.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator
import re


class DocumentFormat(str, Enum):
    """Supported document formats."""

    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    MD = "md"
    HTML = "html"
    MP3 = "mp3"


class ProcessingStatus(str, Enum):
    """Document processing lifecycle states."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Document(BaseModel):
    """
    Document model representing an uploaded file.

    Attributes:
        id: Unique document identifier
        filename: Original filename
        format: Document format (PDF, DOCX, etc.)
        content_hash: SHA-256 hash of file content for deduplication
        file_size: File size in bytes
        status: Current processing status
        upload_timestamp: When the document was uploaded
        processing_started: When processing began (optional)
        processing_completed: When processing finished (optional)
        error_message: Error details if processing failed (optional)
    """

    id: str = Field(..., description="Unique document identifier")
    filename: str = Field(..., min_length=1, description="Original filename")
    format: DocumentFormat = Field(..., description="Document format")
    content_hash: str = Field(..., description="SHA-256 hash for deduplication")
    file_size: int = Field(..., gt=0, description="File size in bytes")
    status: ProcessingStatus = Field(
        default=ProcessingStatus.PENDING, description="Processing status"
    )
    upload_timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Upload time"
    )
    processing_started: Optional[datetime] = Field(
        default=None, description="Processing start time"
    )
    processing_completed: Optional[datetime] = Field(
        default=None, description="Processing completion time"
    )
    error_message: Optional[str] = Field(default=None, description="Error details if failed")

    @field_validator("content_hash")
    @classmethod
    def validate_sha256(cls, v: str) -> str:
        """Validate that content_hash is a valid SHA-256 hex string."""
        if not re.match(r"^[a-f0-9]{64}$", v.lower()):
            raise ValueError("content_hash must be a valid SHA-256 hex string (64 hex characters)")
        return v.lower()

    @field_validator("file_size")
    @classmethod
    def validate_file_size(cls, v: int) -> int:
        """Validate file size is positive and within limits (100MB)."""
        if v <= 0:
            raise ValueError("file_size must be positive")
        if v > 100 * 1024 * 1024:  # 100MB limit
            raise ValueError("file_size must not exceed 100MB (104857600 bytes)")
        return v

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "id": "doc-123",
                "filename": "research-paper.pdf",
                "format": "pdf",
                "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                "file_size": 1048576,
                "status": "pending",
                "upload_timestamp": "2025-10-12T10:30:00Z",
            }
        }
