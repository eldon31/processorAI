"""
FastAPI Application for RAG Agent API.

Provides REST API endpoints for:
- Document upload and ingestion
- RAG-based question answering
- Document management
- System health checks
"""

import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.storage.chroma_client import initialize_chroma, close_chroma, get_chroma_client
from src.config.providers import ProviderConfig

# Import monitoring and middleware
from src.monitoring import configure_logging, get_metrics, collect_system_metrics, Timer
from src.api.middleware import (
    configure_cors,
    configure_error_handling,
    validation_exception_handler,
    rag_exception_handler,
)
from src.exceptions import RAGException

# Import route modules
from src.api import routes
from src.api import collection_routes
from src.api import batch_routes


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager.
    
    Initializes and cleans up resources on startup/shutdown.
    """
    # Startup: Initialize connections
    print("=" * 60)
    print("Starting RAG Agent API...")
    print("=" * 60)
    
    # Configure logging first
    log_level = os.getenv("LOG_LEVEL", "INFO")
    json_format = os.getenv("LOG_FORMAT", "colored") == "json"
    configure_logging(level=log_level, json_format=json_format)
    
    try:
        # Initialize Chroma client
        print("Initializing Chroma vector database...")
        await initialize_chroma()
        print("✓ Chroma client initialized")
        
        # Start background system metrics collection
        import asyncio
        async def collect_metrics_loop():
            while True:
                try:
                    collect_system_metrics()
                    await asyncio.sleep(60)  # Collect every 60 seconds
                except Exception as e:
                    print(f"Error collecting system metrics: {e}")
                    await asyncio.sleep(60)
        
        # Start metrics collection in background (don't await)
        asyncio.create_task(collect_metrics_loop())
        
        print("=" * 60)
        print("✓ RAG Agent API ready!")
        print(f"  - Logging: {log_level} ({'JSON' if json_format else 'Colored'})")
        print(f"  - Chroma: Connected")
        print(f"  - Metrics: Collecting every 60s")
        print("=" * 60)
        
    except Exception as e:
        print(f"✗ Failed to initialize services: {e}")
        raise
    
    yield
    
    # Shutdown: Clean up resources
    print("=" * 60)
    print("Shutting down RAG Agent API...")
    print("=" * 60)
    
    try:
        # Close Chroma connection
        print("Closing Chroma client...")
        await close_chroma()
        print("✓ Chroma client closed")
        
        print("=" * 60)
        print("✓ RAG Agent API shutdown complete")
        print("=" * 60)
        
    except Exception as e:
        print(f"✗ Error during shutdown: {e}")


# Create FastAPI application
app = FastAPI(
    title="RAG Agent API",
    description="REST API for document ingestion and RAG-based question answering with knowledge graph",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure middleware (ORDER MATTERS!)
# 1. CORS first (must be before error handling)
configure_cors(app)

# 2. Error handling middleware
configure_error_handling(app)

# 3. Register custom exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(RAGException, rag_exception_handler)

# Include routers
app.include_router(routes.router)  # Already has /api/v1 prefix
app.include_router(collection_routes.collection_router)
app.include_router(batch_routes.router)  # Batch processing routes


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "name": "RAG Agent API",
        "version": "1.0.0",
        "description": "Document ingestion and RAG-based question answering with knowledge graph",
        "endpoints": {
            "health": "/health",
            "ingest_document": "/api/v1/ingest/document",
            "ingest_status": "/api/v1/ingest/status/{document_id}",
            "ingest_stream": "/api/v1/ingest/stream/{document_id}",
            "batch_create": "/api/v1/ingest/batch",
            "batch_status": "/api/v1/ingest/batch/{batch_id}",
            "batch_stream": "/api/v1/ingest/batch/{batch_id}/stream",
            "query": "/api/v1/query",
            "documents": "/api/v1/documents",
            "collections": "/api/v1/collections",
        },
        "features": {
            "multi_collection_support": True,
            "collection_categories": 20,
            "streaming_responses": True,
            "sse_progress_tracking": True,
        },
        "docs": "/docs",
        "redoc": "/redoc",
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Verifies that all critical services are accessible.
    """
    health_status = {
        "status": "healthy",
        "services": {},
        "timestamp": None,
    }
    
    from datetime import datetime
    health_status["timestamp"] = datetime.utcnow().isoformat()
    
    all_healthy = True
    
    # Check Chroma
    try:
        chroma_client = get_chroma_client()
        if chroma_client and chroma_client._initialized:
            health_status["services"]["chroma"] = {
                "status": "connected",
                "type": "vector_database"
            }
        else:
            health_status["services"]["chroma"] = {
                "status": "not_initialized",
                "type": "vector_database"
            }
            all_healthy = False
    except Exception as e:
        health_status["services"]["chroma"] = {
            "status": "error",
            "error": str(e),
            "type": "vector_database"
        }
        all_healthy = False
    
    # Set overall status
    health_status["status"] = "healthy" if all_healthy else "degraded"
    
    # Return appropriate status code
    status_code = 200 if all_healthy else 503
    
    return JSONResponse(status_code=status_code, content=health_status)


# Metrics endpoint
@app.get("/metrics")
async def metrics_endpoint():
    """
    Prometheus-compatible metrics endpoint.
    
    Returns metrics in JSON format with statistics.
    """
    metrics = get_metrics()
    
    return {
        "format": "json",
        "metrics": metrics.export_json(),
        "prometheus_format": "/metrics/prometheus",  # Future endpoint
    }


# Metrics in Prometheus format
@app.get("/metrics/prometheus")
async def prometheus_metrics():
    """
    Prometheus-compatible metrics endpoint.
    
    Returns metrics in Prometheus text format.
    """
    from fastapi.responses import PlainTextResponse
    
    metrics = get_metrics()
    prometheus_text = metrics.export_prometheus()
    
    return PlainTextResponse(content=prometheus_text, media_type="text/plain")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
    )
