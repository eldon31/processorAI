"""
Batch document processing for directory ingestion.

Provides functionality for:
- Directory scanning with format filtering
- Parallel document processing with concurrency limits
- Progress tracking and SSE streaming
- Resumable ingestion with state persistence
- Error recovery and retry logic

Adapted from common batch processing patterns for RAG systems.
"""

import asyncio
import logging
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
from uuid import uuid4
from enum import Enum

from pydantic import BaseModel, Field

from .ingest import DocumentIngestionPipeline, IngestionConfig, IngestionResult

logger = logging.getLogger(__name__)


class BatchStatus(str, Enum):
    """Batch job status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class DocumentStatus(str, Enum):
    """Individual document status in batch."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class BatchJob(BaseModel):
    """Batch ingestion job."""
    batch_id: str = Field(default_factory=lambda: str(uuid4()))
    status: BatchStatus = Field(default=BatchStatus.PENDING)
    
    # Configuration
    source_directory: str
    file_patterns: List[str] = Field(default=["*.pdf", "*.docx", "*.md", "*.txt"])
    recursive: bool = Field(default=True)
    max_concurrent: int = Field(default=5, ge=1, le=20)
    
    # Progress
    total_files: int = 0
    processed_files: int = 0
    successful_files: int = 0
    failed_files: int = 0
    skipped_files: int = 0
    
    # Results
    total_chunks: int = 0
    total_entities: int = 0
    total_relationships: int = 0
    
    # Timestamps
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    
    # Error tracking
    errors: List[Dict[str, str]] = Field(default_factory=list)
    
    @property
    def progress(self) -> float:
        """Calculate progress percentage."""
        if self.total_files == 0:
            return 0.0
        return self.processed_files / self.total_files
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.processed_files == 0:
            return 0.0
        return self.successful_files / self.processed_files


class BatchDocument(BaseModel):
    """Individual document in batch job."""
    document_id: str = Field(default_factory=lambda: str(uuid4()))
    batch_id: str
    file_path: str
    status: DocumentStatus = Field(default=DocumentStatus.PENDING)
    
    # Results
    chunks_created: Optional[int] = None
    entities_extracted: Optional[int] = None
    relationships_created: Optional[int] = None
    
    # Timestamps
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    
    # Error tracking
    error: Optional[str] = None
    retry_count: int = 0


