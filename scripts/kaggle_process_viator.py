"""
Kaggle-optimized Viator API Documentation Processing Pipeline
For GPU T4 x2 with nomic-ai/nomic-embed-code

This script is optimized for Kaggle's environment:
- Uses GPU acceleration (CUDA)
- Reduced batch size to prevent OOM
- Progress tracking for long operations
- Automatic cleanup to manage disk space
"""

import asyncio
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import torch

# Check GPU availability
print(f"\n{'='*60}")
print("GPU SETUP")
print(f"{'='*60}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU count: {torch.cuda.device_count()}")
if torch.cuda.is_available():
    for i in range(torch.cuda.device_count()):
        print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
        print(f"  Memory: {torch.cuda.get_device_properties(i).total_memory / 1e9:.2f} GB")
print(f"{'='*60}\n")

from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat
from docling.chunking import HybridChunker
from transformers import AutoTokenizer
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, OptimizersConfigDiff

# Configuration - Optimized for Kaggle GPU T4 x2
EMBEDDING_MODEL = "nomic-ai/nomic-embed-text-v1.5"  # Code model alternative
VECTOR_SIZE = 768  # Updated for v1.5
MAX_CHUNK_SIZE = 1024
BATCH_SIZE = 8  # Reduced for GPU memory safety
QDRANT_HOST = "localhost"  # Change if using remote Qdrant
QDRANT_PORT = 6333
COLLECTION_NAME = "viator_api"

# Paths
BASE_DIR = Path(__file__).parent.parent
INPUT_DIR = BASE_DIR / "Docs" / "viator_api_documentation"
OUTPUT_DIR = BASE_DIR / "output" / "viator_api"
CONVERTED_DIR = OUTPUT_DIR / "converted"
CHUNKED_DIR = OUTPUT_DIR / "chunked"
EMBEDDINGS_DIR = OUTPUT_DIR / "embeddings"

# Create output directories
CONVERTED_DIR.mkdir(parents=True, exist_ok=True)
CHUNKED_DIR.mkdir(parents=True, exist_ok=True)
EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)


def string_to_int_id(string_id: str) -> int:
    """Convert string ID to integer using hash for Qdrant compatibility."""
    hash_bytes = hashlib.sha256(string_id.encode()).digest()
    return int.from_bytes(hash_bytes[:8], byteorder='big', signed=False) % (2**63)


def convert_documents():
    """Step 1: Convert PDFs and JSON to markdown."""
    print(f"\n{'='*60}")
    print("STEP 1: CONVERTING DOCUMENTS")
    print(f"{'='*60}\n")
    
    # Setup converter
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = False
    pipeline_options.do_table_structure = True
    
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )
    
    # Process all files
    files = list(INPUT_DIR.glob("*"))
    for idx, file_path in enumerate(files, 1):
        print(f"[{idx}/{len(files)}] Converting: {file_path.name}")
        start = datetime.now()
        
        if file_path.suffix.lower() == '.json':
            # For JSON files, wrap in markdown code block
            with open(file_path, 'r', encoding='utf-8') as f:
                json_content = f.read()
            
            markdown = f"# {file_path.stem}\n\n```json\n{json_content}\n```"
            output_path = CONVERTED_DIR / f"{file_path.stem}.md"
            output_path.write_text(markdown, encoding='utf-8')
            
        else:
            # Convert PDF using Docling
            result = converter.convert(str(file_path))
            markdown = result.document.export_to_markdown()
            
            output_path = CONVERTED_DIR / f"{file_path.stem}.md"
            output_path.write_text(markdown, encoding='utf-8')
        
        duration = (datetime.now() - start).total_seconds()
        print(f"  ✓ Completed in {duration:.1f}s → {output_path.name}\n")
    
    print(f"✓ Converted {len(files)} files\n")


