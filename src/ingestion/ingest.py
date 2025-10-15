"""
Ingestion pipeline for processing documents into Chroma vector DB and Neo4j knowledge graph.

Orchestrates: Docling → HybridChunker → Embedder → Chroma + Neo4j (Graphiti)
"""

import os
import asyncio
import logging
import json
import glob
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import argparse

from pydantic import BaseModel, Field

from .chunker import ChunkingConfig, create_chunker, DocumentChunk
from .embedder import create_embedder
from .processor import DocumentProcessor
from ..storage.chroma_client import get_chroma_client, initialize_chroma, close_chroma
from ..models.document import Document, ProcessingStatus

logger = logging.getLogger(__name__)


class IngestionConfig(BaseModel):
    """Configuration for document ingestion pipeline."""
    
    chunk_size: int = Field(default=1000, ge=100, le=2000)
    chunk_overlap: int = Field(default=200, ge=0, le=500)
    max_chunk_size: int = Field(default=1500, ge=500, le=3000)
    use_semantic_chunking: bool = Field(default=True)


class IngestionResult(BaseModel):
    """Result of ingesting a single document."""
    
    document_id: str
    title: str
    chunks_created: int
    processing_time_ms: float
    errors: List[str] = Field(default_factory=list)


class DocumentIngestionPipeline:
    """Pipeline for ingesting documents into Chroma vector DB and Neo4j knowledge graph."""
    
    def __init__(
        self,
        config: IngestionConfig,
        documents_folder: str = "documents",
        clean_before_ingest: bool = True
    ):
        """
        Initialize ingestion pipeline.

        Args:
            config: Ingestion configuration
            documents_folder: Folder containing documents to ingest
            clean_before_ingest: Whether to clean existing data before ingestion
        """
        self.config = config
        self.documents_folder = documents_folder
        self.clean_before_ingest = clean_before_ingest
        
        # Initialize components
        self.chunker_config = ChunkingConfig(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            max_chunk_size=config.max_chunk_size,
            use_semantic_splitting=config.use_semantic_chunking
        )
        
        self.chunker = create_chunker(self.chunker_config)
        self.embedder = create_embedder()
        self.processor = DocumentProcessor()
        
        self._initialized = False
    
    async def initialize(self):
        """Initialize database connections."""
        if self._initialized:
            return
        
        logger.info("Initializing ingestion pipeline...")
        
        # Initialize Chroma
        await initialize_chroma()
        
        self._initialized = True
        logger.info("Ingestion pipeline initialized")
    
    async def close(self):
        """Close database connections."""
        if self._initialized:
            await close_chroma()
            self._initialized = False
    
    async def ingest_documents(
        self,
        progress_callback: Optional[callable] = None
    ) -> List[IngestionResult]:
        """
        Ingest all documents from the documents folder.
        
        Args:
            progress_callback: Optional callback for progress updates
        
        Returns:
            List of ingestion results
        """
        if not self._initialized:
            await self.initialize()
        
        # Clean existing data if requested
        if self.clean_before_ingest:
            await self._clean_databases()
        
        # Find all supported document files
        document_files = self._find_document_files()

        if not document_files:
            logger.warning(f"No supported document files found in {self.documents_folder}")
            return []

        logger.info(f"Found {len(document_files)} document files to process")

        results = []

        for i, file_path in enumerate(document_files):
            try:
                logger.info(f"Processing file {i+1}/{len(document_files)}: {file_path}")

                result = await self._ingest_single_document(file_path)
                results.append(result)

                if progress_callback:
                    progress_callback(i + 1, len(document_files))
                
            except Exception as e:
                logger.error(f"Failed to process {file_path}: {e}")
                results.append(IngestionResult(
                    document_id="",
                    title=os.path.basename(file_path),
                    chunks_created=0,
                    entities_extracted=0,
                    relationships_created=0,
                    processing_time_ms=0,
                    errors=[str(e)]
                ))
        
        # Log summary
        total_chunks = sum(r.chunks_created for r in results)
        total_entities = sum(r.entities_extracted for r in results)
        total_relationships = sum(r.relationships_created for r in results)
        total_errors = sum(len(r.errors) for r in results)
        
        logger.info(
            f"Ingestion complete: {len(results)} documents, {total_chunks} chunks, "
            f"{total_entities} entities, {total_relationships} relationships, {total_errors} errors"
        )
        
        return results
    
    async def _ingest_single_document(self, file_path: str) -> IngestionResult:
        """
        Ingest a single document.

        Args:
            file_path: Path to the document file

        Returns:
            Ingestion result
        """
        start_time = datetime.now()

        # Read document (returns tuple: content, docling_doc)
        document_content, docling_doc = self._read_document(file_path)
        document_title = self._extract_title(document_content, file_path)
        document_source = os.path.relpath(file_path, self.documents_folder)

        # Extract metadata from content
        document_metadata = self._extract_document_metadata(document_content, file_path)

        logger.info(f"Processing document: {document_title}")

        # Chunk the document - pass DoclingDocument for HybridChunker
        chunks = await self.chunker.chunk_document(
            content=document_content,
            title=document_title,
            source=document_source,
            metadata=document_metadata,
            docling_doc=docling_doc  # Pass DoclingDocument for HybridChunker
        )
        
        if not chunks:
            logger.warning(f"No chunks created for {document_title}")
            return IngestionResult(
                document_id="",
                title=document_title,
                chunks_created=0,
                entities_extracted=0,
                relationships_created=0,
                processing_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
                errors=["No chunks created"]
            )
        
        logger.info(f"Created {len(chunks)} chunks")
        
        # Generate embeddings
        embedded_chunks = await self.embedder.embed_chunks(chunks)
        logger.info(f"Generated embeddings for {len(embedded_chunks)} chunks")
        
        # Save to Chroma
        document_id = await self._save_to_chroma(
            document_title,
            document_source,
            document_content,
            embedded_chunks,
            document_metadata
        )
        
        logger.info(f"Saved document to Chroma with ID: {document_id}")
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return IngestionResult(
            document_id=document_id,
            title=document_title,
            chunks_created=len(chunks),
            processing_time_ms=processing_time,
        )
    
    def _find_document_files(self) -> List[str]:
        """Find all supported document files in the documents folder."""
        if not os.path.exists(self.documents_folder):
            logger.error(f"Documents folder not found: {self.documents_folder}")
            return []

        # Supported file patterns - Docling + text formats + audio
        patterns = [
            "*.md", "*.markdown", "*.txt",  # Text formats
            "*.pdf",  # PDF
            "*.docx", "*.doc",  # Word
            "*.pptx", "*.ppt",  # PowerPoint
            "*.xlsx", "*.xls",  # Excel
            "*.html", "*.htm",  # HTML
            "*.mp3", "*.wav", "*.m4a", "*.flac",  # Audio formats
        ]
        files = []

        for pattern in patterns:
            files.extend(glob.glob(os.path.join(self.documents_folder, "**", pattern), recursive=True))

        return sorted(files)
    
    def _read_document(self, file_path: str) -> tuple[str, Optional[Any]]:
        """
        Read document content from file using DocumentProcessor.

        Returns:
            Tuple of (markdown_content, docling_document)
            docling_document is None for text files and audio files
        """
        try:
            # Use DocumentProcessor for unified multi-format support
            processed_doc = self.processor.process_file(file_path)
            
            # Return content and Docling document (if available for hybrid chunking)
            return (processed_doc.content, processed_doc.docling_document)
            
        except Exception as e:
            logger.error(f"Failed to process {file_path}: {e}")
            # Return error placeholder
            return (f"[Error: Could not read file {os.path.basename(file_path)}]", None)

    def _extract_title(self, content: str, file_path: str) -> str:
        """Extract title from document content or filename."""
        # Try to find markdown title
        lines = content.split('\n')
        for line in lines[:10]:  # Check first 10 lines
            line = line.strip()
            if line.startswith('# '):
                return line[2:].strip()
        
        # Fallback to filename
        return os.path.splitext(os.path.basename(file_path))[0]
    
    def _extract_document_metadata(self, content: str, file_path: str) -> Dict[str, Any]:
        """Extract metadata from document content."""
        metadata = {
            "file_path": file_path,
            "file_size": len(content),
            "ingestion_date": datetime.now().isoformat()
        }
        
        # Try to extract YAML frontmatter
        if content.startswith('---'):
            try:
                import yaml
                end_marker = content.find('\n---\n', 4)
                if end_marker != -1:
                    frontmatter = content[4:end_marker]
                    yaml_metadata = yaml.safe_load(frontmatter)
                    if isinstance(yaml_metadata, dict):
                        metadata.update(yaml_metadata)
            except ImportError:
                logger.warning("PyYAML not installed, skipping frontmatter extraction")
            except Exception as e:
                logger.warning(f"Failed to parse frontmatter: {e}")
        
        # Extract some basic metadata from content
        lines = content.split('\n')
        metadata['line_count'] = len(lines)
        metadata['word_count'] = len(content.split())
        
        return metadata
    
    async def _save_to_chroma(
        self,
        title: str,
        source: str,
        content: str,
        chunks: List[DocumentChunk],
        metadata: Dict[str, Any]
    ) -> str:
        """
        Save document and chunks to Chroma vector database.
        
        Args:
            title: Document title
            source: Document source path
            content: Full document content
            chunks: List of embedded chunks
            metadata: Document metadata
        
        Returns:
            Document ID
        """
        import hashlib
        
        # Generate document ID from content hash
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        document_id = f"doc_{content_hash[:16]}"
        
        # Get Chroma client
        chroma_client = get_chroma_client()
        
        # Prepare embeddings for batch insertion
        embeddings = []
        chunk_ids = []
        chunk_contents = []
        chunk_metadatas = []
        
        for i, chunk in enumerate(chunks):
            chunk_id = f"{document_id}_chunk_{i}"
            chunk_ids.append(chunk_id)
            embeddings.append(chunk.embedding)
            chunk_contents.append(chunk.content)
            
            # Combine document metadata with chunk metadata
            chunk_metadata = {
                "document_id": document_id,
                "document_title": title,
                "document_source": source,
                "chunk_index": i,
                "token_count": chunk.token_count,
                **chunk.metadata,
                **metadata
            }
            chunk_metadatas.append(chunk_metadata)
        
        # Batch insert into Chroma
        await chroma_client.add_embeddings(
            ids=chunk_ids,
            embeddings=embeddings,
            documents=chunk_contents,
            metadatas=chunk_metadatas
        )
        
        logger.info(f"Saved {len(chunks)} chunks to Chroma for document: {document_id}")
        
        return document_id
    
    async def _clean_databases(self):
        """Clean existing data from databases."""
        logger.warning("Cleaning existing data from databases...")
        
        # Clean Chroma - delete and recreate collection
        chroma_client = get_chroma_client()
        try:
            # Delete all documents (this will remove all chunks)
            # Chroma doesn't have a direct "delete all" so we list and delete
            documents = await chroma_client.list_documents(limit=1000)
            for doc in documents:
                doc_id = doc.get("id")
                if doc_id:
                    await chroma_client.delete_document(doc_id)
            
            logger.info("Cleaned Chroma vector database")
        except Exception as e:
            logger.warning(f"Failed to clean Chroma (may be empty): {e}")
        



