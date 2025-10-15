"""
Performance monitoring and metrics collection.

Tracks:
- Request latency and throughput
- Memory usage
- Error rates
- Database operation performance
- Cache hit rates
"""

import time
import psutil
import logging
from typing import Dict, Any, Optional, List
from collections import defaultdict, deque
from datetime import datetime, timedelta
from enum import Enum

logger = logging.getLogger(__name__)


class MetricType(str, Enum):
    """Types of metrics to track."""
    COUNTER = "counter"  # Incrementing value
    GAUGE = "gauge"  # Point-in-time value
    HISTOGRAM = "histogram"  # Distribution of values
    TIMER = "timer"  # Duration measurements


class MetricsCollector:
    """Collect and aggregate performance metrics."""
    
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        
        # Metric storage
        self.counters: Dict[str, int] = defaultdict(int)
        self.gauges: Dict[str, float] = {}
        self.histograms: Dict[str, deque] = defaultdict(lambda: deque(maxlen=max_history))
        self.timers: Dict[str, deque] = defaultdict(lambda: deque(maxlen=max_history))
        
        # Timestamps
        self.start_time = datetime.utcnow()
        self.last_reset = datetime.utcnow()
    
    def increment(self, metric_name: str, value: int = 1, tags: Optional[Dict[str, str]] = None):
        """Increment a counter metric."""
        key = self._make_key(metric_name, tags)
        self.counters[key] += value
    
    def gauge(self, metric_name: str, value: float, tags: Optional[Dict[str, str]] = None):
        """Set a gauge metric to specific value."""
        key = self._make_key(metric_name, tags)
        self.gauges[key] = value
    
    def histogram(self, metric_name: str, value: float, tags: Optional[Dict[str, str]] = None):
        """Add value to histogram."""
        key = self._make_key(metric_name, tags)
        self.histograms[key].append({
            "value": value,
            "timestamp": datetime.utcnow()
        })
    
    def timer(self, metric_name: str, duration_ms: float, tags: Optional[Dict[str, str]] = None):
        """Record timing measurement."""
        key = self._make_key(metric_name, tags)
        self.timers[key].append({
            "duration_ms": duration_ms,
            "timestamp": datetime.utcnow()
        })
    
    def _make_key(self, metric_name: str, tags: Optional[Dict[str, str]] = None) -> str:
        """Create metric key with tags."""
        if not tags:
            return metric_name
        
        tag_str = ",".join(f"{k}={v}" for k, v in sorted(tags.items()))
        return f"{metric_name}{{{tag_str}}}"
    
    def get_counter(self, metric_name: str, tags: Optional[Dict[str, str]] = None) -> int:
        """Get counter value."""
        key = self._make_key(metric_name, tags)
        return self.counters.get(key, 0)
    
    def get_gauge(self, metric_name: str, tags: Optional[Dict[str, str]] = None) -> Optional[float]:
        """Get gauge value."""
        key = self._make_key(metric_name, tags)
        return self.gauges.get(key)
    
    def get_histogram_stats(
        self,
        metric_name: str,
        tags: Optional[Dict[str, str]] = None
    ) -> Dict[str, float]:
        """Get histogram statistics (min, max, avg, p50, p95, p99)."""
        key = self._make_key(metric_name, tags)
        values = [entry["value"] for entry in self.histograms.get(key, [])]
        
        if not values:
            return {}
        
        sorted_values = sorted(values)
        count = len(sorted_values)
        
        return {
            "count": count,
            "min": sorted_values[0],
            "max": sorted_values[-1],
            "avg": sum(sorted_values) / count,
            "p50": sorted_values[int(count * 0.50)] if count > 0 else 0,
            "p95": sorted_values[int(count * 0.95)] if count > 0 else 0,
            "p99": sorted_values[int(count * 0.99)] if count > 0 else 0,
        }
    
    def get_timer_stats(
        self,
        metric_name: str,
        tags: Optional[Dict[str, str]] = None
    ) -> Dict[str, float]:
        """Get timer statistics."""
        key = self._make_key(metric_name, tags)
        durations = [entry["duration_ms"] for entry in self.timers.get(key, [])]
        
        if not durations:
            return {}
        
        sorted_durations = sorted(durations)
        count = len(sorted_durations)
        
        return {
            "count": count,
            "min_ms": sorted_durations[0],
            "max_ms": sorted_durations[-1],
            "avg_ms": sum(sorted_durations) / count,
            "p50_ms": sorted_durations[int(count * 0.50)] if count > 0 else 0,
            "p95_ms": sorted_durations[int(count * 0.95)] if count > 0 else 0,
            "p99_ms": sorted_durations[int(count * 0.99)] if count > 0 else 0,
        }
    
    def reset(self):
        """Reset all metrics."""
        self.counters.clear()
        self.gauges.clear()
        self.histograms.clear()
        self.timers.clear()
        self.last_reset = datetime.utcnow()
    
    def export_prometheus(self) -> str:
        """Export metrics in Prometheus format."""
        lines = []
        
        # Counters
        for key, value in self.counters.items():
            lines.append(f"{key} {value}")
        
        # Gauges
        for key, value in self.gauges.items():
            lines.append(f"{key} {value}")
        
        return "\n".join(lines)
    
    def export_json(self) -> Dict[str, Any]:
        """Export all metrics as JSON."""
        return {
            "uptime_seconds": (datetime.utcnow() - self.start_time).total_seconds(),
            "last_reset": self.last_reset.isoformat(),
            "counters": dict(self.counters),
            "gauges": dict(self.gauges),
            "histograms": {
                key: self.get_histogram_stats(key.split("{")[0])
                for key in self.histograms.keys()
            },
            "timers": {
                key: self.get_timer_stats(key.split("{")[0])
                for key in self.timers.keys()
            },
        }


