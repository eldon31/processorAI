"""Embed a single chunk directly using sentence-transformers.

Usage:
    python scripts/embed_single_chunk_direct.py [chunk_index]

If no index is provided, chunk 0 is used.
"""

import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("Embedding single chunk with sentence-transformers...")

# Load the chunked data
chunks_file = Path("output/chunks/apps_docling_chunks.json")

if not chunks_file.exists():
    print(f"ERROR: Chunks file not found: {chunks_file}")
    sys.exit(1)

with open(chunks_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

chunks = data.get('chunks', [])
if not chunks:
    print("ERROR: No chunks found in the file")
    sys.exit(1)

chunk_index = int(sys.argv[1]) if len(sys.argv) > 1 else 0

if chunk_index < 0 or chunk_index >= len(chunks):
    print(f"ERROR: Chunk index {chunk_index} out of range (0-{len(chunks)-1})")
    sys.exit(1)

chunk = chunks[chunk_index]
text = chunk.get('text', '')
char_count = len(text)
token_count = chunk.get('token_count', 0)

print(f"Chunk {chunk_index}: {char_count} chars, {token_count} tokens")
preview = text[:200].replace('\n', ' ')
print(f"Preview: {preview}...")

# Load sentence-transformers model
print("\nLoading sentence-transformers model...")
try:
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("nomic-ai/nomic-embed-code", trust_remote_code=True, device="cpu")
    print("Model loaded successfully")
except Exception as e:
    print(f"ERROR loading model: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Embed the chunk
print("\nEmbedding chunk...")
try:
    embedding = model.encode(text, show_progress_bar=False)
    print("Embedding generated successfully")
    print(f"Dimension: {len(embedding)}")
    print(f"First 10 values: {embedding[:10]}")
except Exception as e:
    print(f"ERROR embedding chunk: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nDone!")