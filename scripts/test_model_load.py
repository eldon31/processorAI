import os
os.environ['TORCHDYNAMO_DISABLE'] = '1'
os.environ['TORCHINDUCTOR_FORCE_DISABLE_CACHES'] = '1'

print("Starting model load...")
from sentence_transformers import SentenceTransformer
print("SentenceTransformer imported")

model = SentenceTransformer("nomic-ai/nomic-embed-code", trust_remote_code=True, device="cpu")
print("Model loaded successfully")

# Test encoding
test_text = "Hello world"
embedding = model.encode(test_text)
print(f"Test embedding shape: {embedding.shape}")
print("Model test completed")