import os
os.environ['TORCHDYNAMO_DISABLE'] = '1'
os.environ['TORCHINDUCTOR_FORCE_DISABLE_CACHES'] = '1'

print("Testing simpler model...")
from sentence_transformers import SentenceTransformer
print("SentenceTransformer imported")

# Try a simpler model first
model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
print("Simple model loaded")

test_text = "Hello world"
embedding = model.encode(test_text)
print(f"Test embedding shape: {embedding.shape}")
print("Simple model test completed")