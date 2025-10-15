import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Any
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set environment variables to prevent PyTorch issues
os.environ['TORCHDYNAMO_DISABLE'] = '1'
os.environ['TORCHINDUCTOR_FORCE_DISABLE_CACHES'] = '1'

class ChunkEmbedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", device: str = "cpu"):
        self.model_name = model_name
        self.device = device
        self.model = None
        self._load_model()

    def _load_model(self):
        """Load the sentence transformer model"""
        try:
            logger.info(f"Loading model: {self.model_name}")
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(self.model_name, device=self.device)
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model {self.model_name}: {e}")
            raise

    def embed_chunk(self, chunk: Dict[str, Any]) -> Dict[str, Any]:
        """Embed a single chunk and return enriched chunk data"""
        try:
            if self.model is None:
                raise RuntimeError("Model not loaded")

            text = chunk['text']
            if not text or not text.strip():
                logger.warning(f"Empty text in chunk {chunk.get('index', 'unknown')}")
                return {**chunk, 'embedding': None, 'embedding_error': 'empty_text'}

            logger.debug(f"Embedding chunk {chunk.get('index', 'unknown')} (chars: {chunk.get('char_count', 0)})")

            # Generate embedding
            embedding = self.model.encode(text, convert_to_numpy=True).tolist()

            return {
                **chunk,
                'embedding': embedding,
                'embedding_model': self.model_name,
                'embedding_dimension': len(embedding)
            }

        except Exception as e:
            logger.error(f"Failed to embed chunk {chunk.get('index', 'unknown')}: {e}")
            return {**chunk, 'embedding': None, 'embedding_error': str(e)}

class ChunkProcessor:
    def __init__(self, embedder: ChunkEmbedder, max_workers: int = 4):
        self.embedder = embedder
        self.max_workers = max_workers

    def process_chunks_parallel(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process chunks in parallel using thread pool"""
        logger.info(f"Processing {len(chunks)} chunks with {self.max_workers} workers")

        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all embedding tasks
            future_to_chunk = {
                executor.submit(self.embedder.embed_chunk, chunk): chunk
                for chunk in chunks
            }

            # Collect results as they complete
            for future in as_completed(future_to_chunk):
                chunk = future_to_chunk[future]
                try:
                    result = future.result()
                    results.append(result)

                    # Log progress
                    success = result.get('embedding') is not None
                    status = "SUCCESS" if success else "FAILED"
                    logger.info(f"Chunk {result.get('index', 'unknown')}: {status}")

                except Exception as e:
                    logger.error(f"Unexpected error processing chunk {chunk.get('index', 'unknown')}: {e}")
                    results.append({**chunk, 'embedding': None, 'embedding_error': str(e)})

        return results

    def process_chunks_sequential(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process chunks sequentially for debugging"""
        logger.info(f"Processing {len(chunks)} chunks sequentially")

        results = []
        for i, chunk in enumerate(chunks):
            logger.info(f"Processing chunk {i+1}/{len(chunks)}")
            result = self.embedder.embed_chunk(chunk)
            results.append(result)

            success = result.get('embedding') is not None
            status = "SUCCESS" if success else "FAILED"
            logger.info(f"Chunk {result.get('index', 'unknown')}: {status}")

        return results

def load_chunks_from_file(file_path: str) -> List[Dict[str, Any]]:
    """Load chunks from JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if 'chunks' in data:
            logger.info(f"Loaded {len(data['chunks'])} chunks from {file_path}")
            return data['chunks']
        else:
            logger.error(f"No 'chunks' key found in {file_path}")
            return []

    except Exception as e:
        logger.error(f"Failed to load chunks from {file_path}: {e}")
        return []

def save_embedded_chunks(chunks: List[Dict[str, Any]], output_path: str):
    """Save embedded chunks to JSON file"""
    try:
        # Create output directory if it doesn't exist
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'embedded_chunks': chunks,
                'total_chunks': len(chunks),
                'successful_embeddings': sum(1 for c in chunks if c.get('embedding') is not None),
                'failed_embeddings': sum(1 for c in chunks if c.get('embedding') is None)
            }, f, indent=2, ensure_ascii=False)

        logger.info(f"Saved embedded chunks to {output_path}")

    except Exception as e:
        logger.error(f"Failed to save embedded chunks to {output_path}: {e}")

def main():
    # Configuration
    chunks_dir = Path("output/chunks")
    input_file = chunks_dir / "apps_docling_chunks.json"
    output_file = chunks_dir / "embedded_chunks.json"

    # Use working model instead of problematic nomic model
    model_name = "all-MiniLM-L6-v2"  # 384 dimensions, works reliably
    max_workers = 2  # Conservative number for CPU
    use_parallel = True

    logger.info("Starting chunk embedding process")
    logger.info(f"Input: {input_file}")
    logger.info(f"Output: {output_file}")
    logger.info(f"Model: {model_name}")
    logger.info(f"Parallel processing: {use_parallel} (workers: {max_workers})")

    # Load chunks
    chunks = load_chunks_from_file(str(input_file))
    if not chunks:
        logger.error("No chunks loaded, exiting")
        sys.exit(1)

    # Initialize embedder
    try:
        embedder = ChunkEmbedder(model_name=model_name)
    except Exception as e:
        logger.error(f"Failed to initialize embedder: {e}")
        sys.exit(1)

    # Initialize processor
    processor = ChunkProcessor(embedder, max_workers=max_workers)

    # Process chunks
    if use_parallel:
        embedded_chunks = processor.process_chunks_parallel(chunks)
    else:
        embedded_chunks = processor.process_chunks_sequential(chunks)

    # Save results
    save_embedded_chunks(embedded_chunks, str(output_file))

    # Summary
    successful = sum(1 for c in embedded_chunks if c.get('embedding') is not None)
    failed = len(embedded_chunks) - successful

    logger.info("Embedding process completed")
    logger.info(f"Total chunks: {len(embedded_chunks)}")
    logger.info(f"Successful embeddings: {successful}")
    logger.info(f"Failed embeddings: {failed}")

    if failed > 0:
        logger.warning("Some chunks failed to embed. Check the output file for details.")

if __name__ == "__main__":
    main()