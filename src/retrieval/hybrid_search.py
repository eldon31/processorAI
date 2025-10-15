"""
Hybrid search combining vector and graph search with RRF ranking.

Implements Reciprocal Rank Fusion (RRF) to combine results from multiple
search methods. Adapted from agentic-rag-knowledge-graph/agent/db_utils.py:hybrid_search()

RRF Formula: score = sum(1 / (k + rank_i)) for each ranking
Standard k value: 60 (from academic literature)

Key differences from PostgreSQL implementation:
- Application-level RRF (not database function)
- Combines vector (Chroma) + graph (Graphiti) instead of vector + text
- Parallel execution for better performance
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from .vector_search import vector_search, VectorSearchResult, vector_search_by_text
from .graph_search import graph_search, GraphSearchResult

logger = logging.getLogger(__name__)


class HybridSearchResult(BaseModel):
    """Result from hybrid search combining multiple sources."""
    
    content: str = Field(..., description="Result content (chunk or fact)")
    source_type: str = Field(..., description="Source of result: 'vector' or 'graph'")
    combined_score: float = Field(..., description="Combined RRF score")
    vector_score: Optional[float] = Field(None, description="Vector similarity score")
    graph_score: Optional[float] = Field(None, description="Graph relevance score")
    
    # Original result data
    chunk_id: Optional[str] = Field(None, description="Chunk ID (for vector results)")
    document_id: Optional[str] = Field(None, description="Document ID (for vector results)")
    fact_uuid: Optional[str] = Field(None, description="Fact UUID (for graph results)")
    
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    document_title: Optional[str] = Field(None, description="Document title")
    document_source: Optional[str] = Field(None, description="Document source")
    collection: Optional[str] = Field(None, description="Collection name (for vector results)")


async def hybrid_search(
    query_text: str,
    collection_name: Optional[str] = None,
    limit: int = 10,
    vector_weight: float = 0.7,
    graph_weight: float = 0.3,
    rrf_k: int = 60,
    use_graph: bool = True,
    metadata_filter: Optional[Dict[str, Any]] = None
) -> List[HybridSearchResult]:
    """
    Perform hybrid search combining vector and graph search with RRF ranking.
    
    This function runs vector similarity search and graph knowledge search
    in parallel, then combines results using Reciprocal Rank Fusion (RRF).
    
    Args:
        query_text: Natural language query
        collection_name: Optional collection for vector search (None = all collections)
        limit: Maximum number of results to return
        vector_weight: Weight for vector search results (0-1, default 0.7)
        graph_weight: Weight for graph search results (0-1, default 0.3)
        rrf_k: RRF constant (default 60, standard from literature)
        use_graph: Whether to include graph search (default True)
        metadata_filter: Optional metadata filter for vector search
    
    Returns:
        List of hybrid search results ordered by combined RRF score
    
    RRF Formula:
        For each result: score = Σ(weight_i / (k + rank_i))
        where rank_i is the position in each ranking (0-indexed + 1)
    
    Example:
        >>> results = await hybrid_search(
        ...     query_text="What is Python used for?",
        ...     limit=10,
        ...     vector_weight=0.7,  # 70% vector, 30% graph
        ...     graph_weight=0.3
        ... )
        >>> for result in results:
        ...     print(f"{result.source_type}: {result.combined_score:.3f}")
        ...     print(f"  {result.content[:100]}")
    
    Notes:
        - Vector and graph searches run in parallel for better performance
        - RRF is more robust than score averaging when combining different metrics
        - Graph search can be disabled (use_graph=False) for faster queries
    """
    try:
        # Validate weights
        if abs((vector_weight + graph_weight) - 1.0) > 0.01:
            logger.warning(f"Weights don't sum to 1.0: {vector_weight} + {graph_weight} = {vector_weight + graph_weight}")
            # Normalize weights
            total = vector_weight + graph_weight
            vector_weight = vector_weight / total
            graph_weight = graph_weight / total
        
        # Run vector and graph searches in parallel
        search_tasks = []
        
        # Vector search task
        vector_task = vector_search_by_text(
            query_text=query_text,
            collection_name=collection_name,
            limit=limit * 2,  # Get more results for fusion
            metadata_filter=metadata_filter
        )
        search_tasks.append(vector_task)
        
        # Graph search task (if enabled)
        if use_graph:
            graph_task = graph_search(
                query=query_text,
                limit=limit * 2  # Get more results for fusion
            )
            search_tasks.append(graph_task)
        
        # Execute searches in parallel
        if use_graph:
            vector_results, graph_results = await asyncio.gather(*search_tasks)
        else:
            vector_results = await vector_task
            graph_results = []
        
        logger.info(f"Hybrid search: {len(vector_results)} vector + {len(graph_results)} graph results")
        
        # Apply RRF ranking
        combined_results = _apply_rrf_ranking(
            vector_results=vector_results,
            graph_results=graph_results,
            vector_weight=vector_weight,
            graph_weight=graph_weight,
            rrf_k=rrf_k,
            limit=limit
        )
        
        logger.info(f"Hybrid search returned {len(combined_results)} combined results")
        return combined_results
        
    except Exception as e:
        logger.error(f"Hybrid search failed: {e}")
        return []


def _apply_rrf_ranking(
    vector_results: List[VectorSearchResult],
    graph_results: List[GraphSearchResult],
    vector_weight: float,
    graph_weight: float,
    rrf_k: int,
    limit: int
) -> List[HybridSearchResult]:
    """
    Apply Reciprocal Rank Fusion to combine vector and graph results.
    
    RRF is a rank-based fusion method that is more robust than score-based
    methods when combining results from different scoring systems.
    
    Args:
        vector_results: Vector search results (already ranked)
        graph_results: Graph search results (already ranked)
        vector_weight: Weight for vector scores
        graph_weight: Weight for graph scores
        rrf_k: RRF constant (typically 60)
        limit: Maximum results to return
    
    Returns:
        Combined and re-ranked results
    """
    # Track results by unique identifier
    result_scores: Dict[str, Dict[str, Any]] = {}
    
    # Process vector results
    for rank, vector_result in enumerate(vector_results):
        result_id = f"vector_{vector_result.chunk_id}"
        
        # Calculate RRF score for this ranking
        rrf_score = 1.0 / (rrf_k + rank + 1)  # rank is 0-indexed, so +1
        weighted_score = rrf_score * vector_weight
        
        result_scores[result_id] = {
            "content": vector_result.content,
            "source_type": "vector",
            "combined_score": weighted_score,
            "vector_score": vector_result.similarity,
            "graph_score": None,
            "chunk_id": vector_result.chunk_id,
            "document_id": vector_result.document_id,
            "fact_uuid": None,
            "metadata": vector_result.metadata,
            "document_title": vector_result.document_title,
            "document_source": vector_result.document_source,
            "collection": vector_result.collection,
            "vector_rank": rank + 1,
            "graph_rank": None
        }
    
    # Process graph results
    for rank, graph_result in enumerate(graph_results):
        result_id = f"graph_{graph_result.uuid}"
        
        # Calculate RRF score for this ranking
        rrf_score = 1.0 / (rrf_k + rank + 1)
        weighted_score = rrf_score * graph_weight
        
        # Check if this result also appeared in vector search (unlikely but possible)
        if result_id in result_scores:
            # Combine scores (result appeared in both rankings)
            result_scores[result_id]["combined_score"] += weighted_score
            result_scores[result_id]["graph_score"] = graph_result.score
            result_scores[result_id]["graph_rank"] = rank + 1
        else:
            # New result from graph only
            result_scores[result_id] = {
                "content": graph_result.fact,
                "source_type": "graph",
                "combined_score": weighted_score,
                "vector_score": None,
                "graph_score": graph_result.score,
                "chunk_id": None,
                "document_id": None,
                "fact_uuid": graph_result.uuid,
                "metadata": {
                    "valid_at": graph_result.valid_at,
                    "invalid_at": graph_result.invalid_at,
                    "source_node_uuid": graph_result.source_node_uuid
                },
                "document_title": None,
                "document_source": None,
                "collection": None,
                "vector_rank": None,
                "graph_rank": rank + 1
            }
    
    # Sort by combined RRF score (descending)
    sorted_results = sorted(
        result_scores.items(),
        key=lambda x: x[1]["combined_score"],
        reverse=True
    )
    
    # Convert to HybridSearchResult objects and limit
    hybrid_results = []
    for result_id, result_data in sorted_results[:limit]:
        # Remove ranking info (internal use only)
        result_data.pop("vector_rank", None)
        result_data.pop("graph_rank", None)
        
        hybrid_results.append(HybridSearchResult(**result_data))
    
    return hybrid_results


async def hybrid_search_with_reranking(
    query_text: str,
    collection_name: Optional[str] = None,
    limit: int = 10,
    vector_weight: float = 0.7,
    graph_weight: float = 0.3,
    use_llm_reranking: bool = False
) -> List[HybridSearchResult]:
    """
    Hybrid search with optional LLM-based reranking.
    
    This is an enhanced version that can optionally use an LLM to rerank
    the top results for better relevance.
    
    Args:
        query_text: Search query
        collection_name: Optional collection filter
        limit: Maximum results
        vector_weight: Vector search weight
        graph_weight: Graph search weight
        use_llm_reranking: Whether to use LLM for final reranking (slower but more accurate)
    
    Returns:
        Hybrid search results (potentially reranked)
    
    Note:
        LLM reranking is currently not implemented. This is a placeholder
        for future enhancement using a cross-encoder or LLM reranking model.
    """
    # Get initial hybrid results
    results = await hybrid_search(
        query_text=query_text,
        collection_name=collection_name,
        limit=limit * 2 if use_llm_reranking else limit,
        vector_weight=vector_weight,
        graph_weight=graph_weight
    )
    
    if use_llm_reranking and len(results) > 0:
        # TODO: Implement LLM-based reranking
        # For now, just return the RRF results
        logger.warning("LLM reranking not yet implemented, returning RRF results")
        pass
    
    return results[:limit]
