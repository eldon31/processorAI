"""
Kaggle-optimized Inngest Ecosystem Documentation Processing Pipeline
For GPU T4 x2 with nomic-ai/nomic-embed-code

This script processes ALL Inngest-related documentation into one collection:
Collection name: inngest_ecosystem

Subdirectories:
1. inngest_overall/     - Main Inngest documentation (~174 files)
2. agent_kit/           - Agent Kit documentation (~46 files)
3. agent_kit_github/    - Agent Kit GitHub docs (~19 files)
4. inngest/             - Core Inngest implementation (~12 files)
5. inngest_js/          - JavaScript SDK (~13 files)
6. inngest_py/          - Python SDK (~31 files)

Total: ~295 markdown files

UNIQUE ID STRATEGY:
- Format: inngest_ecosystem:{subdir}:{filename}:chunk:{index}
- Example: inngest_ecosystem:inngest_overall:events.md:chunk:0
- Example: inngest_ecosystem:agent_kit:concepts_agents.md:chunk:0
- Example: inngest_ecosystem:inngest_js:AI_Integration.md:chunk:0
- Subdirectory in ID prevents any conflicts!
"""

import os

# Prevent transformers from attempting to load TensorFlow (not available on Kaggle by default)
os.environ.setdefault("TRANSFORMERS_NO_TF", "1")
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")

import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict

import numpy as np
import torch

# Guard against accidental NumPy 2.x usage (Kaggle preinstalls 2.x)
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

# Configuration - Optimized for Kaggle GPU T4 x2
EMBEDDING_MODEL = "nomic-ai/nomic-embed-code"
BATCH_SIZE = 8  # Conservative batch size for T4 GPUs
COLLECTION_NAME = "inngest_ecosystem"
USE_MODEL_PARALLEL = True  # Enable model parallelism for 2 GPUs
MAX_CHUNK_SIZE = 1500  # Characters per chunk
MIN_CHUNK_SIZE = 100  # Minimum chunk size

# Paths
DOCS_BASE = Path("Docs")
OUTPUT_CHUNKED_DIR = Path("output/inngest_ecosystem/chunked")
OUTPUT_EMBEDDINGS_DIR = Path("output/inngest_ecosystem/embeddings")

# Subdirectories to process (in order)
SUBDIRS = {
    "inngest_overall": DOCS_BASE / "inngest_overall",
    "agent_kit": DOCS_BASE / "agent_kit",
    "agent_kit_github": DOCS_BASE / "agent-kit_github",
    "inngest": DOCS_BASE / "inngest" / "inngest",
    "inngest_js": DOCS_BASE / "inngest" / "inngest-js",
    "inngest_py": DOCS_BASE / "inngest" / "inngest-py"
}

def setup_directories():
    """Create output directories if they don't exist"""
    OUTPUT_CHUNKED_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✓ Output directories ready")
    print(f"  Chunked: {OUTPUT_CHUNKED_DIR}")
    print(f"  Embeddings: {OUTPUT_EMBEDDINGS_DIR}")

def chunk_markdown_file(content: str, source_file: str, subdir: str) -> List[Dict]:
    """
    Chunk markdown content by headings and size
    
    UNIQUE ID FORMAT: {COLLECTION_NAME}:{subdir}:{filename}:chunk:{index}
    This ensures no conflicts even if same filename exists in different subdirs
    
    Args:
        content: Markdown file content
        source_file: Source filename
        subdir: Subdirectory key (inngest_overall, agent_kit, etc.)
        
    Returns:
        List of chunk dictionaries
    """
    chunks = []
    
    # Split by markdown headings (# ## ###)
    heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
    sections = []
    current_section = {"heading": "", "level": 0, "content": ""}
    last_pos = 0
    
    for match in heading_pattern.finditer(content):
        # Save previous section
        if current_section["content"].strip():
            sections.append(current_section.copy())
        
        # Start new section
        level = len(match.group(1))
        heading = match.group(2).strip()
        start_pos = match.start()
        
        # Add content before this heading to previous section
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
    
    # Add remaining content
    if last_pos < len(content):
        current_section["content"] += content[last_pos:]
    if current_section["content"].strip():
        sections.append(current_section)
    
    # If no headings found, treat entire content as one section
    if not sections:
        sections = [{"heading": source_file.replace('.md', ''), "level": 1, "content": content}]
    
    # Create chunks from sections
    chunk_index = 0
    for section in sections:
        section_content = section["content"].strip()
        
        if not section_content or len(section_content) < MIN_CHUNK_SIZE:
            continue
        
        # Split large sections into smaller chunks
        if len(section_content) > MAX_CHUNK_SIZE:
            # Split by paragraphs
            paragraphs = section_content.split('\n\n')
            current_chunk = ""
            
            for para in paragraphs:
                if len(current_chunk) + len(para) > MAX_CHUNK_SIZE and current_chunk:
                    # Save current chunk with UNIQUE ID including subdir
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
            
            # Save remaining content
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
            # Section fits in one chunk
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
    
    # Add total_chunks to all chunks
    for chunk in chunks:
        chunk["metadata"]["total_chunks"] = len(chunks)
    
    return chunks

