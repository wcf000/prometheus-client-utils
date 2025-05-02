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

# System metrics
SYSTEM_CPU_USAGE = Gauge(
    'system_cpu_usage_percent',
    'System CPU usage percentage'
)
