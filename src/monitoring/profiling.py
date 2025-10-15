"""
Memory profiling decorator for tracking memory-intensive operations.

Helps identify operations that risk exceeding 2GB memory limit.
"""

import logging
import psutil
import tracemalloc
from typing import Callable, Any, Optional
from functools import wraps

from ..exceptions import MemoryLimitError

logger = logging.getLogger(__name__)


class MemoryProfiler:
    """Profile memory usage of operations."""
    
    def __init__(
        self,
        operation_name: str,
        warning_threshold_mb: int = 1024,
        error_threshold_mb: int = 2048,
        trace_allocations: bool = False
    ):
        self.operation_name = operation_name
        self.warning_threshold_mb = warning_threshold_mb
        self.error_threshold_mb = error_threshold_mb
        self.trace_allocations = trace_allocations
        
        self.start_memory_mb = 0
        self.peak_memory_mb = 0
        self.end_memory_mb = 0
        self.memory_increase_mb = 0
    
    def __enter__(self):
        """Start memory profiling."""
        # Start tracing allocations if requested
        if self.trace_allocations and not tracemalloc.is_tracing():
            tracemalloc.start()
        
        # Get current memory usage
        process = psutil.Process()
        self.start_memory_mb = process.memory_info().rss / (1024 * 1024)
        
        logger.debug(
            f"Memory profiling started for '{self.operation_name}'",
            extra={
                "operation": self.operation_name,
                "start_memory_mb": self.start_memory_mb
            }
        )
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop memory profiling and report results."""
        # Get final memory usage
        process = psutil.Process()
        self.end_memory_mb = process.memory_info().rss / (1024 * 1024)
        self.memory_increase_mb = self.end_memory_mb - self.start_memory_mb
        
        # Get peak memory if tracing
        if self.trace_allocations and tracemalloc.is_tracing():
            current, peak = tracemalloc.get_traced_memory()
            self.peak_memory_mb = peak / (1024 * 1024)
            tracemalloc.stop()
        else:
            self.peak_memory_mb = self.end_memory_mb
        
        # Log results
        logger.info(
            f"Memory profiling complete for '{self.operation_name}'",
            extra={
                "operation": self.operation_name,
                "start_memory_mb": round(self.start_memory_mb, 2),
                "end_memory_mb": round(self.end_memory_mb, 2),
                "peak_memory_mb": round(self.peak_memory_mb, 2),
                "increase_mb": round(self.memory_increase_mb, 2)
            }
        )
        
        # Check thresholds
        if self.peak_memory_mb >= self.error_threshold_mb:
            logger.error(
                f"Memory limit exceeded: {self.peak_memory_mb:.2f}MB (limit: {self.error_threshold_mb}MB)",
                extra={
                    "operation": self.operation_name,
                    "peak_memory_mb": self.peak_memory_mb,
                    "limit_mb": self.error_threshold_mb
                }
            )
            raise MemoryLimitError(
                operation=self.operation_name,
                estimated_mb=self.peak_memory_mb,
                limit_mb=self.error_threshold_mb
            )
        
        elif self.peak_memory_mb >= self.warning_threshold_mb:
            logger.warning(
                f"High memory usage: {self.peak_memory_mb:.2f}MB (warning threshold: {self.warning_threshold_mb}MB)",
                extra={
                    "operation": self.operation_name,
                    "peak_memory_mb": self.peak_memory_mb,
                    "threshold_mb": self.warning_threshold_mb
                }
            )
    
    def get_stats(self) -> dict:
        """Get memory profiling statistics."""
        return {
            "operation": self.operation_name,
            "start_memory_mb": round(self.start_memory_mb, 2),
            "end_memory_mb": round(self.end_memory_mb, 2),
            "peak_memory_mb": round(self.peak_memory_mb, 2),
            "increase_mb": round(self.memory_increase_mb, 2),
        }


def profile_memory(
    warning_threshold_mb: int = 1024,
    error_threshold_mb: int = 2048,
    trace_allocations: bool = False
):
    """
    Decorator for profiling memory usage of functions.
    
    Args:
        warning_threshold_mb: Log warning if memory exceeds this (MB)
        error_threshold_mb: Raise error if memory exceeds this (MB)
        trace_allocations: Enable detailed allocation tracing
    
    Example:
        @profile_memory(warning_threshold_mb=512, error_threshold_mb=2048)
        async def process_large_file(file_path: str):
            # Function implementation
            pass
    """
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            with MemoryProfiler(
                operation_name=f"{func.__module__}.{func.__name__}",
                warning_threshold_mb=warning_threshold_mb,
                error_threshold_mb=error_threshold_mb,
                trace_allocations=trace_allocations
            ):
                return await func(*args, **kwargs)
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            with MemoryProfiler(
                operation_name=f"{func.__module__}.{func.__name__}",
                warning_threshold_mb=warning_threshold_mb,
                error_threshold_mb=error_threshold_mb,
                trace_allocations=trace_allocations
            ):
                return func(*args, **kwargs)
        
        # Return appropriate wrapper
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


def check_memory_available(required_mb: int, safety_margin_mb: int = 512) -> bool:
    """
    Check if enough memory is available for operation.
    
    Args:
        required_mb: Required memory in MB
        safety_margin_mb: Additional safety margin in MB
    
    Returns:
        True if enough memory available, False otherwise
    """
    memory = psutil.virtual_memory()
    available_mb = memory.available / (1024 * 1024)
    
    total_required = required_mb + safety_margin_mb
    
    if available_mb < total_required:
        logger.warning(
            f"Insufficient memory: need {total_required}MB, have {available_mb:.2f}MB",
            extra={
                "required_mb": required_mb,
                "safety_margin_mb": safety_margin_mb,
                "available_mb": available_mb
            }
        )
        return False
    
    return True


def get_current_memory_mb() -> float:
    """Get current process memory usage in MB."""
    process = psutil.Process()
    return process.memory_info().rss / (1024 * 1024)


def estimate_batch_memory(
    num_items: int,
    item_size_mb: float,
    overhead_factor: float = 1.5
) -> float:
    """
    Estimate memory required for batch operation.
    
    Args:
        num_items: Number of items in batch
        item_size_mb: Estimated size per item in MB
        overhead_factor: Multiplier for overhead (default 1.5x)
    
    Returns:
        Estimated memory in MB
    """
    base_memory = num_items * item_size_mb
    estimated = base_memory * overhead_factor
    
    logger.debug(
        f"Batch memory estimate: {estimated:.2f}MB ({num_items} items × {item_size_mb}MB × {overhead_factor})",
        extra={
            "num_items": num_items,
            "item_size_mb": item_size_mb,
            "overhead_factor": overhead_factor,
            "estimated_mb": estimated
        }
    )
    
    return estimated


def suggest_batch_size(
    item_size_mb: float,
    max_memory_mb: int = 2048,
    overhead_factor: float = 1.5
) -> int:
    """
    Suggest safe batch size given item size and memory limit.
    
    Args:
        item_size_mb: Estimated size per item in MB
        max_memory_mb: Maximum memory to use in MB
        overhead_factor: Multiplier for overhead
    
    Returns:
        Recommended batch size
    """
    # Leave 512MB for other operations
    available = max_memory_mb - 512
    
    # Calculate batch size
    batch_size = int(available / (item_size_mb * overhead_factor))
    
    # Ensure at least 1
    batch_size = max(1, batch_size)
    
    logger.info(
        f"Recommended batch size: {batch_size} (item_size={item_size_mb}MB, limit={max_memory_mb}MB)",
        extra={
            "batch_size": batch_size,
            "item_size_mb": item_size_mb,
            "max_memory_mb": max_memory_mb
        }
    )
    
    return batch_size
