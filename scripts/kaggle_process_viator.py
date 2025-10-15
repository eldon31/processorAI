#!/usr/bin/env python3
"""
Kaggle-optimized Viator API Documentation Processing Pipeline with Subdirectories
Runs on GPU T4 x2 (2x16GB VRAM, 73GB disk, 30GB RAM)

Collection Structure:
- viator_api:affiliate - Affiliate Attribution documentation
- viator_api:technical_guides - Technical Guide + Viator Partner API
- viator_api:api_specs - OpenAPI JSON specification

Pipeline: PDF/JSON → Markdown → Chunks → Embeddings (JSONL)
Model: nomic-ai/nomic-embed-code (26GB, 768-dim, distributed across 2 GPUs)
Output: Single consolidated viator_api_embeddings.jsonl file
"""

import os

# Prevent transformers from attempting to load TensorFlow
os.environ.setdefault("TRANSFORMERS_NO_TF", "1")
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict

import numpy as np
import torch

# Guard against NumPy 2.x
if tuple(map(int, np.__version__.split(".")[:2])) >= (2, 0):
    raise RuntimeError(
        "NumPy 2.x detected. Please run `pip install -q --force-reinstall \"numpy==1.26.4\" \"scikit-learn==1.4.2\"` "
        "in a fresh Kaggle cell and restart the runtime before executing this script."
    )

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

from transformers import AutoTokenizer, AutoModel

# Configuration
EMBEDDING_MODEL = "nomic-ai/nomic-embed-code"
MAX_CHUNK_SIZE = 1500
MIN_CHUNK_SIZE = 100
BATCH_SIZE = 8
COLLECTION_NAME = "viator_api"

# Paths
BASE_DIR = Path(__file__).parent.parent
DOCS_BASE = BASE_DIR / "Docs" / "viator_api_documentation"
OUTPUT_DIR = BASE_DIR / "output" / "viator_api"
CONVERTED_DIR = OUTPUT_DIR / "converted"
CHUNKED_DIR = OUTPUT_DIR / "chunked"
EMBEDDINGS_DIR = OUTPUT_DIR / "embeddings"

# Subdirectories mapping (subdir_key -> list of filenames)
SUBDIRS = {
    "affiliate": [
        "Affiliate Attribution_ How It Works - Viator Partner Resource Center.pdf"
    ],
    "technical_guides": [
        "Technical Guide - Viator Partner API - Viator Partner Resource Center.pdf",
        "Viator Partner API.pdf"
    ],
    "api_specs": [
        "openapi (1).json"
    ]
}

# Create output directories
CONVERTED_DIR.mkdir(parents=True, exist_ok=True)
CHUNKED_DIR.mkdir(parents=True, exist_ok=True)
EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)

print(f"📁 Input directory: {DOCS_BASE}")
print(f"📁 Output directory: {OUTPUT_DIR}")
print(f"📦 Collection: {COLLECTION_NAME}")
print(f"📂 Subdirectories: {len(SUBDIRS)}")
for subdir, files in SUBDIRS.items():
    print(f"   - {subdir}: {len(files)} files")
print()


def convert_documents():
    """Convert PDFs to markdown using Docling, copy JSON as-is."""
    print(f"\n{'='*60}")
    print("STEP 1: DOCUMENT CONVERSION")
    print(f"{'='*60}\n")
    
    try:
        from docling.document_converter import DocumentConverter
    except ImportError as e:
        raise RuntimeError(
            "Docling not installed. Run: pip install docling"
        ) from e
    
    converter = DocumentConverter()
    total_files = sum(len(files) for files in SUBDIRS.values())
    converted = 0
    
    for subdir_key, filenames in SUBDIRS.items():
        print(f"\n📂 Processing subdirectory: {subdir_key}")
        
        for filename in filenames:
            source_path = DOCS_BASE / filename
            
            if not source_path.exists():
                print(f"   ⚠️  File not found: {filename}")
                continue
            
            # Determine output filename
            base_name = source_path.stem
            output_path = CONVERTED_DIR / f"{base_name}.md"
            
            if source_path.suffix.lower() == '.json':
                # Copy JSON as markdown (wrapped in code block)
                print(f"   📄 Copying JSON: {filename}")
                with open(source_path, 'r', encoding='utf-8') as f:
                    json_content = f.read()
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(f"# {base_name}\n\n```json\n")
                    f.write(json_content)
                    f.write("\n```\n")
            
            else:
                # Convert PDF to markdown using Docling
                print(f"   📄 Converting PDF: {filename}")
                try:
                    result = converter.convert(str(source_path))
                    markdown_content = result.document.export_to_markdown()
                    
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(markdown_content)
                
                except Exception as e:
                    print(f"   ❌ Conversion failed: {e}")
                    continue
            
            converted += 1
            print(f"   ✓ Saved: {output_path.name}")
    
    print(f"\n✓ Conversion complete: {converted}/{total_files} files")
    return converted