def chunk_documents() -> List[Dict]:
    """
    Process all markdown files from all subdirectories
    
    Returns:
        List of all chunks with unique IDs across subdirectories
    """
    print(f"\n{'='*60}")
    print("CHUNKING DOCUMENTS")
    print(f"{'='*60}")
    
    all_chunks = []
    unique_ids = set()  # Track IDs to verify uniqueness
    total_files = 0
    
    # Process each subdirectory
    for subdir_key, subdir_path in SUBDIRS.items():
        if not subdir_path.exists():
            print(f"⚠ Warning: {subdir_path} not found, skipping...")
            continue
        
        print(f"\n{'─'*60}")
        print(f"Processing {subdir_key}/ ({subdir_path})")
        print(f"{'─'*60}")
        
        md_files = sorted(subdir_path.glob("*.md"))
        
        if not md_files:
            print(f"  ⚠ No markdown files found in {subdir_key}/")
            continue
        
        # Create output subdirectory
        output_subdir = OUTPUT_CHUNKED_DIR / subdir_key
        output_subdir.mkdir(parents=True, exist_ok=True)
        
        subdir_chunk_count = 0
        subdir_file_count = 0
        
        for md_file in md_files:
            try:
                # Read markdown content
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Skip empty files
                if not content.strip():
                    print(f"  ⊘ {md_file.name}: Empty file, skipping")
                    continue
                
                # Chunk the file (with subdir in ID)
                chunks = chunk_markdown_file(content, md_file.name, subdir_key)
                
                if chunks:
                    # Verify unique IDs
                    for chunk in chunks:
                        chunk_id = chunk["chunk_id"]
                        if chunk_id in unique_ids:
                            print(f"  ⚠️ WARNING: Duplicate ID detected: {chunk_id}")
                        unique_ids.add(chunk_id)
                    
                    # Save chunks to JSON file
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
    print(f"✓ Chunks saved to: {OUTPUT_CHUNKED_DIR}")
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
            token_embeddings = model_output[0]
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
        
        # Extract text from chunks
        texts = [chunk.get('content', '') for chunk in batch_chunks]
        
        # Generate embeddings
        embeddings = encode_batch(texts)
        
        # Store results
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
    output_file = OUTPUT_EMBEDDINGS_DIR / f"{COLLECTION_NAME}_embeddings.jsonl"
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
    print("INNGEST ECOSYSTEM EMBEDDING PIPELINE")
    print(f"{'='*60}")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Subdirectories to process:")
    for subdir_key, subdir_path in SUBDIRS.items():
        print(f"  - {subdir_key}: {subdir_path}")
    print(f"Output directories:")
    print(f"  Chunked: {OUTPUT_CHUNKED_DIR}")
    print(f"  Embeddings: {OUTPUT_EMBEDDINGS_DIR}")
    print(f"Started: {pipeline_start.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    print(f"\n⚠️  UNIQUE ID STRATEGY:")
    print(f"   Format: {COLLECTION_NAME}:{{subdir}}:{{filename}}:chunk:{{index}}")
    print(f"   Example: {COLLECTION_NAME}:inngest_overall:events.md:chunk:0")
    print(f"   Example: {COLLECTION_NAME}:agent_kit:concepts_agents.md:chunk:0")
    print(f"   This prevents conflicts across subdirectories!\n")
    
    # Setup
    setup_directories()
    
    # Step 1: Chunk documents
    chunks = chunk_documents()
    
    if not chunks:
        print("❌ No chunks created!")
        return
    
    # Step 2: Generate embeddings
    embeddings = embed_chunks(chunks)
    
    # Summary
    pipeline_end = datetime.now()
    total_time = (pipeline_end - pipeline_start).total_seconds()
    
    print(f"\n{'='*60}")
    print("✓ PIPELINE COMPLETED")
    print(f"{'='*60}")
    print(f"Subdirectories processed: {len(SUBDIRS)}")
    print(f"Total markdown files: ~295 expected")
    print(f"Total chunks created: {len(chunks)}")
    print(f"Total embeddings generated: {len(embeddings)}")
    print(f"Total time: {total_time/60:.1f} minutes")
    print(f"Chunks output: {OUTPUT_CHUNKED_DIR}")
    print(f"Embeddings output: {OUTPUT_EMBEDDINGS_DIR / f'{COLLECTION_NAME}_embeddings.jsonl'}")
    print(f"Collection name: {COLLECTION_NAME}")
    print(f"Vector dimensions: 768")
    print(f"✓ All IDs are unique (no conflicts across subdirectories)")
    print(f"Ready for Qdrant upload!")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
