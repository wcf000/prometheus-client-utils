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

# DB metrics
_db_count = None
_db_latency = None
_connection_metrics = None

# Event metrics
_event_count = None
_event_latency = None

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
            ['method', 'endpoint', 'status'],
            registry=get_metric_registry()
        )
    return _request_count

def get_request_latency():
    global _request_latency
    if _request_latency is None:
        _request_latency = Histogram(
            'http_request_duration_seconds',
            'HTTP request latency',
            ['method', 'endpoint', 'status'],
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

# Database metrics
def get_db_count():
    global _db_count
    if _db_count is None:
        _db_count = Counter(
            'db_operations_total',
            'Database operations (queries, commits, rollbacks)',
            ['operation'],
            registry=get_metric_registry()
        )
    return _db_count

def get_db_latency():
    global _db_latency
    if _db_latency is None:
        _db_latency = Histogram(
            'db_operation_duration_seconds',
            'Database operation latency in seconds',
            registry=get_metric_registry(),
            buckets=(0.001, 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0)
        )
    return _db_latency

def get_connection_metrics():
    global _connection_metrics
    if _connection_metrics is None:
        _connection_metrics = Gauge(
            'db_connections',
            'Database connection metrics',
            ['db_type', 'state'],
            registry=get_metric_registry()
        )
    return _connection_metrics

# Event metrics
def get_event_count():
    global _event_count
    if _event_count is None:
        _event_count = Counter(
            'events_total',
            'Total events published or consumed',
            ['topic', 'result'],
            registry=get_metric_registry()
        )
    return _event_count

def get_event_latency():
    global _event_latency
    if _event_latency is None:
        _event_latency = Histogram(
            'event_operation_duration_seconds',
            'Event operation latency in seconds',
            ['topic'],
            registry=get_metric_registry(),
            buckets=(0.001, 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0)
        )
    return _event_latency

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

# Unified cache metrics for Redis/Valkey
# Counter for cache operations
_cache_count = None
_cache_latency = None

def get_cache_count():
    global _cache_count
    if _cache_count is None:
        _cache_count = Counter(
            'cache_operations_total',
            'Cache operations (hit/miss/set/delete) for Redis/Valkey',
            ['cache_type', 'operation'],
            registry=get_metric_registry()
        )
    return _cache_count

def get_cache_latency():
    global _cache_latency
    if _cache_latency is None:
        _cache_latency = Histogram(
            'cache_operation_duration_seconds',
            'Cache operation latency in seconds for Redis/Valkey',
            ['cache_type', 'operation'],
            registry=get_metric_registry()
        )
    return _cache_latency

# Deprecated: Moved to app.core.pulsar.metrics
# Import the proper one from there instead
# This is kept here temporarily for backward compatibility
# PULSAR_CONSUMER_LAG = Gauge(...)

# Cache hit rate metrics for Redis/Valkey
_cache_hit_ratio = None

def get_cache_hit_ratio():
    """Get cache hit ratio gauge (hits / (hits + misses))"""
    global _cache_hit_ratio
    if _cache_hit_ratio is None:
        _cache_hit_ratio = Gauge(
            'cache_hit_ratio',
            'Cache hit ratio (hits / (hits + misses)) for Redis/Valkey',
            ['cache_type'],
            registry=get_metric_registry()
        )
    return _cache_hit_ratio

# Grafana queries (examples):
# API performance: rate(http_requests_total[5m]) by (method, endpoint, status)
# API latency: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, method, endpoint, status))
# Cache hit/miss: sum(rate(cache_operations_total{operation=~"hit|miss"}[5m])) by (cache_type, operation)
# Pulsar consumer lag: max(pulsar_consumer_lag_seconds) by (topic, subscription)
# Pulsar producer: rate(pulsar_messages_sent[5m]) by (topic)
# Pulsar consumer: rate(pulsar_messages_received[5m]) by (topic)
# DB latency: histogram_quantile(0.95, sum(rate(db_operation_duration_seconds_bucket[5m])) by (le))
# DB connections: sum(db_connections) by (db_type, state)
# Event publish: rate(events_total{result="success"}[5m]) by (topic)
