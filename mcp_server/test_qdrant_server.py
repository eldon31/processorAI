"""Test script for the Qdrant Code MCP server."""

import asyncio
import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.config.jina_provider import EmbedderConfig, SentenceTransformerEmbedder
from src.storage.qdrant_store import QdrantStoreConfig, QdrantStore


async def test_search():
    """Test search functionality."""
    print("=== Testing Qdrant Search ===\n")
    
    # Initialize embedder
    print("Initializing embedder (nomic-ai/nomic-embed-code)...")
    embedder_config = EmbedderConfig(
        model_name="nomic-ai/nomic-embed-code",
        device="cpu",
        batch_size=32
    )
    embedder = SentenceTransformerEmbedder(embedder_config)
    print("✓ Embedder initialized\n")
    
    # Initialize Qdrant stores
    collections = {
        "agent_kit": QdrantStore(QdrantStoreConfig(
            host="localhost",
            port=6333,
            collection_name="agent_kit",
            vector_size=3584,
            enable_quantization=True,
            prefer_grpc=False
        )),
        "inngest_overall": QdrantStore(QdrantStoreConfig(
            host="localhost",
            port=6333,
            collection_name="inngest_overall",
            vector_size=3584,
            enable_quantization=True,
            prefer_grpc=False
        ))
    }
    
    # Test 1: Search agent_kit
    print("Test 1: Searching agent_kit for 'how to create an agent'")
    query = "how to create an agent"
    embedding = await embedder.embed_documents([query])
    results = collections["agent_kit"].search(
        query_embedding=embedding[0],
        limit=3,
        score_threshold=0.5
    )
    
    print(f"Found {len(results)} results:")
    for idx, result in enumerate(results, 1):
        print(f"\n  Result {idx}:")
        print(f"    Score: {result['score']:.3f}")
        print(f"    Content: {result['content'][:150]}...")
        print(f"    Source: {result['metadata'].get('document_title', 'N/A')}")
    
    # Test 2: Search inngest_overall
    print("\n\nTest 2: Searching inngest_overall for 'functions and workflows'")
    query = "functions and workflows"
    embedding = await embedder.embed_documents([query])
    results = collections["inngest_overall"].search(
        query_embedding=embedding[0],
        limit=3,
        score_threshold=0.5
    )
    
    print(f"Found {len(results)} results:")
    for idx, result in enumerate(results, 1):
        print(f"\n  Result {idx}:")
        print(f"    Score: {result['score']:.3f}")
        print(f"    Content: {result['content'][:150]}...")
        print(f"    Source: {result['metadata'].get('document_title', 'N/A')}")
    
    # Test 3: Get stats
    print("\n\nTest 3: Collection Statistics")
    for name, store in collections.items():
        stats = store.get_stats()
        print(f"\n  {name}:")
        print(f"    Points: {stats['points_count']}")
        print(f"    Indexed: {stats['indexed_vectors_count']}")
        print(f"    Status: {stats['status']}")
    
    print("\n\n✓ All tests passed!")


if __name__ == "__main__":
    asyncio.run(test_search())
