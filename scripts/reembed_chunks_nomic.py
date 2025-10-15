import argparse
import json
import os
from pathlib import Path
from typing import Any, Dict, List

os.environ.setdefault("TORCHDYNAMO_DISABLE", "1")
os.environ.setdefault("TORCHINDUCTOR_FORCE_DISABLE_CACHES", "1")


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_json(data: Dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)


def collect_chunks(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    if "embedded_chunks" in data and isinstance(data["embedded_chunks"], list):
        return data["embedded_chunks"]
    if "chunks" in data and isinstance(data["chunks"], list):
        return data["chunks"]
    raise ValueError("Input JSON does not contain 'embedded_chunks' or 'chunks'.")


def reembed_chunks(
    chunks: List[Dict[str, Any]],
    model_name: str,
    device: str,
    batch_size: int,
) -> Dict[str, Any]:
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(model_name, device=device, trust_remote_code=True)

    vector_dim = 0
    for idx, chunk in enumerate(chunks):
        text = chunk.get("text", "")
        if not text or not text.strip():
            chunk["embedding"] = None
            chunk["embedding_error"] = "empty_text"
            continue

        vector = model.encode(text, batch_size=batch_size, convert_to_numpy=True)
        if vector_dim == 0:
            vector_dim = len(vector)

        chunk["embedding"] = vector.tolist()
        chunk["embedding_model"] = model_name
        chunk["embedding_dimension"] = len(vector)
        chunk.pop("embedding_error", None)

    successful = sum(1 for chunk in chunks if chunk.get("embedding") is not None)
    failed = len(chunks) - successful

    return {
        "chunks": chunks,
        "model": model_name,
        "dimension": vector_dim,
        "successful": successful,
        "failed": failed,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Re-embed chunks with nomic-ai/nomic-embed-code.")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("output/chunks/embedded_chunks.json"),
        help="Path to the JSON file containing chunks.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output/chunks/embedded_chunks_nomic.json"),
        help="Destination for the re-embedded JSON.",
    )
    parser.add_argument(
        "--model",
        default="nomic-ai/nomic-embed-code",
        help="SentenceTransformer model to use.",
    )
    parser.add_argument(
        "--device",
        default="cpu",
        help="Torch device (e.g., cpu or cuda).",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=4,
        help="Batch size for embedding calls.",
    )
    args = parser.parse_args()

    if not args.input.exists():
        raise FileNotFoundError(f"Input file not found: {args.input}")

    data = load_json(args.input)
    chunks = collect_chunks(data)
    result = reembed_chunks(
        chunks=chunks,
        model_name=args.model,
        device=args.device,
        batch_size=args.batch_size,
    )

    updated: Dict[str, Any] = dict(data)
    updated["embedded_chunks"] = chunks
    updated["embedding_model"] = result["model"]
    updated["embedding_dimension"] = result["dimension"]
    updated["total_chunks"] = len(chunks)
    updated["successful_embeddings"] = result["successful"]
    updated["failed_embeddings"] = result["failed"]

    save_json(updated, args.output)

    print(f"Embedded chunks saved to: {args.output}")
    print(f"Model: {result['model']}")
    print(f"Dimension: {result['dimension']}")
    print(f"Successful: {result['successful']}")
    print(f"Failed: {result['failed']}")


if __name__ == "__main__":
    main()
