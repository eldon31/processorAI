"""
API middleware for standardized error handling and request processing.

Provides:
- Standardized error response format
- Pydantic ValidationError handling
- Request/response logging
- CORS configuration
- Exception to HTTP status code mapping
"""

import logging
import time
from typing import Callable, Dict, Any
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from ..exceptions import (
    RAGException,
    DocumentProcessingError,
    UnsupportedFormatError,
    FileSizeError,
    VectorStoreError,
    ChromaConnectionError,
    CollectionNotFoundError,
    ConfigurationError,
    EmbeddingError,
    MemoryLimitError,
)

logger = logging.getLogger(__name__)


# Exception to HTTP status code mapping
EXCEPTION_STATUS_CODES: Dict[type, int] = {
    UnsupportedFormatError: status.HTTP_400_BAD_REQUEST,
    FileSizeError: status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
    CollectionNotFoundError: status.HTTP_404_NOT_FOUND,
    ChromaConnectionError: status.HTTP_503_SERVICE_UNAVAILABLE,
    ConfigurationError: status.HTTP_500_INTERNAL_SERVER_ERROR,
    EmbeddingError: status.HTTP_502_BAD_GATEWAY,
    MemoryLimitError: status.HTTP_507_INSUFFICIENT_STORAGE,
    DocumentProcessingError: status.HTTP_422_UNPROCESSABLE_ENTITY,
    VectorStoreError: status.HTTP_500_INTERNAL_SERVER_ERROR,
    RAGException: status.HTTP_500_INTERNAL_SERVER_ERROR,
}


def get_status_code_for_exception(exc: Exception) -> int:
    """Get appropriate HTTP status code for exception."""
    for exc_type, status_code in EXCEPTION_STATUS_CODES.items():
        if isinstance(exc, exc_type):
            return status_code
    return status.HTTP_500_INTERNAL_SERVER_ERROR


def format_error_response(
    exc: Exception,
    status_code: int,
    request_id: str
) -> Dict[str, Any]:
    """Format exception into standardized error response."""
    
    # Handle RAGException with remediation
    if isinstance(exc, RAGException):
        response = exc.to_dict()
    # Handle Pydantic ValidationError
    elif isinstance(exc, (ValidationError, RequestValidationError)):
        response = {
            "error": "ValidationError",
            "message": "Invalid request data",
            "details": exc.errors() if hasattr(exc, 'errors') else str(exc),
            "remediation": "Check request body against API schema"
        }
    # Generic exception
    else:
        response = {
            "error": exc.__class__.__name__,
            "message": str(exc),
        }
    
    # Add standard fields
    response["status_code"] = status_code
    response["request_id"] = request_id
    
    return response


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware for standardized error handling across all endpoints."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request with error handling."""
        
        # Generate request ID for tracing
        request_id = request.headers.get("X-Request-ID", f"req_{int(time.time() * 1000)}")
        request.state.request_id = request_id
        
        # Log request
        logger.info(
            f"Request started",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "client": request.client.host if request.client else None,
            }
        )
        
        start_time = time.time()
        
        try:
            response = await call_next(request)
            
            # Log successful response
            duration_ms = (time.time() - start_time) * 1000
            logger.info(
                f"Request completed",
                extra={
                    "request_id": request_id,
                    "status_code": response.status_code,
                    "duration_ms": duration_ms,
                }
            )
            
            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            
            return response
            
        except Exception as exc:
            # Get appropriate status code
            status_code = get_status_code_for_exception(exc)
            
            # Format error response
            error_response = format_error_response(exc, status_code, request_id)
            
            # Log error
            duration_ms = (time.time() - start_time) * 1000
            logger.error(
                f"Request failed: {exc}",
                extra={
                    "request_id": request_id,
                    "error_type": exc.__class__.__name__,
                    "status_code": status_code,
                    "duration_ms": duration_ms,
                },
                exc_info=True
            )
            
            # Return JSON error response
            return JSONResponse(
                status_code=status_code,
                content=error_response,
                headers={"X-Request-ID": request_id}
            )


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for detailed request/response logging."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Log request details."""
        
        # Log request body for POST/PUT (with size limit)
        if request.method in ["POST", "PUT", "PATCH"]:
            # Don't log file uploads (multipart/form-data)
            content_type = request.headers.get("content-type", "")
            if "multipart/form-data" not in content_type:
                try:
                    body = await request.body()
                    if len(body) < 1024:  # Only log small bodies
                        logger.debug(f"Request body: {body.decode('utf-8')[:500]}")
                except Exception:
                    pass
        
        response = await call_next(request)
        return response


def configure_cors(app) -> None:
    """Configure CORS middleware for API."""
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure based on environment
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID"],
    )


def configure_error_handling(app) -> None:
    """Configure error handling middleware."""
    
    app.add_middleware(ErrorHandlingMiddleware)
    app.add_middleware(RequestLoggingMiddleware)


# Custom exception handlers for FastAPI
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors."""
    request_id = getattr(request.state, "request_id", "unknown")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "ValidationError",
            "message": "Invalid request data",
            "details": exc.errors(),
            "remediation": "Check request body against API schema",
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "request_id": request_id,
        }
    )


async def rag_exception_handler(request: Request, exc: RAGException):
    """Handle RAG system exceptions."""
    request_id = getattr(request.state, "request_id", "unknown")
    status_code = get_status_code_for_exception(exc)
    
    response = exc.to_dict()
    response["status_code"] = status_code
    response["request_id"] = request_id
    
    return JSONResponse(
        status_code=status_code,
        content=response
    )
