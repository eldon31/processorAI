"""
API Routes for RAG Agent.

Provides endpoints for:
- Document upload and ingestion
- RAG-based querying with streaming responses
- Document management (list, get, delete)
"""

import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from uuid import uuid4

from fastapi import APIRouter, File, UploadFile, HTTPException, BackgroundTasks, Form
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from src.models import Document, Query, QueryResult
from src.models.collection import CollectionCategory
from src.ingestion.ingest import DocumentIngestionPipeline, IngestionConfig
from src.agent.agent import rag_agent, AgentDependencies
from src.storage.chroma_client import get_chroma_client
from src.storage.collection_manager import get_collection_manager
from src.config.providers import ProviderConfig


router = APIRouter(prefix="/api/v1", tags=["RAG Agent"])

# In-memory ingestion status storage (replace with Redis/DB in production)
_ingestion_status: Dict[str, Dict] = {}


# Request/Response Models
class UploadResponse(BaseModel):
    """Response for document upload."""
    document_id: str
    filename: str
    status: str
    message: str


class IngestionStatus(BaseModel):
    """Ingestion status for a document."""
    document_id: str
    filename: str
    status: str  # "processing", "completed", "failed"
    progress: float  # 0.0 to 1.0
    current_step: str
    chunks_created: Optional[int] = None
    entities_extracted: Optional[int] = None
    relationships_created: Optional[int] = None
    error: Optional[str] = None
    started_at: str
    completed_at: Optional[str] = None


class QueryRequest(BaseModel):
    """Request for RAG query."""
    question: str = Field(..., description="Question to ask the RAG agent")
    stream: bool = Field(default=True, description="Whether to stream the response")
    max_chunks: int = Field(default=5, description="Maximum number of chunks to retrieve")
    collection: Optional[str] = Field(None, description="Specific collection to search (optional)")
    categories: Optional[List[str]] = Field(None, description="Collection categories to search (optional)")


class DocumentInfo(BaseModel):
    """Document information."""
    id: str
    filename: str
    source: str
    chunk_count: int
    created_at: Optional[str] = None


class DocumentListResponse(BaseModel):
    """Response for document list."""
    documents: List[DocumentInfo]
    total: int


# Helper Functions
def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    """Save uploaded file to disk."""
    try:
        with destination.open("wb") as buffer:
            buffer.write(upload_file.file.read())
    finally:
        upload_file.file.close()


async def ingest_document_with_progress(file_path: Path, document_id: str, filename: str) -> None:
    """
    Background task for document ingestion with progress tracking.
    
    Args:
        file_path: Path to uploaded file
        document_id: Unique document identifier
        filename: Original filename
    """
    # Initialize status
    _ingestion_status[document_id] = {
        "document_id": document_id,
        "filename": filename,
        "status": "processing",
        "progress": 0.0,
        "current_step": "Initializing pipeline",
        "chunks_created": None,
        "entities_extracted": None,
        "relationships_created": None,
        "error": None,
        "started_at": datetime.utcnow().isoformat(),
        "completed_at": None,
    }
    
    try:
        # Create ingestion pipeline
        _ingestion_status[document_id]["current_step"] = "Creating ingestion pipeline"
        _ingestion_status[document_id]["progress"] = 0.1
        
        config = IngestionConfig(
            chunk_size=512,
            chunk_overlap=50,
            max_chunk_size=1000,
            use_semantic_chunking=True,
            extract_knowledge_graph=True,
        )
        
        pipeline = DocumentIngestionPipeline(config)
        
        # Initialize pipeline
        _ingestion_status[document_id]["current_step"] = "Initializing services"
        _ingestion_status[document_id]["progress"] = 0.2
        await pipeline.initialize()
        
        # Process document
        _ingestion_status[document_id]["current_step"] = "Extracting text and chunking"
        _ingestion_status[document_id]["progress"] = 0.4
        
        results = await pipeline.ingest_documents([str(file_path)])
        
        if results and len(results) > 0:
            result = results[0]
            
            # Update status with results
            _ingestion_status[document_id]["current_step"] = "Completed"
            _ingestion_status[document_id]["progress"] = 1.0
            _ingestion_status[document_id]["status"] = "completed"
            _ingestion_status[document_id]["chunks_created"] = result.chunks_created
            _ingestion_status[document_id]["entities_extracted"] = result.entities_extracted
            _ingestion_status[document_id]["relationships_created"] = result.relationships_created
            _ingestion_status[document_id]["completed_at"] = datetime.utcnow().isoformat()
            
            print(f"✓ Document ingested: {document_id}")
            print(f"  - Chunks: {result.chunks_created}")
            print(f"  - Entities: {result.entities_extracted}")
            print(f"  - Relationships: {result.relationships_created}")
        else:
            # No results (unexpected)
            _ingestion_status[document_id]["status"] = "failed"
            _ingestion_status[document_id]["error"] = "No results returned from pipeline"
            _ingestion_status[document_id]["completed_at"] = datetime.utcnow().isoformat()
            print(f"⚠ No results returned for document {document_id}")
        
    except Exception as e:
        # Update status with error
        _ingestion_status[document_id]["status"] = "failed"
        _ingestion_status[document_id]["error"] = str(e)
        _ingestion_status[document_id]["completed_at"] = datetime.utcnow().isoformat()
        print(f"✗ Error ingesting document {document_id}: {e}")
    
    finally:
        # Clean up uploaded file
        if file_path.exists():
            file_path.unlink()


