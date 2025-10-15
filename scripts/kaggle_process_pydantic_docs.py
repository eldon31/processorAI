"""
Kaggle-optimized Pydantic Documentation Processing Pipeline
For GPU T4 x2 with nomic-ai/nomic-embed-code (model parallelism)

This script processes Pydantic library documentation:
Collection name: pydantic_docs

Single directory:
- pydantic/ (~270 markdown files)

UNIQUE ID STRATEGY:
- Format: pydantic_docs:{filename}:chunk:{index}
- Example: pydantic_docs:BaseModel.md:chunk:0
"""

import os

os.environ.setdefault("TRANSFORMERS_NO_TF", "1")
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
# Enable PyTorch memory optimization
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict

import numpy as np
import torch

if tuple(map(int, np.__version__.split(".")[:2])) >= (2, 0):
    raise RuntimeError(
        "NumPy 2.x detected. Please run `pip install -q --force-reinstall \"numpy==1.26.4\" \"scikit-learn==1.4.2\"`"
    )

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

EMBEDDING_MODEL = "nomic-ai/nomic-embed-code"
BATCH_SIZE = 8
COLLECTION_NAME = "pydantic_docs"
USE_MODEL_PARALLEL = True
MAX_CHUNK_SIZE = 1500
MIN_CHUNK_SIZE = 100

INPUT_DIR = Path("Docs/python_sdk_and_pydantic/pydantic")
OUTPUT_CHUNKED_DIR = Path("output/pydantic_docs/chunked")

# Save to /kaggle/working for easy download (falls back to local output/ if not on Kaggle)
KAGGLE_WORKING = Path("/kaggle/working")
if KAGGLE_WORKING.exists():
    OUTPUT_EMBEDDINGS_DIR = KAGGLE_WORKING
else:
    OUTPUT_EMBEDDINGS_DIR = Path("output/pydantic_docs/embeddings")

def setup_directories():
    OUTPUT_CHUNKED_DIR.mkdir(parents=True, exist_ok=True)
    if not KAGGLE_WORKING.exists():
        OUTPUT_EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✓ Output directories ready")