def chunk_documents():
    """Step 2: Chunk markdown documents."""
    print(f"\n{'='*60}")
    print("STEP 2: CHUNKING DOCUMENTS")
    print(f"{'='*60}\n")
    
    # Load tokenizer for HybridChunker
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL)
    
    # Setup chunker
    chunker = HybridChunker(
        tokenizer=tokenizer,
        max_tokens=2048,
        merge_peers=True
    )
    
    # Setup converter for re-processing
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = False
    pipeline_options.do_table_structure = True
    
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )
    
    converted_files = list(CONVERTED_DIR.glob("*.md"))
    total_chunks = 0
    
    for idx, md_file in enumerate(converted_files, 1):
        print(f"[{idx}/{len(converted_files)}] Chunking: {md_file.name}")
        
        # Find original file
        original_name = md_file.stem
        original_file = INPUT_DIR / f"{original_name}.pdf"
        
        if not original_file.exists():
            original_file = INPUT_DIR / f"{original_name}.json"
        
        if original_file.suffix.lower() == '.pdf':
            # Re-convert PDF to get DoclingDocument
            result = converter.convert(str(original_file))
            doc = result.document
            
            # Chunk using HybridChunker
            chunks = list(chunker.chunk(doc))
            
        elif original_file.suffix.lower() == '.json':
            # For JSON, use simple text-based chunking
            markdown_text = md_file.read_text(encoding='utf-8')
            
            # Split by headings or size
            chunks = []
            current_chunk = ""
            
            for line in markdown_text.split('\n'):
                if line.startswith('#') and current_chunk:
                    if len(current_chunk) > 100:
                        chunks.append({"text": current_chunk.strip()})
                    current_chunk = line + '\n'
                else:
                    current_chunk += line + '\n'
                    
                    # Split large chunks
                    if len(current_chunk) > MAX_CHUNK_SIZE * 4:
                        chunks.append({"text": current_chunk.strip()})
                        current_chunk = ""
            
            if current_chunk.strip():
                chunks.append({"text": current_chunk.strip()})
        
        # Save chunks
        chunk_data = []
        for chunk_idx, chunk in enumerate(chunks):
            chunk_text = chunk.text if hasattr(chunk, 'text') else chunk.get('text', '')
            
            chunk_data.append({
                "id": f"{md_file.stem}_chunk_{chunk_idx}",
                "text": chunk_text,
                "metadata": {
                    "source": md_file.stem,
                    "chunk_index": chunk_idx,
                    "total_chunks": len(chunks)
                }
            })
        
        output_path = CHUNKED_DIR / f"{md_file.stem}_chunks.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(chunk_data, f, indent=2, ensure_ascii=False)
        
        print(f"  ✓ Created {len(chunks)} chunks → {output_path.name}\n")
        total_chunks += len(chunks)
    
    print(f"✓ Total chunks created: {total_chunks}\n")


def embed_chunks():
    """Step 3: Generate embeddings using GPU acceleration."""
    print(f"\n{'='*60}")
    print("STEP 3: GENERATING EMBEDDINGS (GPU)")
    print(f"{'='*60}\n")
    
    # Load embedding model on GPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Loading embedding model on {device}...")
    print(f"Model: {EMBEDDING_MODEL}")
    
    model = SentenceTransformer(EMBEDDING_MODEL, device=device)
    print(f"✓ Model loaded on {device}\n")
    
    chunk_files = list(CHUNKED_DIR.glob("*_chunks.json"))
    all_embeddings = []
    
    for idx, chunk_file in enumerate(chunk_files, 1):
        print(f"[{idx}/{len(chunk_files)}] Embedding: {chunk_file.name}")
        
        # Load chunks
        with open(chunk_file, 'r', encoding='utf-8') as f:
            chunks = json.load(f)
        
        # Extract texts
        texts = [chunk['text'] for chunk in chunks]
        
        # Generate embeddings in batches
        embeddings = []
        for i in range(0, len(texts), BATCH_SIZE):
            batch_texts = texts[i:i + BATCH_SIZE]
            batch_embeddings = model.encode(
                batch_texts,
                show_progress_bar=True,
                batch_size=BATCH_SIZE,
                device=device
            )
            embeddings.extend(batch_embeddings)
            
            # Clear GPU cache periodically
            if torch.cuda.is_available() and i % (BATCH_SIZE * 4) == 0:
                torch.cuda.empty_cache()
        
        # Save embeddings
        for chunk, embedding in zip(chunks, embeddings):
            all_embeddings.append({
                "id": chunk['id'],
                "text": chunk['text'],
                "embedding": embedding.tolist(),
                "metadata": chunk['metadata']
            })
        
        print(f"  ✓ Embedded {len(chunks)} chunks\n")
    
    # Save all embeddings
    output_path = EMBEDDINGS_DIR / "viator_api_embeddings.jsonl"
    with open(output_path, 'w', encoding='utf-8') as f:
        for item in all_embeddings:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    print(f"✓ Saved {len(all_embeddings)} embeddings → {output_path.name}\n")
    
    # Clear GPU memory
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        print("✓ Cleared GPU cache\n")


