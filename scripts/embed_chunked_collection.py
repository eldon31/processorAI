"""Embed chunked JSON files into Qdrant collections."""

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.config.jina_provider import EmbedderConfig, SentenceTransformerEmbedder


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Embed chunked JSON files and store them in Qdrant.")
    parser.add_argument(
        "--chunks-dir",
        default="output/chunked/agent_kit",
        help="Directory containing chunked JSON files.",
    )
    parser.add_argument(
        "--collection",
        default="agent_kit",
        help="Qdrant collection name.",
    )
    parser.add_argument(
        "--out-dir",
        default="output/embeddings",
        help="Directory where embeddings JSONL files will be written (no Qdrant ingest).",
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=None,
        help="Limit the number of chunk JSON files to embed (useful for smoke tests).",
    )
    parser.add_argument(
        "--max-chunks",
        type=int,
        default=None,
        help="Limit the number of chunks embedded per document (e.g. 1 for quick validation).",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=32,
        help="Batch size for sentence-transformers encoding.",
    )
    parser.add_argument(
        "--device",
        default="cpu",
        help="Device for embeddings (cpu, cuda, or mps).",
    )
    return parser.parse_args()


def build_chunk_id(collection: str, source: str, index: int) -> str:
    """Create a deterministic chunk identifier."""
    relative = Path(source).as_posix().replace("/", "_")
    return f"{collection}:{relative}:chunk:{index}"


def prepare_payload(
    document: Dict[str, Any],
    chunk: Dict[str, Any],
    collection: str,
) -> Dict[str, Any]:
    """Merge document and chunk metadata for Qdrant payload."""
    metadata = dict(chunk.get("metadata", {}))
    metadata.update({
        "collection": collection,
        "document_title": document.get("title"),
        "document_source": document.get("source"),
        "chunk_index": chunk.get("index"),
        "total_chunks": document.get("num_chunks"),
        "char_count": chunk.get("char_count"),
        "token_count": chunk.get("token_count"),
        "content": chunk.get("text", ""),
    })
    return metadata


async def embed_directory() -> None:
    args = parse_args()
    chunks_dir = (ROOT_DIR / args.chunks_dir).resolve()

    if not chunks_dir.exists():
        raise SystemExit(f"Chunks directory not found: {chunks_dir}")

    chunk_files = sorted(chunks_dir.glob("*.json"))
    if not chunk_files:
        raise SystemExit(f"No chunked JSON files found in {chunks_dir}")

    output_dir = (ROOT_DIR / args.out_dir / Path(args.collection)).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    embedder_config = EmbedderConfig(
        model_name="nomic-ai/nomic-embed-code",
        device=args.device,
        batch_size=args.batch_size,
    )
    embedder = SentenceTransformerEmbedder(embedder_config)
    print(
        f"Embedding model: {embedder_config.model_name} | device={embedder_config.device} | batch_size={embedder_config.batch_size}"
    )

    total_chunks = 0
    total_files = 0

    selected_files = chunk_files[: args.max_files] if args.max_files else chunk_files

    for json_path in selected_files:
        data = json.loads(json_path.read_text(encoding="utf-8"))
        chunks: List[Dict[str, Any]] = data.get("chunks", [])
        if not chunks:
            continue

        selected_chunks = chunks[: args.max_chunks] if args.max_chunks else chunks
        if not selected_chunks:
            print(f"No chunks selected from {json_path.name}; skipping.")
            continue

        texts = [chunk.get("text", "") for chunk in selected_chunks]

        print(f"Embedding {len(texts)} chunks from {json_path.name}...")
        embeddings: List[List[float]] = []
        total_batches = (len(texts) + embedder_config.batch_size - 1) // embedder_config.batch_size
        for batch_index in range(total_batches):
            start = batch_index * embedder_config.batch_size
            end = start + embedder_config.batch_size
            batch_texts = texts[start:end]
            print(f"  Batch {batch_index + 1}/{total_batches} (chunks {start + 1}-{min(end, len(texts))})")
            batch_embeddings = await embedder.embed_documents(batch_texts)
            embeddings.extend(batch_embeddings)

        written = 0
        output_file = output_dir / f"{json_path.stem}_embeddings.jsonl"
        with output_file.open("w", encoding="utf-8") as out_handle:
            for chunk, embedding in zip(selected_chunks, embeddings):
                text = chunk.get("text", "")
                if not text.strip():
                    continue
                chunk_id = build_chunk_id(
                    args.collection,
                    data.get("source", json_path.name),
                    chunk.get("index", 0),
                )
                record = {
                    "id": chunk_id,
                    "collection": args.collection,
                    "metadata": prepare_payload(data, chunk, args.collection),
                    "embedding": embedding,
                }
                out_handle.write(json.dumps(record))
                out_handle.write("\n")
                written += 1

        total_chunks += written
        total_files += 1
        print(f"Embedded {written} chunks from {json_path.name} -> {output_file.relative_to(ROOT_DIR)}")

    print(f"Embedded {total_chunks} chunks across {total_files} files into {output_dir.relative_to(ROOT_DIR)}.")


if __name__ == "__main__":
    asyncio.run(embed_directory())
