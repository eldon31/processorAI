"""
Kaggle-optimized FastMCP Documentation Chunking
For GPU T4 x2 with nomic-ai/nomic-embed-code

Chunks all markdown files in fast_mcp_api_python folder
"""

import json
from pathlib import Path
from datetime import datetime
import torch
from typing import List

# Check GPU
print(f"\n{'='*60}")
print("GPU SETUP")
print(f"{'='*60}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU count: {torch.cuda.device_count()}")
    for i in range(torch.cuda.device_count()):
        print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
print(f"{'='*60}\n")

from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker
from transformers import AutoTokenizer

# Configuration
EMBEDDING_MODEL = "nomic-ai/nomic-embed-text-v1.5"
MAX_TOKENS = 2048

# Paths
BASE_DIR = Path(__file__).parent.parent
INPUT_DIR = BASE_DIR / "Docs" / "fast_mcp_api_python"
OUTPUT_DIR = BASE_DIR / "output" / "fast_mcp_api_python" / "chunked"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def find_markdown_files(directory: Path) -> List[Path]:
    """Recursively find all markdown files."""
    return sorted(directory.rglob("*.md"))


def chunk_markdown_files():
    """Chunk all markdown files preserving folder structure."""
    print(f"\n{'='*60}")
    print("CHUNKING FASTMCP DOCUMENTATION")
    print(f"{'='*60}\n")
    
    # Find all markdown files
    print("Finding markdown files...")
    md_files = find_markdown_files(INPUT_DIR)
    print(f"✓ Found {len(md_files)} markdown files\n")
    
    # Load tokenizer
    print(f"Loading tokenizer: {EMBEDDING_MODEL}")
    tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL)
    print("✓ Tokenizer loaded\n")
    
    # Setup chunker
    chunker = HybridChunker(
        tokenizer=tokenizer,
        max_tokens=MAX_TOKENS,
        merge_peers=True
    )
    
    # Setup converter
    converter = DocumentConverter()
    
    total_chunks = 0
    
    for idx, md_file in enumerate(md_files, 1):
        # Get relative path to preserve folder structure
        rel_path = md_file.relative_to(INPUT_DIR)
        
        print(f"[{idx}/{len(md_files)}] Chunking: {rel_path}")
        
        try:
            # Convert markdown to DoclingDocument
            result = converter.convert(str(md_file))
            doc = result.document
            
            # Chunk the document
            chunks = list(chunker.chunk(doc))
            
            # Prepare chunk data
            chunk_data = []
            for chunk_idx, chunk in enumerate(chunks):
                chunk_data.append({
                    "id": f"{md_file.stem}_chunk_{chunk_idx}",
                    "text": chunk.text,
                    "metadata": {
                        "source": str(rel_path),
                        "folder": rel_path.parent.name,
                        "filename": md_file.name,
                        "chunk_index": chunk_idx,
                        "total_chunks": len(chunks)
                    }
                })
            
            # Create output path preserving folder structure
            output_subdir = OUTPUT_DIR / rel_path.parent
            output_subdir.mkdir(parents=True, exist_ok=True)
            
            output_path = output_subdir / f"{md_file.stem}_chunks.json"
            
            # Save chunks
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(chunk_data, f, indent=2, ensure_ascii=False)
            
            print(f"  ✓ Created {len(chunks)} chunks → {output_path.relative_to(OUTPUT_DIR)}\n")
            total_chunks += len(chunks)
            
        except Exception as e:
            print(f"  ❌ Error: {str(e)}\n")
            continue
    
    print(f"{'='*60}")
    print(f"✓ CHUNKING COMPLETED")
    print(f"  Files processed: {len(md_files)}")
    print(f"  Total chunks: {total_chunks}")
    print(f"{'='*60}\n")


def main():
    """Run chunking pipeline."""
    start_time = datetime.now()
    
    try:
        chunk_markdown_files()
        
        duration = (datetime.now() - start_time).total_seconds()
        print(f"\n✓ Completed in {duration/60:.1f} minutes\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
