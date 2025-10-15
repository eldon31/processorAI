#!/usr/bin/env python3
"""
Quick Reference: Kaggle Processing Scripts
Copy-paste these commands directly into Kaggle notebooks

NOTE: All embeddings are saved directly to /kaggle/working/ 
      and will appear in the Output tab automatically!
"""

# ============================================================================
# COLLECTION 1: VIATOR API (Pre-chunked JSON → Embeddings)
# ============================================================================

# --- CELL 1: Install Dependencies (Viator - NO PDF conversion needed) ---
"""
!pip install -q --force-reinstall "numpy==1.26.4" "scipy==1.11.4" "scikit-learn==1.4.2"
!pip install -q transformers accelerate torch sentencepiece
"""

# --- CELL 2: Run Processing ---
"""
!python scripts/kaggle_process_viator.py
"""

# Output: /kaggle/working/viator_api_embeddings.jsonl (appears in Output tab)

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

# Output: /kaggle/working/fast_docs_embeddings.jsonl (appears in Output tab)

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

# Output: /kaggle/working/pydantic_docs_embeddings.jsonl (appears in Output tab)

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

# Output: /kaggle/working/inngest_ecosystem_embeddings.jsonl (appears in Output tab)

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

# If CUDA out of memory (unlikely with dual-GPU setup):
"""
# Edit script and change:
# BATCH_SIZE = 8  →  BATCH_SIZE = 4
"""

# ============================================================================
# MOVE EXISTING EMBEDDINGS TO /kaggle/working/ (if already processed)
# ============================================================================

# If you already ran scripts and embeddings are in output/ folders:
"""
!cp output/viator_api/embeddings/viator_api_embeddings.jsonl /kaggle/working/
!cp output/fast_docs/embeddings/fast_docs_embeddings.jsonl /kaggle/working/
!cp output/pydantic_docs/embeddings/pydantic_docs_embeddings.jsonl /kaggle/working/
!cp output/inngest_ecosystem/embeddings/inngest_ecosystem_embeddings.jsonl /kaggle/working/
"""

# Or move all at once:
"""
!find output -name "*_embeddings.jsonl" -exec cp {{}} /kaggle/working/ \\;
"""

# Files will now appear in Output tab for easy download!
