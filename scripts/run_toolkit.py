"""Command-line entry point for the consolidated knowledge ingestion toolkit."""

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.toolkit import CollectionConfig, KnowledgeToolkit, ToolkitSettings


def load_config(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_collections(raw_collections: List[Dict[str, Any]]) -> List[CollectionConfig]:
    return [CollectionConfig(**collection) for collection in raw_collections]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the knowledge ingestion toolkit pipeline.")
    parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Path to the JSON configuration file describing collections.",
    )
    args = parser.parse_args()

    config_data = load_config(args.config)

    settings = ToolkitSettings(**config_data.get("settings", {}))
    collections = parse_collections(config_data.get("collections", []))

    if not collections:
        raise SystemExit("No collections defined in configuration file.")

    toolkit = KnowledgeToolkit(settings)

    results = asyncio.run(toolkit.run_collections(collections))

    for result in results:
        print(f"Collection: {result.collection.name}")
        print(f"  Success: {result.succeeded}")
        print(f"  Failed: {result.failed}")
        for doc in result.documents:
            status = "OK" if doc.error is None else f"FAILED: {doc.error}"
            print(
                f"    - {doc.document_id} | chunks={doc.chunks} embeddings={doc.embeddings} "
                f"output={doc.output_path} {status}"
            )
            for warning in doc.warnings:
                print(f"        warning: {warning}")


if __name__ == "__main__":
    main()
