"""
Prometheus metrics configuration following best practices from:
- alerting.md
- dos_donts.md 
- instrumentation.md
"""
from prometheus_client import Counter, Gauge, Histogram

# Request metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP Requests',
    ['method', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

# Celery metrics
CELERY_TASK_COUNT = Counter(
    'celery_tasks_total',
    'Total Celery tasks executed',
    ['task_name', 'status']
)

CELERY_TASK_LATENCY = Histogram(
    'celery_task_duration_seconds',
    'Celery task execution time',
    ['task_name']
)

# Celery cache metrics
CELERY_CACHE_HITS = Counter(
    'celery_cache_hits_total',
    'Number of cache hits inside Celery tasks',
    ['task_name']
)
CELERY_CACHE_MISSES = Counter(
    'celery_cache_misses_total',
    'Number of cache misses inside Celery tasks',
    ['task_name']
)
CELERY_CACHE_SETS = Counter(
    'celery_cache_sets_total',
    'Number of cache set operations inside Celery tasks',
    ['task_name']
)
CELERY_CACHE_DELETES = Counter(
    'celery_cache_deletes_total',
    'Number of cache delete operations inside Celery tasks',
    ['task_name']
)

# System metrics
SYSTEM_CPU_USAGE = Gauge(
    'system_cpu_usage_percent',
    'System CPU usage percentage'
)

# Pulsar cache metrics
PULSAR_CACHE_HITS = Counter(
    'pulsar_cache_hits_total',
    'Number of cache hits for Pulsar operations'
)
PULSAR_CACHE_MISSES = Counter(
    'pulsar_cache_misses_total',
    'Number of cache misses for Pulsar operations'
)
PULSAR_CACHE_SETS = Counter(
    'pulsar_cache_sets_total',
    'Number of cache sets for Pulsar operations'
)
PULSAR_CACHE_DELETES = Counter(
    'pulsar_cache_deletes_total',
    'Number of cache deletes for Pulsar operations'
)

# VALKEY cache metrics
VALKEY_CACHE_HITS = Counter(
    'valkey_cache_hits_total',
    'Number of cache hits for VALKEY operations'
)
VALKEY_CACHE_MISSES = Counter(
    'valkey_cache_misses_total',
    'Number of cache misses for VALKEY operations'
)
VALKEY_CACHE_SETS = Counter(
    'valkey_cache_sets_total',
    'Number of cache sets for VALKEY operations'
)
VALKEY_CACHE_DELETES = Counter(
    'valkey_cache_deletes_total',
    'Number of cache deletes for VALKEY operations'
)
VALKEY_CACHE_ERRORS = Counter(
    'valkey_cache_errors_total',
    'Number of errors during VALKEY cache operations'
)
