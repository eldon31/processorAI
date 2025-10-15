"""
Server-Sent Events (SSE) streaming framework for long-running operations.

Provides:
- SSE response formatting
- Progress tracking and streaming
- Event types for different stages
- Automatic cleanup and error handling
"""

import asyncio
import json
import logging
from typing import AsyncGenerator, Dict, Any, Optional, List
from enum import Enum
from datetime import datetime
from fastapi.responses import StreamingResponse

logger = logging.getLogger(__name__)


class EventType(str, Enum):
    """SSE event types for different operation stages."""
    
    # Document processing events
    STARTED = "started"
    PENDING = "pending"
    PROCESSING = "processing"
    CHUNKING = "chunking"
    EMBEDDING = "embedding"
    GRAPH_BUILDING = "graph_building"
    STORING = "storing"
    COMPLETED = "completed"
    
    # Batch processing events
    BATCH_STARTED = "batch_started"
    BATCH_PROGRESS = "batch_progress"
    BATCH_FILE_COMPLETED = "batch_file_completed"
    BATCH_FILE_FAILED = "batch_file_failed"
    BATCH_COMPLETED = "batch_completed"
    
    # Query/search events
    SEARCH_STARTED = "search_started"
    SEARCH_VECTOR = "search_vector"
    SEARCH_GRAPH = "search_graph"
    SEARCH_HYBRID = "search_hybrid"
    SEARCH_COMPLETED = "search_completed"
    
    # Agent events
    AGENT_THINKING = "agent_thinking"
    AGENT_TOOL_USE = "agent_tool_use"
    AGENT_STREAMING = "agent_streaming"
    AGENT_RESPONSE = "agent_response"
    
    # Error and status events
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    HEARTBEAT = "heartbeat"


class SSEEvent:
    """Server-Sent Event with formatting."""
    
    def __init__(
        self,
        event_type: EventType,
        data: Dict[str, Any],
        id: Optional[str] = None,
        retry: Optional[int] = None
    ):
        self.event_type = event_type
        self.data = data
        self.id = id
        self.retry = retry
        self.timestamp = datetime.utcnow().isoformat()
    
    def format(self) -> str:
        """Format event as SSE message."""
        lines = []
        
        # Add event type
        lines.append(f"event: {self.event_type}")
        
        # Add event ID if provided
        if self.id:
            lines.append(f"id: {self.id}")
        
        # Add retry interval if provided
        if self.retry:
            lines.append(f"retry: {self.retry}")
        
        # Add data (include timestamp)
        data_with_timestamp = {
            **self.data,
            "timestamp": self.timestamp,
            "event": self.event_type
        }
        lines.append(f"data: {json.dumps(data_with_timestamp)}")
        
        # SSE format requires double newline at end
        return "\n".join(lines) + "\n\n"


class ProgressTracker:
    """Track and stream progress for long-running operations."""
    
    def __init__(self, total_steps: int = 100, operation: str = "processing"):
        self.total_steps = total_steps
        self.current_step = 0
        self.operation = operation
        self.start_time = datetime.utcnow()
        self.events: List[SSEEvent] = []
    
    def update(
        self,
        step: int,
        event_type: EventType,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ) -> SSEEvent:
        """Update progress and create event."""
        self.current_step = step
        
        data = {
            "operation": self.operation,
            "step": step,
            "total": self.total_steps,
            "progress": round((step / self.total_steps) * 100, 2),
            "message": message,
        }
        
        if details:
            data.update(details)
        
        event = SSEEvent(event_type=event_type, data=data)
        self.events.append(event)
        
        return event
    
    def increment(
        self,
        event_type: EventType,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ) -> SSEEvent:
        """Increment progress by 1 step."""
        return self.update(
            step=self.current_step + 1,
            event_type=event_type,
            message=message,
            details=details
        )
    
    def complete(self, message: str = "Operation completed") -> SSEEvent:
        """Mark operation as completed."""
        return self.update(
            step=self.total_steps,
            event_type=EventType.COMPLETED,
            message=message,
            details={
                "duration_seconds": (datetime.utcnow() - self.start_time).total_seconds()
            }
        )
    
    def error(self, error_message: str, details: Optional[Dict[str, Any]] = None) -> SSEEvent:
        """Create error event."""
        error_data = {
            "operation": self.operation,
            "step": self.current_step,
            "total": self.total_steps,
            "message": error_message,
        }
        
        if details:
            error_data.update(details)
        
        event = SSEEvent(event_type=EventType.ERROR, data=error_data)
        self.events.append(event)
        
        return event


async def stream_events(events: AsyncGenerator[SSEEvent, None]) -> StreamingResponse:
    """Create StreamingResponse for SSE events."""
    
    async def event_generator():
        """Generate SSE formatted events."""
        try:
            async for event in events:
                yield event.format()
                # Small delay to prevent overwhelming client
                await asyncio.sleep(0.01)
        except Exception as e:
            # Send error event before closing
            error_event = SSEEvent(
                event_type=EventType.ERROR,
                data={
                    "message": str(e),
                    "error_type": e.__class__.__name__
                }
            )
            yield error_event.format()
            logger.error(f"SSE streaming error: {e}", exc_info=True)
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        }
    )


