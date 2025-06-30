"""
Prometheus metrics package for FastAPI applications.

This package provides utilities for instrumenting FastAPI applications
with Prometheus metrics. It includes middleware, configuration, and metric
definitions following Prometheus best practices.
"""
from app.core.prometheus.metrics import get_metric_registry
from app.core.prometheus.middleware import PrometheusMiddleware
from app.core.prometheus.config import get_prometheus_config

# Make sure the config is initialized at import time
prometheus_config = get_prometheus_config()

# By default, metrics should be enabled
if not hasattr(prometheus_config, 'ENABLED'):
    prometheus_config.ENABLED = True

__all__ = ['get_metric_registry', 'PrometheusMiddleware', 'get_prometheus_config']
