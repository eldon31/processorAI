"""
Vector similarity search using Chroma.

Adapted from agentic-rag-knowledge-graph/agent/db_utils.py:vector_search()
Key changes:
- PostgreSQL pgvector → Chroma client
- Distance to similarity conversion (Chroma returns distances, lower = better)
- Metadata filtering support
"""

import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from ..storage.chroma_client import get_chroma_client
from ..storage.collection_manager import get_collection_manager

logger = logging.getLogger(__name__)


class VectorSearchResult(BaseModel):
    """Result from vector similarity search."""
    
    chunk_id: str = Field(..., description="Unique chunk identifier")
    document_id: str = Field(..., description="Document ID this chunk belongs to")
    content: str = Field(..., description="Chunk content")
    similarity: float = Field(..., description="Similarity score (0-1, higher = better)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Chunk metadata")
    document_title: Optional[str] = Field(None, description="Document title")
    document_source: Optional[str] = Field(None, description="Document source")
    collection: Optional[str] = Field(None, description="Collection name")


async def vector_search(
    query_embedding: List[float],
    collection_name: Optional[str] = None,
    limit: int = 10,
    metadata_filter: Optional[Dict[str, Any]] = None,
    min_similarity: float = 0.0
) -> List[VectorSearchResult]:
    """
    Perform vector similarity search using Chroma.
    
    This function searches across document chunks using semantic similarity
    based on embedding vectors. Results are ranked by similarity score.
    
    Args:
        query_embedding: Query embedding vector (must match model dimensions)
        collection_name: Specific collection to search (None = search all via manager)
        limit: Maximum number of results to return (1-100)
        metadata_filter: Optional metadata filtering (e.g., {"language": "python"})
        min_similarity: Minimum similarity threshold (0-1)
    
    Returns:
        List of matching chunks ordered by similarity (best first)
    
    Example:
        >>> from src.ingestion.embedder import create_embedder
        >>> embedder = create_embedder()
        >>> embedding = await embedder.generate_embedding("What is Python?")
        >>> results = await vector_search(
        ...     query_embedding=embedding,
        ...     collection_name="python_docs",
        ...     limit=5,
        ...     min_similarity=0.7
        ... )
        >>> for result in results:
        ...     print(f"{result.similarity:.2f}: {result.content[:100]}")
    """
    try:
        chroma_client = get_chroma_client()
        
        # If no collection specified, use collection manager for cross-collection search
        if collection_name is None:
            collection_manager = get_collection_manager()
            
            # Search across all collections
            all_results = []
            collections = await collection_manager.list_collections()
            for coll_info in collections:
                coll_name = coll_info["name"]
                try:
                    coll_results = await _search_collection(
                        chroma_client=chroma_client,
                        collection_name=coll_name,
                        query_embedding=query_embedding,
                        limit=limit,
                        metadata_filter=metadata_filter
                    )
                    all_results.extend(coll_results)
                except Exception as e:
                    logger.warning(f"Failed to search collection {coll_name}: {e}")
                    continue
            
            # Sort by similarity and take top results
            all_results.sort(key=lambda x: x.similarity, reverse=True)
            results = all_results[:limit]
        else:
            # Search single collection
            results = await _search_collection(
                chroma_client=chroma_client,
                collection_name=collection_name,
                query_embedding=query_embedding,
                limit=limit,
                metadata_filter=metadata_filter
            )
        
        # Filter by minimum similarity
        if min_similarity > 0.0:
            results = [r for r in results if r.similarity >= min_similarity]
        
        logger.info(f"Vector search returned {len(results)} results (collection: {collection_name or 'all'})")
        return results
        
    except Exception as e:
        logger.error(f"Vector search failed: {e}")
        return []


async def _search_collection(
    chroma_client,
    collection_name: str,
    query_embedding: List[float],
    limit: int,
    metadata_filter: Optional[Dict[str, Any]] = None
) -> List[VectorSearchResult]:
    """
    Search a single Chroma collection.
    
    Internal helper function that performs the actual Chroma query.
    
    Args:
        chroma_client: Chroma client instance
        collection_name: Collection to search
        query_embedding: Query embedding vector
        limit: Maximum results
        metadata_filter: Optional metadata filter
    
    Returns:
        List of search results
    """
    try:
        # Get collection
        collection = chroma_client.get_collection(collection_name)
        
        # Perform Chroma query
        # NOTE: Chroma returns DISTANCES (lower = better), we need SIMILARITY (higher = better)
        query_results = collection.query(
            query_embeddings=[query_embedding],
            n_results=limit,
            where=metadata_filter,  # Chroma metadata filtering
            include=["documents", "metadatas", "distances"]
        )
        
        # Convert Chroma results to VectorSearchResult objects
        results = []
        
        if not query_results["ids"] or not query_results["ids"][0]:
            return results
        
        for i in range(len(query_results["ids"][0])):
            chunk_id = query_results["ids"][0][i]
            distance = query_results["distances"][0][i]
            content = query_results["documents"][0][i]
            metadata = query_results["metadatas"][0][i] or {}
            
            # Convert distance to similarity
            # Chroma uses L2 distance, convert to cosine similarity approximation
            # For normalized embeddings: similarity ≈ 1 - (distance² / 2)
            # Simpler approximation: similarity = 1 / (1 + distance)
            similarity = 1.0 / (1.0 + distance)
            
            results.append(
                VectorSearchResult(
                    chunk_id=chunk_id,
                    document_id=metadata.get("document_id", ""),
                    content=content,
                    similarity=similarity,
                    metadata=metadata,
                    document_title=metadata.get("document_title"),
                    document_source=metadata.get("document_source"),
                    collection=collection_name
                )
            )
        
        return results
        
    except Exception as e:
        logger.error(f"Collection search failed for {collection_name}: {e}")
        return []


async def vector_search_by_text(
    query_text: str,
    collection_name: Optional[str] = None,
    limit: int = 10,
    metadata_filter: Optional[Dict[str, Any]] = None,
    min_similarity: float = 0.0
) -> List[VectorSearchResult]:
    """
    Perform vector search using text query (generates embedding automatically).
    
    Convenience function that generates the embedding from text and then
    calls vector_search().
    
    Args:
        query_text: Text query to search for
        collection_name: Optional collection to search
        limit: Maximum results
        metadata_filter: Optional metadata filter
        min_similarity: Minimum similarity threshold
    
    Returns:
        List of matching chunks
    
    Example:
        >>> results = await vector_search_by_text(
        ...     query_text="How to install Python?",
        ...     collection_name="tutorials",
        ...     limit=3
        ... )
    """
    from ..ingestion.embedder import create_embedder
    
    try:
        # Generate embedding for query text
        embedder = create_embedder()
        embedding = await embedder.generate_embedding(query_text)
        
        # Perform vector search
        return await vector_search(
            query_embedding=embedding,
            collection_name=collection_name,
            limit=limit,
            metadata_filter=metadata_filter,
            min_similarity=min_similarity
        )
        
    except Exception as e:
        logger.error(f"Vector search by text failed: {e}")
        return []
