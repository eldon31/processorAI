"""
Kaggle-optimized FastMCP & API Documentation Processing Pipeline
For GPU T4 x2 with nomic-ai/nomic-embed-code

This script processes FastAPI and FastMCP documentation chunks and generates embeddings.
Collection name: create_fast_mcp_with_api
"""

import os

# Prevent transformers from attempting to load TensorFlow (not available on Kaggle by default)
os.environ.setdefault("TRANSFORMERS_NO_TF", "1")
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")

import json
from pathlib import Path
from datetime import datetime
from typing import List

import numpy as np
import torch

# Guard against accidental NumPy 2.x usage (Kaggle preinstalls 2.x); docling and matplotlib require 1.x
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
from sentence_transformers import SentenceTransformer
from accelerate import init_empty_weights, load_checkpoint_and_dispatch

# Configuration - Optimized for Kaggle GPU T4 x2
EMBEDDING_MODEL = "nomic-ai/nomic-embed-code"
BATCH_SIZE = 8  # Conservative batch size for T4 GPUs
COLLECTION_NAME = "create_fast_mcp_with_api"
USE_MODEL_PARALLEL = True  # Enable model parallelism for 2 GPUs

# Paths
INPUT_DIR = Path("output/fast_mcp_and_api/chunked")
OUTPUT_DIR = Path("output/fast_mcp_and_api/embeddings")

