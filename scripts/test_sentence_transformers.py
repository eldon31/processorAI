"""
Test sentence-transformers with nomic-embed-code
Verify the model loads correctly
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("Testing sentence-transformers with nomic-embed-code...")
print("=" * 70)

# Test 1: Direct sentence-transformers
print("\n1. Testing direct sentence-transformers import...")
try:
    from sentence_transformers import SentenceTransformer
    print("   OK sentence_transformers imported successfully")
except Exception as e:
    print(f"   ERROR: {e}")
    sys.exit(1)

# Test 2: Load nomic-embed-code model
print("\n2. Loading nomic-ai/nomic-embed-code model...")
print("   (Code-specific embeddings for documentation and APIs)")
try:
    cache_dir = Path(__file__).parent.parent / ".cache" / "nomic-embed-code"
    cache_dir.mkdir(parents=True, exist_ok=True)
    model = SentenceTransformer(
        "nomic-ai/nomic-embed-code",
        trust_remote_code=True,
        cache_folder=str(cache_dir)
    )
    print("   OK Model loaded successfully")
    print(f"   DIMENSION: {model.get_sentence_embedding_dimension()}")
except Exception as e:
    print(f"   ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Generate test embedding
print("\n3. Generating test embedding...")
try:
    test_text = "This is a test sentence for embedding"
    embedding = model.encode(test_text, show_progress_bar=False)
    print("   OK Embedding generated")
    print(f"   SHAPE: {embedding.shape}")
    print(f"   SAMPLE VALUES: {embedding[:5]}")
except Exception as e:
    print(f"   ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Batch encoding
print("\n4. Testing batch encoding...")
try:
    test_texts = [
        "First document about Python programming",
        "Second document about machine learning",
        "Third document about web development"
    ]
    embeddings = model.encode(test_texts, show_progress_bar=True, batch_size=2)
    print("   OK Batch encoding successful")
    print(f"   SHAPE: {embeddings.shape}")
    print(f"   GENERATED {len(embeddings)} embeddings of dimension {embeddings.shape[1]}")
except Exception as e:
    print(f"   ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 70)
print("ALL TESTS PASSED!")
print("=" * 70)
print("\nsentence-transformers is working correctly")
print("   You can now use it for embedding your documents")
