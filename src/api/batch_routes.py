"""
API routes for batch document processing.

Provides endpoints for:
- Creating batch ingestion jobs
- Monitoring batch progress
- Streaming progress updates via SSE
- Managing batch job lifecycle
"""

import asyncio
import json
from typing import Optional, List
from pathlib import Path

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from src.ingestion.batch_processor import (
    BatchProcessor,
    BatchJob,
    BatchStatus,
    create_and_process_batch
)
from src.ingestion.ingest import IngestionConfig

router = APIRouter(prefix="/api/v1/ingest/batch", tags=["Batch Processing"])

# Global batch processor instance
_batch_processor: Optional[BatchProcessor] = None


def get_batch_processor() -> BatchProcessor:
    """Get or create batch processor instance."""
    global _batch_processor
    if _batch_processor is None:
        _batch_processor = BatchProcessor()
    return _batch_processor


# Request/Response Models
class BatchJobCreateRequest(BaseModel):
    """Request to create batch job."""
    source_directory: str = Field(..., description="Directory containing documents")
    file_patterns: Optional[List[str]] = Field(None, description="File patterns to match (e.g., ['*.pdf', '*.md'])")
    recursive: bool = Field(True, description="Whether to scan recursively")
    max_concurrent: int = Field(5, ge=1, le=20, description="Maximum concurrent document processing")
    
    # Ingestion config
    chunk_size: int = Field(512, ge=128, le=2048, description="Chunk size")
    chunk_overlap: int = Field(50, ge=0, le=500, description="Chunk overlap")
    use_semantic_chunking: bool = Field(True, description="Use semantic chunking")
    extract_knowledge_graph: bool = Field(True, description="Extract knowledge graph")


class BatchJobResponse(BaseModel):
    """Response for batch job."""
    batch_id: str
    status: str
    total_files: int
    processed_files: int = 0
    successful_files: int = 0
    failed_files: int = 0
    progress: float = 0.0
    message: str


class BatchProgressResponse(BaseModel):
    """Response for batch progress."""
    batch_id: str
    status: str
    progress: float
    total_files: int
    processed_files: int
    successful_files: int
    failed_files: int
    success_rate: float
    total_chunks: int
    total_entities: int
    total_relationships: int
    status_breakdown: dict
    created_at: str
    started_at: Optional[str]
    completed_at: Optional[str]


# Background task for batch processing
async def process_batch_background(batch_id: str) -> None:
    """
    Background task for processing batch job.
    
    Args:
        batch_id: Batch job ID
    """
    try:
        processor = get_batch_processor()
        await processor.process_batch(batch_id, resume=True)
        print(f"✓ Batch job {batch_id} completed")
    except Exception as e:
        print(f"✗ Batch job {batch_id} failed: {e}")