async def stream_progress(
    tracker: ProgressTracker,
    operation_func,
    *args,
    **kwargs
) -> AsyncGenerator[SSEEvent, None]:
    """
    Stream progress events while executing operation.
    
    Args:
        tracker: ProgressTracker instance
        operation_func: Async function to execute
        *args, **kwargs: Arguments for operation_func
    
    Yields:
        SSEEvent instances tracking progress
    """
    # Send start event
    start_event = tracker.update(
        step=0,
        event_type=EventType.STARTED,
        message=f"Starting {tracker.operation}"
    )
    yield start_event
    
    try:
        # Execute operation (should update tracker internally)
        result = await operation_func(*args, **kwargs)
        
        # Send completion event
        complete_event = tracker.complete()
        yield complete_event
        
        # Optionally yield result as final event
        if result:
            result_event = SSEEvent(
                event_type=EventType.INFO,
                data={"result": result}
            )
            yield result_event
            
    except Exception as e:
        # Send error event
        error_event = tracker.error(
            error_message=str(e),
            details={"error_type": e.__class__.__name__}
        )
        yield error_event
        raise


async def heartbeat_generator(interval: int = 15) -> AsyncGenerator[SSEEvent, None]:
    """
    Generate heartbeat events to keep connection alive.
    
    Args:
        interval: Seconds between heartbeats
    
    Yields:
        Heartbeat SSEEvent instances
    """
    while True:
        await asyncio.sleep(interval)
        yield SSEEvent(
            event_type=EventType.HEARTBEAT,
            data={"message": "Connection alive"}
        )


async def stream_with_heartbeat(
    events: AsyncGenerator[SSEEvent, None],
    heartbeat_interval: int = 15
) -> AsyncGenerator[SSEEvent, None]:
    """
    Merge event stream with heartbeat to prevent timeout.
    
    Args:
        events: Main event stream
        heartbeat_interval: Seconds between heartbeats
    
    Yields:
        Events from main stream plus heartbeats
    """
    heartbeat_task = None
    last_event_time = datetime.utcnow()
    
    try:
        async for event in events:
            yield event
            last_event_time = datetime.utcnow()
            
            # Send heartbeat if no event for interval
            elapsed = (datetime.utcnow() - last_event_time).total_seconds()
            if elapsed >= heartbeat_interval:
                heartbeat = SSEEvent(
                    event_type=EventType.HEARTBEAT,
                    data={"message": "Connection alive"}
                )
                yield heartbeat
                last_event_time = datetime.utcnow()
                
    finally:
        if heartbeat_task:
            heartbeat_task.cancel()


# Helper functions for common streaming scenarios

async def stream_document_processing(
    file_path: str,
    process_func,
) -> AsyncGenerator[SSEEvent, None]:
    """Stream document processing progress."""
    tracker = ProgressTracker(total_steps=5, operation="document_processing")
    
    # Step 1: Pending
    yield tracker.update(1, EventType.PENDING, f"Queued: {file_path}")
    
    # Step 2: Processing (extraction)
    yield tracker.update(2, EventType.PROCESSING, "Extracting content")
    
    # Step 3: Chunking
    yield tracker.update(3, EventType.CHUNKING, "Splitting into chunks")
    
    # Step 4: Embedding
    yield tracker.update(4, EventType.EMBEDDING, "Generating embeddings")
    
    # Step 5: Storing
    yield tracker.update(5, EventType.STORING, "Storing in vector database")
    
    try:
        await process_func(file_path)
        yield tracker.complete(f"Successfully processed: {file_path}")
    except Exception as e:
        yield tracker.error(f"Failed to process: {e}")
        raise


async def stream_batch_progress(
    files: List[str],
    process_each_func,
) -> AsyncGenerator[SSEEvent, None]:
    """Stream batch processing progress."""
    total_files = len(files)
    tracker = ProgressTracker(total_steps=total_files, operation="batch_processing")
    
    # Batch started
    yield SSEEvent(
        event_type=EventType.BATCH_STARTED,
        data={
            "total_files": total_files,
            "files": [f for f in files[:10]]  # Preview first 10
        }
    )
    
    completed = 0
    failed = 0
    
    for idx, file_path in enumerate(files, 1):
        try:
            # Process file
            await process_each_func(file_path)
            completed += 1
            
            # File completed event
            yield SSEEvent(
                event_type=EventType.BATCH_FILE_COMPLETED,
                data={
                    "file": file_path,
                    "index": idx,
                    "total": total_files,
                    "progress": round((idx / total_files) * 100, 2),
                    "completed": completed,
                    "failed": failed
                }
            )
            
        except Exception as e:
            failed += 1
            
            # File failed event
            yield SSEEvent(
                event_type=EventType.BATCH_FILE_FAILED,
                data={
                    "file": file_path,
                    "index": idx,
                    "total": total_files,
                    "error": str(e),
                    "completed": completed,
                    "failed": failed
                }
            )
    
    # Batch completed
    yield SSEEvent(
        event_type=EventType.BATCH_COMPLETED,
        data={
            "total_files": total_files,
            "completed": completed,
            "failed": failed,
            "success_rate": round((completed / total_files) * 100, 2)
        }
    )
