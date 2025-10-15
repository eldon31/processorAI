import os
import time

os.environ.setdefault("TORCHDYNAMO_DISABLE", "1")
os.environ.setdefault("TORCHINDUCTOR_FORCE_DISABLE_CACHES", "1")

print("Testing nomic-ai/nomic-embed-code load")
start = time.time()

try:
    from sentence_transformers import SentenceTransformer
    print("SentenceTransformer imported", time.time() - start)
    model = SentenceTransformer(
        "nomic-ai/nomic-embed-code",
        trust_remote_code=True,
        device="cpu",
    )
    print("Model loaded", time.time() - start)
    vector = model.encode("quick smoke test", convert_to_numpy=True)
    print("Embedding shape", vector.shape)
    print("Embedding preview", vector[:10])
except Exception as exc:
    print("Failure:", exc)
