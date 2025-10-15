"""Chunk markdown documentation into JSON files (defaults to Docs/agent_kit)."""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import List

CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Ensure a public tokenizer is selected for chunking even if the environment overrides it
os.environ.setdefault("EMBEDDING_MODEL", "nomic-ai/nomic-embed-code")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chunk markdown files into JSON chunks.")
    parser.add_argument(
        "--input-dir",
        default="Docs/agent_kit",
        help="Directory containing markdown files to chunk (relative to repo root).",
    )
    parser.add_argument(
        "--output-dir",
        default="output/chunked/agent_kit",
        help="Directory to write chunked JSON (relative to repo root).",
    )
    return parser.parse_args()

from src.ingestion.processor import DocumentProcessor
from src.ingestion.chunker import ChunkingConfig, create_chunker, DocumentChunk

def serialise_chunks(chunks: List[DocumentChunk]) -> List[dict]:
    serialised = []
    for chunk in chunks:
        serialised.append(
            {
                "index": chunk.index,
                "text": chunk.content,
                "char_count": len(chunk.content),
                "token_count": chunk.token_count,
                "metadata": chunk.metadata,
            }
        )
    return serialised


def write_output(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False, default=str)


async def chunk_file(
    processor: DocumentProcessor,
    chunker,
    file_path: Path,
    output_dir: Path,
) -> None:
    processed = processor.process_file(str(file_path))
    chunks = await chunker.chunk_document(
        content=processed.content,
        title=processed.metadata.title or file_path.stem,
        source=str(file_path),
        metadata=processed.metadata.model_dump(mode="json"),
        docling_doc=processed.docling_document,
    )

    output_data = {
        "source": str(file_path),
        "title": processed.metadata.title or file_path.stem,
        "num_chunks": len(chunks),
        "total_chars": sum(len(chunk.content) for chunk in chunks),
        "chunks": serialise_chunks(chunks),
    }

    output_file = output_dir / f"{file_path.stem}_chunks.json"
    write_output(output_file, output_data)
    print(f"Chunked {file_path.name}: {len(chunks)} chunks -> {output_file}")


async def main() -> None:
    args = parse_args()
    input_dir = (ROOT_DIR / args.input_dir).resolve()
    output_dir = (ROOT_DIR / args.output_dir).resolve()

    if not input_dir.exists():
        raise SystemExit(f"Input directory not found: {input_dir}")

    processor = DocumentProcessor()
    chunk_config = ChunkingConfig(max_tokens=2048, chunk_overlap=100, min_chunk_size=100)
    chunker = create_chunker(chunk_config)

    markdown_files = sorted(input_dir.glob("*.md"))
    if not markdown_files:
        raise SystemExit(f"No markdown files found in {input_dir}")

    for file_path in markdown_files:
        await chunk_file(processor, chunker, file_path, output_dir)


if __name__ == "__main__":
    asyncio.run(main())
