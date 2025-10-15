"""
Custom exception classes with actionable error messages.

Provides standardized exceptions with remediation hints for:
- Document processing errors
- Vector store operations
- Graph store operations
- Configuration issues
"""

from typing import Optional, Dict, Any


class RAGException(Exception):
    """Base exception for RAG system with remediation hints."""
    
    def __init__(
        self,
        message: str,
        remediation: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.remediation = remediation
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for API responses."""
        result = {
            "error": self.__class__.__name__,
            "message": self.message,
        }
        if self.remediation:
            result["remediation"] = self.remediation
        if self.details:
            result["details"] = self.details
        return result


class DocumentProcessingError(RAGException):
    """Raised when document processing fails."""
    
    def __init__(
        self,
        message: str,
        file_path: Optional[str] = None,
        stage: Optional[str] = None,
        remediation: Optional[str] = None
    ):
        details = {}
        if file_path:
            details["file_path"] = file_path
        if stage:
            details["processing_stage"] = stage
        
        super().__init__(message, remediation, details)


class UnsupportedFormatError(DocumentProcessingError):
    """Raised when file format is not supported."""
    
    SUPPORTED_FORMATS = ["pdf", "docx", "txt", "md", "html"]
    
    def __init__(self, file_path: str, file_format: str):
        message = f"Unsupported file format: .{file_format}"
        remediation = f"Supported formats: {', '.join(self.SUPPORTED_FORMATS)}"
        super().__init__(
            message=message,
            file_path=file_path,
            stage="format_validation",
            remediation=remediation
        )


class FileSizeError(DocumentProcessingError):
    """Raised when file exceeds size limit."""
    
    def __init__(self, file_path: str, size_mb: float, max_size_mb: int = 500):
        message = f"File size ({size_mb:.1f}MB) exceeds limit ({max_size_mb}MB)"
        remediation = "Split the file into smaller parts or use batch processing"
        super().__init__(
            message=message,
            file_path=file_path,
            stage="size_validation",
            remediation=remediation
        )


class VectorStoreError(RAGException):
    """Raised when vector store operations fail."""
    
    def __init__(
        self,
        message: str,
        operation: Optional[str] = None,
        collection: Optional[str] = None,
        remediation: Optional[str] = None
    ):
        details = {}
        if operation:
            details["operation"] = operation
        if collection:
            details["collection"] = collection
        
        super().__init__(message, remediation, details)


class ChromaConnectionError(VectorStoreError):
    """Raised when Chroma connection fails."""
    
    def __init__(self, host: str, port: int, original_error: Optional[Exception] = None):
        message = f"Failed to connect to Chroma at {host}:{port}"
        remediation = "Check that Chroma server is running: docker-compose up chroma"
        details = {"host": host, "port": port}
        if original_error:
            details["original_error"] = str(original_error)
        
        super().__init__(message, remediation=remediation)
        self.details.update(details)


class CollectionNotFoundError(VectorStoreError):
    """Raised when collection doesn't exist."""
    
    def __init__(self, collection_name: str):
        message = f"Collection '{collection_name}' not found"
        remediation = f"Create the collection first or use auto-create option"
        super().__init__(
            message=message,
            operation="get_collection",
            collection=collection_name,
            remediation=remediation
        )


class ConfigurationError(RAGException):
    """Raised when configuration is invalid or missing."""
    
    def __init__(self, message: str, config_key: Optional[str] = None):
        details = {}
        if config_key:
            details["config_key"] = config_key
            remediation = f"Set {config_key} in environment variables or config file"
        else:
            remediation = "Check .env file and environment variables"
        
        super().__init__(message, remediation, details)


class EmbeddingError(RAGException):
    """Raised when embedding generation fails."""
    
    def __init__(
        self,
        message: str,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        remediation: Optional[str] = None
    ):
        details = {}
        if provider:
            details["provider"] = provider
        if model:
            details["model"] = model
        
        if not remediation and provider == "openai":
            remediation = "Check OPENAI_API_KEY environment variable"
        elif not remediation and provider == "ollama":
            remediation = "Check that Ollama is running: ollama serve"
        
        super().__init__(message, remediation, details)


class MemoryLimitError(RAGException):
    """Raised when operation would exceed memory limits."""
    
    def __init__(self, operation: str, estimated_mb: float, limit_mb: int = 2048):
        message = f"Operation '{operation}' would use ~{estimated_mb:.0f}MB (limit: {limit_mb}MB)"
        remediation = "Process in smaller batches or increase memory limit"
        details = {
            "operation": operation,
            "estimated_mb": estimated_mb,
            "limit_mb": limit_mb
        }
        
        super().__init__(message, remediation, details)
