#!/usr/bin/env python3
"""
Quick Reference: Kaggle Processing Scripts
Copy-paste these commands directly into Kaggle notebooks
"""

# ============================================================================
# COLLECTION 1: VIATOR API (PDF + JSON → Embeddings)
# ============================================================================

# --- CELL 1: Install Dependencies (Viator - includes Docling for PDF) ---
"""
!pip install -q --force-reinstall "numpy==1.26.4" "scipy==1.11.4" "scikit-learn==1.4.2"
!pip install -q docling docling-core transformers accelerate torch sentencepiece
"""

# --- CELL 2: Run Processing ---
"""
!python scripts/kaggle_process_viator.py
"""

# --- CELL 3: Download Embeddings ---
"""
!zip -r viator_api_embeddings.zip output/viator_api/embeddings/
from IPython.display import FileLink
FileLink('viator_api_embeddings.zip')
"""

# ============================================================================
# COLLECTION 2: FAST DOCS (Markdown → Embeddings)
# ============================================================================

# --- CELL 1: Install Dependencies (No PDF conversion needed) ---
"""
!pip install -q --force-reinstall "numpy==1.26.4" "scipy==1.11.4" "scikit-learn==1.4.2"
!pip install -q transformers accelerate torch sentencepiece
"""

# --- CELL 2: Run Processing ---
"""
!python scripts/kaggle_process_fast_docs.py
"""

# --- CELL 3: Download Embeddings ---
"""
!zip -r fast_docs_embeddings.zip output/fast_docs/embeddings/
from IPython.display import FileLink
FileLink('fast_docs_embeddings.zip')
"""

# ============================================================================
# COLLECTION 3: PYDANTIC DOCS (Markdown → Embeddings)
# ============================================================================

# --- CELL 1: Install Dependencies ---
"""
!pip install -q --force-reinstall "numpy==1.26.4" "scipy==1.11.4" "scikit-learn==1.4.2"
!pip install -q transformers accelerate torch sentencepiece
"""

# --- CELL 2: Run Processing ---
"""
!python scripts/kaggle_process_pydantic_docs.py
"""

# --- CELL 3: Download Embeddings ---
"""
!zip -r pydantic_docs_embeddings.zip output/pydantic_docs/embeddings/
from IPython.display import FileLink
FileLink('pydantic_docs_embeddings.zip')
"""

# ============================================================================
# COLLECTION 4: INNGEST ECOSYSTEM (Markdown → Embeddings)
# ============================================================================

# --- CELL 1: Install Dependencies ---
"""
!pip install -q --force-reinstall "numpy==1.26.4" "scipy==1.11.4" "scikit-learn==1.4.2"
!pip install -q transformers accelerate torch sentencepiece
"""

# --- CELL 2: Run Processing ---
"""
!python scripts/kaggle_process_inngest_ecosystem.py
"""

# --- CELL 3: Download Embeddings ---
"""
!zip -r inngest_ecosystem_embeddings.zip output/inngest_ecosystem/embeddings/
from IPython.display import FileLink
FileLink('inngest_ecosystem_embeddings.zip')
"""

# ============================================================================
# VERIFICATION: Check GPU Usage During Processing
# ============================================================================

# --- Run in separate cell while processing ---
"""
!nvidia-smi
"""

# Expected output:
# GPU 0: ~13GB used (Tesla T4)
# GPU 1: ~13GB used (Tesla T4)
# Total: ~26GB model distributed across 2 GPUs

# ============================================================================
# TROUBLESHOOTING
# ============================================================================

# If you get NumPy 2.x error:
"""
!pip install -q --force-reinstall "numpy==1.26.4" "scipy==1.11.4" "scikit-learn==1.4.2"
# Then restart runtime: Runtime → Restart Runtime
"""

# If CUDA out of memory (unlikely with device_map="auto"):
"""
# Edit script and change:
# BATCH_SIZE = 8  →  BATCH_SIZE = 4
"""

# If download not showing in Output tab:
"""
from IPython.display import FileLink
FileLink('your_embeddings.zip')
"""