def upload_to_qdrant():
    """Step 4: Upload embeddings to Qdrant."""
    print(f"\n{'='*60}")
    print("STEP 4: UPLOADING TO QDRANT")
    print(f"{'='*60}\n")
    
    # Initialize Qdrant client
    print(f"Connecting to Qdrant at {QDRANT_HOST}:{QDRANT_PORT}...")
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, prefer_grpc=False)
    
    # Create collection
    print(f"Creating collection: {COLLECTION_NAME}")
    try:
        client.delete_collection(collection_name=COLLECTION_NAME)
        print("  ✓ Deleted existing collection")
    except:
        pass
    
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE
        ),
        optimizers_config=OptimizersConfigDiff(
            default_segment_number=2
        )
    )
    print("  ✓ Created new collection\n")
    
    # Load embeddings
    embeddings_file = EMBEDDINGS_DIR / "viator_api_embeddings.jsonl"
    print(f"Loading embeddings from {embeddings_file.name}...")
    
    points = []
    with open(embeddings_file, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            
            points.append(PointStruct(
                id=string_to_int_id(item['id']),
                vector=item['embedding'],
                payload={
                    "text": item['text'],
                    "source": item['metadata']['source'],
                    "chunk_index": item['metadata']['chunk_index']
                }
            ))
    
    print(f"  ✓ Loaded {len(points)} points\n")
    
    # Upload in batches
    print("Uploading to Qdrant...")
    batch_size = 100
    for i in range(0, len(points), batch_size):
        batch = points[i:i + batch_size]
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=batch
        )
        print(f"  ✓ Uploaded batch {i//batch_size + 1}/{(len(points)-1)//batch_size + 1}")
    
    print(f"\n✓ Uploaded {len(points)} vectors to Qdrant\n")
    
    # Verify
    info = client.get_collection(collection_name=COLLECTION_NAME)
    print(f"Collection info:")
    print(f"  Vectors: {info.vectors_count}")
    print(f"  Points: {info.points_count}")


def main():
    """Run complete pipeline."""
    print("\n" + "="*60)
    print("KAGGLE VIATOR API PROCESSING PIPELINE")
    print("GPU T4 x2 | nomic-ai/nomic-embed-code")
    print("="*60)
    
    start_time = datetime.now()
    
    try:
        convert_documents()
        chunk_documents()
        embed_chunks()
        # upload_to_qdrant()  # Disabled - will upload locally later
        
        duration = (datetime.now() - start_time).total_seconds()
        print(f"\n{'='*60}")
        print(f"✓ PIPELINE COMPLETED in {duration/60:.1f} minutes")
        print(f"✓ Embeddings saved to: {EMBEDDINGS_DIR}")
        print(f"  Download and upload to Qdrant locally")
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Clear GPU memory on error
        if torch.cuda.is_available():
            torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
