"""
Complete pipeline to process Viator API documentation:
1. Convert files using Docling
2. Chunk the converted documents
3. Generate embeddings
4. Upload to Qdrant

Collection: viator_api
"""

import asyncio
import json
import logging
import sys
import hashlib
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

# Add project root to path
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker
from transformers import AutoTokenizer
from src.config.jina_provider import EmbedderConfig, SentenceTransformerEmbedder
from src.storage.qdrant_store import QdrantStoreConfig, QdrantStore

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
INPUT_DIR = ROOT_DIR / "Docs" / "viator_api_documentation"
OUTPUT_BASE = ROOT_DIR / "output" / "viator_api"
CONVERTED_DIR = OUTPUT_BASE / "converted"
CHUNKED_DIR = OUTPUT_BASE / "chunked"
EMBEDDINGS_DIR = OUTPUT_BASE / "embeddings"
COLLECTION_NAME = "viator_api"
EMBEDDING_MODEL = "nomic-ai/nomic-embed-code"
VECTOR_SIZE = 3584
MAX_CHUNK_SIZE = 1024
BATCH_SIZE = 32

# Qdrant configuration
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333


def ensure_directories():
    """Create output directories if they don't exist."""
    CONVERTED_DIR.mkdir(parents=True, exist_ok=True)
    CHUNKED_DIR.mkdir(parents=True, exist_ok=True)
    EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)
    logger.info(f"Output directories ready at: {OUTPUT_BASE}")


def string_to_int_id(string_id: str) -> int:
    """Convert string ID to integer using hash."""
    hash_obj = hashlib.sha256(string_id.encode())
    hash_int = int.from_bytes(hash_obj.digest()[:8], byteorder='big', signed=True)
    return hash_int % (2**63)


def convert_documents():
    """Step 1: Convert documents using Docling."""
    logger.info("=" * 80)
    logger.info("STEP 1: Converting documents with Docling")
    logger.info("=" * 80)
    
    converter = DocumentConverter()
    files = list(INPUT_DIR.glob("*"))
    supported_files = [f for f in files if f.suffix.lower() in ['.pdf', '.json', '.md', '.txt']]
    
    logger.info(f"Found {len(supported_files)} supported files to convert")
    
    converted_files = []
    for file_path in supported_files:
        logger.info(f"Converting: {file_path.name}")
        
        # Handle JSON files specially (like OpenAPI specs)
        if file_path.suffix.lower() == '.json':
            try:
                # Read JSON and convert to formatted markdown
                json_content = json.loads(file_path.read_text(encoding='utf-8'))
                
                # Create markdown representation
                markdown_lines = [f"# {file_path.stem}\n"]
                markdown_lines.append("```json")
                markdown_lines.append(json.dumps(json_content, indent=2, ensure_ascii=False))
                markdown_lines.append("```")
                
                output_path = CONVERTED_DIR / f"{file_path.stem}.md"
                output_path.write_text('\n'.join(markdown_lines), encoding='utf-8')
                
                logger.info(f"  ✓ Saved JSON as markdown to: {output_path.name}")
                converted_files.append(output_path)
                
            except Exception as e:
                logger.error(f"  ✗ Error converting JSON {file_path.name}: {e}")
                continue
        else:
            # Use Docling for PDFs and other formats
            try:
                result = converter.convert(str(file_path))
                
                # Export as markdown
                output_path = CONVERTED_DIR / f"{file_path.stem}.md"
                markdown_content = result.document.export_to_markdown()
                output_path.write_text(markdown_content, encoding='utf-8')
                
                logger.info(f"  ✓ Saved to: {output_path.name}")
                converted_files.append(output_path)
                
            except Exception as e:
                logger.error(f"  ✗ Error converting {file_path.name}: {e}")
                continue
    
    logger.info(f"\nConverted {len(converted_files)} files successfully")
    return converted_files


