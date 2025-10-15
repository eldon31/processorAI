"""
Background Worker for Document Processing.

Monitors a queue or directory for new documents and processes them
using the document ingestion pipeline.

This is a simple implementation that can be extended with:
- Redis queue for distributed processing
- Celery for advanced task management
- File system watcher for automatic ingestion
"""

import asyncio
import os
import time
from pathlib import Path
from typing import Optional

from src.ingestion.ingest import DocumentIngestionPipeline, IngestionConfig
from src.config.providers import ProviderConfig
from src.storage.chroma_client import initialize_chroma, close_chroma
from src.graph.graph_client import _get_global_client as get_graph_client


class DocumentWorker:
    """
    Background worker for document processing.
    
    Monitors the uploads directory and processes any new documents.
    """
    
    def __init__(
        self,
        watch_dir: str = "uploads",
        processed_dir: str = "processed",
        poll_interval: int = 5,
    ):
        """
        Initialize document worker.
        
        Args:
            watch_dir: Directory to watch for new documents
            processed_dir: Directory to move processed documents
            poll_interval: Seconds between directory checks
        """
        self.watch_dir = Path(watch_dir)
        self.processed_dir = Path(processed_dir)
        self.poll_interval = poll_interval
        
        # Create directories if they don't exist
        self.watch_dir.mkdir(exist_ok=True)
        self.processed_dir.mkdir(exist_ok=True)
        
        # Initialize ingestion pipeline
        config = IngestionConfig(
            chunk_size=512,
            chunk_overlap=50,
            max_chunk_size=1000,
            use_semantic_chunking=True,
            extract_knowledge_graph=True,
        )
        self.pipeline = DocumentIngestionPipeline(config)
        
        print(f"Worker initialized:")
        print(f"  - Watch directory: {self.watch_dir.absolute()}")
        print(f"  - Processed directory: {self.processed_dir.absolute()}")
        print(f"  - Poll interval: {self.poll_interval}s")
    
    async def process_file(self, file_path: Path) -> bool:
        """
        Process a single document file.
        
        Args:
            file_path: Path to document file
            
        Returns:
            True if processing succeeded, False otherwise
        """
        try:
            print(f"\n{'='*60}")
            print(f"Processing: {file_path.name}")
            print(f"{'='*60}")
            
            # Initialize pipeline if needed
            await self.pipeline.initialize()
            
            # Process document
            result = await self.pipeline.ingest_documents([str(file_path)])
            
            # Get first result (we only processed one file)
            if result and len(result) > 0:
                doc_result = result[0]
            
                print(f"\n✓ Document processed successfully!")
                print(f"  - Chunks created: {doc_result.chunks_created}")
                print(f"  - Entities extracted: {doc_result.entities_extracted}")
                print(f"  - Relationships extracted: {doc_result.relationships_created}")
                print(f"  - Processing time: {doc_result.processing_time_ms / 1000:.2f}s")
                
                if doc_result.errors:
                    print(f"  ⚠ Errors encountered: {len(doc_result.errors)}")
                    for error in doc_result.errors[:3]:  # Show first 3 errors
                        print(f"    - {error}")
            else:
                print(f"\n✗ No results returned from ingestion pipeline")
            
            # Move to processed directory
            processed_path = self.processed_dir / file_path.name
            file_path.rename(processed_path)
            print(f"  → Moved to: {processed_path}")
            
            return True
            
        except Exception as e:
            print(f"\n✗ Error processing {file_path.name}: {e}")
            
            # Move to error directory
            error_dir = self.processed_dir / "errors"
            error_dir.mkdir(exist_ok=True)
            error_path = error_dir / file_path.name
            file_path.rename(error_path)
            print(f"  → Moved to: {error_path}")
            
            return False
    
    async def run(self):
        """
        Run the worker loop.
        
        Continuously monitors the watch directory for new documents.
        """
        print("\n" + "="*60)
        print("Document Worker Started")
        print("="*60)
        print(f"Watching: {self.watch_dir.absolute()}")
        print(f"Press Ctrl+C to stop\n")
        
        # Initialize services
        print("Initializing services...")
        await initialize_chroma()
        graph_client = get_graph_client()
        print("✓ Services initialized\n")
        
        try:
            while True:
                # Get all files in watch directory
                files = [
                    f for f in self.watch_dir.iterdir()
                    if f.is_file() and not f.name.startswith('.')
                ]
                
                if files:
                    print(f"Found {len(files)} file(s) to process")
                    
                    # Process each file
                    for file_path in files:
                        await self.process_file(file_path)
                
                # Wait before next check
                await asyncio.sleep(self.poll_interval)
                
        except KeyboardInterrupt:
            print("\n\nShutting down worker...")
            
        finally:
            # Clean up
            await close_chroma()
            print("✓ Services closed")
            print("Worker stopped")


async def main():
    """Main entry point for worker."""
    # Get configuration from environment
    watch_dir = os.getenv("WORKER_WATCH_DIR", "uploads")
    processed_dir = os.getenv("WORKER_PROCESSED_DIR", "processed")
    poll_interval = int(os.getenv("WORKER_POLL_INTERVAL", "5"))
    
    # Create and run worker
    worker = DocumentWorker(
        watch_dir=watch_dir,
        processed_dir=processed_dir,
        poll_interval=poll_interval,
    )
    
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