def chunk_documents():
    """Chunk markdown files using heading-based splitting."""
    print(f"\n{'='*60}")
    print("STEP 2: DOCUMENT CHUNKING")
    print(f"{'='*60}\n")
    
    try:
        from docling_core.transforms.chunker import HybridChunker
    except ImportError as e:
        raise RuntimeError("Docling-core not installed. Run: pip install docling-core") from e
    
    chunker = HybridChunker(
        tokenizer="sentence-transformers/all-MiniLM-L6-v2",
        max_tokens=MAX_CHUNK_SIZE,
        min_tokens=MIN_CHUNK_SIZE
    )
    
    total_chunks = 0
    unique_ids = set()
    
    for subdir_key, filenames in SUBDIRS.items():
        print(f"\n📂 Chunking subdirectory: {subdir_key}")
        
        for filename in filenames:
            # Get corresponding markdown file
            base_name = Path(filename).stem
            md_path = CONVERTED_DIR / f"{base_name}.md"
            
            if not md_path.exists():
                print(f"   ⚠️  Markdown not found: {md_path.name}")
                continue
            
            print(f"   📄 Chunking: {md_path.name}")
            
            # Read markdown content
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split into chunks
            try:
                chunks_iter = chunker.chunk(content)
                chunks_list = list(chunks_iter)
            except Exception as e:
                print(f"   ⚠️  Chunking failed, using paragraph fallback: {e}")
                # Fallback: split by double newlines
                paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
                chunks_list = []
                for para in paragraphs:
                    if MIN_CHUNK_SIZE <= len(para) <= MAX_CHUNK_SIZE:
                        chunks_list.append({'text': para})
                    elif len(para) > MAX_CHUNK_SIZE:
                        # Split long paragraphs by sentences
                        sentences = para.split('. ')
                        current = ""
                        for sent in sentences:
                            if len(current) + len(sent) <= MAX_CHUNK_SIZE:
                                current += sent + ". "
                            else:
                                if current:
                                    chunks_list.append({'text': current.strip()})
                                current = sent + ". "
                        if current:
                            chunks_list.append({'text': current.strip()})
            
            # Process chunks with metadata
            file_chunks = []
            for idx, chunk_obj in enumerate(chunks_list):
                # Extract text (handle both 'text' and 'content' keys)
                chunk_text = chunk_obj.get('text') or chunk_obj.get('content', '')
                
                if not chunk_text or len(chunk_text.strip()) < MIN_CHUNK_SIZE:
                    continue
                
                # Generate unique chunk ID with subdirectory
                chunk_id = f"{COLLECTION_NAME}:{subdir_key}:{base_name}:chunk:{idx}"
                
                # Track ID uniqueness
                if chunk_id in unique_ids:
                    print(f"   ⚠️  Duplicate ID detected: {chunk_id}")
                unique_ids.add(chunk_id)
                
                # Extract heading info if available
                heading = chunk_obj.get('heading', '')
                heading_level = chunk_obj.get('heading_level', 0)
                
                chunk_data = {
                    "chunk_id": chunk_id,
                    "content": chunk_text.strip(),
                    "metadata": {
                        "source": base_name,
                        "subdir": subdir_key,
                        "heading": heading,
                        "heading_level": heading_level,
                        "chunk_index": idx,
                        "total_chunks": len(chunks_list),
                        "collection": COLLECTION_NAME
                    }
                }
                file_chunks.append(chunk_data)
            
            # Save chunks for this file
            output_path = CHUNKED_DIR / f"{base_name}_chunks.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(file_chunks, f, indent=2, ensure_ascii=False)
            
            total_chunks += len(file_chunks)
            print(f"   ✓ Created {len(file_chunks)} chunks → {output_path.name}")
    
    print(f"\n✓ Chunking complete: {total_chunks} total chunks")
    print(f"✓ Unique IDs: {len(unique_ids)} (conflicts: {total_chunks - len(unique_ids)})")
    return total_chunks


