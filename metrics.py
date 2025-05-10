"""
Prometheus metrics configuration following best practices from:
- alerting.md
- dos_donts.md 
- instrumentation.md
"""
from prometheus_client import Counter, Gauge, Histogram, CollectorRegistry

# Singleton registry and metric instances
_metric_registry = None
_request_count = None
_request_latency = None
_celery_task_count = None
_celery_task_latency = None
_celery_cache_hits = None
_celery_cache_misses = None
_celery_cache_sets = None
_celery_cache_deletes = None
_system_cpu_usage = None

def get_metric_registry():
    global _metric_registry
    if _metric_registry is None:
        _metric_registry = CollectorRegistry()
    return _metric_registry

def get_request_count():
    global _request_count
    if _request_count is None:
        _request_count = Counter(
            'http_requests_total',
            'Total HTTP Requests',
            ['method', 'status'],
            registry=get_metric_registry()
        )
    return _request_count

def get_request_latency():
    global _request_latency
    if _request_latency is None:
        _request_latency = Histogram(
            'http_request_duration_seconds',
            'HTTP request latency',
            ['method', 'endpoint'],
            registry=get_metric_registry()
        )
    return _request_latency

def get_celery_task_count():
    global _celery_task_count
    if _celery_task_count is None:
        _celery_task_count = Counter(
            'celery_tasks_total',
            'Total Celery tasks executed',
            ['task_name', 'status'],
            registry=get_metric_registry()
        )
    return _celery_task_count

def get_celery_task_latency():
    global _celery_task_latency
    if _celery_task_latency is None:
        _celery_task_latency = Histogram(
            'celery_task_duration_seconds',
            'Celery task execution time',
            ['task_name'],
            registry=get_metric_registry()
        )
    return _celery_task_latency

def get_celery_cache_hits():
    global _celery_cache_hits
    if _celery_cache_hits is None:
        _celery_cache_hits = Counter(
            'celery_cache_hits_total',
            'Number of cache hits inside Celery tasks',
            ['task_name'],
            registry=get_metric_registry()
        )
    return _celery_cache_hits

def get_celery_cache_misses():
    global _celery_cache_misses
    if _celery_cache_misses is None:
        _celery_cache_misses = Counter(
            'celery_cache_misses_total',
            'Number of cache misses inside Celery tasks',
            ['task_name'],
            registry=get_metric_registry()
        )
    return _celery_cache_misses

def get_celery_cache_sets():
    global _celery_cache_sets
    if _celery_cache_sets is None:
        _celery_cache_sets = Counter(
            'celery_cache_sets_total',
            'Number of cache set operations inside Celery tasks',
            ['task_name'],
            registry=get_metric_registry()
        )
    return _celery_cache_sets

def get_celery_cache_deletes():
    global _celery_cache_deletes
    if _celery_cache_deletes is None:
        _celery_cache_deletes = Counter(
            'celery_cache_deletes_total',
            'Number of cache delete operations inside Celery tasks',
            ['task_name'],
            registry=get_metric_registry()
        )
    return _celery_cache_deletes

def get_system_cpu_usage():
    global _system_cpu_usage
    if _system_cpu_usage is None:
        _system_cpu_usage = Gauge(
            'system_cpu_usage_percent',
            'System CPU usage percentage',
            registry=get_metric_registry()
        )
    return _system_cpu_usage

# todo: Refactor remaining metrics below to use the same singleton getter pattern.

# Pulsar cache metrics (singleton getter pattern)
_pulsar_cache_hits = None
_pulsar_cache_misses = None
_pulsar_cache_sets = None
_pulsar_cache_deletes = None

def get_pulsar_cache_hits():
    global _pulsar_cache_hits
    if _pulsar_cache_hits is None:
        _pulsar_cache_hits = Counter(
            'pulsar_cache_hits_total',
            'Number of cache hits for Pulsar operations',
            registry=get_metric_registry()
        )
    return _pulsar_cache_hits

def get_pulsar_cache_misses():
    global _pulsar_cache_misses
    if _pulsar_cache_misses is None:
        _pulsar_cache_misses = Counter(
            'pulsar_cache_misses_total',
            'Number of cache misses for Pulsar operations',
            registry=get_metric_registry()
        )
    return _pulsar_cache_misses

