"""
Chunk FastMCP/FastAPI/Python-SDK documentation files.
Only performs chunking step - no conversion, embedding, or upload.

Input: Docs/fast_mcp_api_python/ (markdown files)
Output: output/fast_mcp_api_python/chunked/ (JSON chunk files)
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

# Add project root to path
import sys
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker
from transformers import AutoTokenizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
INPUT_DIR = ROOT_DIR / "Docs" / "fast_mcp_api_python"
OUTPUT_DIR = ROOT_DIR / "output" / "fast_mcp_api_python" / "chunked"
COLLECTION_NAME = "fast_mcp_api_python"
EMBEDDING_MODEL = "nomic-ai/nomic-embed-code"
MAX_TOKENS = 2048


def ensure_output_directory():
    """Create output directory if it doesn't exist."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    logger.info(f"Output directory ready: {OUTPUT_DIR}")


def find_markdown_files() -> List[Path]:
    """Find all markdown files in the input directory recursively."""
    md_files = list(INPUT_DIR.rglob("*.md"))
    logger.info(f"Found {len(md_files)} markdown files")
    return sorted(md_files)


def chunk_markdown_files(md_files: List[Path]) -> List[Path]:
    """
    Chunk markdown files using HybridChunker.
    
    For markdown files, we'll convert them to DoclingDocument first using Docling,
    then chunk with HybridChunker for consistency.
    """
    logger.info("\n" + "=" * 80)
    logger.info("CHUNKING MARKDOWN FILES")
    logger.info("=" * 80)
    
    # Initialize tokenizer for HybridChunker (use nomic-embed-code for consistency)
    logger.info(f"Loading tokenizer: {EMBEDDING_MODEL}")
    tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL, trust_remote_code=True)
    
    # Initialize converter and chunker
    converter = DocumentConverter()
    chunker = HybridChunker(
        tokenizer=tokenizer,
        max_tokens=MAX_TOKENS,
        merge_peers=True
    )
    logger.info(f"Initialized HybridChunker (tokenizer: nomic-embed-code, max_tokens: {MAX_TOKENS})")
    
    chunked_files = []
    total_chunks = 0
    
    for idx, md_file in enumerate(md_files, 1):
        # Get relative path for better organization
        rel_path = md_file.relative_to(INPUT_DIR)
        logger.info(f"[{idx}/{len(md_files)}] Chunking: {rel_path}")
        
        try:
            # Convert markdown to DoclingDocument
            result = converter.convert(str(md_file))
            doc = result.document
            
            # Chunk using HybridChunker
            chunk_iter = chunker.chunk(doc)
            chunks_list = list(chunk_iter)
            
            # Prepare chunk data
            chunk_data = []
            for chunk_idx, chunk in enumerate(chunks_list):
                # Extract text from chunk object
                if hasattr(chunk, 'text'):
                    chunk_text = chunk.text
                elif isinstance(chunk, dict):
                    chunk_text = chunk.get("text", str(chunk))
                else:
                    chunk_text = str(chunk)
                
                # Create unique chunk ID including subfolder structure
                subfolder = rel_path.parent.as_posix().replace('/', '_')
                if subfolder:
                    chunk_id = f"{COLLECTION_NAME}:{subfolder}:{md_file.stem}:chunk:{chunk_idx}"
                else:
                    chunk_id = f"{COLLECTION_NAME}:{md_file.stem}:chunk:{chunk_idx}"
                
                chunk_dict = {
                    "chunk_id": chunk_id,
                    "content": chunk_text,
                    "metadata": {
                        "source": str(rel_path),
                        "file_name": md_file.name,
                        "subfolder": str(rel_path.parent),
                        "chunk_index": chunk_idx,
                        "total_chunks": len(chunks_list),
                        "char_count": len(chunk_text),
                        "collection": COLLECTION_NAME,
                        "processing_method": "hybrid_chunker",
                        "timestamp": datetime.now().isoformat()
                    }
                }
                chunk_data.append(chunk_dict)
            
            # Save chunks as JSON (preserve folder structure in output)
            output_subdir = OUTPUT_DIR / rel_path.parent
            output_subdir.mkdir(parents=True, exist_ok=True)
            
            output_path = output_subdir / f"{md_file.stem}_chunks.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(chunk_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"  ✓ Created {len(chunk_data)} chunks → {output_path.relative_to(OUTPUT_DIR)}")
            chunked_files.append(output_path)
            total_chunks += len(chunk_data)
            
        except Exception as e:
            logger.error(f"  ✗ Error chunking {rel_path}: {e}")
            import traceback
            logger.error(traceback.format_exc())
            continue
    
    logger.info(f"\n{'='*80}")
    logger.info(f"✓ CHUNKING COMPLETED")
    logger.info(f"{'='*80}")
    logger.info(f"Files processed: {len(chunked_files)}/{len(md_files)}")
    logger.info(f"Total chunks created: {total_chunks}")
    logger.info(f"Output directory: {OUTPUT_DIR}")
    
    return chunked_files


def main():
    """Run the chunking pipeline."""
    logger.info("Starting Fast MCP/API/Python Documentation Chunking")
    logger.info(f"Input directory: {INPUT_DIR}")
    logger.info(f"Output directory: {OUTPUT_DIR}")
    logger.info(f"Collection name: {COLLECTION_NAME}")
    logger.info("")
    
    try:
        # Ensure output directory exists
        ensure_output_directory()
        
        # Find all markdown files
        md_files = find_markdown_files()
        if not md_files:
            logger.error("No markdown files found. Exiting.")
            return
        
        # Chunk the files
        chunked_files = chunk_markdown_files(md_files)
        
        logger.info("\n✓ Pipeline completed successfully!")
        
    except Exception as e:
        logger.error(f"\n✗ Pipeline failed with error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