def chunk_documents(converted_files: List[Path]) -> List[Path]:
    """Step 2: Chunk the converted documents."""
    logger.info("\n" + "=" * 80)
    logger.info("STEP 2: Chunking documents")
    logger.info("=" * 80)
    
    # Initialize tokenizer for HybridChunker (use nomic-embed-code for consistency)
    logger.info(f"Loading tokenizer: {EMBEDDING_MODEL}")
    tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL, trust_remote_code=True)
    
    # Initialize converter and chunker with proper configuration
    converter = DocumentConverter()
    chunker = HybridChunker(
        tokenizer=tokenizer,
        max_tokens=2048,
        merge_peers=True
    )
    logger.info("Initialized HybridChunker (tokenizer: nomic-embed-code, max_tokens: 2048)")
    chunked_files = []
    
    for md_file in converted_files:
        logger.info(f"Chunking: {md_file.name}")
        
        try:
            # Get original file path (markdown filename corresponds to original file)
            original_name = md_file.stem
            
            # Find original file in INPUT_DIR
            possible_extensions = ['.pdf', '.json', '.md', '.txt']
            original_file = None
            for ext in possible_extensions:
                candidate = INPUT_DIR / f"{original_name}{ext}"
                if candidate.exists():
                    original_file = candidate
                    break
            
            if not original_file:
                logger.warning(f"  ⚠ Could not find original file for {md_file.name}, using text chunking")
                # Fall back to simple text chunking
                content = md_file.read_text(encoding='utf-8')
                chunk_size = MAX_CHUNK_SIZE * 4
                chunks_text = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
                chunks_list = [{"text": chunk} for chunk in chunks_text]
            elif original_file.suffix.lower() == '.json':
                # JSON files (like OpenAPI specs) - chunk the markdown directly
                logger.info(f"  Chunking JSON-based markdown directly (can't re-convert OpenAPI spec)...")
                content = md_file.read_text(encoding='utf-8')
                
                # Simple semantic chunking for JSON content
                # Split by major sections (lines starting with ##)
                lines = content.split('\n')
                chunks_text = []
                current_chunk = []
                current_size = 0
                max_size = MAX_CHUNK_SIZE * 4  # ~4KB chunks for JSON content
                
                for line in lines:
                    line_size = len(line) + 1  # +1 for newline
                    
                    # Start new chunk if we hit a heading and current chunk is substantial
                    if line.startswith('##') and current_size > max_size // 2:
                        if current_chunk:
                            chunks_text.append('\n'.join(current_chunk))
                            current_chunk = []
                            current_size = 0
                    
                    current_chunk.append(line)
                    current_size += line_size
                    
                    # Force split if chunk gets too large
                    if current_size >= max_size:
                        chunks_text.append('\n'.join(current_chunk))
                        current_chunk = []
                        current_size = 0
                
                # Add remaining content
                if current_chunk:
                    chunks_text.append('\n'.join(current_chunk))
                
                chunks_list = [{"text": chunk.strip()} for chunk in chunks_text if chunk.strip()]
            else:
                # PDF files - Re-convert to get DoclingDocument object for HybridChunker
                logger.info(f"  Re-converting {original_file.name} for chunking...")
                result = converter.convert(str(original_file))
                doc = result.document
                
                # Chunk using HybridChunker
                chunk_iter = chunker.chunk(doc)
                chunks_list = list(chunk_iter)
            
            # Prepare chunk data
            chunk_data = []
            for idx, chunk in enumerate(chunks_list):
                # Extract text from chunk object
                if hasattr(chunk, 'text'):
                    chunk_text = chunk.text
                elif isinstance(chunk, dict):
                    chunk_text = chunk.get("text", str(chunk))
                else:
                    chunk_text = str(chunk)
                
                chunk_id = f"{COLLECTION_NAME}:{md_file.stem}:chunk:{idx}"
                chunk_dict = {
                    "chunk_id": chunk_id,
                    "content": chunk_text,
                    "metadata": {
                        "source": str(md_file.relative_to(ROOT_DIR)),
                        "file_name": md_file.name,
                        "chunk_index": idx,
                        "total_chunks": len(chunks_list),
                        "char_count": len(chunk_text),
                        "collection": COLLECTION_NAME,
                        "processing_method": "hybrid_chunker",
                        "timestamp": datetime.now().isoformat()
                    }
                }
                chunk_data.append(chunk_dict)
            
            # Save chunks as JSON
            output_path = CHUNKED_DIR / f"{md_file.stem}_chunks.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(chunk_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"  ✓ Created {len(chunk_data)} chunks → {output_path.name}")
            chunked_files.append(output_path)
            
        except Exception as e:
            logger.error(f"  ✗ Error chunking {md_file.name}: {e}")
            import traceback
            logger.error(traceback.format_exc())
            continue
    
    logger.info(f"\nChunked {len(chunked_files)} files successfully")
    return chunked_files


async def embed_chunks(chunked_files: List[Path]) -> Path:
    """Step 3: Generate embeddings for chunks."""
    logger.info("\n" + "=" * 80)
    logger.info("STEP 3: Generating embeddings")
    logger.info("=" * 80)
    
    # Initialize embedder
    logger.info(f"Loading embedding model: {EMBEDDING_MODEL}")
    embedder_config = EmbedderConfig(model_name=EMBEDDING_MODEL)
    embedder = SentenceTransformerEmbedder(embedder_config)
    
    # Output file for embeddings
    embeddings_file = EMBEDDINGS_DIR / f"{COLLECTION_NAME}_embeddings.jsonl"
    
    total_chunks = 0
    with open(embeddings_file, 'w', encoding='utf-8') as out_f:
        for chunk_file in chunked_files:
            logger.info(f"Embedding: {chunk_file.name}")
            
            # Load chunks
            with open(chunk_file, 'r', encoding='utf-8') as f:
                chunks = json.load(f)
            
            # Extract texts
            texts = [chunk['content'] for chunk in chunks]
            
            # Generate embeddings in batches
            all_embeddings = []
            for i in range(0, len(texts), BATCH_SIZE):
                batch = texts[i:i + BATCH_SIZE]
                embeddings = await embedder.embed_documents(batch)
                all_embeddings.extend(embeddings)
                logger.info(f"  Progress: {min(i + BATCH_SIZE, len(texts))}/{len(texts)} chunks")
            
            # Write to JSONL
            for chunk, embedding in zip(chunks, all_embeddings):
                record = {
                    "id": chunk["chunk_id"],
                    "content": chunk["content"],
                    "embedding": embedding,
                    "metadata": chunk["metadata"]
                }
                out_f.write(json.dumps(record, ensure_ascii=False) + '\n')
            
            total_chunks += len(chunks)
            logger.info(f"  ✓ Embedded {len(chunks)} chunks")
    
    logger.info(f"\nGenerated embeddings for {total_chunks} total chunks")
    logger.info(f"Saved to: {embeddings_file}")
    return embeddings_file


