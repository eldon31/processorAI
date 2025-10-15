"""Test search functionality in the MCP server."""
import sys
import asyncio
from pathlib import Path

# Add project root to path
sys.path.insert(0, '/app')

from src.config.jina_provider import EmbedderConfig, SentenceTransformerEmbedder
from src.storage.qdrant_store import QdrantStoreConfig, QdrantStore

async def test_search():
    print("Initializing embedder...")
    embedder = SentenceTransformerEmbedder(
        EmbedderConfig(model_name='nomic-ai/nomic-embed-code')
    )
    
    print("Generating query embedding...")
    query = "agent framework"
    vec = await embedder.embed_documents([query])
    print(f"Vector shape: {len(vec[0])}")
    
    print("Connecting to Qdrant...")
    store = QdrantStore(
        QdrantStoreConfig(
            host='host.docker.internal',
            port=6333,
            collection_name='agent_kit',
            vector_size=3584,
            prefer_grpc=False
        )
    )
    
    print(f"Searching for: {query}")
    results = store.search(
        query_embedding=vec[0],
        limit=3,
        score_threshold=0.3
    )
    
    print(f"\nResults found: {len(results)}")
    for idx, result in enumerate(results, 1):
        print(f"\n--- Result {idx} ---")
        print(f"Score: {result.get('score', 0):.3f}")
        content = result.get('content', '')
        print(f"Content preview: {content[:200]}...")

if __name__ == "__main__":
    asyncio.run(test_search())
