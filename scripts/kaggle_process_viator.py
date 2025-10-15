"""
Kaggle-optimized Viator API Documentation Processing Pipeline
For GPU T4 x2 with nomic-ai/nomic-embed-code

This script is optimized for Kaggle's environment:
- Uses GPU acceleration (CUDA)
- Reduced batch size to prevent OOM
- Progress tracking for long operations
- Automatic cleanup to manage disk space
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
MAX_CHUNK_SIZE = 1024
BATCH_SIZE = 8  # Reduced for GPU memory safety
USE_MODEL_PARALLEL = True  # Split model across 2 GPUs

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


def convert_documents():
    """Step 1: Ensure markdown conversions exist (reuse if already checked in)."""
    print(f"\n{'='*60}")
    print("STEP 1: CONVERTING DOCUMENTS")
    print(f"{'='*60}\n")

    existing_markdown = list(CONVERTED_DIR.glob("*.md"))
    if existing_markdown:
        print(f"✓ Found {len(existing_markdown)} converted markdown files, skipping conversion\n")
        return

    try:
        from docling.document_converter import DocumentConverter, PdfFormatOption
        from docling.datamodel.pipeline_options import PdfPipelineOptions
        from docling.datamodel.base_models import InputFormat
    except Exception as docling_err:
        raise RuntimeError(
            "Docling is unavailable in this runtime and no pre-converted markdown files were found. "
            "Either install docling dependencies (heavy) or commit the markdown conversions beforehand."
        ) from docling_err
    
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
    """Step 2: Chunk markdown documents (reuse pre-chunked files when available)."""
    print(f"\n{'='*60}")
    print("STEP 2: CHUNKING DOCUMENTS")
    print(f"{'='*60}\n")
    
    existing_chunks = list(CHUNKED_DIR.glob("*_chunks.json"))
    if existing_chunks:
        print(f"✓ Found {len(existing_chunks)} existing chunk files, skipping chunking\n")
        return

    tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL, trust_remote_code=True)

    converter = None
    chunker = None

    try:
        from docling_core.transforms.chunker.hybrid_chunker import HybridChunker
        from docling.document_converter import DocumentConverter, PdfFormatOption
        from docling.datamodel.pipeline_options import PdfPipelineOptions
        from docling.datamodel.base_models import InputFormat
    except Exception as docling_err:
        print("⚠️  Docling chunking unavailable (" + str(docling_err) + "), falling back to simple chunking")
        use_docling = False
    else:
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = False
        pipeline_options.do_table_structure = True

        converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )

        chunker = HybridChunker(
            tokenizer=tokenizer,
            merge_peers=True
        )
        use_docling = True

    converted_files = list(CONVERTED_DIR.glob("*.md"))
    total_chunks = 0
    
    for idx, md_file in enumerate(converted_files, 1):
        print(f"[{idx}/{len(converted_files)}] Chunking: {md_file.name}")
        
        if use_docling and converter is not None and chunker is not None:
            # Find original file
            original_name = md_file.stem
            original_file = INPUT_DIR / f"{original_name}.pdf"

            if not original_file.exists():
                original_file = INPUT_DIR / f"{original_name}.json"

            if original_file.exists() and original_file.suffix.lower() == '.pdf':
                result = converter.convert(str(original_file))
                doc = result.document
                chunks = list(chunker.chunk(doc))
                chunk_texts = [chunk.text for chunk in chunks]
            else:
                markdown_text = md_file.read_text(encoding='utf-8')
                chunk_texts = _simple_chunk_text(markdown_text)
        else:
            markdown_text = md_file.read_text(encoding='utf-8')
            chunk_texts = _simple_chunk_text(markdown_text)
        
        # Save chunks
        chunk_data = []
        for chunk_idx, chunk_text in enumerate(chunk_texts):
            chunk_data.append({
                "id": f"{md_file.stem}_chunk_{chunk_idx}",
                "text": chunk_text,
                "metadata": {
                    "source": md_file.stem,
                    "chunk_index": chunk_idx,
                    "total_chunks": len(chunk_texts)
                }
            })
        
        output_path = CHUNKED_DIR / f"{md_file.stem}_chunks.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(chunk_data, f, indent=2, ensure_ascii=False)
        
        print(f"  ✓ Created {len(chunk_texts)} chunks → {output_path.name}\n")
        total_chunks += len(chunk_texts)
    
    print(f"✓ Total chunks created: {total_chunks}\n")


def _simple_chunk_text(markdown_text: str, min_length: int = 100) -> List[str]:
    """Fallback chunker that splits markdown text by heading boundaries and size."""
    segments: List[str] = []
    current = ""

    for line in markdown_text.split('\n'):
        if line.startswith('#') and current:
            if len(current) >= min_length:
                segments.append(current.strip())
            current = line + '\n'
        else:
            current += line + '\n'
            if len(current) >= MAX_CHUNK_SIZE * 2:
                segments.append(current.strip())
                current = ""

    if current.strip():
        segments.append(current.strip())

    if not segments:
        return [markdown_text.strip()]

    return segments


def embed_chunks():
    """Step 3: Generate embeddings using GPU acceleration with model parallelism."""
    print(f"\n{'='*60}")
    print("STEP 3: GENERATING EMBEDDINGS (GPU - Model Parallel)")
    print(f"{'='*60}\n")
    
    # Check if we can use multiple GPUs
    device = "cuda" if torch.cuda.is_available() else "cpu"
    num_gpus = torch.cuda.device_count() if torch.cuda.is_available() else 0
    
    print(f"Available GPUs: {num_gpus}")
    print(f"Model: {EMBEDDING_MODEL}")
    print(f"Using model parallelism: {USE_MODEL_PARALLEL and num_gpus >= 2}\n")
    
    # Load model with device_map for multi-GPU support
    if USE_MODEL_PARALLEL and num_gpus >= 2:
        print("Loading model across multiple GPUs...")
        
        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL, trust_remote_code=True)
        
        # Load model with automatic device mapping
        model = AutoModel.from_pretrained(
            EMBEDDING_MODEL,
            trust_remote_code=True,
            device_map="auto",  # Automatically split across available GPUs
            torch_dtype=torch.float16,  # Use half precision to save memory
        )
        
        print(f"✓ Model loaded across {num_gpus} GPUs with automatic device mapping\n")
        
        # Function to encode with model parallelism
        def encode_batch(texts):
            inputs = tokenizer(
                texts,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors="pt"
            )
            
            # Move inputs to first GPU (model will handle the rest)
            inputs = {k: v.to("cuda:0") for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = model(**inputs)
                # Mean pooling
                embeddings = outputs.last_hidden_state.mean(dim=1)
            
            return embeddings.cpu().numpy()
    
    else:
        print("Loading model on single GPU...")
        model = SentenceTransformer(EMBEDDING_MODEL, device=device)
        print(f"✓ Model loaded on {device}\n")
        
        def encode_batch(texts):
            return model.encode(
                texts,
                show_progress_bar=False,
                batch_size=BATCH_SIZE,
                device=device
            )
    
    chunk_files = list(CHUNKED_DIR.glob("*_chunks.json"))
    all_embeddings = []
    
    for idx, chunk_file in enumerate(chunk_files, 1):
        print(f"[{idx}/{len(chunk_files)}] Embedding: {chunk_file.name}")
        
        # Load chunks
        with open(chunk_file, 'r', encoding='utf-8') as f:
            chunks = json.load(f)
        
        # Extract texts (handle both 'text' and 'content' keys)
        texts = [chunk.get('text') or chunk.get('content', '') for chunk in chunks]
        
        # Generate embeddings in batches
        embeddings = []
        total_batches = (len(texts) + BATCH_SIZE - 1) // BATCH_SIZE
        
        for i in range(0, len(texts), BATCH_SIZE):
            batch_texts = texts[i:i + BATCH_SIZE]
            batch_num = i // BATCH_SIZE + 1
            
            print(f"  Processing batch {batch_num}/{total_batches}...", end='\r')
            
            batch_embeddings = encode_batch(batch_texts)
            embeddings.extend(batch_embeddings)
            
            # Clear GPU cache periodically
            if torch.cuda.is_available() and i % (BATCH_SIZE * 4) == 0:
                torch.cuda.empty_cache()
        
        # Save embeddings
        for chunk, embedding in zip(chunks, embeddings):
            chunk_text = chunk.get('text') or chunk.get('content', '')
            chunk_id = chunk.get('id') or chunk.get('chunk_id', f"chunk_{idx}")
            
            all_embeddings.append({
                "id": chunk_id,
                "text": chunk_text,
                "embedding": embedding.tolist(),
                "metadata": chunk.get('metadata', {})
            })
        
        print(f"  ✓ Embedded {len(chunks)} chunks" + " " * 20)
    
    # Save all embeddings
    output_path = EMBEDDINGS_DIR / "viator_api_embeddings.jsonl"
    with open(output_path, 'w', encoding='utf-8') as f:
        for item in all_embeddings:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    print(f"\n✓ Saved {len(all_embeddings)} embeddings → {output_path.name}\n")
    
    # Clear GPU memory
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        print("✓ Cleared GPU cache\n")


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
