"""
FastMCP-based Qdrant server with nomic-ai/nomic-embed-code embeddings.
Supports both agent_kit and inngest_overall collections.
"""

import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import Any, Optional

# Add project root to path
CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastmcp import FastMCP

from src.config.jina_provider import EmbedderConfig, SentenceTransformerEmbedder
from src.storage.qdrant_store import QdrantStoreConfig, QdrantStore

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("qdrant-fastmcp")

# Initialize FastMCP server
mcp = FastMCP("qdrant-codes")

# Global state
embedder: Optional[SentenceTransformerEmbedder] = None
stores: dict[str, QdrantStore] = {}

EMBEDDING_MODEL = "nomic-ai/nomic-embed-code"
VECTOR_SIZE = 3584
COLLECTIONS = ["agent_kit", "inngest_overall"]
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))


def get_embedder():
    """Lazy-load and return the embedder."""
    global embedder
    if embedder is None:
        logger.info(f"Initializing embedder: {EMBEDDING_MODEL}")
        embedder_config = EmbedderConfig(
            model_name=EMBEDDING_MODEL,
            device="cpu",
            batch_size=32
        )
        embedder = SentenceTransformerEmbedder(embedder_config)
        logger.info("Embedder initialized")
    return embedder


def get_store(collection: str) -> QdrantStore:
    """Lazy-load and return a Qdrant store."""
    global stores
    if collection not in stores:
        logger.info(f"Connecting to Qdrant collection: {collection}")
        config = QdrantStoreConfig(
            host=QDRANT_HOST,
            port=QDRANT_PORT,
            collection_name=collection,
            vector_size=VECTOR_SIZE,
            enable_quantization=True,
            prefer_grpc=False
        )
        stores[collection] = QdrantStore(config)
        logger.info(f"Connected to collection: {collection}")
    return stores[collection]


@mcp.tool()
async def qdrant_search_agent_kit(query: str, limit: int = 5, score_threshold: float = 0.7) -> str:
    """
    Search the agent_kit collection (AI agent documentation) using semantic similarity.
    
    Args:
        query: Search query text
        limit: Maximum number of results (default: 5)
        score_threshold: Minimum similarity score 0-1 (default: 0.7)
    
    Returns:
        Formatted search results with scores and metadata
    """
    return await _search_collection("agent_kit", query, limit, score_threshold)


@mcp.tool()
async def qdrant_search_inngest(query: str, limit: int = 5, score_threshold: float = 0.7) -> str:
    """
    Search the inngest_overall collection (Inngest workflow platform docs) using semantic similarity.
    
    Args:
        query: Search query text
        limit: Maximum number of results (default: 5)
        score_threshold: Minimum similarity score 0-1 (default: 0.7)
    
    Returns:
        Formatted search results with scores and metadata
    """
    return await _search_collection("inngest_overall", query, limit, score_threshold)


@mcp.tool()
async def qdrant_get_stats() -> str:
    """
    Get statistics for both Qdrant collections (vector counts, index status, etc.).
    
    Returns:
        Formatted statistics for all collections
    """
    stats_lines = ["Qdrant Collection Statistics:\n"]
    
    for collection in COLLECTIONS:
        store = get_store(collection)
        stats = store.get_stats()
        
        stats_lines.append(f"\n{collection}:")
        stats_lines.append(f"  Points: {stats.get('points_count', 0)}")
        stats_lines.append(f"  Indexed: {stats.get('indexed_vectors_count', 0)}")
        stats_lines.append(f"  Status: {stats.get('status', 'unknown')}")
        stats_lines.append(f"  Quantization: {stats.get('quantization_enabled', False)}")
    
    return "\n".join(stats_lines)


async def _search_collection(collection: str, query: str, limit: int, score_threshold: float) -> str:
    """Internal search implementation."""
    if not query:
        return "Error: query is required"
    
    logger.info(f"Searching {collection} for: {query[:50]}...")
    
    # Generate query embedding
    emb = get_embedder()
    embedding = await emb.embed_documents([query])
    query_vector = embedding[0]
    
    # Search Qdrant
    store = get_store(collection)
    results = store.search(
        query_embedding=query_vector,
        limit=limit,
        score_threshold=score_threshold
    )
    
    # Format results
    if not results:
        return f"No results found in {collection} for query: {query}"
    
    output_lines = [f"Found {len(results)} results in {collection}:\n"]
    
    for idx, result in enumerate(results, 1):
        score = result.get("score", 0)
        content = result.get("content", "")
        metadata = result.get("metadata", {})
        
        output_lines.append(f"\n--- Result {idx} (Score: {score:.3f}) ---")
        output_lines.append(f"Content: {content[:500]}..." if len(content) > 500 else f"Content: {content}")
        
        if metadata:
            output_lines.append(f"Metadata:")
            for key, value in metadata.items():
                if key not in ["content", "embedding"]:
                    output_lines.append(f"  {key}: {value}")
    
    return "\n".join(output_lines)


if __name__ == "__main__":
    logger.info("Starting Qdrant FastMCP Server")
    logger.info(f"Collections: {', '.join(COLLECTIONS)}")
    logger.info(f"Embedding model: {EMBEDDING_MODEL}")
    logger.info(f"Qdrant: {QDRANT_HOST}:{QDRANT_PORT}")
    
    mcp.run()
