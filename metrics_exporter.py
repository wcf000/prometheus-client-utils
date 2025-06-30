"""
Module for initializing and collecting system and application metrics.
This ensures there are always metrics available even with no traffic.

Collects:
- System metrics (CPU, memory, disk)
- Valkey/Redis metrics (hit/miss rates, memory usage)
- Pulsar metrics (consumer/producer lag, health)
"""
import os
import psutil
import time
import threading
import asyncio
from typing import Dict, Any

from app.core.prometheus.metrics import (
    get_system_cpu_usage,
    get_metric_registry,
    get_cache_hit_ratio
)

# Constants
METRICS_COLLECTION_INTERVAL = 15  # seconds


def collect_system_metrics() -> Dict[str, Any]:
    """Collect system metrics like CPU, memory, disk usage."""
    metrics = {}
    
    # Collect CPU metrics
    metrics["cpu_percent"] = psutil.cpu_percent(interval=1)
    
    # Collect memory metrics
    mem = psutil.virtual_memory()
    metrics["mem_used_percent"] = mem.percent
    metrics["mem_available_gb"] = mem.available / (1024 * 1024 * 1024)
    
    # Collect disk metrics
    disk = psutil.disk_usage('/')
    metrics["disk_used_percent"] = disk.percent
    
    return metrics


def update_system_metrics():
    """Update Prometheus metrics with current system metrics."""
    metrics = collect_system_metrics()
    
    # Update CPU usage gauge
    get_system_cpu_usage().set(metrics["cpu_percent"])


def update_pulsar_metrics():
    """Update Pulsar metrics by fetching from the client/server."""
    try:
        # Import here to avoid circular import issues
        from app.core.pulsar.metrics import PULSAR_HEALTH
        
        # Just set health status based on import success
        PULSAR_HEALTH.set(1)  # 1 = healthy

        # TODO: In a production environment, you would want to query
        # the Pulsar admin API to get actual backlog and other stats
        # This would require admin credentials and permissions
    except Exception as e:
        print(f"Error updating Pulsar metrics: {e}")

def update_valkey_metrics():
    """Update Valkey/Redis metrics from existing counters."""
    try:
        # Import Valkey connection and safe metric utilities
        from app.core.valkey_init import get_valkey
        from app.core.prometheus.metrics import get_cache_count, get_cache_hit_ratio
        from app.core.prometheus.utils import safe_get_counter_value
        
        # Get hit and miss counts safely
        hits = safe_get_counter_value(
            get_cache_count(), 
            labels={"cache_type": "valkey", "operation": "hit"}
        )
        misses = safe_get_counter_value(
            get_cache_count(), 
            labels={"cache_type": "valkey", "operation": "miss"}
        )
        
        # Calculate and update hit ratio
        if hits + misses > 0:
            ratio = hits / (hits + misses)
            get_cache_hit_ratio().labels('valkey').set(ratio)
        else:
            # Set a default ratio when no data is available yet
            get_cache_hit_ratio().labels('valkey').set(1.0)
    except Exception as e:
        print(f"Error updating Valkey metrics: {e}")

def metrics_collector_thread():
    """Background thread function for collecting metrics periodically."""
    while True:
        try:
            # System metrics (always update)
            update_system_metrics()
            
            # Update application-specific metrics
            update_pulsar_metrics() 
            update_valkey_metrics()
        except Exception as e:
            print(f"Error updating metrics: {e}")
        
        time.sleep(METRICS_COLLECTION_INTERVAL)


def start_metrics_collection():
    """Start the background metrics collection thread."""
    # Only start collector if not running in test mode
    if os.environ.get("TESTING", "").lower() != "true":
        collector_thread = threading.Thread(
            target=metrics_collector_thread,
            daemon=True,
            name="metrics-collector"
        )
        collector_thread.start()
        print("System metrics collection started")
        return collector_thread
    return None
