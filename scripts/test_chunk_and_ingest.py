"""
Proper ingestion workflow: Read → Chunk → Embed → Store

This demonstrates the complete pipeline for ONE document:
1. Read markdown file
2. Chunk with HybridChunker (Docling)
3. Embed with nomic-embed-code
4. Store in Qdrant
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingestion.chunker import ChunkingConfig, DoclingHybridChunker
from src.config.jina_provider import SentenceTransformerEmbedder, EmbedderConfig
from src.storage.qdrant_store import QdrantStore, QdrantStoreConfig

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def chunk_and_ingest_one():
    """Proper workflow: chunk first, then embed and ingest."""
    
    print("\n" + "="*70)
    print("INNGEST DOCUMENT INGESTION PIPELINE")
    print("="*70 + "\n")
    
    # =================================================================
    # STEP 1: Read Document
    # =================================================================
    logger.info("📄 STEP 1: Reading document...")
    
    doc_path = Path("Docs/inngest_overall/getting-started.md")
    if not doc_path.exists():
        # Find first available document
        inngest_docs = list(Path("Docs/inngest_overall").glob("*.md"))
        if not inngest_docs:
            logger.error("❌ No Inngest documents found!")
            return
        doc_path = inngest_docs[0]
    
    content = doc_path.read_text(encoding="utf-8")
    
    # Extract title from markdown
    title = doc_path.stem
    for line in content.split('\n')[:10]:
        if line.startswith('# '):
            title = line[2:].strip()
            break
    
    logger.info(f"   ✓ Document: {title}")
    logger.info(f"   ✓ Path: {doc_path}")
    logger.info(f"   ✓ Size: {len(content):,} characters")
    
    # =================================================================
    # STEP 2: Chunk Document with HybridChunker
    # =================================================================
    logger.info("\n✂️  STEP 2: Chunking document with HybridChunker...")
    
    chunking_config = ChunkingConfig(
        chunk_size=2048,           # Optimized for code
        chunk_overlap=100,         # Small overlap
        max_chunk_size=4096,       # Max size
        max_tokens=2048,           # Token limit
        use_semantic_splitting=True
    )
    
    chunker = DoclingHybridChunker(chunking_config)
    
    # Chunk the document (returns list of DocumentChunk objects)
    chunks = await chunker.chunk_document(
        content=content,
        title=title,
        source=str(doc_path),
        metadata={"doc_type": "inngest_docs"}
    )
    
    logger.info(f"   ✓ Created {len(chunks)} chunks")
    logger.info(f"   ✓ Chunk size: {chunking_config.chunk_size}")
    logger.info(f"   ✓ Chunk overlap: {chunking_config.chunk_overlap}")
    
    # Show sample chunk
    if chunks:
        sample = chunks[0]
        logger.info(f"\n   📝 Sample chunk preview:")
        logger.info(f"      {sample.content[:150]}...")
        logger.info(f"      Tokens: {sample.token_count}")
    
    # =================================================================
    # STEP 3: Generate Embeddings
    # =================================================================
    logger.info("\n🧠 STEP 3: Generating embeddings with nomic-embed-code...")
    
    embedder_config = EmbedderConfig(
        model_name="nomic-ai/nomic-embed-code",
        device="cpu",
        batch_size=8,
        normalize_embeddings=True
    )
    
    embedder = SentenceTransformerEmbedder(embedder_config)
    logger.info(f"   ✓ Model loaded: {embedder_config.model_name}")
    
    # Extract chunk texts
    chunk_texts = [chunk.content for chunk in chunks]
    
    # Generate embeddings in batch
    logger.info(f"   ⏳ Embedding {len(chunk_texts)} chunks...")
    embeddings = await embedder.embed_documents(chunk_texts)
    
    logger.info(f"   ✓ Generated {len(embeddings)} embeddings")
    logger.info(f"   ✓ Embedding dimension: {len(embeddings[0])}")
    
    # =================================================================
    # STEP 4: Store in Qdrant
    # =================================================================
    logger.info("\n💾 STEP 4: Storing in Qdrant vector database...")
    
    qdrant_config = QdrantStoreConfig(
        host="localhost",
        port=6333,
        collection_name="inngest_docs",
        vector_size=1536,
        enable_quantization=True,
        quantization_type="int8"
    )
    
    logger.info(f"   ⏳ Connecting to Qdrant at {qdrant_config.host}:{qdrant_config.port}...")
    qdrant_store = QdrantStore(qdrant_config)
    logger.info(f"   ✓ Connected to collection: {qdrant_config.collection_name}")
    
    # Prepare data for insertion
    ids = [f"{doc_path.stem}_chunk_{i}" for i in range(len(chunks))]
    
    payloads = []
    for i, chunk in enumerate(chunks):
        payload = {
            "title": title,
            "source": str(doc_path),
            "chunk_index": i,
            "total_chunks": len(chunks),
            "token_count": chunk.token_count,
            "text": chunk.content,
            **chunk.metadata  # Include any chunk metadata
        }
        payloads.append(payload)
    
    # Insert into Qdrant
    logger.info(f"   ⏳ Inserting {len(chunks)} vectors...")
    qdrant_store.add_embeddings(
        embeddings=embeddings,
        metadatas=payloads,
        ids=ids
    )
    
    logger.info(f"   ✓ Stored {len(chunks)} vectors with metadata")
    
    # =================================================================
    # STEP 5: Test Search
    # =================================================================
    logger.info("\n🔍 STEP 5: Testing semantic search...")
    
    test_query = "How do I create a function in Inngest?"
    logger.info(f"   Query: '{test_query}'")
    
    # Embed query
    query_embedding = await embedder.embed_query(test_query)
    
    # Search
    results = qdrant_store.search(
        query_embedding=query_embedding,
        limit=3
    )
    
    logger.info(f"   ✓ Found {len(results)} results\n")
    
    for idx, result in enumerate(results, 1):
        logger.info(f"   Result {idx}:")
        logger.info(f"      Score: {result['score']:.4f}")
        logger.info(f"      Source: {result['metadata'].get('source', 'N/A')}")
        logger.info(f"      Chunk: {result['metadata'].get('chunk_index', 'N/A')}/{result['metadata'].get('total_chunks', 'N/A')}")
        logger.info(f"      Preview: {result['content'][:120]}...")
        logger.info("")
    
    # =================================================================
    # SUMMARY
    # =================================================================
    print("\n" + "="*70)
    print("✅ INGESTION COMPLETE!")
    print("="*70)
    print(f"\n📊 Summary:")
    print(f"   Document: {title}")
    print(f"   Chunks created: {len(chunks)}")
    print(f"   Embeddings generated: {len(embeddings)}")
    print(f"   Vectors stored: {len(ids)}")
    print(f"\n📍 Storage Location:")
    print(f"   Database: Qdrant")
    print(f"   Host: {qdrant_config.host}:{qdrant_config.port}")
    print(f"   Collection: {qdrant_config.collection_name}")
    print(f"   Vector size: {qdrant_config.vector_size} dimensions")
    print(f"   Quantization: {qdrant_config.quantization_type} (4x memory savings)")
    print(f"\n🌐 View in Qdrant Dashboard:")
    print(f"   http://localhost:6333/dashboard")
    print(f"   Collection: {qdrant_config.collection_name}")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(chunk_and_ingest_one())
