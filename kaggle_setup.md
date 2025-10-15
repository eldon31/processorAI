# Kaggle GPU T4 x2 Setup Guide

## Step 1: Create Kaggle Notebook

1. Go to https://www.kaggle.com/code
2. Click **"New Notebook"**
3. Go to Settings (right panel)
4. Set **Accelerator** → **GPU T4 x2**
5. Set **Internet** → **On**

## Step 2: Clone Repository

```python
# Clone the repository
!git clone https://github.com/eldon31/processorAI.git
%cd processorAI
```

## Step 3: Install Dependencies

```python
# Align numpy & scikit-learn with Kaggle build to avoid binary mismatch
!pip install -q --force-reinstall "numpy==1.26.4" "scikit-learn==1.4.2"

# Install required packages (scikit-learn already handled above)
!pip install -q docling docling-core transformers sentence-transformers torch

# Optional: Only if uploading to Qdrant from Kaggle
# !pip install -q qdrant-client
```

## Step 4: Verify GPU Setup

```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU count: {torch.cuda.device_count()}")
print(f"GPU 0: {torch.cuda.get_device_name(0)}")
if torch.cuda.device_count() > 1:
    print(f"GPU 1: {torch.cuda.get_device_name(1)}")
print(f"Total GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
```

## Step 5: Run Processing Scripts

### For Viator API Documentation:
```python
# Process Viator docs with GPU acceleration
# Stops at embeddings - upload to Qdrant locally later
!python scripts/kaggle_process_viator.py
```

### For FastMCP Documentation:
```python
# Chunk FastMCP docs
!python scripts/kaggle_chunk_fastmcp.py
```

## Step 6: Download Results

After processing completes, download the embeddings:

```python
# Create a zip file of embeddings and chunks
!zip -r viator_embeddings.zip output/viator_api/embeddings/ output/viator_api/chunked/
!zip -r fastmcp_chunks.zip output/fast_mcp_api_python/chunked/

# Download from Kaggle's Output tab:
# - viator_embeddings.zip (contains embeddings + chunks)
# - fastmcp_chunks.zip (contains chunks only)
```

Then upload to Qdrant locally:

```python
# After downloading to your local machine, upload to Qdrant
# Use your existing upload scripts locally
```

## Important Notes

- **GPU VRAM**: 2x 16GB = 32GB (model loads here, not disk)
- **Disk Storage**: 20GB limit (only for temporary files)
- **Model Size**: nomic-embed-code is 26.35GB but loads into GPU VRAM
- **Batch Size**: Reduced to 8 to prevent GPU OOM
- **Session Time**: 12 hours max per session, 30 hours/week free

## Troubleshooting

### If you get "out of memory" errors:
- Reduce BATCH_SIZE further (to 4 or 2)
- Use single GPU instead of both
- Clear GPU cache: `torch.cuda.empty_cache()`

### If model download is slow:
- Kaggle has fast internet, should take 5-10 minutes
- Model is cached after first download
