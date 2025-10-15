"""
Document processor for multi-format document extraction.

Provides unified interface for processing various document formats:
- PDF, DOCX, PPTX, XLSX via Docling
- Markdown, TXT, HTML (plain text)
- MP3, WAV, M4A (audio transcription via Whisper ASR)

Features:
- Format detection and validation
- File size limits (<500MB)
- SHA-256 content hashing for deduplication
- Streaming support for large files
- Metadata extraction
"""

import hashlib
import logging
import mimetypes
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from pydantic import BaseModel, Field

from src.exceptions import DocumentProcessingError

logger = logging.getLogger(__name__)


class DocumentMetadata(BaseModel):
    """Metadata extracted from document."""
    
    file_path: str
    file_name: str
    file_size: int
    file_format: str
    mime_type: Optional[str] = None
    sha256_hash: str
    title: Optional[str] = None
    author: Optional[str] = None
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None
    page_count: Optional[int] = None
    word_count: Optional[int] = None
    extracted_at: datetime = Field(default_factory=datetime.now)
    processing_method: str = "unknown"
    
    # YAML frontmatter or document properties
    custom_metadata: Dict[str, Any] = Field(default_factory=dict)


class ProcessedDocument(BaseModel):
    """Result of document processing."""
    
    content: str
    metadata: DocumentMetadata
    docling_document: Optional[Any] = None  # DoclingDocument for hybrid chunking
    
    class Config:
        arbitrary_types_allowed = True