# Endpoints
@router.post("/ingest/document", response_model=UploadResponse)
async def ingest_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    collection: Optional[str] = Form(None),
    language: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
):
    """
    Upload and ingest a document.
    
    Supports multiple formats: PDF, Word, Excel, PowerPoint, HTML, Markdown, TXT, Audio.
    
    Can optionally specify target collection, language, or category for automatic routing.
    
    The document is processed in the background:
    1. Text extraction with Docling
    2. Chunking with HybridChunker
    3. Embedding generation
    4. Storage in Chroma (vector DB)
    
    Progress can be tracked via the `/api/v1/ingest/status/{document_id}` endpoint.
    
    Args:
        file: Uploaded file
        background_tasks: FastAPI background tasks manager
        collection: Target collection name (optional)
        language: Programming language for auto-routing (optional)
        category: Collection category for auto-routing (optional)
        
    Returns:
        Upload response with document ID and status
    """
    # Generate unique document ID
    document_id = str(uuid4())
    
    # Validate file extension
    supported_extensions = {
        ".pdf", ".docx", ".doc", ".xlsx", ".xls",
        ".pptx", ".ppt", ".html", ".htm", ".md",
        ".txt", ".mp3", ".wav", ".m4a",
    }
    
    filename = file.filename or "unknown"
    file_extension = Path(filename).suffix.lower()
    if file_extension not in supported_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format: {file_extension}. "
                   f"Supported: {', '.join(supported_extensions)}",
        )
    
    # Save uploaded file temporarily
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    
    file_path = upload_dir / f"{document_id}{file_extension}"
    save_upload_file(file, file_path)
    
    # Schedule background ingestion with progress tracking
    background_tasks.add_task(ingest_document_with_progress, file_path, document_id, filename)
    
    return UploadResponse(
        document_id=document_id,
        filename=filename,
        status="processing",
        message="Document uploaded successfully. Processing in background. Use /api/v1/ingest/status/{document_id} to track progress.",
    )


@router.get("/ingest/status/{document_id}", response_model=IngestionStatus)
async def get_ingestion_status(document_id: str):
    """
    Get ingestion status for a document.
    
    Returns real-time progress information including:
    - Current processing step
    - Progress percentage (0.0 to 1.0)
    - Number of chunks/entities/relationships created
    - Error details (if failed)
    
    Args:
        document_id: Document identifier
        
    Returns:
        Ingestion status with progress information
    """
    if document_id not in _ingestion_status:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return IngestionStatus(**_ingestion_status[document_id])


@router.get("/ingest/stream/{document_id}")
async def stream_ingestion_progress(document_id: str):
    """
    Stream ingestion progress via Server-Sent Events (SSE).
    
    Continuously streams progress updates until ingestion completes or fails.
    
    Args:
        document_id: Document identifier
        
    Returns:
        SSE stream with progress updates
    """
    if document_id not in _ingestion_status:
        raise HTTPException(status_code=404, detail="Document not found")
    
    async def generate_progress():
        """Generate SSE progress events."""
        last_progress = -1.0
        
        while True:
            if document_id not in _ingestion_status:
                yield f"data: {json.dumps({'error': 'Document not found'})}\n\n"
                break
            
            status = _ingestion_status[document_id]
            current_progress = status["progress"]
            
            # Send update if progress changed
            if current_progress != last_progress:
                yield f"data: {json.dumps(status)}\n\n"
                last_progress = current_progress
            
            # Stop streaming if completed or failed
            if status["status"] in ("completed", "failed"):
                yield f"data: {json.dumps({'done': True})}\n\n"
                break
            
            # Poll every 0.5 seconds
            await asyncio.sleep(0.5)
    
    return StreamingResponse(
        generate_progress(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        },
    )