# Endpoints
@router.post("/", response_model=BatchJobResponse)
async def create_batch_job(
    request: BatchJobCreateRequest,
    background_tasks: BackgroundTasks
):
    """
    Create a batch ingestion job.
    
    Scans the specified directory for documents and creates a batch job
    for processing them in parallel. The job runs in the background.
    
    Progress can be tracked via:
    - GET /api/v1/ingest/batch/{batch_id} - Get current status
    - GET /api/v1/ingest/batch/{batch_id}/stream - Stream progress (SSE)
    
    Args:
        request: Batch job creation parameters
        background_tasks: FastAPI background tasks manager
        
    Returns:
        Created batch job information
    """
    try:
        # Validate directory exists
        directory = Path(request.source_directory)
        if not directory.exists():
            raise HTTPException(
                status_code=400,
                detail=f"Directory not found: {request.source_directory}"
            )
        
        if not directory.is_dir():
            raise HTTPException(
                status_code=400,
                detail=f"Path is not a directory: {request.source_directory}"
            )
        
        # Create ingestion config
        config = IngestionConfig(
            chunk_size=request.chunk_size,
            chunk_overlap=request.chunk_overlap,
            use_semantic_chunking=request.use_semantic_chunking,
            extract_knowledge_graph=request.extract_knowledge_graph
        )
        
        # Create batch processor with config
        processor = BatchProcessor(config=config)
        
        # Create batch job
        job = await processor.create_batch_job(
            source_directory=request.source_directory,
            file_patterns=request.file_patterns,
            recursive=request.recursive,
            max_concurrent=request.max_concurrent
        )
        
        # Schedule background processing
        background_tasks.add_task(process_batch_background, job.batch_id)
        
        return BatchJobResponse(
            batch_id=job.batch_id,
            status=job.status.value,
            total_files=job.total_files,
            progress=0.0,
            message=f"Batch job created with {job.total_files} files. Processing in background."
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{batch_id}", response_model=BatchProgressResponse)
async def get_batch_status(batch_id: str):
    """
    Get current status of batch job.
    
    Returns detailed progress information including:
    - Overall progress percentage
    - File processing statistics
    - Success/failure counts
    - Total chunks/entities/relationships created
    - Status breakdown by document
    
    Args:
        batch_id: Batch job ID
        
    Returns:
        Batch job progress information
    """
    try:
        processor = get_batch_processor()
        progress = await processor.get_batch_progress(batch_id)
        
        return BatchProgressResponse(**progress)
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{batch_id}/stream")
async def stream_batch_progress(batch_id: str):
    """
    Stream batch job progress via Server-Sent Events (SSE).
    
    Continuously streams progress updates until the batch job completes or fails.
    Updates are sent every 1 second.
    
    Args:
        batch_id: Batch job ID
        
    Returns:
        SSE stream with progress updates
    """
    processor = get_batch_processor()
    
    # Verify batch exists
    try:
        await processor.get_batch_progress(batch_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    async def generate_progress():
        """Generate SSE progress events."""
        last_progress = -1.0
        
        while True:
            try:
                progress = await processor.get_batch_progress(batch_id)
                current_progress = progress["progress"]
                
                # Send update if progress changed
                if current_progress != last_progress:
                    yield f"data: {json.dumps(progress)}\n\n"
                    last_progress = current_progress
                
                # Stop streaming if completed or failed
                status = progress["status"]
                if status in (BatchStatus.COMPLETED.value, BatchStatus.FAILED.value, BatchStatus.CANCELLED.value):
                    yield f"data: {json.dumps({'done': True})}\n\n"
                    break
                
                # Poll every 1 second
                await asyncio.sleep(1.0)
                
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
                break
    
    return StreamingResponse(
        generate_progress(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@router.delete("/{batch_id}")
async def cancel_batch_job(batch_id: str):
    """
    Cancel a batch job.
    
    Note: This only marks the job as cancelled in the database.
    Already running document processing will complete.
    
    Args:
        batch_id: Batch job ID
        
    Returns:
        Cancellation confirmation
    """
    try:
        processor = get_batch_processor()
        
        # Load job
        job = processor._load_batch_job(batch_id)
        if not job:
            raise HTTPException(status_code=404, detail="Batch job not found")
        
        # Update status
        job.status = BatchStatus.CANCELLED
        processor._save_batch_job(job)
        
        return {
            "status": "success",
            "message": f"Batch job {batch_id} cancelled",
            "batch_id": batch_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{batch_id}/resume")
async def resume_batch_job(
    batch_id: str,
    background_tasks: BackgroundTasks
):
    """
    Resume a paused or failed batch job.
    
    Resumes processing from where it left off, skipping already
    completed documents.
    
    Args:
        batch_id: Batch job ID
        background_tasks: FastAPI background tasks manager
        
    Returns:
        Resume confirmation
    """
    try:
        processor = get_batch_processor()
        
        # Load job
        job = processor._load_batch_job(batch_id)
        if not job:
            raise HTTPException(status_code=404, detail="Batch job not found")
        
        # Check if resumable
        if job.status not in (BatchStatus.PAUSED, BatchStatus.FAILED):
            raise HTTPException(
                status_code=400,
                detail=f"Cannot resume job with status: {job.status.value}"
            )
        
        # Schedule background processing
        background_tasks.add_task(process_batch_background, batch_id)
        
        return {
            "status": "success",
            "message": f"Batch job {batch_id} resumed",
            "batch_id": batch_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