def upload_to_qdrant(embeddings_file: Path):
    """Step 4: Upload embeddings to Qdrant."""
    logger.info("\n" + "=" * 80)
    logger.info("STEP 4: Uploading to Qdrant")
    logger.info("=" * 80)
    
    # Initialize Qdrant store
    logger.info(f"Connecting to Qdrant at {QDRANT_HOST}:{QDRANT_PORT}")
    store_config = QdrantStoreConfig(
        host=QDRANT_HOST,
        port=QDRANT_PORT,
        collection_name=COLLECTION_NAME,
        vector_size=VECTOR_SIZE,
        enable_quantization=True,
        prefer_grpc=False
    )
    store = QdrantStore(store_config)
    
    # Read embeddings and upload in batches
    logger.info(f"Reading embeddings from: {embeddings_file.name}")
    
    batch_embeddings = []
    batch_metadatas = []
    batch_ids = []
    total_uploaded = 0
    
    with open(embeddings_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            record = json.loads(line)
            
            # Prepare metadata (content is part of metadata in Qdrant)
            metadata = record['metadata'].copy()
            metadata['content'] = record['content']
            metadata['chunk_id'] = record['id']
            
            # Convert string ID to integer
            int_id = string_to_int_id(record['id'])
            
            batch_embeddings.append(record['embedding'])
            batch_metadatas.append(metadata)
            batch_ids.append(int_id)
            
            # Upload when batch is full
            if len(batch_embeddings) >= BATCH_SIZE:
                store.add_embeddings(
                    embeddings=batch_embeddings,
                    metadatas=batch_metadatas,
                    ids=batch_ids
                )
                total_uploaded += len(batch_embeddings)
                logger.info(f"  Uploaded batch: {total_uploaded} vectors")
                
                batch_embeddings = []
                batch_metadatas = []
                batch_ids = []
    
    # Upload remaining
    if batch_embeddings:
        store.add_embeddings(
            embeddings=batch_embeddings,
            metadatas=batch_metadatas,
            ids=batch_ids
        )
        total_uploaded += len(batch_embeddings)
    
    logger.info(f"\n✓ Successfully uploaded {total_uploaded} vectors to collection '{COLLECTION_NAME}'")
    
    # Get collection stats
    stats = store.get_stats()
    logger.info(f"\nCollection Statistics:")
    logger.info(f"  Points: {stats.get('points_count', 0)}")
    logger.info(f"  Status: {stats.get('status', 'unknown')}")
    logger.info(f"  Quantization: {stats.get('quantization_enabled', False)}")


async def main():
    """Run the complete pipeline."""
    logger.info("Starting Viator API Documentation Processing Pipeline")
    logger.info(f"Input directory: {INPUT_DIR}")
    logger.info(f"Output directory: {OUTPUT_BASE}")
    logger.info(f"Collection name: {COLLECTION_NAME}")
    logger.info("")
    
    # Ensure output directories exist
    ensure_directories()
    
    try:
        # Step 1: Convert with Docling
        converted_files = convert_documents()
        if not converted_files:
            logger.error("No files were converted. Exiting.")
            return
        
        # Step 2: Chunk
        chunked_files = chunk_documents(converted_files)
        if not chunked_files:
            logger.error("No files were chunked. Exiting.")
            return
        
        logger.info("\n" + "=" * 80)
        logger.info("✓ CHUNKING COMPLETED - Pipeline paused")
        logger.info("=" * 80)
        logger.info(f"Chunked files saved to: {CHUNKED_DIR}")
        logger.info(f"Total chunks created: {len(chunked_files)} files")
        logger.info("\nTo continue with embedding and upload, comment out the return statement below.")
        return  # PAUSE HERE - Comment this line to continue with embedding + upload
        
        # Step 3: Embed
        embeddings_file = await embed_chunks(chunked_files)
        
        # Step 4: Upload to Qdrant
        upload_to_qdrant(embeddings_file)
        
        logger.info("\n" + "=" * 80)
        logger.info("✓ PIPELINE COMPLETED SUCCESSFULLY")
        logger.info("=" * 80)
        logger.info(f"All outputs saved to: {OUTPUT_BASE}")
        
    except Exception as e:
        logger.error(f"\n✗ Pipeline failed with error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
