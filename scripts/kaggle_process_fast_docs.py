"""
Kaggle-optimized Fast Docs Processing Pipeline
For GPU T4 x2 with nomic-ai/nomic-embed-code

This script processes all Fast* framework documentation:
Collection name: fast_docs

Subdirectories:
1. fastapi/      - FastAPI framework documentation (~17 files)
2. fastmcp/      - FastMCP framework documentation (~54 files)
3. python_sdk/   - MCP Python SDK documentation (~38 files)

Total: ~109 markdown files

UNIQUE ID STRATEGY:
- Format: fast_docs:{subdir}:{filename}:chunk:{index}
- Example: fast_docs:fastapi:Overview.md:chunk:0
- Example: fast_docs:fastmcp:Installation.md:chunk:0
- Example: fast_docs:python_sdk:Client_Examples.md:chunk:0
"""

import os

# Prevent transformers from attempting to load TensorFlow
os.environ.setdefault("TRANSFORMERS_NO_TF", "1")
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")

import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict

import numpy as np
import torch

# Guard against NumPy 2.x
if tuple(map(int, np.__version__.split(".")[:2])) >= (2, 0):
    raise RuntimeError(
        "NumPy 2.x detected. Please run `pip install -q --force-reinstall \"numpy==1.26.4\" \"scikit-learn==1.4.2\"`"
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

# Configuration
EMBEDDING_MODEL = "nomic-ai/nomic-embed-code"
BATCH_SIZE = 8
COLLECTION_NAME = "fast_docs"
USE_MODEL_PARALLEL = True
MAX_CHUNK_SIZE = 1500
MIN_CHUNK_SIZE = 100

# Paths
DOCS_BASE = Path("Docs/fast_mcp_api_python")
OUTPUT_CHUNKED_DIR = Path("output/fast_docs/chunked")
OUTPUT_EMBEDDINGS_DIR = Path("output/fast_docs/embeddings")

# Subdirectories
SUBDIRS = {
    "fastapi": DOCS_BASE / "fastapi",
    "fastmcp": DOCS_BASE / "fastmcp",
    "python_sdk": DOCS_BASE / "python-sdk"  # Note: dash in folder name
}

def setup_directories():
    """Create output directories"""
    OUTPUT_CHUNKED_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✓ Output directories ready")
    print(f"  Chunked: {OUTPUT_CHUNKED_DIR}")
    print(f"  Embeddings: {OUTPUT_EMBEDDINGS_DIR}")

def chunk_markdown_file(content: str, source_file: str, subdir: str) -> List[Dict]:
    """Chunk markdown content by headings and size"""
    chunks = []
    
    # Split by markdown headings
    heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
    sections = []
    current_section = {"heading": "", "level": 0, "content": ""}
    last_pos = 0
    
    for match in heading_pattern.finditer(content):
        if current_section["content"].strip():
            sections.append(current_section.copy())
        
        level = len(match.group(1))
        heading = match.group(2).strip()
        start_pos = match.start()
        
        if last_pos < start_pos:
            if sections:
                sections[-1]["content"] += content[last_pos:start_pos]
            else:
                current_section["content"] = content[last_pos:start_pos]
        
        current_section = {
            "heading": heading,
            "level": level,
            "content": match.group(0) + "\n"
        }
        last_pos = match.end()
    
    if last_pos < len(content):
        current_section["content"] += content[last_pos:]
    if current_section["content"].strip():
        sections.append(current_section)
    
    if not sections:
        sections = [{"heading": source_file.replace('.md', ''), "level": 1, "content": content}]
    
    # Create chunks
    chunk_index = 0
    for section in sections:
        section_content = section["content"].strip()
        
        if not section_content or len(section_content) < MIN_CHUNK_SIZE:
            continue
        
        if len(section_content) > MAX_CHUNK_SIZE:
            paragraphs = section_content.split('\n\n')
            current_chunk = ""
            
            for para in paragraphs:
                if len(current_chunk) + len(para) > MAX_CHUNK_SIZE and current_chunk:
                    chunks.append({
                        "chunk_id": f"{COLLECTION_NAME}:{subdir}:{source_file}:chunk:{chunk_index}",
                        "content": current_chunk.strip(),
                        "metadata": {
                            "source": source_file,
                            "subdir": subdir,
                            "heading": section["heading"],
                            "heading_level": section["level"],
                            "chunk_index": chunk_index,
                            "collection": COLLECTION_NAME
                        }
                    })
                    chunk_index += 1
                    current_chunk = para + "\n\n"
                else:
                    current_chunk += para + "\n\n"
            
            if current_chunk.strip():
                chunks.append({
                    "chunk_id": f"{COLLECTION_NAME}:{subdir}:{source_file}:chunk:{chunk_index}",
                    "content": current_chunk.strip(),
                    "metadata": {
                        "source": source_file,
                        "subdir": subdir,
                        "heading": section["heading"],
                        "heading_level": section["level"],
                        "chunk_index": chunk_index,
                        "collection": COLLECTION_NAME
                    }
                })
                chunk_index += 1
        else:
            chunks.append({
                "chunk_id": f"{COLLECTION_NAME}:{subdir}:{source_file}:chunk:{chunk_index}",
                "content": section_content,
                "metadata": {
                    "source": source_file,
                    "subdir": subdir,
                    "heading": section["heading"],
                    "heading_level": section["level"],
                    "chunk_index": chunk_index,
                    "collection": COLLECTION_NAME
                }
            })
            chunk_index += 1
    
    for chunk in chunks:
        chunk["metadata"]["total_chunks"] = len(chunks)
    
    return chunks

def chunk_documents() -> List[Dict]:
    """Process all markdown files"""
    print(f"\n{'='*60}")
    print("CHUNKING DOCUMENTS")
    print(f"{'='*60}")
    
    all_chunks = []
    unique_ids = set()
    total_files = 0
    
    for subdir_key, subdir_path in SUBDIRS.items():
        if not subdir_path.exists():
            print(f"⚠ Warning: {subdir_path} not found, skipping...")
            continue
        
        print(f"\n{'─'*60}")
        print(f"Processing {subdir_key}/ ({subdir_path})")
        print(f"{'─'*60}")
        
        md_files = sorted(subdir_path.glob("*.md"))
        
        if not md_files:
            print(f"  ⚠ No markdown files in {subdir_key}/")
            continue
        
        output_subdir = OUTPUT_CHUNKED_DIR / subdir_key
        output_subdir.mkdir(parents=True, exist_ok=True)
        
        subdir_chunk_count = 0
        subdir_file_count = 0
        
        for md_file in md_files:
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if not content.strip():
                    print(f"  ⊘ {md_file.name}: Empty file, skipping")
                    continue
                
                chunks = chunk_markdown_file(content, md_file.name, subdir_key)
                
                if chunks:
                    for chunk in chunks:
                        chunk_id = chunk["chunk_id"]
                        if chunk_id in unique_ids:
                            print(f"  ⚠️ WARNING: Duplicate ID: {chunk_id}")
                        unique_ids.add(chunk_id)
                    
                    output_file = output_subdir / f"{md_file.stem}_chunks.json"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(chunks, f, ensure_ascii=False, indent=2)
                    
                    all_chunks.extend(chunks)
                    subdir_chunk_count += len(chunks)
                    subdir_file_count += 1
                    print(f"  ✓ {md_file.name}: {len(chunks)} chunks")
                else:
                    print(f"  ⊘ {md_file.name}: No chunks generated")
                
            except Exception as e:
                print(f"  ✗ Error processing {md_file.name}: {e}")
        
        print(f"\n  Subtotal for {subdir_key}/: {subdir_file_count} files, {subdir_chunk_count} chunks")
        total_files += subdir_file_count
    
    print(f"\n{'='*60}")
    print(f"✓ Total files processed: {total_files}")
    print(f"✓ Total chunks created: {len(all_chunks)}")
    print(f"✓ Unique IDs verified: {len(unique_ids)}")
    print(f"✓ ID conflicts: {len(all_chunks) - len(unique_ids)} (should be 0)")
    print(f"{'='*60}\n")
    
    return all_chunks

def embed_chunks(chunks: List[dict]) -> List[dict]:
    """Generate embeddings using nomic-embed-code"""
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
    
    if USE_MODEL_PARALLEL and num_gpus >= 2:
        print("\n🚀 Loading model with multi-GPU parallelism...")
        
        model = AutoModel.from_pretrained(
            EMBEDDING_MODEL,
            device_map="auto",
            torch_dtype=torch.float16,
            trust_remote_code=True
        )
        tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL, trust_remote_code=True)
        
        print("✓ Model loaded across 2 GPUs")
        
        def encode_batch(texts: List[str]) -> np.ndarray:
            encoded_input = tokenizer(
                texts,
                padding=True,
                truncation=True,
                max_length=8192,
                return_tensors='pt'
            )
            
            encoded_input = {k: v.to('cuda:0') for k, v in encoded_input.items()}
            
            with torch.no_grad():
                model_output = model(**encoded_input)
            
            attention_mask = encoded_input['attention_mask']
            token_embeddings = model_output[0]
            input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
            embeddings = torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
            embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
            
            return embeddings.cpu().numpy()
    else:
        print("\n🚀 Loading model with SentenceTransformer...")
        model = SentenceTransformer(EMBEDDING_MODEL, trust_remote_code=True)
        if torch.cuda.is_available():
            model = model.to('cuda')
        print("✓ Model loaded on single GPU")
        
        def encode_batch(texts: List[str]) -> np.ndarray:
            return model.encode(texts, batch_size=BATCH_SIZE, show_progress_bar=False)
    
    total_chunks = len(chunks)
    print(f"\nProcessing {total_chunks} chunks in batches of {BATCH_SIZE}...")
    
    for i in range(0, total_chunks, BATCH_SIZE):
        batch_chunks = chunks[i:i + BATCH_SIZE]
        texts = [chunk.get('content', '') for chunk in batch_chunks]
        embeddings = encode_batch(texts)
        
        for idx, (chunk, embedding) in enumerate(zip(batch_chunks, embeddings)):
            chunk_id = chunk.get('chunk_id', f"chunk_{i + idx}")
            chunk_text = chunk.get('content', '')
            
            embedding_data = {
                "id": chunk_id,
                "text": chunk_text,
                "embedding": embedding.tolist(),
                "metadata": chunk.get('metadata', {})
            }
            all_embeddings.append(embedding_data)
        
        processed = min(i + BATCH_SIZE, total_chunks)
        elapsed = (datetime.now() - start_time).total_seconds()
        rate = processed / elapsed if elapsed > 0 else 0
        eta = (total_chunks - processed) / rate if rate > 0 else 0
        
        print(f"  Progress: {processed}/{total_chunks} chunks "
              f"({processed/total_chunks*100:.1f}%) - "
              f"{rate:.1f} chunks/sec - ETA: {eta/60:.1f} min")
    
    output_file = OUTPUT_EMBEDDINGS_DIR / f"{COLLECTION_NAME}_embeddings.jsonl"
    print(f"\n💾 Saving embeddings to {output_file}...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for embedding_data in all_embeddings:
            f.write(json.dumps(embedding_data, ensure_ascii=False) + '\n')
    
    elapsed_time = (datetime.now() - start_time).total_seconds()
    print(f"✓ Embeddings saved: {len(all_embeddings)} chunks")
    print(f"✓ Time elapsed: {elapsed_time/60:.1f} minutes")
    
    return all_embeddings

def main():
    """Main pipeline execution"""
    pipeline_start = datetime.now()
    
    print(f"\n{'='*60}")
    print("FAST DOCS EMBEDDING PIPELINE")
    print(f"{'='*60}")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Subdirectories:")
    for subdir_key, subdir_path in SUBDIRS.items():
        print(f"  - {subdir_key}: {subdir_path}")
    print(f"Started: {pipeline_start.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    setup_directories()
    chunks = chunk_documents()
    
    if not chunks:
        print("❌ No chunks created!")
        return
    
    embeddings = embed_chunks(chunks)
    
    pipeline_end = datetime.now()
    total_time = (pipeline_end - pipeline_start).total_seconds()
    
    print(f"\n{'='*60}")
    print("✓ PIPELINE COMPLETED")
    print(f"{'='*60}")
    print(f"Total chunks: {len(chunks)}")
    print(f"Total embeddings: {len(embeddings)}")
    print(f"Total time: {total_time/60:.1f} minutes")
    print(f"Output: {OUTPUT_EMBEDDINGS_DIR / f'{COLLECTION_NAME}_embeddings.jsonl'}")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Vector dimensions: 768")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
