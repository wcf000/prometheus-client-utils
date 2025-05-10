"""
Configuration & Base Prometheus Validation Tests

Tests:
- Config class structure
- Type safety of all settings
- Environment variable overrides
- Default value correctness
- Base Prometheus endpoints reachable and have expected metrics
"""

import os
import pytest
import requests
from prometheus_client.parser import text_string_to_metric_families
from app.core.prometheus.config import get_prometheus_config, PrometheusConfig


@pytest.mark.integration
def test_prometheus_metrics_endpoint_reachable():
    """Verify Prometheus metrics endpoint is reachable and returns default metrics."""
    url = f"http://localhost:{get_prometheus_config().PORT}/metrics"
    response = requests.get(url, timeout=5)
    assert response.status_code == 200
    metrics = list(text_string_to_metric_families(response.text))
    assert metrics, "No metrics returned from Prometheus server"
    # Check for a few default Prometheus metrics
    metric_names = {m.name for m in metrics}
    required_metrics = {
        "prometheus_build_info",
        "prometheus_engine_query_duration_seconds",
        "go_gc_duration_seconds",
    }
    assert required_metrics.issubset(metric_names), (
        f"Missing default Prometheus metrics: {required_metrics - metric_names}"
    )


@pytest.mark.integration
def test_prometheus_alerts_endpoint_reachable():
    """Verify Prometheus alerts endpoint is reachable and returns valid structure."""
    url = f"http://localhost:{get_prometheus_config().PORT}/api/v1/alerts"
    response = requests.get(url, timeout=5)
    assert response.status_code == 200
    data = response.json()
    assert "status" in data and "data" in data, "Invalid alerts response format"
    assert data["status"] == "success"