def setup_directories():
    """Create output directories if they don't exist"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✓ Output directory ready: {OUTPUT_DIR}")

def load_chunks() -> List[dict]:
    """
    Load all JSON chunks from fastapi/ and fastmcp/ subdirectories
    
    Returns:
        List of chunk dictionaries with unified schema
    """
    all_chunks = []
    
    print(f"\n{'='*60}")
    print("LOADING CHUNKS")
    print(f"{'='*60}")
    
    # Process both subdirectories
    for subdir in ["fastapi", "fastmcp"]:
        subdir_path = INPUT_DIR / subdir
        if not subdir_path.exists():
            print(f"⚠ Warning: {subdir_path} not found, skipping...")
            continue
            
        print(f"\nProcessing {subdir}/...")
        chunk_files = sorted(subdir_path.glob("*.json"))
        
        for chunk_file in chunk_files:
            try:
                with open(chunk_file, 'r', encoding='utf-8') as f:
                    chunks = json.load(f)
                    
                # Handle both single chunk and list of chunks
                if isinstance(chunks, dict):
                    chunks = [chunks]
                
                # Add source information to metadata
                for chunk in chunks:
                    if 'metadata' not in chunk:
                        chunk['metadata'] = {}
                    chunk['metadata']['source_file'] = chunk_file.name
                    chunk['metadata']['source_subdir'] = subdir
                    chunk['metadata']['collection'] = COLLECTION_NAME
                
                all_chunks.extend(chunks)
                print(f"  ✓ {chunk_file.name}: {len(chunks)} chunks")
                
            except Exception as e:
                print(f"  ✗ Error loading {chunk_file.name}: {e}")
    
    print(f"\n{'='*60}")
    print(f"✓ Total chunks loaded: {len(all_chunks)}")
    print(f"{'='*60}\n")
    
    return all_chunks

def embed_chunks(chunks: List[dict]) -> List[dict]:
    """
    Generate embeddings for all chunks using nomic-embed-code
    
    Args:
        chunks: List of chunk dictionaries
        
    Returns:
        List of dictionaries with embeddings
    """
    print(f"\n{'='*60}")
    print("GENERATING EMBEDDINGS")
    print(f"{'='*60}")
    print(f"Model: {EMBEDDING_MODEL}")
    print(f"Batch size: {BATCH_SIZE}")
    
    num_gpus = torch.cuda.device_count()
    print(f"Available GPUs: {num_gpus}")
    print(f"Using model parallelism: {USE_MODEL_PARALLEL and num_gpus >= 2}")
    
    start_time = datetime.now()
    all_embeddings = []
    
    # Choose embedding strategy based on GPU count
    if USE_MODEL_PARALLEL and num_gpus >= 2:
        print("\n🚀 Loading model with multi-GPU parallelism...")
        
        # Load model with automatic device mapping across GPUs
        model = AutoModel.from_pretrained(
            EMBEDDING_MODEL,
            device_map="auto",  # Automatically distributes layers across GPUs
            torch_dtype=torch.float16,  # Use half precision to reduce memory
            trust_remote_code=True
        )
        tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL, trust_remote_code=True)
        
        print("✓ Model loaded across 2 GPUs with automatic device mapping")
        
        def encode_batch(texts: List[str]) -> np.ndarray:
            """Encode a batch of texts using manual tokenization and mean pooling"""
            # Tokenize
            encoded_input = tokenizer(
                texts,
                padding=True,
                truncation=True,
                max_length=8192,
                return_tensors='pt'
            )
            
            # Move inputs to first GPU (model will handle distribution)
            encoded_input = {k: v.to('cuda:0') for k, v in encoded_input.items()}
            
            # Forward pass
            with torch.no_grad():
                model_output = model(**encoded_input)
            
            # Mean pooling
            attention_mask = encoded_input['attention_mask']
            token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
            input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
            embeddings = torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
            
            # Normalize embeddings
            embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
            
            return embeddings.cpu().numpy()
    
    else:
        print("\n🚀 Loading model with SentenceTransformer (single GPU)...")
        model = SentenceTransformer(EMBEDDING_MODEL, trust_remote_code=True)
        if torch.cuda.is_available():
            model = model.to('cuda')
        print("✓ Model loaded on single GPU")
        
        def encode_batch(texts: List[str]) -> np.ndarray:
            """Encode using SentenceTransformer"""
            return model.encode(texts, batch_size=BATCH_SIZE, show_progress_bar=False)
    
    # Process chunks in batches
    total_chunks = len(chunks)
    print(f"\nProcessing {total_chunks} chunks in batches of {BATCH_SIZE}...")
    
    for i in range(0, total_chunks, BATCH_SIZE):
        batch_chunks = chunks[i:i + BATCH_SIZE]
        batch_size = len(batch_chunks)
        
        # Extract text from chunks (handle both 'content' and 'text' keys)
        texts = [chunk.get('text') or chunk.get('content', '') for chunk in batch_chunks]
        
        # Generate embeddings
        embeddings = encode_batch(texts)
        
        # Store results
        for idx, (chunk, embedding) in enumerate(zip(batch_chunks, embeddings)):
            # Extract chunk ID (handle both 'id' and 'chunk_id' keys)
            chunk_id = chunk.get('id') or chunk.get('chunk_id', f"chunk_{i + idx}")
            chunk_text = chunk.get('text') or chunk.get('content', '')
            
            embedding_data = {
                "id": chunk_id,
                "text": chunk_text,
                "embedding": embedding.tolist(),
                "metadata": chunk.get('metadata', {})
            }
            all_embeddings.append(embedding_data)
        
        # Progress update
        processed = min(i + BATCH_SIZE, total_chunks)
        elapsed = (datetime.now() - start_time).total_seconds()
        rate = processed / elapsed if elapsed > 0 else 0
        eta = (total_chunks - processed) / rate if rate > 0 else 0
        
        print(f"  Progress: {processed}/{total_chunks} chunks "
              f"({processed/total_chunks*100:.1f}%) - "
              f"{rate:.1f} chunks/sec - "
              f"ETA: {eta/60:.1f} min")
    
    # Save all embeddings to single JSONL file
    output_file = OUTPUT_DIR / f"{COLLECTION_NAME}_embeddings.jsonl"
    print(f"\n💾 Saving embeddings to {output_file}...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for embedding_data in all_embeddings:
            f.write(json.dumps(embedding_data, ensure_ascii=False) + '\n')
    
    elapsed_time = (datetime.now() - start_time).total_seconds()
    print(f"✓ Embeddings saved: {len(all_embeddings)} chunks")
    print(f"✓ Time elapsed: {elapsed_time/60:.1f} minutes")
    print(f"✓ Output file: {output_file}")
    
    return all_embeddings

def main():
    """Main pipeline execution"""
    pipeline_start = datetime.now()
    
    print(f"\n{'='*60}")
    print("FAST MCP & API EMBEDDING PIPELINE")
    print(f"{'='*60}")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Input directory: {INPUT_DIR}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Started: {pipeline_start.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    # Setup
    setup_directories()
    
    # Load chunks
    chunks = load_chunks()
    
    if not chunks:
        print("❌ No chunks found to process!")
        return
    
    # Generate embeddings
    embeddings = embed_chunks(chunks)
    
    # Summary
    pipeline_end = datetime.now()
    total_time = (pipeline_end - pipeline_start).total_seconds()
    
    print(f"\n{'='*60}")
    print("✓ PIPELINE COMPLETED")
    print(f"{'='*60}")
    print(f"Total chunks processed: {len(embeddings)}")
    print(f"Total time: {total_time/60:.1f} minutes")
    print(f"Output: {OUTPUT_DIR / f'{COLLECTION_NAME}_embeddings.jsonl'}")
    print(f"Collection name: {COLLECTION_NAME}")
    print(f"Vector dimensions: 768")
    print(f"Ready for Qdrant upload!")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