def embed_chunks():
    """Generate embeddings using nomic-embed-code with model parallelism."""
    print(f"\n{'='*60}")
    print("STEP 3: EMBEDDING GENERATION")
    print(f"{'='*60}\n")
    
    # Check GPU availability
    print(f"🔍 Checking GPU availability...")
    print(f"   CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"   GPU count: {torch.cuda.device_count()}")
        for i in range(torch.cuda.device_count()):
            print(f"   GPU {i}: {torch.cuda.get_device_name(i)}")
            print(f"   GPU {i} Memory: {torch.cuda.get_device_properties(i).total_memory / 1e9:.2f} GB")
    print()
    
    # Load model with automatic device mapping (model parallelism)
    print("📥 Loading nomic-embed-code model (26GB)...")
    print("   Strategy: Model parallelism across 2 GPUs with FP16 precision")
    
    tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL, trust_remote_code=True)
    model = AutoModel.from_pretrained(
        EMBEDDING_MODEL,
        trust_remote_code=True,
        device_map="auto",  # Automatically split model across available GPUs
        torch_dtype=torch.float16  # Use FP16 to reduce memory usage
    )
    model.eval()
    
    print("   ✓ Model loaded across 2 GPUs with automatic device mapping")
    print()
    
    # Collect all chunks from all subdirectories
    all_chunks = []
    for subdir_key, filenames in SUBDIRS.items():
        for filename in filenames:
            base_name = Path(filename).stem
            chunk_file = CHUNKED_DIR / f"{base_name}_chunks.json"
            
            if not chunk_file.exists():
                continue
            
            with open(chunk_file, 'r', encoding='utf-8') as f:
                chunks = json.load(f)
                all_chunks.extend(chunks)
    
    print(f"📊 Processing {len(all_chunks)} chunks in batches of {BATCH_SIZE}")
    print()
    
    # Process in batches
    embedded_chunks = []
    for i in range(0, len(all_chunks), BATCH_SIZE):
        batch = all_chunks[i:i + BATCH_SIZE]
        batch_texts = [chunk['content'] for chunk in batch]
        
        # Tokenize and embed
        with torch.no_grad():
            inputs = tokenizer(
                batch_texts,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors="pt"
            )
            
            # Move inputs to first available device (model will handle distribution)
            inputs = {k: v.to('cuda:0') for k, v in inputs.items()}
            
            # Generate embeddings
            outputs = model(**inputs)
            embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()
        
        # Attach embeddings to chunks
        for chunk, embedding in zip(batch, embeddings):
            chunk['embedding'] = embedding.tolist()
            embedded_chunks.append(chunk)
        
        if (i + BATCH_SIZE) % 100 == 0 or (i + BATCH_SIZE) >= len(all_chunks):
            print(f"   ✓ Embedded {min(i + BATCH_SIZE, len(all_chunks))}/{len(all_chunks)} chunks")
    
    # Save consolidated embeddings
    output_path = EMBEDDINGS_DIR / f"{COLLECTION_NAME}_embeddings.jsonl"
    with open(output_path, 'w', encoding='utf-8') as f:
        for chunk in embedded_chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + '\n')
    
    print(f"\n✓ Embeddings saved: {output_path}")
    print(f"✓ Total embedded chunks: {len(embedded_chunks)}")
    print(f"✓ Embedding dimension: {len(embedded_chunks[0]['embedding'])}")
    return len(embedded_chunks)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    start_time = datetime.now()
    
    try:
        # Step 1: Convert documents
        converted_count = convert_documents()
        
        # Step 2: Chunk documents
        chunk_count = chunk_documents()
        
        # Step 3: Embed chunks
        embedded_count = embed_chunks()
        
        # Summary
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds() / 60
        
        print("\n" + "=" * 80)
        print("PIPELINE SUMMARY")
        print("=" * 80)
        print(f"✓ Documents converted: {converted_count}")
        print(f"✓ Chunks created: {chunk_count}")
        print(f"✓ Chunks embedded: {embedded_count}")
        print(f"✓ Collection: {COLLECTION_NAME}")
        print(f"✓ Subdirectories: {len(SUBDIRS)}")
        for subdir in SUBDIRS.keys():
            print(f"   - {subdir}")
        print(f"✓ Output: {EMBEDDINGS_DIR / f'{COLLECTION_NAME}_embeddings.jsonl'}")
        print(f"✓ Duration: {duration:.1f} minutes")
        print()
        print("🎉 PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

