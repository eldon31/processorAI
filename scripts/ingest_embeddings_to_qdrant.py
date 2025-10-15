"""Ingest precomputed embeddings JSONL files into a Qdrant collection."""

import argparse
import json
import hashlib
from pathlib import Path
from typing import Iterable, List, Dict, Any

from src.storage.qdrant_store import QdrantStore, QdrantStoreConfig


def string_to_int_id(s: str) -> int:
    """Convert a string ID to a deterministic integer ID for Qdrant (64-bit unsigned)."""
    # Use first 16 hex digits, mod to keep within uint64 range
    hash_int = int(hashlib.sha256(s.encode()).hexdigest()[:16], 16)
    return hash_int % (2**63)  # Keep within positive signed int64 range for safety


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Upload JSONL embeddings to Qdrant.")
    parser.add_argument(
        "--embeddings-dir",
        default="output/embeddings/agent_kit",
        help="Directory containing *.jsonl embeddings produced by the embedding script.",
    )
    parser.add_argument(
        "--collection",
        default="agent_kit",
        help="Target Qdrant collection name.",
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="Qdrant host.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=6333,
        help="Qdrant port.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=200,
        help="Number of vectors to upsert per batch.",
    )
    parser.add_argument(
        "--disable-quantization",
        action="store_true",
        help="Do not enable scalar quantization when creating the collection.",
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=None,
        help="Optional limit on the number of JSONL files to ingest.",
    )
    return parser.parse_args()


def iter_embedding_records(file_path: Path) -> Iterable[Dict[str, Any]]:
    """Yield JSON records from a JSONL embeddings file."""
    with file_path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            raw_line = raw_line.strip()
            if not raw_line:
                continue
            try:
                yield json.loads(raw_line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON at {file_path}:{line_number}: {exc}")


def load_vector_size(sample_file: Path) -> int:
    """Determine embedding dimensionality from the first record."""
    for record in iter_embedding_records(sample_file):
        embedding = record.get("embedding")
        if not embedding:
            continue
        return len(embedding)
    raise ValueError(f"No embeddings found in {sample_file}")


def ensure_collection(vector_size: int, args: argparse.Namespace) -> QdrantStore:
    """Instantiate QdrantStore with the detected vector size."""
    config = QdrantStoreConfig(
        host=args.host,
        port=args.port,
        collection_name=args.collection,
        vector_size=vector_size,
        enable_quantization=not args.disable_quantization,
    )
    return QdrantStore(config)


def ingest_file(store: QdrantStore, file_path: Path, batch_size: int) -> int:
    """Read a JSONL file and push its records into Qdrant."""
    embeddings: List[List[float]] = []
    metadatas: List[Dict[str, Any]] = []
    ids: List[int] = []
    written = 0

    for record in iter_embedding_records(file_path):
        embedding = record.get("embedding")
        if not embedding:
            continue

        chunk_id = record.get("id")
        metadata = dict(record.get("metadata", {}))
        metadata.setdefault("collection", record.get("collection"))
        metadata.setdefault("source_file", file_path.name)
        if chunk_id:
            metadata.setdefault("chunk_id", chunk_id)

        embeddings.append(embedding)
        metadatas.append(metadata)
        # Convert string ID to integer for Qdrant compatibility
        numeric_id = string_to_int_id(chunk_id) if chunk_id else string_to_int_id(f"{file_path.stem}:{len(ids)}")
        ids.append(numeric_id)

        if len(embeddings) >= batch_size:
            store.add_embeddings(embeddings, metadatas, ids)
            written += len(ids)
            embeddings.clear()
            metadatas.clear()
            ids.clear()

    if embeddings:
        store.add_embeddings(embeddings, metadatas, ids)
        written += len(ids)

    return written


def main() -> None:
    args = parse_args()
    embeddings_dir = Path(args.embeddings_dir).resolve()

    if not embeddings_dir.exists():
        raise SystemExit(f"Embeddings directory not found: {embeddings_dir}")

    files = sorted(embeddings_dir.glob("*.jsonl"))
    if args.max_files:
        files = files[: args.max_files]

    if not files:
        raise SystemExit(f"No embeddings JSONL files found in {embeddings_dir}")

    vector_size = load_vector_size(files[0])
    print(f"Detected embedding dimension: {vector_size}")

    store = ensure_collection(vector_size, args)

    total_vectors = 0
    for index, file_path in enumerate(files, start=1):
        print(f"[{index}/{len(files)}] Ingesting {file_path.name}...")
        before = total_vectors
        count = ingest_file(store, file_path, args.batch_size)
        total_vectors = before + count
        print(f"  Added {count} vectors from {file_path.name}")

    print(f"Finished ingesting {total_vectors} vectors into collection '{args.collection}'.")


if __name__ == "__main__":
    main()
