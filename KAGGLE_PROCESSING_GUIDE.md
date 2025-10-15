# 📋 Kaggle Processing Guide - All Collections

This guide shows how to process each documentation collection on Kaggle GPU T4 x2.

---

## ✅ GPU Configuration (ALL SCRIPTS)

**All scripts are configured for 2-GPU parallelism:**
- ✅ `device_map="auto"` - Automatically splits 26GB model across 2 GPUs (~13GB each)
- ✅ `torch_dtype=torch.float16` - Uses FP16 precision to reduce memory
- ✅ Model: `nomic-ai/nomic-embed-code` (768-dim embeddings)
- ✅ Batch size: 8 (optimized for GPU memory)

**This means each GPU handles ~13GB of the model, utilizing BOTH T4 x2 GPUs efficiently!**

---

## 📦 Collection 1: Viator API (RESTRUCTURED)

### Collection Structure:
```
viator_api/
├── affiliate/           - Affiliate Attribution (1 PDF)
├── technical_guides/    - Technical Guide + Partner API (2 PDFs)
└── api_specs/          - OpenAPI JSON (1 file)
```

### Kaggle Setup:

**1. Upload to Kaggle:**
```
Docs/viator_api_documentation/  (4 files)
scripts/kaggle_process_viator.py
```

**2. Install Dependencies:**
```python
# Cell 1: Install dependencies
!pip install -q --force-reinstall "numpy==1.26.4" "scipy==1.11.4" "scikit-learn==1.4.2"
!pip install -q docling docling-core transformers accelerate torch sentencepiece
```

**3. Run Processing:**
```python
# Cell 2: Process Viator API
!python scripts/kaggle_process_viator.py
```

**4. Download Output:**
```python
# Cell 3: Package embeddings
!zip -r viator_api_embeddings.zip output/viator_api/embeddings/
```

### Expected Output:
- **File:** `output/viator_api/embeddings/viator_api_embeddings.jsonl`
- **Chunks:** ~995 chunks (based on previous run)
- **Duration:** ~7-10 minutes
- **Chunk ID Format:** `viator_api:affiliate:filename:chunk:0`

---

## 📦 Collection 2: Fast Docs (FastAPI + FastMCP + PythonSDK)

### Collection Structure:
```
fast_docs/
├── fastapi/       - FastAPI framework docs
├── fastmcp/       - FastMCP docs
└── python_sdk/    - Python SDK docs
```

### Kaggle Setup:

**1. Upload to Kaggle:**
```
Docs/fast_mcp_api_python/fastapi/     (~40 files)
Docs/fast_mcp_api_python/fastmcp/     (~35 files)
Docs/fast_mcp_api_python/python_sdk/  (~34 files)
scripts/kaggle_process_fast_docs.py
```

**2. Install Dependencies:**
```python
# Cell 1: Install dependencies
!pip install -q --force-reinstall "numpy==1.26.4" "scipy==1.11.4" "scikit-learn==1.4.2"
!pip install -q transformers accelerate torch sentencepiece
```

**3. Run Processing:**
```python
# Cell 2: Process Fast Docs
!python scripts/kaggle_process_fast_docs.py
```

**4. Download Output:**
```python
# Cell 3: Package embeddings
!zip -r fast_docs_embeddings.zip output/fast_docs/embeddings/
```

### Expected Output:
- **File:** `output/fast_docs/embeddings/fast_docs_embeddings.jsonl`
- **Chunks:** ~2,000-3,000 chunks (estimate based on ~109 markdown files)
- **Duration:** ~15-20 minutes
- **Chunk ID Format:** `fast_docs:fastapi:filename:chunk:0`

**Note:** This script processes **markdown files only** (no PDF conversion needed).

---

## 📦 Collection 3: Pydantic Docs

### Collection Structure:
```
pydantic_docs/
└── (single directory - no subdirs)
```

### Kaggle Setup:

**1. Upload to Kaggle:**
```
Docs/python_sdk_and_pydantic/pydantic/  (~270 markdown files)
scripts/kaggle_process_pydantic_docs.py
```

