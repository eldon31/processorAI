"""
Test script to ingest a single Inngest document into Qdrant.
Shows where embeddings are stored and how to query them.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.jina_provider import SentenceTransformerEmbedder, EmbedderConfig
from src.storage.qdrant_store import QdrantStore, QdrantStoreConfig

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def ingest_one_document():
    """Ingest a single Inngest document and show storage location."""
    
    # 1. Read one Inngest document
    doc_path = Path("Docs/inngest_overall/getting-started.md")
    
    if not doc_path.exists():
        # Try alternative document
        inngest_docs = list(Path("Docs/inngest_overall").glob("*.md"))
        if not inngest_docs:
            logger.error("No Inngest documents found!")
            return
        doc_path = inngest_docs[0]
    
    logger.info(f"📄 Reading document: {doc_path}")
    content = doc_path.read_text(encoding="utf-8")
    
    # Extract title
    lines = content.split('\n')
    title = doc_path.stem
    for line in lines[:10]:
        if line.startswith('# '):
            title = line[2:].strip()
            break
    
    logger.info(f"📝 Title: {title}")
    logger.info(f"📊 Content length: {len(content)} chars")
    
    # 2. Create simple chunks (not using Docling for simplicity)
    chunk_size = 2048
    chunks = []
    for i in range(0, len(content), chunk_size):
        chunk_text = content[i:i + chunk_size]
        chunks.append({
            "text": chunk_text,
            "index": len(chunks),
            "source": str(doc_path)
        })
    
    logger.info(f"✂️  Created {len(chunks)} chunks")
    
    # 3. Initialize Qdrant
    logger.info("🔌 Connecting to Qdrant...")
    qdrant_config = QdrantStoreConfig(
        host="localhost",
        port=6333,
        collection_name="inngest_docs",
        vector_size=1536,  # nomic-embed-code dimension
        enable_quantization=True
    )
    
    qdrant_store = QdrantStore(qdrant_config)
    logger.info("✅ Qdrant connected!")
    
    # 4. Initialize embedding provider
    logger.info("🧠 Initializing nomic-embed-code embeddings...")
    embedder_config = EmbedderConfig(
        model_name="nomic-ai/nomic-embed-code",
        device="cpu",
        batch_size=8
    )
    embedder = SentenceTransformerEmbedder(embedder_config)
    logger.info("✅ Embedder ready!")
    
    # 5. Generate embeddings and store
    logger.info("🔢 Generating embeddings...")
    
    # Get all chunk texts for batch embedding
    chunk_texts = [chunk["text"] for chunk in chunks]
    
    # Generate embeddings in batch
    embeddings = await embedder.embed_documents(chunk_texts)
    
    # Prepare all data for batch insertion
    ids = [f"{doc_path.stem}_chunk_{i}" for i in range(len(chunks))]
    payloads = [{
        "title": title,
        "source": str(doc_path),
        "chunk_index": i,
        "total_chunks": len(chunks),
        "text": chunk["text"]
    } for i, chunk in enumerate(chunks)]
    
    # Store all in Qdrant at once
    qdrant_store.add_embeddings(
        ids=ids,
        embeddings=embeddings,
        payloads=payloads
    )
    
    logger.info(f"  ✓ All {len(chunks)} chunks embedded and stored")
    
    logger.info("\n" + "="*70)
    logger.info("🎉 SUCCESS! Document ingested into Qdrant")
    logger.info("="*70)
    logger.info(f"\n📍 STORAGE LOCATION:")
    logger.info(f"   - Vector Database: Qdrant")
    logger.info(f"   - Host: {qdrant_config.host}:{qdrant_config.port}")
    logger.info(f"   - Collection: {qdrant_config.collection_name}")
    logger.info(f"   - Vectors stored: {len(chunks)}")
    logger.info(f"   - Vector dimension: 1536")
    logger.info(f"   - Quantization: int8 (4x memory savings)")
    logger.info(f"\n📊 METADATA:")
    logger.info(f"   - Document: {title}")
    logger.info(f"   - Source: {doc_path}")
    logger.info(f"   - Chunks: {len(chunks)}")
    logger.info(f"   - Model: nomic-ai/nomic-embed-code")
    
    # 6. Test a simple search
    logger.info(f"\n🔍 Testing search...")
    query = "How do I create a function?"
    query_embeddings = await embedder.embed_query(query)
    
    results = qdrant_store.search(
        query_embedding=query_embeddings,
        limit=3
    )
    
    logger.info(f"   Query: '{query}'")
    logger.info(f"   Results found: {len(results)}")
    for idx, result in enumerate(results):
        logger.info(f"   {idx+1}. Score: {result.score:.4f}")
        logger.info(f"      Preview: {result.payload.get('text', 'N/A')[:100]}...")
    
    logger.info("\n" + "="*70)
    logger.info("✅ INGESTION COMPLETE!")
    logger.info("="*70)
    logger.info(f"\nTo view in Qdrant Dashboard:")
    logger.info(f"   Open browser: http://localhost:6333/dashboard")
    logger.info(f"   Collection: {qdrant_config.collection_name}")


if __name__ == "__main__":
    asyncio.run(ingest_one_document())
