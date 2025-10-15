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
# Install required packages
!pip install -q docling docling-core transformers sentence-transformers qdrant-client torch
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
!python scripts/kaggle_process_viator.py
```

### For FastMCP Documentation:
```python
# Chunk FastMCP docs
!python scripts/kaggle_chunk_fastmcp.py
```

## Step 6: Download Results

After processing completes, download the output files:

```python
# Create a zip file of all outputs
!zip -r outputs.zip output/

# The file will be available in Kaggle's Output tab
# Download it from there
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
