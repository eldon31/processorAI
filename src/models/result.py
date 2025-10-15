"""
QueryResult model with RRF score calculation and source citations.

Represents search results from vector/graph/hybrid queries.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ResultChunk(BaseModel):
    """
    Individual result chunk with score and metadata.

    Attributes:
        chunk_id: Reference to chunk
        text: Chunk text content
        document_id: Source document ID
        document_name: Source document filename
        score: Relevance score (0-1)
        char_start: Character offset in document
        char_end: Character offset end in document
        metadata: Additional metadata
    """

    chunk_id: str = Field(..., description="Chunk identifier")
    text: str = Field(..., description="Chunk text content")
    document_id: str = Field(..., description="Source document ID")
    document_name: Optional[str] = Field(default=None, description="Source document filename")
    score: float = Field(..., ge=0.0, le=1.0, description="Relevance score (0-1)")
    char_start: Optional[int] = Field(default=None, description="Character offset start")
    char_end: Optional[int] = Field(default=None, description="Character offset end")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class QueryResult(BaseModel):
    """
    Query result model with RRF-ranked results.

    For hybrid search, uses Reciprocal Rank Fusion (RRF) to combine
    vector similarity scores and knowledge graph scores.

    Attributes:
        query_id: Reference to query
        chunks: List of result chunks
        total_results: Total number of results found
        search_mode: Search mode used
        processing_time_ms: Query processing time in milliseconds
        entities: Related entities from knowledge graph (optional)
        relationships: Related relationships from graph (optional)
        answer_synthesis: Generated answer (optional)
        timestamp: Result timestamp
    """

    query_id: str = Field(..., description="Query identifier")
    chunks: List[ResultChunk] = Field(
        default_factory=list, description="Result chunks with scores"
    )
    total_results: int = Field(..., ge=0, description="Total results found")
    search_mode: str = Field(default="hybrid", description="Search mode used")
    processing_time_ms: Optional[int] = Field(
        default=None, description="Processing time in ms"
    )
    entities: List[Dict[str, Any]] = Field(
        default_factory=list, description="Related entities from knowledge graph"
    )
    relationships: List[Dict[str, Any]] = Field(
        default_factory=list, description="Related relationships from graph"
    )
    answer_synthesis: Optional[str] = Field(
        default=None, description="LLM-generated answer"
    )
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Result time")

    def calculate_rrf_score(
        self, vector_rank: int, graph_rank: int, k: int = 60
    ) -> float:
        """
        Calculate Reciprocal Rank Fusion (RRF) score.

        RRF = 1/(k + vector_rank) + 1/(k + graph_rank)

        Args:
            vector_rank: Rank from vector search (1-based)
            graph_rank: Rank from graph search (1-based)
            k: Constant to reduce impact of high ranks (default 60)

        Returns:
            RRF score (higher is better)
        """
        return 1.0 / (k + vector_rank) + 1.0 / (k + graph_rank)

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "query_id": "query-1",
                "chunks": [
                    {
                        "chunk_id": "chunk-1",
                        "text": "Python is widely used for data science and machine learning.",
                        "document_id": "doc-123",
                        "document_name": "python-guide.pdf",
                        "score": 0.95,
                        "char_start": 0,
                        "char_end": 61,
                        "metadata": {},
                    }
                ],
                "total_results": 1,
                "search_mode": "hybrid",
                "processing_time_ms": 1250,
                "entities": [],
                "relationships": [],
                "timestamp": "2025-10-12T10:36:00Z",
            }
        }