# Global metrics collector
_metrics = MetricsCollector()


def get_metrics() -> MetricsCollector:
    """Get global metrics collector."""
    return _metrics


# System metrics collection

def collect_system_metrics():
    """Collect system-level metrics (CPU, memory, disk)."""
    metrics = get_metrics()
    
    # CPU usage
    cpu_percent = psutil.cpu_percent(interval=0.1)
    metrics.gauge("system_cpu_percent", cpu_percent)
    
    # Memory usage
    memory = psutil.virtual_memory()
    metrics.gauge("system_memory_used_mb", memory.used / (1024 * 1024))
    metrics.gauge("system_memory_percent", memory.percent)
    
    # Disk usage
    disk = psutil.disk_usage('/')
    metrics.gauge("system_disk_used_gb", disk.used / (1024 * 1024 * 1024))
    metrics.gauge("system_disk_percent", disk.percent)
    
    # Process metrics
    process = psutil.Process()
    metrics.gauge("process_memory_mb", process.memory_info().rss / (1024 * 1024))
    metrics.gauge("process_cpu_percent", process.cpu_percent())
    
    logger.debug(f"System metrics: CPU={cpu_percent}%, Memory={memory.percent}%, Process={process.memory_info().rss / (1024 * 1024):.1f}MB")


# Decorator for timing functions

class Timer:
    """Context manager and decorator for timing operations."""
    
    def __init__(self, metric_name: str, tags: Optional[Dict[str, str]] = None):
        self.metric_name = metric_name
        self.tags = tags
        self.start_time = None
        self.duration_ms = None
    
    def __enter__(self):
        self.start_time = time.perf_counter()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.perf_counter()
        self.duration_ms = (end_time - self.start_time) * 1000
        
        # Record metric
        metrics = get_metrics()
        metrics.timer(self.metric_name, self.duration_ms, self.tags)
        
        # Log slow operations (>2s)
        if self.duration_ms > 2000:
            logger.warning(
                f"Slow operation: {self.metric_name} took {self.duration_ms:.2f}ms",
                extra={"metric": self.metric_name, "duration_ms": self.duration_ms}
            )
    
    def __call__(self, func):
        """Use as decorator."""
        async def async_wrapper(*args, **kwargs):
            with self:
                return await func(*args, **kwargs)
        
        def sync_wrapper(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        
        # Return appropriate wrapper based on function type
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper


# Pre-defined metric helpers

def track_request(endpoint: str, method: str, status_code: int, duration_ms: float):
    """Track HTTP request metrics."""
    metrics = get_metrics()
    
    tags = {
        "endpoint": endpoint,
        "method": method,
        "status": str(status_code)
    }
    
    metrics.increment("http_requests_total", tags=tags)
    metrics.timer("http_request_duration", duration_ms, tags)
    
    if status_code >= 400:
        metrics.increment("http_errors_total", tags=tags)


def track_document_processing(stage: str, duration_ms: float, success: bool):
    """Track document processing metrics."""
    metrics = get_metrics()
    
    tags = {
        "stage": stage,
        "success": str(success)
    }
    
    metrics.increment("document_processing_total", tags=tags)
    metrics.timer("document_processing_duration", duration_ms, tags)


def track_vector_search(collection: str, results_count: int, duration_ms: float):
    """Track vector search metrics."""
    metrics = get_metrics()
    
    tags = {"collection": collection}
    
    metrics.increment("vector_search_total", tags=tags)
    metrics.timer("vector_search_duration", duration_ms, tags)
    metrics.histogram("vector_search_results", results_count, tags)


def track_graph_query(query_type: str, duration_ms: float, nodes_returned: int):
    """Track graph query metrics."""
    metrics = get_metrics()
    
    tags = {"query_type": query_type}
    
    metrics.increment("graph_queries_total", tags=tags)
    metrics.timer("graph_query_duration", duration_ms, tags)
    metrics.histogram("graph_query_nodes", nodes_returned, tags)


def track_cache(operation: str, hit: bool):
    """Track cache operations."""
    metrics = get_metrics()
    
    tags = {
        "operation": operation,
        "hit": str(hit)
    }
    
    metrics.increment("cache_operations_total", tags=tags)
    
    if hit:
        metrics.increment("cache_hits_total", tags={"operation": operation})
    else:
        metrics.increment("cache_misses_total", tags={"operation": operation})