class DocumentProcessor:
    """
    Multi-format document processor with Docling integration.
    
    Supported formats:
    - Documents: PDF, DOCX, DOC, PPTX, PPT, XLSX, XLS, HTML, HTM
    - Text: MD, MARKDOWN, TXT
    - Audio: MP3, WAV, M4A, FLAC
    """
    
    # Format categories
    DOCLING_FORMATS = {'.pdf', '.docx', '.doc', '.pptx', '.ppt', '.xlsx', '.xls', '.html', '.htm'}
    TEXT_FORMATS = {'.md', '.markdown', '.txt'}
    AUDIO_FORMATS = {'.mp3', '.wav', '.m4a', '.flac'}
    
    ALL_SUPPORTED_FORMATS = DOCLING_FORMATS | TEXT_FORMATS | AUDIO_FORMATS
    
    # Size limits
    MAX_FILE_SIZE_MB = 500
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
    
    def __init__(self):
        """Initialize document processor."""
        self._docling_converter = None
    
    def _get_docling_converter(self):
        """Lazy-load Docling converter."""
        if self._docling_converter is None:
            try:
                from docling.document_converter import DocumentConverter
                self._docling_converter = DocumentConverter()
                logger.info("Docling DocumentConverter initialized")
            except ImportError:
                raise DocumentProcessingError(
                    message="Docling is not installed",
                    remediation="Install docling: pip install docling[vlm]>=2.55.0"
                )
        return self._docling_converter
    
    def process_file(self, file_path: str) -> ProcessedDocument:
        """
        Process a document file and extract content + metadata.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            ProcessedDocument with content and metadata
            
        Raises:
            DocumentProcessingError: If processing fails
        """
        # Validate file
        self._validate_file(file_path)
        
        # Get file info
        path = Path(file_path)
        file_ext = path.suffix.lower()
        
        # Process based on format
        if file_ext in self.TEXT_FORMATS:
            return self._process_text_file(file_path)
        elif file_ext in self.DOCLING_FORMATS:
            return self._process_with_docling(file_path)
        elif file_ext in self.AUDIO_FORMATS:
            return self._process_audio_file(file_path)
        else:
            raise DocumentProcessingError(
                message=f"Unsupported file format: {file_ext}",
                remediation=f"Supported formats: {', '.join(sorted(self.ALL_SUPPORTED_FORMATS))}",
                details={"file_path": file_path, "format": file_ext}
            )
    
    def _validate_file(self, file_path: str) -> None:
        """
        Validate file exists and meets requirements.
        
        Args:
            file_path: Path to the file
            
        Raises:
            DocumentProcessingError: If validation fails
        """
        path = Path(file_path)
        
        # Check existence
        if not path.exists():
            raise DocumentProcessingError(
                message=f"File not found: {file_path}",
                remediation="Verify the file path is correct"
            )
        
        if not path.is_file():
            raise DocumentProcessingError(
                message=f"Path is not a file: {file_path}",
                remediation="Provide a path to a file, not a directory"
            )
        
        # Check format
        file_ext = path.suffix.lower()
        if file_ext not in self.ALL_SUPPORTED_FORMATS:
            raise DocumentProcessingError(
                message=f"Unsupported file format: {file_ext}",
                remediation=f"Supported formats: {', '.join(sorted(self.ALL_SUPPORTED_FORMATS))}"
            )
        
        # Check size
        file_size = path.stat().st_size
        if file_size > self.MAX_FILE_SIZE_BYTES:
            size_mb = file_size / (1024 * 1024)
            raise DocumentProcessingError(
                message=f"File size ({size_mb:.2f} MB) exceeds maximum ({self.MAX_FILE_SIZE_MB} MB)",
                remediation="Split large files or compress before uploading",
                details={"file_size_mb": size_mb, "max_size_mb": self.MAX_FILE_SIZE_MB}
            )
    
    def _process_text_file(self, file_path: str) -> ProcessedDocument:
        """
        Process plain text file (MD, TXT).
        
        Args:
            file_path: Path to text file
            
        Returns:
            ProcessedDocument
        """
        path = Path(file_path)
        
        try:
            # Read text content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Attempt to convert markdown to DoclingDocument for better chunking
            docling_doc = None
            processing_method = "text_file"

            if path.suffix.lower() in {'.md', '.markdown'}:
                try:
                    converter = self._get_docling_converter()
                    from docling.datamodel.base_models import InputFormat

                    result = converter.convert_string(
                        content=content,
                        format=InputFormat.MD,
                        name=path.name
                    )
                    docling_doc = result.document
                    processing_method = "markdown_docling"
                    logger.info("Converted markdown to DoclingDocument for chunking")
                except DocumentProcessingError as docling_error:
                    logger.warning(
                        "Docling not available for markdown conversion, using raw text: %s",
                        docling_error
                    )
                except Exception as docling_exc:
                    logger.warning(
                        "Docling markdown conversion failed (%s), using raw text",
                        docling_exc
                    )

            # Extract metadata
            metadata = self._extract_text_metadata(file_path, content)
            metadata.processing_method = processing_method

            logger.info(f"Processed text file: {path.name} ({len(content)} chars)")

            return ProcessedDocument(
                content=content,
                metadata=metadata,
                docling_document=docling_doc
            )
            
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.read()
                
                docling_doc = None
                processing_method = "text_file_latin1"

                if path.suffix.lower() in {'.md', '.markdown'}:
                    try:
                        converter = self._get_docling_converter()
                        from docling.datamodel.base_models import InputFormat

                        result = converter.convert_string(
                            content=content,
                            format=InputFormat.MD,
                            name=path.name
                        )
                        docling_doc = result.document
                        processing_method = "markdown_docling"
                        logger.info("Converted markdown (latin-1) to DoclingDocument for chunking")
                    except DocumentProcessingError as docling_error:
                        logger.warning(
                            "Docling not available for markdown conversion (latin-1), using raw text: %s",
                            docling_error
                        )
                    except Exception as docling_exc:
                        logger.warning(
                            "Docling markdown conversion (latin-1) failed (%s), using raw text",
                            docling_exc
                        )

                metadata = self._extract_text_metadata(file_path, content)
                metadata.processing_method = processing_method
                
                logger.warning(f"Used latin-1 encoding for: {path.name}")
                
                return ProcessedDocument(
                    content=content,
                    metadata=metadata,
                    docling_document=docling_doc
                )
            except Exception as e:
                raise DocumentProcessingError(
                    message=f"Failed to read text file: {e}",
                    remediation="Ensure file is a valid text file with UTF-8 or Latin-1 encoding",
                    details={"file_path": file_path}
                )
        except Exception as e:
            raise DocumentProcessingError(
                message=f"Failed to process text file: {e}",
                remediation="Check file permissions and encoding",
                details={"file_path": file_path}
            )
    
    def _process_with_docling(self, file_path: str) -> ProcessedDocument:
        """
        Process document with Docling (PDF, DOCX, PPTX, XLSX, HTML).
        
        Args:
            file_path: Path to document file
            
        Returns:
            ProcessedDocument with DoclingDocument attached
        """
        path = Path(file_path)
        
        try:
            converter = self._get_docling_converter()
            
            logger.info(f"Converting with Docling: {path.name}")
            
            # Convert document
            result = converter.convert(file_path)
            
            # Export to markdown for consistent processing
            markdown_content = result.document.export_to_markdown()
            
            # Extract metadata from Docling result
            metadata = self._extract_docling_metadata(file_path, result.document, markdown_content)
            metadata.processing_method = "docling"
            
            logger.info(f"Docling conversion complete: {path.name} ({len(markdown_content)} chars)")
            
            return ProcessedDocument(
                content=markdown_content,
                metadata=metadata,
                docling_document=result.document  # Keep for hybrid chunking
            )
            
        except Exception as e:
            logger.error(f"Docling conversion failed for {path.name}: {e}")
            
            # Try fallback for certain formats
            if path.suffix.lower() in {'.html', '.htm'}:
                logger.warning(f"Falling back to raw HTML extraction for: {path.name}")
                return self._process_text_file(file_path)
            
            raise DocumentProcessingError(
                message=f"Failed to convert document with Docling: {e}",
                remediation="Ensure file is not corrupted and Docling dependencies are installed",
                details={"file_path": file_path, "error": str(e)}
            )
    
    def _process_audio_file(self, file_path: str) -> ProcessedDocument:
        """
        Process audio file with Whisper ASR transcription.
        
        Args:
            file_path: Path to audio file
            
        Returns:
            ProcessedDocument with transcribed text
        """
        path = Path(file_path)
        
        try:
            from pathlib import Path as PathLib
            from docling.document_converter import DocumentConverter, AudioFormatOption
            from docling.datamodel.pipeline_options import AsrPipelineOptions
            from docling.datamodel import asr_model_specs
            from docling.datamodel.base_models import InputFormat
            
            logger.info(f"Transcribing audio with Whisper: {path.name}")
            
            # Configure ASR pipeline with Whisper Turbo
            asr_options = AsrPipelineOptions(
                model_spec=asr_model_specs.WhisperTurboV1ModelSpec(),
                language="en"  # Can be auto-detected or configured
            )
            
            # Create converter with ASR configuration
            converter = DocumentConverter(
                format_options={
                    InputFormat.AUDIO: AudioFormatOption(pipeline_options=asr_options)
                }
            )
            
            # Convert audio to text
            audio_path = PathLib(file_path).resolve()
            result = converter.convert(audio_path)
            
            # Export transcription
            transcript = result.document.export_to_markdown()
            
            # Extract metadata
            metadata = self._extract_audio_metadata(file_path, transcript)
            metadata.processing_method = "whisper_asr"
            
            logger.info(f"Audio transcription complete: {path.name} ({len(transcript)} chars)")
            
            return ProcessedDocument(
                content=transcript,
                metadata=metadata,
                docling_document=None
            )
            
        except ImportError as e:
            raise DocumentProcessingError(
                message="Audio transcription dependencies not installed",
                remediation="Install Docling with audio support: pip install docling[vlm]>=2.55.0",
                details={"error": str(e)}
            )
        except Exception as e:
            raise DocumentProcessingError(
                message=f"Failed to transcribe audio: {e}",
                remediation="Ensure audio file is valid and not corrupted",
                details={"file_path": file_path, "error": str(e)}
            )
    
    def _extract_text_metadata(self, file_path: str, content: str) -> DocumentMetadata:
        """Extract metadata from text file."""
        path = Path(file_path)
        stat = path.stat()
        
        # Calculate SHA-256 hash
        sha256_hash = self._calculate_hash(content)
        
        # Extract title (first heading or filename)
        title = self._extract_title_from_content(content, path.stem)
        
        # Parse YAML frontmatter if present
        custom_metadata = self._extract_frontmatter(content)
        
        # Detect MIME type
        mime_type, _ = mimetypes.guess_type(file_path)
        
        return DocumentMetadata(
            file_path=file_path,
            file_name=path.name,
            file_size=stat.st_size,
            file_format=path.suffix.lower(),
            mime_type=mime_type,
            sha256_hash=sha256_hash,
            title=title,
            created_at=datetime.fromtimestamp(stat.st_ctime),
            modified_at=datetime.fromtimestamp(stat.st_mtime),
            word_count=len(content.split()),
            custom_metadata=custom_metadata
        )
    
    def _extract_docling_metadata(
        self, 
        file_path: str, 
        docling_doc: Any, 
        markdown_content: str
    ) -> DocumentMetadata:
        """Extract metadata from Docling document."""
        path = Path(file_path)
        stat = path.stat()
        
        # Calculate SHA-256 hash
        sha256_hash = self._calculate_hash(markdown_content)
        
        # Extract title
        title = self._extract_title_from_content(markdown_content, path.stem)
        
        # Try to get metadata from Docling document
        page_count = None
        author = None
        
        try:
            # Docling documents may have metadata
            if hasattr(docling_doc, 'metadata'):
                doc_metadata = docling_doc.metadata
                if hasattr(doc_metadata, 'page_count'):
                    page_count = doc_metadata.page_count
                if hasattr(doc_metadata, 'author'):
                    author = doc_metadata.author
        except Exception:
            pass  # Metadata extraction is best-effort
        
        # Detect MIME type
        mime_type, _ = mimetypes.guess_type(file_path)
        
        return DocumentMetadata(
            file_path=file_path,
            file_name=path.name,
            file_size=stat.st_size,
            file_format=path.suffix.lower(),
            mime_type=mime_type,
            sha256_hash=sha256_hash,
            title=title,
            author=author,
            created_at=datetime.fromtimestamp(stat.st_ctime),
            modified_at=datetime.fromtimestamp(stat.st_mtime),
            page_count=page_count,
            word_count=len(markdown_content.split())
        )
    
    def _extract_audio_metadata(self, file_path: str, transcript: str) -> DocumentMetadata:
        """Extract metadata from audio file."""
        path = Path(file_path)
        stat = path.stat()
        
        # Calculate SHA-256 hash
        sha256_hash = self._calculate_hash(transcript)
        
        # Extract title
        title = f"Transcript: {path.stem}"
        
        # Detect MIME type
        mime_type, _ = mimetypes.guess_type(file_path)
        
        return DocumentMetadata(
            file_path=file_path,
            file_name=path.name,
            file_size=stat.st_size,
            file_format=path.suffix.lower(),
            mime_type=mime_type,
            sha256_hash=sha256_hash,
            title=title,
            created_at=datetime.fromtimestamp(stat.st_ctime),
            modified_at=datetime.fromtimestamp(stat.st_mtime),
            word_count=len(transcript.split())
        )
    
    def _calculate_hash(self, content: str) -> str:
        """Calculate SHA-256 hash of content."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def _extract_title_from_content(self, content: str, fallback: str) -> str:
        """
        Extract title from content.
        
        Priority:
        1. First H1 heading (# Title)
        2. First line if short
        3. Filename as fallback
        """
        lines = content.split('\n')
        
        # Look for markdown H1
        for line in lines[:10]:  # Check first 10 lines
            line = line.strip()
            if line.startswith('# '):
                return line[2:].strip()
        
        # Use first non-empty line if short enough
        for line in lines[:5]:
            line = line.strip()
            if line and len(line) < 100:
                return line
        
        # Fallback to filename
        return fallback
    
    def _extract_frontmatter(self, content: str) -> Dict[str, Any]:
        """
        Extract YAML frontmatter from content.
        
        Format:
        ---
        key: value
        ---
        content...
        """
        if not content.startswith('---'):
            return {}
        
        try:
            import yaml
            
            # Find end of frontmatter
            end_marker = content.find('\n---\n', 4)
            if end_marker == -1:
                return {}
            
            # Extract YAML
            frontmatter = content[4:end_marker]
            metadata = yaml.safe_load(frontmatter)
            
            if isinstance(metadata, dict):
                return metadata
            
        except ImportError:
            logger.debug("PyYAML not installed, skipping frontmatter extraction")
        except Exception as e:
            logger.warning(f"Failed to parse YAML frontmatter: {e}")
        
        return {}
    
    @staticmethod
    def get_supported_formats() -> set:
        """Get set of all supported file formats."""
        return DocumentProcessor.ALL_SUPPORTED_FORMATS
    
    @staticmethod
    def is_supported(file_path: str) -> bool:
        """Check if file format is supported."""
        ext = Path(file_path).suffix.lower()
        return ext in DocumentProcessor.ALL_SUPPORTED_FORMATS
