"""
Custom MCP server for Qdrant with nomic-ai/nomic-embed-code embeddings.
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

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)

from src.config.jina_provider import EmbedderConfig, SentenceTransformerEmbedder
from src.storage.qdrant_store import QdrantStoreConfig, QdrantStore

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("qdrant-code-mcp")

# Global state
embedder: Optional[SentenceTransformerEmbedder] = None
stores: dict[str, QdrantStore] = {}

EMBEDDING_MODEL = "nomic-ai/nomic-embed-code"
VECTOR_SIZE = 3584
COLLECTIONS = ["agent_kit", "inngest_overall"]


async def initialize_embedder():
    """Initialize the embedding model."""
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


async def initialize_qdrant_stores():
    """Initialize Qdrant connections for both collections."""
    global stores
    
    for collection in COLLECTIONS:
        if collection not in stores:
            logger.info(f"Connecting to Qdrant collection: {collection}")
            config = QdrantStoreConfig(
                host="localhost",
                port=6333,
                collection_name=collection,
                vector_size=VECTOR_SIZE,
                enable_quantization=True,
                prefer_grpc=False
            )
            stores[collection] = QdrantStore(config)
            logger.info(f"Connected to collection: {collection}")


# Create MCP server
server = Server("qdrant-code-server")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="qdrant_search_agent_kit",
            description="Search the agent_kit collection (AI agent documentation) using semantic similarity with nomic-embed-code",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of results (default: 5)",
                        "default": 5
                    },
                    "score_threshold": {
                        "type": "number",
                        "description": "Minimum similarity score (0-1, default: 0.7)",
                        "default": 0.7
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="qdrant_search_inngest",
            description="Search the inngest_overall collection (Inngest workflow platform docs) using semantic similarity with nomic-embed-code",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of results (default: 5)",
                        "default": 5
                    },
                    "score_threshold": {
                        "type": "number",
                        "description": "Minimum similarity score (0-1, default: 0.7)",
                        "default": 0.7
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="qdrant_store_agent_kit",
            description="Store a new text chunk in the agent_kit collection with semantic embedding",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text content to store"
                    },
                    "metadata": {
                        "type": "object",
                        "description": "Optional metadata (e.g., source, tags, title)",
                        "default": {}
                    }
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="qdrant_store_inngest",
            description="Store a new text chunk in the inngest_overall collection with semantic embedding",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text content to store"
                    },
                    "metadata": {
                        "type": "object",
                        "description": "Optional metadata (e.g., source, tags, title)",
                        "default": {}
                    }
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="qdrant_get_stats",
            description="Get statistics for both Qdrant collections (vector counts, index status, etc.)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool execution."""
    
    # Initialize on first use
    await initialize_embedder()
    await initialize_qdrant_stores()
    
    try:
        if name == "qdrant_search_agent_kit":
            return await search_collection("agent_kit", arguments)
        
        elif name == "qdrant_search_inngest":
            return await search_collection("inngest_overall", arguments)
        
        elif name == "qdrant_store_agent_kit":
            return await store_in_collection("agent_kit", arguments)
        
        elif name == "qdrant_store_inngest":
            return await store_in_collection("inngest_overall", arguments)
        
        elif name == "qdrant_get_stats":
            return await get_collection_stats()
        
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    except Exception as e:
        logger.error(f"Error executing {name}: {e}", exc_info=True)
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def search_collection(collection: str, arguments: dict) -> list[TextContent]:
    """Search a Qdrant collection."""
    query = arguments.get("query", "")
    limit = arguments.get("limit", 5)
    score_threshold = arguments.get("score_threshold", 0.7)
    
    if not query:
        return [TextContent(type="text", text="Error: query is required")]
    
    logger.info(f"Searching {collection} for: {query[:50]}...")
    
    # Generate query embedding
    embedding = await embedder.embed_documents([query])
    query_vector = embedding[0]
    
    # Search Qdrant
    store = stores[collection]
    results = store.search(
        query_embedding=query_vector,
        limit=limit,
        score_threshold=score_threshold
    )
    
    # Format results
    if not results:
        return [TextContent(
            type="text",
            text=f"No results found in {collection} for query: {query}"
        )]
    
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
    
    return [TextContent(type="text", text="\n".join(output_lines))]


async def store_in_collection(collection: str, arguments: dict) -> list[TextContent]:
    """Store text in a Qdrant collection."""
    text = arguments.get("text", "")
    metadata = arguments.get("metadata", {})
    
    if not text:
        return [TextContent(type="text", text="Error: text is required")]
    
    logger.info(f"Storing text in {collection}: {text[:50]}...")
    
    # Generate embedding
    embedding = await embedder.embed_documents([text])
    
    # Add content to metadata
    metadata["content"] = text
    metadata["collection"] = collection
    
    # Store in Qdrant
    store = stores[collection]
    ids = store.add_embeddings(
        embeddings=embedding,
        metadatas=[metadata]
    )
    
    return [TextContent(
        type="text",
        text=f"Successfully stored text in {collection} with ID: {ids[0]}\nText length: {len(text)} chars"
    )]


async def get_collection_stats() -> list[TextContent]:
    """Get statistics for all collections."""
    stats_lines = ["Qdrant Collection Statistics:\n"]
    
    for collection in COLLECTIONS:
        store = stores[collection]
        stats = store.get_stats()
        
        stats_lines.append(f"\n{collection}:")
        stats_lines.append(f"  Points: {stats.get('points_count', 0)}")
        stats_lines.append(f"  Indexed: {stats.get('indexed_vectors_count', 0)}")
        stats_lines.append(f"  Status: {stats.get('status', 'unknown')}")
        stats_lines.append(f"  Quantization: {stats.get('quantization_enabled', False)}")
    
    return [TextContent(type="text", text="\n".join(stats_lines))]


async def main():
    """Run the MCP server."""
    logger.info("Starting Qdrant Code MCP Server")
    logger.info(f"Collections: {', '.join(COLLECTIONS)}")
    logger.info(f"Embedding model: {EMBEDDING_MODEL}")
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="qdrant-code-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