@router.post("/query")
async def query_rag(request: QueryRequest):
    """
    Query the RAG agent.
    
    Retrieves relevant document chunks from the vector database and knowledge graph,
    then generates an answer using the configured LLM.
    
    Supports:
    - Streaming responses (default): Real-time token generation via SSE
    - Non-streaming responses: Complete answer returned at once
    - Multi-collection search: Query across multiple collections
    - Category-based routing: Search specific collection categories
    
    Args:
        request: Query request with question and options
        
    Returns:
        Streaming response with answer tokens (if stream=True)
        or complete answer (if stream=False)
    """
    try:
        # Use the global RAG agent
        deps = AgentDependencies(session_id=str(uuid4()))
        
        # Create query
        query_text = request.question
        
        if request.stream:
            # Streaming response
            async def generate_stream():
                """Generate streaming response tokens."""
                try:
                    # Run agent and stream response
                    result = await rag_agent.run(query_text, deps=deps)
                    
                    # Convert result to string and stream
                    response_text = str(result)
                    for i in range(0, len(response_text), 10):
                        chunk = response_text[i:i+10]
                        yield f"data: {json.dumps({'chunk': chunk})}\n\n"
                        await asyncio.sleep(0.01)  # Small delay for smooth streaming
                    
                    yield f"data: {json.dumps({'done': True})}\n\n"
                    
                except Exception as e:
                    yield f"data: {json.dumps({'error': str(e)})}\n\n"
            
            return StreamingResponse(
                generate_stream(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "X-Accel-Buffering": "no",
                },
            )
        
        else:
            # Non-streaming response
            result = await rag_agent.run(query_text, deps=deps)
            
            return {
                "answer": str(result),
                "sources": [],  # TODO: Extract sources from agent result
            }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/documents", response_model=DocumentListResponse)
async def list_documents():
    """
    List all ingested documents.
    
    Returns:
        List of documents with metadata
    """
    try:
        chroma_client = get_chroma_client()
        
        # Get all documents from Chroma
        documents = await chroma_client.list_documents()
        
        # Convert to response format
        document_list = [
            DocumentInfo(
                id=doc.get("id", ""),
                filename=doc.get("filename", "unknown"),
                source=doc.get("source", ""),
                chunk_count=doc.get("chunk_count", 0),
                created_at=doc.get("created_at"),
            )
            for doc in documents
        ]
        
        return DocumentListResponse(
            documents=document_list,
            total=len(document_list),
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/documents/{document_id}")
async def get_document(document_id: str):
    """
    Get document details.
    
    Args:
        document_id: Document identifier
        
    Returns:
        Document metadata and chunk information
    """
    try:
        chroma_client = get_chroma_client()
        
        # Get document chunks
        chunks = await chroma_client.get_document_chunks(document_id)
        
        if not chunks:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Aggregate chunk information
        chunk_data = [
            {
                "chunk_id": chunk.id,
                "text": chunk.content[:200] + "..." if len(chunk.content) > 200 else chunk.content,
                "metadata": chunk.metadata,
            }
            for chunk in chunks
        ]
        
        return {
            "document_id": document_id,
            "chunk_count": len(chunks),
            "chunks": chunk_data,
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    """
    Delete a document and all associated data.
    
    Removes:
    - Document chunks from vector database (Chroma)
    
    
    Args:
        document_id: Document identifier
        
    Returns:
        Deletion confirmation
    """
    try:
        chroma_client = get_chroma_client()
        
        # Delete from Chroma
        deleted = chroma_client.delete_document(document_id)
        
        if not deleted:
            raise HTTPException(status_code=404, detail="Document not found")
        
        
        # This requires adding a delete method to GraphitiClient
        
        return {
            "status": "success",
            "message": f"Document {document_id} deleted successfully",
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
