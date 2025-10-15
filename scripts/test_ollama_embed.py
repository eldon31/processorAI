import os
from typing import Any, Dict, List, Optional

import httpx

try:  # Optional dependency so we can still run without the pip package.
    from ollama import Client as OllamaClient  # type: ignore
except ImportError:  # pragma: no cover - best effort import guard
    OllamaClient = None  # type: ignore[assignment]


def embed_with_httpx(host: str, model: str, inputs: List[str], options: Optional[Dict[str, int]]) -> List[List[float]]:
    url = f"{host.rstrip('/')}/api/embed"
    payload: Dict[str, Any] = {"model": model, "input": inputs}
    if options:
        payload["options"] = options

    with httpx.Client(timeout=120) as client:
        response = client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

    if "embeddings" not in data:
        raise RuntimeError(f"Unexpected response keys: {list(data.keys())}")

    return data["embeddings"]


def embed_with_native_client(host: str, model: str, inputs: List[str], options: Optional[Dict[str, int]]) -> List[List[float]]:
    if OllamaClient is None:
        raise RuntimeError("ollama.Client is unavailable; install the ollama package to use this path.")

    client = OllamaClient(host=host)
    vectors: List[List[float]] = []

    for text in inputs:
        payload: Dict[str, Any] = {"model": model, "prompt": text}
        if options:
            payload["options"] = options

        response = client.embeddings(**payload)
        if "embedding" not in response:
            raise RuntimeError(f"Unexpected response keys: {list(response.keys())}")

        vectors.append(response["embedding"])

    return vectors


def main() -> None:
    host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    model = os.environ.get("OLLAMA_MODEL", "manutic/nomic-embed-code:latest")
    options = {
        # Reduce batch and context to avoid ggml asserts on Windows builds that over-allocate buffers.
        "num_ctx": int(os.environ.get("OLLAMA_NUM_CTX", "2048")),
        "batch": int(os.environ.get("OLLAMA_BATCH", "128")),
        "num_thread": int(os.environ.get("OLLAMA_NUM_THREAD", "2")),
    }
    # Allow empty options if callers explicitly disable them via env.
    if os.environ.get("OLLAMA_DISABLE_OPTIONS", "0") == "1":
        options = {}

    sample_inputs = [
        "Inngest apps map directly to your projects or services.",
        "Deployment details for Inngest app environments.",
    ]

    print(f"Requesting embeddings from {host} using model '{model}'")
    use_native_client = os.environ.get("OLLAMA_USE_CLIENT", "1") != "0"
    try:
        if use_native_client:
            embeddings = embed_with_native_client(host, model, sample_inputs, options)
        else:
            raise RuntimeError("Native client disabled via OLLAMA_USE_CLIENT=0")
    except Exception as client_error:
        print(f"Native client path failed: {client_error}. Falling back to raw HTTP...")
        try:
            embeddings = embed_with_httpx(host, model, sample_inputs, options)
        except httpx.HTTPStatusError as exc:
            print(f"HTTP error: {exc.response.status_code} {exc.response.text}")
            raise

    for idx, vector in enumerate(embeddings):
        print(f"Input {idx}: received vector of length {len(vector)}")

    print("Sample (first 5 values):", embeddings[0][:5])


if __name__ == "__main__":
    main()
