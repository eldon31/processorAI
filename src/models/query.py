"""
Query model with SearchMode enum (vector/graph/hybrid).

Represents a user search query with parameters.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class SearchMode(str, Enum):
    """Search modes for querying knowledge base."""

    VECTOR = "vector"  # Pure vector similarity search
    GRAPH = "graph"  # Knowledge graph traversal
    HYBRID = "hybrid"  # Combined vector + graph with RRF


class Query(BaseModel):
    """
    Query model representing a user search request.

    Attributes:
        id: Unique query identifier
        query_text: Natural language query
        search_mode: Search mode (vector/graph/hybrid)
        top_k: Number of results to return (default 10)
        max_depth: Maximum graph traversal depth for graph/hybrid mode (default 3)
        min_confidence: Minimum confidence threshold for results (0-1)
        timestamp: Query timestamp
    """

    id: Optional[str] = Field(default=None, description="Unique query identifier")
    query_text: str = Field(..., min_length=1, description="Natural language query")
    search_mode: SearchMode = Field(
        default=SearchMode.HYBRID, description="Search mode (vector/graph/hybrid)"
    )
    top_k: int = Field(default=10, ge=1, le=100, description="Number of results (1-100)")
    max_depth: int = Field(
        default=3, ge=1, le=5, description="Max graph traversal depth (1-5)"
    )
    min_confidence: float = Field(
        default=0.7, ge=0.0, le=1.0, description="Minimum confidence threshold"
    )
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Query time")

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "id": "query-1",
                "query_text": "What is Python used for?",
                "search_mode": "hybrid",
                "top_k": 10,
                "max_depth": 3,
                "min_confidence": 0.7,
                "timestamp": "2025-10-12T10:35:00Z",
            }
        }
