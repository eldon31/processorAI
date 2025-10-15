"""
Pydantic models for the Universal File-to-Knowledge Converter.

This package contains all core data models with validation:
- Document: Uploaded files with processing status
- Chunk: Text segments from documents
- Embedding: Vector embeddings for semantic search
- Entity: Named entities extracted from text
- Relationship: Connections between entities
- Query: User search queries
- QueryResult: Search results with citations
"""

from src.models.document import Document, ProcessingStatus, DocumentFormat
from src.models.chunk import Chunk, ChunkType
from src.models.embedding import Embedding
from src.models.entity import Entity, EntityType
from src.models.relationship import Relationship, RelationshipType
from src.models.query import Query, SearchMode
from src.models.result import QueryResult, ResultChunk
from src.models.collection import (
    CollectionCategory,
    CollectionConfig,
    CollectionMetadata,
    PREDEFINED_COLLECTIONS,
    get_collection_config,
)

__all__ = [
    "Document",
    "ProcessingStatus",
    "DocumentFormat",
    "Chunk",
    "ChunkType",
    "Embedding",
    "Entity",
    "EntityType",
    "Relationship",
    "RelationshipType",
    "Query",
    "SearchMode",
    "QueryResult",
    "ResultChunk",
    "CollectionCategory",
    "CollectionConfig",
    "CollectionMetadata",
    "PREDEFINED_COLLECTIONS",
    "get_collection_config",
]