class BatchProcessor:
    """
    Process multiple documents in batch with concurrency control.
    
    Features:
    - Directory scanning with pattern matching
    - Parallel processing with semaphore
    - Progress tracking and persistence
    - Resumable ingestion
    - Error recovery
    """
    
    # Supported file extensions
    SUPPORTED_EXTENSIONS = {
        ".pdf", ".docx", ".doc", ".xlsx", ".xls",
        ".pptx", ".ppt", ".html", ".htm", ".md",
        ".txt", ".mp3", ".wav", ".m4a"
    }
    
    def __init__(
        self,
        config: Optional[IngestionConfig] = None,
        state_db_path: str = "batch_state.db"
    ):
        """
        Initialize batch processor.
        
        Args:
            config: Ingestion configuration (uses defaults if None)
            state_db_path: Path to SQLite database for state persistence
        """
        self.config = config or IngestionConfig()
        self.state_db_path = state_db_path
        self.pipeline: Optional[DocumentIngestionPipeline] = None
        
        # Initialize state database
        self._init_state_db()
    
    def _init_state_db(self) -> None:
        """Initialize SQLite database for state persistence."""
        conn = sqlite3.connect(self.state_db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS batch_jobs (
                batch_id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                source_directory TEXT NOT NULL,
                total_files INTEGER DEFAULT 0,
                processed_files INTEGER DEFAULT 0,
                successful_files INTEGER DEFAULT 0,
                failed_files INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                started_at TEXT,
                completed_at TEXT,
                config_json TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS batch_documents (
                document_id TEXT PRIMARY KEY,
                batch_id TEXT NOT NULL,
                file_path TEXT NOT NULL,
                status TEXT NOT NULL,
                chunks_created INTEGER,
                entities_extracted INTEGER,
                relationships_created INTEGER,
                created_at TEXT NOT NULL,
                started_at TEXT,
                completed_at TEXT,
                error TEXT,
                retry_count INTEGER DEFAULT 0,
                FOREIGN KEY (batch_id) REFERENCES batch_jobs(batch_id)
            )
        """)
        
        conn.commit()
        conn.close()
        logger.info(f"Initialized state database at {self.state_db_path}")
    
    async def scan_directory(
        self,
        directory: Path,
        patterns: List[str],
        recursive: bool = True
    ) -> List[Path]:
        """
        Scan directory for matching files.
        
        Args:
            directory: Directory to scan
            patterns: File patterns (e.g., ["*.pdf", "*.docx"])
            recursive: Whether to scan recursively
        
        Returns:
            List of file paths matching patterns
        """
        files = []
        
        if recursive:
            for pattern in patterns:
                files.extend(directory.rglob(pattern))
        else:
            for pattern in patterns:
                files.extend(directory.glob(pattern))
        
        # Filter by supported extensions
        supported_files = [
            f for f in files
            if f.suffix.lower() in self.SUPPORTED_EXTENSIONS
        ]
        
        logger.info(f"Found {len(supported_files)} supported files in {directory}")
        return supported_files
    
    async def create_batch_job(
        self,
        source_directory: str,
        file_patterns: Optional[List[str]] = None,
        recursive: bool = True,
        max_concurrent: int = 5
    ) -> BatchJob:
        """
        Create a new batch job.
        
        Args:
            source_directory: Directory containing documents
            file_patterns: File patterns to match (defaults to all supported)
            recursive: Whether to scan recursively
            max_concurrent: Maximum concurrent document processing
        
        Returns:
            Created batch job
        """
        directory = Path(source_directory)
        if not directory.exists():
            raise ValueError(f"Directory not found: {source_directory}")
        
        patterns = file_patterns or ["*.*"]
        
        # Scan directory
        files = await self.scan_directory(directory, patterns, recursive)
        
        # Create job
        job = BatchJob(
            source_directory=source_directory,
            file_patterns=patterns,
            recursive=recursive,
            max_concurrent=max_concurrent,
            total_files=len(files)
        )
        
        # Save to database
        self._save_batch_job(job)
        
        # Create document entries
        for file_path in files:
            doc = BatchDocument(
                batch_id=job.batch_id,
                file_path=str(file_path)
            )
            self._save_batch_document(doc)
        
        logger.info(f"Created batch job {job.batch_id} with {len(files)} files")
        return job
    
    async def process_batch(
        self,
        batch_id: str,
        resume: bool = True
    ) -> BatchJob:
        """
        Process all documents in batch job.
        
        Args:
            batch_id: Batch job ID
            resume: Whether to resume from previous state
        
        Returns:
            Updated batch job
        """
        # Load job
        job = self._load_batch_job(batch_id)
        if not job:
            raise ValueError(f"Batch job not found: {batch_id}")
        
        # Update status
        job.status = BatchStatus.RUNNING
        job.started_at = datetime.utcnow().isoformat()
        self._save_batch_job(job)
        
        # Initialize pipeline
        self.pipeline = DocumentIngestionPipeline(self.config)
        await self.pipeline.initialize()
        
        try:
            # Load pending documents
            documents = self._load_batch_documents(
                batch_id,
                status=DocumentStatus.PENDING if not resume else None
            )
            
            # Process with concurrency limit
            semaphore = asyncio.Semaphore(job.max_concurrent)
            tasks = [
                self._process_document_with_semaphore(doc, job, semaphore)
                for doc in documents
            ]
            
            # Wait for all tasks
            await asyncio.gather(*tasks, return_exceptions=True)
            
            # Update final status
            job.status = BatchStatus.COMPLETED
            job.completed_at = datetime.utcnow().isoformat()
            
        except Exception as e:
            logger.error(f"Batch processing failed: {e}")
            job.status = BatchStatus.FAILED
            job.errors.append({
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            })
        
        finally:
            # Save final state
            self._save_batch_job(job)
        
        return job
    
    async def _process_document_with_semaphore(
        self,
        doc: BatchDocument,
        job: BatchJob,
        semaphore: asyncio.Semaphore
    ) -> None:
        """
        Process single document with concurrency control.
        
        Args:
            doc: Document to process
            job: Parent batch job
            semaphore: Concurrency semaphore
        """
        async with semaphore:
            await self._process_single_document(doc, job)
    
    async def _process_single_document(
        self,
        doc: BatchDocument,
        job: BatchJob
    ) -> None:
        """
        Process a single document.
        
        Args:
            doc: Document to process
            job: Parent batch job
        """
        # Update status
        doc.status = DocumentStatus.PROCESSING
        doc.started_at = datetime.utcnow().isoformat()
        self._save_batch_document(doc)
        
        try:
            # Process document
            results = await self.pipeline.ingest_documents([doc.file_path])
            
            if results and len(results) > 0:
                result = results[0]
                
                # Update document
                doc.status = DocumentStatus.COMPLETED
                doc.chunks_created = result.chunks_created
                doc.entities_extracted = result.entities_extracted
                doc.relationships_created = result.relationships_created
                doc.completed_at = datetime.utcnow().isoformat()
                
                # Update job totals
                job.successful_files += 1
                job.total_chunks += result.chunks_created
                job.total_entities += result.entities_extracted
                job.total_relationships += result.relationships_created
                
                logger.info(f"✓ Processed {doc.file_path}: {result.chunks_created} chunks")
            else:
                # No results (unexpected)
                doc.status = DocumentStatus.FAILED
                doc.error = "No results returned from pipeline"
                doc.completed_at = datetime.utcnow().isoformat()
                job.failed_files += 1
                
        except Exception as e:
            # Processing failed
            doc.status = DocumentStatus.FAILED
            doc.error = str(e)
            doc.completed_at = datetime.utcnow().isoformat()
            job.failed_files += 1
            
            logger.error(f"✗ Failed to process {doc.file_path}: {e}")
        
        finally:
            # Update counts
            job.processed_files += 1
            
            # Save state
            self._save_batch_document(doc)
            self._save_batch_job(job)
    
    def _save_batch_job(self, job: BatchJob) -> None:
        """Save batch job to database."""
        conn = sqlite3.connect(self.state_db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO batch_jobs
            (batch_id, status, source_directory, total_files, processed_files,
             successful_files, failed_files, created_at, started_at, completed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            job.batch_id, job.status.value, job.source_directory,
            job.total_files, job.processed_files, job.successful_files,
            job.failed_files, job.created_at, job.started_at, job.completed_at
        ))
        
        conn.commit()
        conn.close()
    
    def _load_batch_job(self, batch_id: str) -> Optional[BatchJob]:
        """Load batch job from database."""
        conn = sqlite3.connect(self.state_db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT batch_id, status, source_directory, total_files, processed_files,
                   successful_files, failed_files, created_at, started_at, completed_at
            FROM batch_jobs
            WHERE batch_id = ?
        """, (batch_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return BatchJob(
            batch_id=row[0],
            status=BatchStatus(row[1]),
            source_directory=row[2],
            total_files=row[3],
            processed_files=row[4],
            successful_files=row[5],
            failed_files=row[6],
            created_at=row[7],
            started_at=row[8],
            completed_at=row[9]
        )
    
    def _save_batch_document(self, doc: BatchDocument) -> None:
        """Save batch document to database."""
        conn = sqlite3.connect(self.state_db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO batch_documents
            (document_id, batch_id, file_path, status, chunks_created,
             entities_extracted, relationships_created, created_at,
             started_at, completed_at, error, retry_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            doc.document_id, doc.batch_id, doc.file_path, doc.status.value,
            doc.chunks_created, doc.entities_extracted, doc.relationships_created,
            doc.created_at, doc.started_at, doc.completed_at, doc.error, doc.retry_count
        ))
        
        conn.commit()
        conn.close()
    
    def _load_batch_documents(
        self,
        batch_id: str,
        status: Optional[DocumentStatus] = None
    ) -> List[BatchDocument]:
        """Load batch documents from database."""
        conn = sqlite3.connect(self.state_db_path)
        cursor = conn.cursor()
        
        if status:
            cursor.execute("""
                SELECT document_id, batch_id, file_path, status, chunks_created,
                       entities_extracted, relationships_created, created_at,
                       started_at, completed_at, error, retry_count
                FROM batch_documents
                WHERE batch_id = ? AND status = ?
            """, (batch_id, status.value))
        else:
            cursor.execute("""
                SELECT document_id, batch_id, file_path, status, chunks_created,
                       entities_extracted, relationships_created, created_at,
                       started_at, completed_at, error, retry_count
                FROM batch_documents
                WHERE batch_id = ?
            """, (batch_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        documents = []
        for row in rows:
            documents.append(BatchDocument(
                document_id=row[0],
                batch_id=row[1],
                file_path=row[2],
                status=DocumentStatus(row[3]),
                chunks_created=row[4],
                entities_extracted=row[5],
                relationships_created=row[6],
                created_at=row[7],
                started_at=row[8],
                completed_at=row[9],
                error=row[10],
                retry_count=row[11]
            ))
        
        return documents
    
    async def get_batch_progress(self, batch_id: str) -> Dict[str, Any]:
        """
        Get current progress of batch job.
        
        Args:
            batch_id: Batch job ID
        
        Returns:
            Progress information
        """
        job = self._load_batch_job(batch_id)
        if not job:
            raise ValueError(f"Batch job not found: {batch_id}")
        
        documents = self._load_batch_documents(batch_id)
        
        # Calculate statistics
        status_counts = {}
        for status in DocumentStatus:
            count = sum(1 for d in documents if d.status == status)
            status_counts[status.value] = count
        
        return {
            "batch_id": job.batch_id,
            "status": job.status.value,
            "progress": job.progress,
            "total_files": job.total_files,
            "processed_files": job.processed_files,
            "successful_files": job.successful_files,
            "failed_files": job.failed_files,
            "success_rate": job.success_rate,
            "total_chunks": job.total_chunks,
            "total_entities": job.total_entities,
            "total_relationships": job.total_relationships,
            "status_breakdown": status_counts,
            "created_at": job.created_at,
            "started_at": job.started_at,
            "completed_at": job.completed_at
        }


# Convenience function
async def create_and_process_batch(
    source_directory: str,
    file_patterns: Optional[List[str]] = None,
    recursive: bool = True,
    max_concurrent: int = 5,
    config: Optional[IngestionConfig] = None
) -> BatchJob:
    """
    Create and process batch job in one call.
    
    Args:
        source_directory: Directory containing documents
        file_patterns: File patterns to match
        recursive: Whether to scan recursively
        max_concurrent: Maximum concurrent processing
        config: Ingestion configuration
    
    Returns:
        Completed batch job
    """
    processor = BatchProcessor(config=config)
    
    # Create job
    job = await processor.create_batch_job(
        source_directory=source_directory,
        file_patterns=file_patterns,
        recursive=recursive,
        max_concurrent=max_concurrent
    )
    
    # Process job
    completed_job = await processor.process_batch(job.batch_id)
    
    return completed_job