def get_pulsar_cache_sets():
    global _pulsar_cache_sets
    if _pulsar_cache_sets is None:
        _pulsar_cache_sets = Counter(
            'pulsar_cache_sets_total',
            'Number of cache sets for Pulsar operations',
            registry=get_metric_registry()
        )
    return _pulsar_cache_sets

def get_pulsar_cache_deletes():
    global _pulsar_cache_deletes
    if _pulsar_cache_deletes is None:
        _pulsar_cache_deletes = Counter(
            'pulsar_cache_deletes_total',
            'Number of cache deletes for Pulsar operations',
            registry=get_metric_registry()
        )
    return _pulsar_cache_deletes


# VALKEY cache metrics (singleton getter pattern)
_redis_cache_hits = None
_redis_cache_misses = None
_redis_cache_sets = None
_redis_cache_deletes = None
_redis_cache_errors = None

def get_redis_cache_hits():
    global _redis_cache_hits
    if _redis_cache_hits is None:
        _redis_cache_hits = Counter(
            'redis_cache_hits_total',
            'Number of cache hits for Redis operations',
            registry=get_metric_registry()
        )
    return _redis_cache_hits

def get_redis_cache_misses():
    global _redis_cache_misses
    if _redis_cache_misses is None:
        _redis_cache_misses = Counter(
            'redis_cache_misses_total',
            'Number of cache misses for Redis operations',
            registry=get_metric_registry()
        )
    return _redis_cache_misses

def get_redis_cache_sets():
    global _redis_cache_sets
    if _redis_cache_sets is None:
        _redis_cache_sets = Counter(
            'redis_cache_sets_total',
            'Number of cache sets for Redis operations',
            registry=get_metric_registry()
        )
    return _redis_cache_sets

def get_redis_cache_deletes():
    global _redis_cache_deletes
    if _redis_cache_deletes is None:
        _redis_cache_deletes = Counter(
            'redis_cache_deletes_total',
            'Number of cache deletes for Redis operations',
            registry=get_metric_registry()
        )
    return _redis_cache_deletes

def get_redis_cache_errors():
    global _redis_cache_errors
    if _redis_cache_errors is None:
        _redis_cache_errors = Counter(
            'redis_cache_errors_total',
            'Number of errors during Redis cache operations',
            registry=get_metric_registry()
        )
    return _redis_cache_errors

# VALKEY cache metrics (singleton getter pattern)
_valkey_cache_hits = None
_valkey_cache_misses = None
_valkey_cache_sets = None
_valkey_cache_deletes = None
_valkey_cache_errors = None

def get_valkey_cache_hits():
    global _valkey_cache_hits
    if _valkey_cache_hits is None:
        _valkey_cache_hits = Counter(
            'valkey_cache_hits_total',
            'Number of cache hits for VALKEY operations',
            registry=get_metric_registry()
        )
    return _valkey_cache_hits

def get_valkey_cache_misses():
    global _valkey_cache_misses
    if _valkey_cache_misses is None:
        _valkey_cache_misses = Counter(
            'valkey_cache_misses_total',
            'Number of cache misses for VALKEY operations',
            registry=get_metric_registry()
        )
    return _valkey_cache_misses

def get_valkey_cache_sets():
    global _valkey_cache_sets
    if _valkey_cache_sets is None:
        _valkey_cache_sets = Counter(
            'valkey_cache_sets_total',
            'Number of cache sets for VALKEY operations',
            registry=get_metric_registry()
        )
    return _valkey_cache_sets

def get_valkey_cache_deletes():
    global _valkey_cache_deletes
    if _valkey_cache_deletes is None:
        _valkey_cache_deletes = Counter(
            'valkey_cache_deletes_total',
            'Number of cache deletes for VALKEY operations',
            registry=get_metric_registry()
        )
    return _valkey_cache_deletes

def get_valkey_cache_errors():
    global _valkey_cache_errors
    if _valkey_cache_errors is None:
        _valkey_cache_errors = Counter(
            'valkey_cache_errors_total',
            'Number of errors during VALKEY cache operations',
            registry=get_metric_registry()
        )
    return _valkey_cache_errors