**2. Install Dependencies:**
```python
# Cell 1: Install dependencies
!pip install -q --force-reinstall "numpy==1.26.4" "scipy==1.11.4" "scikit-learn==1.4.2"
!pip install -q transformers accelerate torch sentencepiece
```

**3. Run Processing:**
```python
# Cell 2: Process Pydantic Docs
!python scripts/kaggle_process_pydantic_docs.py
```

**4. Download Output:**
```python
# Cell 3: Package embeddings
!zip -r pydantic_docs_embeddings.zip output/pydantic_docs/embeddings/
```

### Expected Output:
- **File:** `output/pydantic_docs/embeddings/pydantic_docs_embeddings.jsonl`
- **Chunks:** ~5,000-8,000 chunks (estimate based on ~270 markdown files)
- **Duration:** ~25-35 minutes
- **Chunk ID Format:** `pydantic_docs:filename:chunk:0` (no subdir)

**Note:** Largest collection by file count. Processes markdown files only.

---

## 📦 Collection 4: Inngest Ecosystem (6 Subdirectories)

### Collection Structure:
```
inngest_ecosystem/
├── inngest_overall/     - Main Inngest docs
├── agent_kit/          - Agent Kit docs
├── agent_kit_github/   - Agent Kit GitHub docs
├── inngest/            - Inngest core
├── inngest_js/         - JavaScript SDK
└── inngest_py/         - Python SDK
```

### Kaggle Setup:

**1. Upload to Kaggle:**
```
Docs/inngest_docs/inngest_overall/    (~80 files)
Docs/inngest_docs/agent_kit/          (~45 files)
Docs/agent_kit_github/                (~19 files)
Docs/inngest_docs/inngest/            (~80 files)
Docs/inngest_docs/inngest_js/         (~35 files)
Docs/inngest_docs/inngest_py/         (~36 files)
scripts/kaggle_process_inngest_ecosystem.py
```

**2. Install Dependencies:**
```python
# Cell 1: Install dependencies
!pip install -q --force-reinstall "numpy==1.26.4" "scipy==1.11.4" "scikit-learn==1.4.2"
!pip install -q transformers accelerate torch sentencepiece
```

**3. Run Processing:**
```python
# Cell 2: Process Inngest Ecosystem
!python scripts/kaggle_process_inngest_ecosystem.py
```

**4. Download Output:**
```python
# Cell 3: Package embeddings
!zip -r inngest_ecosystem_embeddings.zip output/inngest_ecosystem/embeddings/
```

### Expected Output:
- **File:** `output/inngest_ecosystem/embeddings/inngest_ecosystem_embeddings.jsonl`
- **Chunks:** ~6,000-10,000 chunks (estimate based on ~295 markdown files)
- **Duration:** ~30-40 minutes
- **Chunk ID Format:** `inngest_ecosystem:inngest_js:filename:chunk:0`

**Note:** Largest collection by subdirectory count (6 subdirs). Processes markdown files only.

---

## 🚀 Recommended Processing Order

### Option A: By Size (Smallest to Largest)
1. **Viator API** (~10 min) - 4 files, includes PDF conversion
2. **Fast Docs** (~20 min) - ~109 markdown files
3. **Pydantic Docs** (~30 min) - ~270 markdown files
4. **Inngest Ecosystem** (~40 min) - ~295 markdown files

### Option B: By Priority
1. **Viator API** - If you need this for production first
2. **Inngest Ecosystem** - Most complex structure
3. **Fast Docs** - Important framework docs
4. **Pydantic Docs** - Library documentation

---

## 📊 Summary Table

| Collection | Script | Files | Subdirs | Est. Chunks | Est. Time | PDF Conversion |
|------------|--------|-------|---------|-------------|-----------|----------------|
| **viator_api** | `kaggle_process_viator.py` | 4 | 3 | ~1,000 | 10 min | ✅ Yes (Docling) |
| **fast_docs** | `kaggle_process_fast_docs.py` | ~109 | 3 | ~3,000 | 20 min | ❌ No (markdown only) |
| **pydantic_docs** | `kaggle_process_pydantic_docs.py` | ~270 | 0 | ~7,000 | 30 min | ❌ No (markdown only) |
| **inngest_ecosystem** | `kaggle_process_inngest_ecosystem.py` | ~295 | 6 | ~8,000 | 40 min | ❌ No (markdown only) |

