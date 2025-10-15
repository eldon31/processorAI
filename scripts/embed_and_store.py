"""
Steps 3-4: Embed chunks and store in Qdrant
Reads the chunked JSON file and completes the RAG pipeline
"""

import json
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.jina_provider import SentenceTransformerEmbedder, EmbedderConfig
from src.storage.qdrant_store import QdrantStore, QdrantStoreConfig


async def embed_and_store():
    """Steps 3-4: Embed chunks and store in Qdrant."""

    print("=" * 70)
    print("STEPS 3-4: EMBED & STORE IN QDRANT")
    print("=" * 70)

    # Load the chunked data
    chunks_file = Path("output/chunks/apps_docling_chunks.json")

    if not chunks_file.exists():
        print(f"ERROR: Chunks file not found: {chunks_file}")
        return

    print("\nLOADING CHUNKS")
    print(f"   File: {chunks_file}")

    with open(chunks_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    chunks = data.get('chunks', [])
    if not chunks:
        print("ERROR: No chunks found in the chunk file")
        return

    print(f"   Loaded {len(chunks)} chunks")
    print(f"   Source: {data.get('source')}")
    print(f"   Title: {data.get('title')}")

    # ================================================================
    # STEP 3: GENERATE EMBEDDINGS
    # ================================================================
    print("\n" + "=" * 70)
    print("STEP 3: GENERATING EMBEDDINGS")
    print("=" * 70)

    print("\nInitializing embedder...")
    embedder_config = EmbedderConfig(
        model_name="nomic-ai/nomic-embed-code",
        device="cpu",
        batch_size=8,
        normalize_embeddings=True
    )
    embedder = SentenceTransformerEmbedder(embedder_config)

    print("   Model: nomic-ai/nomic-embed-code")
    print("   Dimension: 1536")
    print("   Device: CPU")

    print(f"\nEmbedding {len(chunks)} chunks...")
    chunk_texts = [chunk.get('text', '') for chunk in chunks]
    char_lengths = [len(text) for text in chunk_texts]
    token_counts = [chunk.get('token_count', 0) for chunk in chunks]
    max_chars = max(char_lengths) if char_lengths else 0
    max_tokens = max(token_counts) if token_counts else 0
    avg_chars = sum(char_lengths) / len(char_lengths) if char_lengths else 0

    print(f"   Longest chunk characters: {max_chars}")
    print(f"   Longest chunk tokens: {max_tokens}")
    print(f"   Average characters per chunk: {avg_chars:.1f}")
    if max_chars > 8000:
        print("   WARNING: A chunk exceeds 8000 characters. Consider re-chunking or truncating.")
    if max_tokens and max_tokens > 6000:
        print("   WARNING: A chunk exceeds 6000 tokens. This may exceed model context limits.")

    embeddings = []
    failed_chunks = []
    for idx, text in enumerate(chunk_texts):
        char_count = char_lengths[idx]
        token_count = token_counts[idx]
        print(f"   -> Embedding chunk {idx + 1}/{len(chunk_texts)} (chars={char_count}, tokens={token_count})")

        if not text.strip():
            print("      WARNING: Chunk text is empty. Skipping this chunk.")
            failed_chunks.append({
                "index": idx,
                "char_count": char_count,
                "token_count": token_count,
                "preview": "",
                "error": "Empty chunk"
            })
            continue

        try:
            result = await embedder.embed_documents([text])
            if not result:
                raise ValueError("Empty embedding returned")
            embeddings.append(result[0])
        except Exception as exc:
            preview = text[:120].replace('\n', ' ')
            print(f"      ERROR embedding chunk {idx}: {exc}")
            failed_chunks.append({
                "index": idx,
                "char_count": char_count,
                "token_count": token_count,
                "preview": preview,
                "error": str(exc)
            })

    if failed_chunks:
        print("\nERROR: Some chunks failed to embed. Summary of up to 10 failures:")
        for failure in failed_chunks[:10]:
            print(
                f"   Chunk {failure['index']} chars={failure['char_count']} tokens={failure['token_count']} "
                f"error={failure['error']} preview='{failure['preview']}'"
            )
        print("\nAborting before storing to Qdrant due to embedding failures.")
        return

    if not embeddings:
        print("ERROR: No embeddings generated. Aborting.")
        return

    print(f"   Generated {len(embeddings)} embeddings")
    print(f"   Vector dimension: {len(embeddings[0])}")
    print(f"   Total vectors: {len(embeddings) * len(embeddings[0]):,} floats")

    # ================================================================
    # STEP 4: STORE IN QDRANT
    # ================================================================
    print("\n" + "=" * 70)
    print("STEP 4: STORING IN QDRANT")
    print("=" * 70)

    print("\nConnecting to Qdrant...")
    qdrant_config = QdrantStoreConfig(
        host="localhost",
        port=6333,
        collection_name="inngest_docs",
        vector_size=1536,
        enable_quantization=True,
        distance_metric="Cosine"
    )

    try:
        qdrant_store = QdrantStore(qdrant_config)
        print("   Connected to Qdrant")
        print(f"   Host: {qdrant_config.host}:{qdrant_config.port}")
        print(f"   Collection: {qdrant_config.collection_name}")
        print(f"   Vector size: {qdrant_config.vector_size}")
        print(f"   Quantization: {'Enabled (int8)' if qdrant_config.enable_quantization else 'Disabled'}")

        # Prepare data for storage
        print("\nPreparing data for storage...")

        doc_name = Path(data.get('source', 'document')).stem
        ids = [f"{doc_name}_chunk_{i}" for i in range(len(chunks))]

        payloads = []
        for i, chunk in enumerate(chunks):
            payload = {
                "title": data.get('title'),
                "source": data.get('source'),
                "chunk_index": i,
                "total_chunks": len(chunks),
                "text": chunk.get('text'),
                "char_count": chunk.get('char_count'),
                "token_count": chunk.get('token_count'),
                "chunker": data.get('chunker'),
                "embedder": "nomic-ai/nomic-embed-code"
            }

            if chunk.get('meta', {}).get('headings'):
                payload['headings'] = chunk['meta']['headings']

            payloads.append(payload)

        print(f"   IDs: {len(ids)}")
        print(f"   Payloads: {len(payloads)}")
        print(f"   Vectors: {len(embeddings)}")

        # Store in Qdrant
        print("\nStoring vectors in Qdrant...")
        qdrant_store.add_embeddings(
            ids=ids,
            embeddings=embeddings,
            metadatas=payloads
        )

        print(f"   Stored {len(chunks)} vectors successfully!")

        # ================================================================
        # STEP 5: VERIFY WITH SEARCH TEST
        # ================================================================
        print("\n" + "=" * 70)
        print("STEP 5: TESTING SEARCH")
        print("=" * 70)

        test_queries = [
            "What is an Inngest app?",
            "How do I deploy my app?",
            "SDK configuration"
        ]

        for query in test_queries:
            print(f"\nQuery: '{query}'")

            query_embedding = await embedder.embed_query(query)
            results = qdrant_store.search(
                query_embedding=query_embedding,
                limit=2
            )

            print(f"   Found {len(results)} results:")
            for i, result in enumerate(results):
                print(f"\n   --- Result {i + 1} (Score: {result['score']:.4f}) ---")
                print(f"   Chunk: {result['metadata'].get('chunk_index')}/{result['metadata'].get('total_chunks')}")
                if result['metadata'].get('headings'):
                    print(f"   Headings: {result['metadata'].get('headings')}")
                preview = result['metadata'].get('text', '')[:120].replace('\n', ' ')
                print(f"   Preview: {preview}...")

        # ================================================================
        # FINAL SUMMARY
        # ================================================================
        print("\n" + "=" * 70)
        print("PIPELINE COMPLETE!")
        print("=" * 70)

        print("\nSUMMARY:")
        print(f"   Document chunked: {data.get('title')}")
        print(f"   Chunks created: {len(chunks)}")
        print(f"   Embeddings generated: {len(embeddings)}")
        print(f"   Vectors stored in Qdrant: {len(chunks)}")

        print("\nSTORAGE LOCATION:")
        print("   Database: Qdrant Vector DB")
        print("   Host: localhost:6333")
        print(f"   Collection: {qdrant_config.collection_name}")
        print("   Dashboard: http://localhost:6333/dashboard")

        print("\nNEXT STEPS:")
        print("   1. Chunk all 173 Inngest documents")
        print("   2. Embed and store them all in Qdrant")
        print("   3. Query the complete knowledge base")

    except Exception as e:
        print(f"\nERROR: {e}")
        print("\nMake sure Qdrant is running:")
        print("   docker run -p 6333:6333 qdrant/qdrant")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(embed_and_store())
