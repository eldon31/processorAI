#!/usr/bin/env python3
"""
Kaggle-optimized Viator API Documentation Embedding Pipeline
Runs on GPU T4 x2 (2x16GB VRAM, 73GB disk, 30GB RAM)

NOTE: This script SKIPS conversion and chunking - uses pre-chunked files!
Input: Pre-chunked JSON files from output/viator_api/chunked/

Pipeline: Pre-chunked JSON → Embeddings (JSONL)
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
BATCH_SIZE = 8
COLLECTION_NAME = "viator_api"

# Paths
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output" / "viator_api"
CHUNKED_DIR = OUTPUT_DIR / "chunked"

# Save to /kaggle/working for easy download (falls back to local output/ if not on Kaggle)
KAGGLE_WORKING = Path("/kaggle/working")
if KAGGLE_WORKING.exists():
    EMBEDDINGS_DIR = KAGGLE_WORKING
else:
    EMBEDDINGS_DIR = OUTPUT_DIR / "embeddings"
    EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)

print(f"📁 Input directory (chunked): {CHUNKED_DIR}")
print(f"📁 Output directory: {EMBEDDINGS_DIR}")
print(f"📦 Collection: {COLLECTION_NAME}")
print()


def load_chunked_files():
    """Load all pre-chunked JSON files from the chunked directory."""
    print(f"\n{'='*60}")
    print("STEP 1: LOADING PRE-CHUNKED FILES")
    print(f"{'='*60}\n")
    
    all_chunks = []
    chunk_files = list(CHUNKED_DIR.glob("*_chunks.json"))
    
    if not chunk_files:
        raise RuntimeError(f"No chunked files found in {CHUNKED_DIR}")
    
    print(f"📂 Found {len(chunk_files)} chunked files:")
    
    for chunk_file in sorted(chunk_files):
        print(f"   📄 Loading: {chunk_file.name}")
        
        with open(chunk_file, 'r', encoding='utf-8') as f:
            chunks = json.load(f)
            all_chunks.extend(chunks)
            print(f"      ✓ Loaded {len(chunks)} chunks")
    
    print(f"\n✓ Total chunks loaded: {len(all_chunks)}")
    return all_chunks


def embed_chunks():
    """Generate embeddings using nomic-embed-code with data parallelism."""
    print(f"\n{'='*60}")
    print("STEP 2: EMBEDDING GENERATION")
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
    print("   Strategy: Data parallelism - Process batches on BOTH GPUs simultaneously")
    
    # Load model on BOTH GPUs
    tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL, trust_remote_code=True)
    
    # Load model instance on GPU 0
    print("   Loading model on GPU 0...")
    model_gpu0 = AutoModel.from_pretrained(
        EMBEDDING_MODEL,
        trust_remote_code=True,
        torch_dtype=torch.float16
    ).to('cuda:0')
    model_gpu0.eval()
    
    # Load model instance on GPU 1
    print("   Loading model on GPU 1...")
    model_gpu1 = AutoModel.from_pretrained(
        EMBEDDING_MODEL,
        trust_remote_code=True,
        torch_dtype=torch.float16
    ).to('cuda:1')
    model_gpu1.eval()
    
    print(f"   ✓ Model loaded on BOTH GPUs (data parallelism)")
    print(f"   ✓ GPU 0: {torch.cuda.get_device_name(0)}")
    print(f"   ✓ GPU 1: {torch.cuda.get_device_name(1)}")
    print()
    
    # Collect all chunks from all chunked files
    all_chunks = []
    chunk_files = list(CHUNKED_DIR.glob("*_chunks.json"))
    
    if not chunk_files:
        raise RuntimeError(f"No chunked files found in {CHUNKED_DIR}")
    
    print(f"📂 Loading chunks from {len(chunk_files)} files...")
    
    for chunk_file in sorted(chunk_files):
        with open(chunk_file, 'r', encoding='utf-8') as f:
            chunks = json.load(f)
            all_chunks.extend(chunks)
    
    print(f"📊 Processing {len(all_chunks)} chunks in batches of {BATCH_SIZE}")
    print(f"   Strategy: Split batches across GPU 0 and GPU 1")
    print()
    
    # Process in batches using BOTH GPUs
    embedded_chunks = []
    
    for i in range(0, len(all_chunks), BATCH_SIZE * 2):  # Process 2 batches at once
        # Split into 2 sub-batches for parallel processing
        batch_gpu0 = all_chunks[i:i + BATCH_SIZE]
        batch_gpu1 = all_chunks[i + BATCH_SIZE:i + BATCH_SIZE * 2]
        
        if not batch_gpu0:
            break
        
        # Prepare texts for both GPUs
        texts_gpu0 = [chunk['content'] for chunk in batch_gpu0]
        texts_gpu1 = [chunk['content'] for chunk in batch_gpu1] if batch_gpu1 else []
        
        # Process on GPU 0
        with torch.no_grad():
            inputs_gpu0 = tokenizer(
                texts_gpu0,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors="pt"
            ).to('cuda:0')
            
            outputs_gpu0 = model_gpu0(**inputs_gpu0)
            embeddings_gpu0 = outputs_gpu0.last_hidden_state[:, 0, :].cpu().numpy()
        
        # Process on GPU 1 (if we have a second batch)
        if texts_gpu1:
            with torch.no_grad():
                inputs_gpu1 = tokenizer(
                    texts_gpu1,
                    padding=True,
                    truncation=True,
                    max_length=512,
                    return_tensors="pt"
                ).to('cuda:1')
                
                outputs_gpu1 = model_gpu1(**inputs_gpu1)
                embeddings_gpu1 = outputs_gpu1.last_hidden_state[:, 0, :].cpu().numpy()
        else:
            embeddings_gpu1 = None
        
        # Attach embeddings from GPU 0
        for chunk, embedding in zip(batch_gpu0, embeddings_gpu0):
            chunk['embedding'] = embedding.tolist()
            embedded_chunks.append(chunk)
        
        # Attach embeddings from GPU 1
        if embeddings_gpu1 is not None:
            for chunk, embedding in zip(batch_gpu1, embeddings_gpu1):
                chunk['embedding'] = embedding.tolist()
                embedded_chunks.append(chunk)
        
        if (i + BATCH_SIZE * 2) % 100 == 0 or (i + BATCH_SIZE * 2) >= len(all_chunks):
            print(f"   ✓ Embedded {min(i + BATCH_SIZE * 2, len(all_chunks))}/{len(all_chunks)} chunks (using both GPUs)")
        
        # Clear cache every 10 dual-batches
        if i % (BATCH_SIZE * 20) == 0 and torch.cuda.is_available():
            torch.cuda.empty_cache()
    
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
        # Step 1: Load pre-chunked files
        all_chunks = load_chunked_files()
        
        # Step 2: Embed chunks
        embedded_count = embed_chunks()
        
        # Summary
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds() / 60
        
        print("\n" + "=" * 80)
        print("PIPELINE SUMMARY")
        print("=" * 80)
        print(f"✓ Chunks loaded: {len(all_chunks)}")
        print(f"✓ Chunks embedded: {embedded_count}")
        print(f"✓ Collection: {COLLECTION_NAME}")
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