def chunk_markdown_file(content: str, source_file: str) -> List[Dict]:
    """Chunk markdown content"""
    chunks = []
    
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
                        "chunk_id": f"{COLLECTION_NAME}:{source_file}:chunk:{chunk_index}",
                        "content": current_chunk.strip(),
                        "metadata": {
                            "source": source_file,
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
                    "chunk_id": f"{COLLECTION_NAME}:{source_file}:chunk:{chunk_index}",
                    "content": current_chunk.strip(),
                    "metadata": {
                        "source": source_file,
                        "heading": section["heading"],
                        "heading_level": section["level"],
                        "chunk_index": chunk_index,
                        "collection": COLLECTION_NAME
                    }
                })
                chunk_index += 1
        else:
            chunks.append({
                "chunk_id": f"{COLLECTION_NAME}:{source_file}:chunk:{chunk_index}",
                "content": section_content,
                "metadata": {
                    "source": source_file,
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
    print(f"\n{'='*60}")
    print("CHUNKING DOCUMENTS")
    print(f"{'='*60}")
    
    if not INPUT_DIR.exists():
        print(f"❌ Error: {INPUT_DIR} not found!")
        return []
    
    all_chunks = []
    unique_ids = set()
    
    md_files = sorted(INPUT_DIR.glob("*.md"))
    print(f"Found {len(md_files)} markdown files\n")
    
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.strip():
                print(f"  ⊘ {md_file.name}: Empty")
                continue
            
            chunks = chunk_markdown_file(content, md_file.name)
            
            if chunks:
                for chunk in chunks:
                    chunk_id = chunk["chunk_id"]
                    if chunk_id in unique_ids:
                        print(f"  ⚠️ Duplicate ID: {chunk_id}")
                    unique_ids.add(chunk_id)
                
                output_file = OUTPUT_CHUNKED_DIR / f"{md_file.stem}_chunks.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(chunks, f, ensure_ascii=False, indent=2)
                
                all_chunks.extend(chunks)
                print(f"  ✓ {md_file.name}: {len(chunks)} chunks")
        
        except Exception as e:
            print(f"  ✗ Error: {md_file.name}: {e}")
    
    print(f"\n{'='*60}")
    print(f"✓ Total chunks: {len(all_chunks)}")
    print(f"✓ Unique IDs: {len(unique_ids)}")
    print(f"{'='*60}\n")
    
    return all_chunks

def embed_chunks(chunks: List[dict]) -> List[dict]:
    print(f"\n{'='*60}")
    print("GENERATING EMBEDDINGS")
    print(f"{'='*60}")
    
    num_gpus = torch.cuda.device_count()
    start_time = datetime.now()
    all_embeddings = []
    
    if USE_MODEL_PARALLEL and num_gpus >= 2:
        print("\n🚀 Loading model with OPTIMIZED model parallelism...")
        print("   Strategy: Layers distributed across GPUs, memory limits enforced")
        
        tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL, trust_remote_code=True)
        
        # Load model with automatic device mapping
        model = AutoModel.from_pretrained(
            EMBEDDING_MODEL,
            torch_dtype=torch.float16,
            trust_remote_code=True,
            device_map="auto",
            low_cpu_mem_usage=True,
            max_memory={0: "13GB", 1: "13GB"}
        )
        model.eval()
        
        print(f"✓ Model loaded with optimized model parallelism")
        print(f"✓ Memory limits: GPU0=13GB, GPU1=13GB")
        
        def encode_batch(texts: List[str]) -> np.ndarray:
            with torch.no_grad():
                encoded = tokenizer(texts, padding=True, truncation=True, max_length=8192, return_tensors='pt')
                
                if hasattr(model, 'device'):
                    encoded = {k: v.to(model.device) for k, v in encoded.items()}
                
                output = model(**encoded)
                mask = encoded['attention_mask']
                tokens = output[0]
                mask_expanded = mask.unsqueeze(-1).expand(tokens.size()).float()
                embeddings = torch.sum(tokens * mask_expanded, 1) / torch.clamp(mask_expanded.sum(1), min=1e-9)
                embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1).cpu().numpy()
                
                del encoded, output, mask, tokens, mask_expanded
                
            return embeddings
    
    else:
        model = SentenceTransformer(EMBEDDING_MODEL, trust_remote_code=True)
        if torch.cuda.is_available():
            model = model.to('cuda')
        
        def encode_batch(texts: List[str]) -> np.ndarray:
            return model.encode(texts, batch_size=BATCH_SIZE, show_progress_bar=False)
    
    total_chunks = len(chunks)
    print(f"\nProcessing {total_chunks} chunks...")
    
    for i in range(0, total_chunks, BATCH_SIZE):
        batch_chunks = chunks[i:i + BATCH_SIZE]
        texts = [chunk.get('content', '') for chunk in batch_chunks]
        embeddings = encode_batch(texts)
        
        for idx, (chunk, embedding) in enumerate(zip(batch_chunks, embeddings)):
            all_embeddings.append({
                "id": chunk.get('chunk_id', f"chunk_{i + idx}"),
                "text": chunk.get('content', ''),
                "embedding": embedding.tolist(),
                "metadata": chunk.get('metadata', {})
            })
        
        processed = min(i + BATCH_SIZE, total_chunks)
        elapsed = (datetime.now() - start_time).total_seconds()
        rate = processed / elapsed if elapsed > 0 else 0
        eta = (total_chunks - processed) / rate if rate > 0 else 0
        
        print(f"  {processed}/{total_chunks} ({processed/total_chunks*100:.1f}%) - {rate:.1f} chunks/sec - ETA: {eta/60:.1f} min")
    
    output_file = OUTPUT_EMBEDDINGS_DIR / f"{COLLECTION_NAME}_embeddings.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for emb in all_embeddings:
            f.write(json.dumps(emb, ensure_ascii=False) + '\n')
    
    print(f"\n✓ Saved: {len(all_embeddings)} embeddings")
    print(f"✓ Time: {(datetime.now() - start_time).total_seconds()/60:.1f} minutes")
    
    return all_embeddings

def main():
    pipeline_start = datetime.now()
    
    print(f"\n{'='*60}")
    print("PYDANTIC DOCS EMBEDDING PIPELINE")
    print(f"{'='*60}")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Input: {INPUT_DIR}")
    print(f"{'='*60}\n")
    
    setup_directories()
    chunks = chunk_documents()
    
    if not chunks:
        print("❌ No chunks!")
        return
    
    embeddings = embed_chunks(chunks)
    
    total_time = (datetime.now() - pipeline_start).total_seconds()
    
    print(f"\n{'='*60}")
    print("✓ COMPLETED")
    print(f"{'='*60}")
    print(f"Chunks: {len(chunks)}")
    print(f"Embeddings: {len(embeddings)}")
    print(f"Time: {total_time/60:.1f} minutes")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