---

## 🔧 Common Issues & Solutions

### Issue 1: NumPy 2.x Error
**Error:** `ufunc 'cos' not supported for the input types`

**Solution:**
```python
!pip install -q --force-reinstall "numpy==1.26.4" "scipy==1.11.4" "scikit-learn==1.4.2"
# Restart runtime after this
```

### Issue 2: CUDA Out of Memory
**Error:** `CUDA out of memory`

**Solution:**
- All scripts already use `device_map="auto"` + FP16
- If still failing, reduce `BATCH_SIZE` in script from 8 to 4

### Issue 3: Chunk Key Mismatch
**Error:** `KeyError: 'text'` or `KeyError: 'content'`

**Solution:**
- All scripts handle both `chunk.get('text')` and `chunk.get('content')`
- This is already fixed in all consolidated scripts

### Issue 4: Download Not Showing
**Problem:** ZIP file created but not in Kaggle Output tab

**Solution:**
```python
# Use Kaggle's display function
from IPython.display import FileLink
FileLink('viator_api_embeddings.zip')
```

---

## 📥 After Processing - Local Upload to Qdrant

Once you download the embeddings from Kaggle:

### Upload Script:
```bash
python scripts/upload_to_qdrant.py \
    --collection viator_api \
    --file output/viator_api/embeddings/viator_api_embeddings.jsonl \
    --mode replace
```

### Upload Modes:
- **`upsert`** - Update existing points, insert new ones (recommended for first upload)
- **`skip`** - Skip files already in collection (fast for partial updates)
- **`replace`** - Delete old data from source, insert fresh (use for viator_api restructure)

### Upload All Collections:
```bash
# Viator API (replace old flat structure)
python scripts/upload_to_qdrant.py --collection viator_api --file output/viator_api/embeddings/viator_api_embeddings.jsonl --mode replace

# Fast Docs (first upload)
python scripts/upload_to_qdrant.py --collection fast_docs --file output/fast_docs/embeddings/fast_docs_embeddings.jsonl --mode upsert

# Pydantic Docs (first upload)
python scripts/upload_to_qdrant.py --collection pydantic_docs --file output/pydantic_docs/embeddings/pydantic_docs_embeddings.jsonl --mode upsert

# Inngest Ecosystem (first upload)
python scripts/upload_to_qdrant.py --collection inngest_ecosystem --file output/inngest_ecosystem/embeddings/inngest_ecosystem_embeddings.jsonl --mode upsert
```

---

## ✅ Verification Checklist

After processing each collection:

- [ ] Check JSONL file size (should be several hundred MB)
- [ ] Verify chunk count matches expectations
- [ ] Check for unique IDs (scripts print conflict count - should be 0)
- [ ] Confirm embedding dimension is 768
- [ ] Download ZIP from Kaggle
- [ ] Upload to local Qdrant
- [ ] Test semantic search on collection

---

## 🎯 GPU Utilization Verification

**All scripts print GPU info at startup:**
```
GPU SETUP
============================================================
CUDA available: True
GPU count: 2
GPU 0: Tesla T4
  Memory: 16.00 GB
GPU 1: Tesla T4
  Memory: 16.00 GB
============================================================

✓ Model loaded across 2 GPUs with automatic device mapping
```

**How to verify BOTH GPUs are being used:**

During processing, run this in a separate cell:
```python
!nvidia-smi
```

You should see:
- GPU 0: ~13GB used (model layers)
- GPU 1: ~13GB used (model layers)
- Total: ~26GB distributed across 2 GPUs

---

## 📞 Need Help?

- **Script errors:** Check the error section above
- **GPU issues:** Verify `nvidia-smi` shows 2 GPUs
- **Slow processing:** Check GPU utilization with `nvidia-smi`
- **Memory errors:** Reduce `BATCH_SIZE` in script

Good luck with your processing! 🚀
