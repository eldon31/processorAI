"""
Tools for the Pydantic AI agent.

REFACTORED from: agentic-rag-knowledge-graph/agent/tools.py
Changes:
- Uses new retrieval module (vector_search, graph_search, hybrid_search)
- Added Pydantic models for all tool inputs
- Maintained all RAG tool functionality
- Updated imports to use new module structure
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncio

from pydantic import BaseModel, Field

from ..models.chunk import Chunk
from ..models.result import QueryResult
from ..models.document import Document
from ..config.providers import get_embedding_client, get_embedding_model
from ..storage.chroma_client import get_chroma_client
from ..storage.collection_manager import get_collection_manager
from ..graph.graph_client import (
    search_knowledge_graph,
    get_entity_relationships as get_graph_entity_relationships,
    _get_global_client as get_graph_client,
)
# Import new retrieval functions
from ..retrieval.vector_search import vector_search_by_text
from ..retrieval.graph_search import graph_search, get_entity_relationships, get_entity_timeline
from ..retrieval.hybrid_search import hybrid_search

logger = logging.getLogger(__name__)

# Initialize embedding client
embedding_client = get_embedding_client()
EMBEDDING_MODEL = get_embedding_model()


async def generate_embedding(text: str) -> List[float]:
    """
    Generate embedding for text using configured provider.
    
    Args:
        text: Text to embed
    
    Returns:
        Embedding vector
    """
    try:
        response = await embedding_client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        logger.error(f"Failed to generate embedding: {e}")
        raise


# Tool Input Models
class VectorSearchInput(BaseModel):
    """Input for vector search tool."""
    query: str = Field(..., description="Search query")
    limit: int = Field(default=10, ge=1, le=50, description="Maximum number of results")


class GraphSearchInput(BaseModel):
    """Input for graph search tool."""
    query: str = Field(..., description="Search query")


class HybridSearchInput(BaseModel):
    """Input for hybrid search tool."""
    query: str = Field(..., description="Search query")
    limit: int = Field(default=10, ge=1, le=50, description="Maximum number of results")
    text_weight: float = Field(default=0.3, ge=0.0, le=1.0, description="Weight for text similarity")


class DocumentInput(BaseModel):
    """Input for document retrieval."""
    document_id: str = Field(..., description="Document ID to retrieve")


class DocumentListInput(BaseModel):
    """Input for listing documents."""
    limit: int = Field(default=20, ge=1, le=100, description="Maximum number of documents")
    offset: int = Field(default=0, ge=0, description="Number of documents to skip")


class EntityRelationshipInput(BaseModel):
    """Input for entity relationship query."""
    entity_name: str = Field(..., description="Name of the entity")
    depth: int = Field(default=2, ge=1, le=5, description="Maximum traversal depth")


class EntityTimelineInput(BaseModel):
    """Input for entity timeline query."""
    entity_name: str = Field(..., description="Name of the entity")
    start_date: Optional[str] = Field(None, description="Start date (ISO format)")
    end_date: Optional[str] = Field(None, description="End date (ISO format)")


# Tool Implementation Functions
async def vector_search_tool(input_data: VectorSearchInput) -> List[Dict[str, Any]]:
    """
    Perform vector similarity search using the new retrieval module.
    
    Args:
        input_data: Search parameters
    
    Returns:
        List of matching chunks with similarity scores
    """
    try:
        # Use new vector_search_by_text function
        results = await vector_search_by_text(
            query_text=input_data.query,
            limit=input_data.limit
        )
        
        # Convert VectorSearchResult to dictionaries for agent
        return [
            {
                "chunk_id": r.chunk_id,
                "document_id": r.metadata.get("document_id", ""),
                "content": r.content,
                "score": r.similarity,
                "metadata": r.metadata,
                "document_title": r.metadata.get("title", ""),
                "document_source": r.metadata.get("source", "")
            }
            for r in results
        ]
        
    except Exception as e:
        logger.error(f"Vector search failed: {e}")
        return []


async def graph_search_tool(input_data: GraphSearchInput) -> List[Dict[str, Any]]:
    """
    Search the knowledge graph using the new retrieval module.
    
    Args:
        input_data: Search parameters
    
    Returns:
        List of graph search results with facts and temporal data
    """
    try:
        results = await graph_search(query=input_data.query)
        
        # Convert GraphSearchResult to dictionaries for agent
        return [
            {
                "fact": r.fact,
                "uuid": r.uuid,
                "valid_at": r.valid_at if isinstance(r.valid_at, str) else (r.valid_at.isoformat() if r.valid_at else None),
                "invalid_at": r.invalid_at if isinstance(r.invalid_at, str) else (r.invalid_at.isoformat() if r.invalid_at else None),
            }
            for r in results
        ]
        
    except Exception as e:
        logger.error(f"Graph search failed: {e}")
        return []


async def hybrid_search_tool(input_data: HybridSearchInput) -> List[Dict[str, Any]]:
    """
    Perform hybrid search (vector + graph) using the new retrieval module.
    
    Args:
        input_data: Search parameters
    
    Returns:
        List of matching results with combined relevance scores
    """
    try:
        # Calculate graph weight from text weight (complementary)
        graph_weight = 1.0 - input_data.text_weight
        
        # Use new hybrid_search function
        results = await hybrid_search(
            query_text=input_data.query,
            limit=input_data.limit,
            vector_weight=input_data.text_weight,
            graph_weight=graph_weight
        )
        
        # Convert HybridSearchResult to dictionaries for agent
        return [
            {
                "chunk_id": r.chunk_id or r.fact_uuid or "",
                "content": r.content,
                "combined_score": r.combined_score,
                "vector_score": r.vector_score or 0.0,
                "graph_score": r.graph_score or 0.0,
                "source_type": r.source_type,
                "metadata": r.metadata,
            }
            for r in results
        ]
        
    except Exception as e:
        logger.error(f"Hybrid search failed: {e}")
        return []
        logger.error(f"Hybrid search failed: {e}")
        return []


async def get_document_tool(input_data: DocumentInput) -> Optional[Dict[str, Any]]:
    """
    Retrieve a complete document from Chroma.
    
    Args:
        input_data: Document retrieval parameters
    
    Returns:
        Document data with all chunks or None if not found
    """
    try:
        # Use Chroma client to get all chunks for the document
        chroma_client = get_chroma_client()
        chunks = await chroma_client.get_document_chunks(
            document_id=input_data.document_id
        )
        
        if not chunks:
            return None
        
        # Reconstruct document from chunks
        first_chunk = chunks[0]
        document = {
            "id": input_data.document_id,
            "title": first_chunk.document_title,
            "source": first_chunk.document_source,
            "content": "\n\n".join(chunk.content for chunk in chunks),
            "chunk_count": len(chunks),
            "created_at": first_chunk.metadata.get("created_at", "")
        }
        
        return document
        
    except Exception as e:
        logger.error(f"Document retrieval failed: {e}")
        return None


async def list_documents_tool(input_data: DocumentListInput) -> List[Dict[str, Any]]:
    """
    List available documents from Chroma.
    
    Args:
        input_data: Listing parameters
    
    Returns:
        List of document metadata
    """
    try:
        # Use Chroma client for document listing
        chroma_client = get_chroma_client()
        documents = await chroma_client.list_documents(
            limit=input_data.limit,
            offset=input_data.offset
        )
        
        return documents
        
    except Exception as e:
        logger.error(f"Document listing failed: {e}")
        return []


async def get_entity_relationships_tool(input_data: EntityRelationshipInput) -> Dict[str, Any]:
    """
    Get relationships for an entity from the knowledge graph.
    
    Args:
        input_data: Entity relationship parameters
    
    Returns:
        Entity relationships and connected entities
    """
    try:
        # Use new get_entity_relationships function from retrieval module
        # This returns a Dict with central_entity, relationships, related_entities, etc.
        result = await get_entity_relationships(
            entity_name=input_data.entity_name,
            depth=input_data.depth
        )
        
        # Result is already in the correct format
        return result
        
    except Exception as e:
        logger.error(f"Entity relationship query failed: {e}")
        return {
            "central_entity": input_data.entity_name,
            "relationships": [],
            "related_entities": [],
            "total_facts": 0,
            "search_method": "graphiti_entity_relationships",
            "error": str(e)
        }


async def get_entity_timeline_tool(input_data: EntityTimelineInput) -> List[Dict[str, Any]]:
    """
    Get timeline of facts for an entity from the knowledge graph.
    
    Args:
        input_data: Timeline query parameters
    
    Returns:
        Chronological list of facts with timestamps
    """
    try:
        # Parse dates if provided
        start_date = None
        end_date = None
        
        if input_data.start_date:
            start_date = datetime.fromisoformat(input_data.start_date)
        if input_data.end_date:
            end_date = datetime.fromisoformat(input_data.end_date)
        
        # Use new get_entity_timeline function from retrieval module
        results = await get_entity_timeline(
            entity_name=input_data.entity_name,
            start_date=start_date,
            end_date=end_date
        )
        
        # Convert GraphSearchResult to dictionaries
        return [
            {
                "fact": r.fact,
                "uuid": r.uuid,
                "valid_at": r.valid_at if isinstance(r.valid_at, str) else (r.valid_at.isoformat() if r.valid_at else None),
                "invalid_at": r.invalid_at if isinstance(r.invalid_at, str) else (r.invalid_at.isoformat() if r.invalid_at else None),
            }
            for r in results
        ]
        
    except Exception as e:
        logger.error(f"Entity timeline query failed: {e}")
        return []


# Combined search function for comprehensive queries
async def perform_comprehensive_search(
    query: str,
    use_vector: bool = True,
    use_graph: bool = True,
    limit: int = 10
) -> Dict[str, Any]:
    """
    Perform a comprehensive search using multiple methods.
    
    Args:
        query: Search query
        use_vector: Whether to use vector search
        use_graph: Whether to use graph search
        limit: Maximum results per search type
    
    Returns:
        Combined search results from vector and graph searches
    """
    results: Dict[str, Any] = {
        "query": query,
        "vector_results": [],
        "graph_results": [],
        "total_results": 0
    }
    
    tasks = []
    
    if use_vector:
        tasks.append(vector_search_tool(VectorSearchInput(query=query, limit=limit)))
    
    if use_graph:
        tasks.append(graph_search_tool(GraphSearchInput(query=query)))
    
    if tasks:
        search_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        if use_vector and len(search_results) > 0 and not isinstance(search_results[0], Exception):
            results["vector_results"] = search_results[0]
        
        if use_graph:
            graph_idx = 1 if use_vector else 0
            if len(search_results) > graph_idx and not isinstance(search_results[graph_idx], Exception):
                results["graph_results"] = search_results[graph_idx]
    
    # Safe len() calls with type guards
    vector_count = len(results["vector_results"]) if isinstance(results["vector_results"], list) else 0
    graph_count = len(results["graph_results"]) if isinstance(results["graph_results"], list) else 0
    results["total_results"] = vector_count + graph_count
    
    return results