async def main():
    """Main function for running ingestion."""
    parser = argparse.ArgumentParser(description="Ingest documents into Chroma vector DB")
    parser.add_argument("--documents", "-d", default="documents", help="Documents folder path")
    parser.add_argument("--no-clean", action="store_true", help="Skip cleaning existing data before ingestion")
    parser.add_argument("--chunk-size", type=int, default=1000, help="Chunk size for splitting documents")
    parser.add_argument("--chunk-overlap", type=int, default=200, help="Chunk overlap size")
    parser.add_argument("--max-chunk-size", type=int, default=1500, help="Maximum chunk size")
    parser.add_argument("--no-semantic", action="store_true", help="Disable semantic chunking")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Create ingestion configuration
    config = IngestionConfig(
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        max_chunk_size=args.max_chunk_size,
        use_semantic_chunking=not args.no_semantic,
    )

    # Create and run pipeline
    pipeline = DocumentIngestionPipeline(
        config=config,
        documents_folder=args.documents,
        clean_before_ingest=not args.no_clean
    )
    
    def progress_callback(current: int, total: int):
        print(f"Progress: {current}/{total} documents processed")
    
    try:
        start_time = datetime.now()
        
        results = await pipeline.ingest_documents(progress_callback)
        
        end_time = datetime.now()
        total_time = (end_time - start_time).total_seconds()
        
        # Print summary
        print("\n" + "="*70)
        print("INGESTION SUMMARY")
        print("="*70)
        print(f"Documents processed: {len(results)}")
        print(f"Total chunks created: {sum(r.chunks_created for r in results)}")
        print(f"Total errors: {sum(len(r.errors) for r in results)}")
        print(f"Total processing time: {total_time:.2f} seconds")
        print()
        
        # Print individual results
        for result in results:
            status = "✓" if not result.errors else "✗"
            print(
                f"{status} {result.title}: {result.chunks_created} chunks"
            )
            
            if result.errors:
                for error in result.errors:
                    print(f"  Error: {error}")
        
    except KeyboardInterrupt:
        print("\nIngestion interrupted by user")
    except Exception as e:
        logger.error(f"Ingestion failed: {e}", exc_info=True)
        raise
    finally:
        await pipeline.close()


if __name__ == "__main__":
    asyncio.run(main())
