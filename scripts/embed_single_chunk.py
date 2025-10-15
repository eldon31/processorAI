"""Embed a single chunk using the SentenceTransformer embedder.

Usage:
    python scripts/embed_single_chunk.py [chunk_index]

If no index is provided, chunk 0 is used.
"""

import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.jina_provider import SentenceTransformerEmbedder, EmbedderConfig


async def main(chunk_index: int) -> None:
    chunks_path = Path("output/chunks/apps_docling_chunks.json")
    if not chunks_path.exists():
        print(f"ERROR: Chunk file not found at {chunks_path}")
        return

    with open(chunks_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    chunks = data.get("chunks", [])
    if not chunks:
        print("ERROR: No chunks present in the JSON file")
        return

    if chunk_index < 0 or chunk_index >= len(chunks):
        print(f"ERROR: Chunk index {chunk_index} is out of range (0-{len(chunks) - 1})")
        return

    chunk = chunks[chunk_index]
    text = chunk.get("text", "")
    char_count = len(text)
    token_count = chunk.get("token_count", 0)

    print(f"Embedding chunk {chunk_index}")
    print(f"   Characters: {char_count}")
    print(f"   Tokens: {token_count}")
    preview = text[:200].replace("\n", " ")
    print(f"   Preview: {preview}...")

    config = EmbedderConfig(
        model_name="nomic-ai/nomic-embed-code",
        device="cpu",
        batch_size=1,
        normalize_embeddings=True
    )
    embedder = SentenceTransformerEmbedder(config)

    try:
        embedding = await embedder.embed_documents([text])
    except Exception as exc:
        print(f"ERROR: Failed to embed chunk {chunk_index}: {exc}")
        raise

    if not embedding:
        print("ERROR: Embedding result is empty")
        return

    vector = embedding[0]
    print(f"Embedding generated successfully with dimension {len(vector)}")
    print(f"First 10 values: {vector[:10]}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            index = int(sys.argv[1])
        except ValueError:
            print("ERROR: chunk_index must be an integer")
            sys.exit(1)
    else:
        index = 0

    asyncio.run(main(index))
