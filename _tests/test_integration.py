"""
Prometheus Integration Tests

Tests:
- Metric collection and formatting
- Alert evaluation
- Endpoint availability
- Performance under load
"""

import time

import pytest
import requests
from prometheus_client.parser import text_string_to_metric_families
from requests.exceptions import RequestException

from app.core.prometheus.config import get_prometheus_config


@pytest.mark.integration
def test_metrics_endpoint(prometheus_service):
    """Verify metrics endpoint returns valid metrics"""
    max_retries = 3
    timeout = get_prometheus_config().HEALTH_TIMEOUT
    metrics_url = f"{prometheus_service}/metrics"

    for attempt in range(max_retries):
        try:
            response = requests.get(metrics_url, timeout=timeout)
            response.raise_for_status()

            # Validate metrics format
            metrics = list(text_string_to_metric_families(response.text))
            assert metrics, "No metrics returned"

            # Check for required metrics
            # Only check metrics always present in default Prometheus server
            required_metrics = {
                "prometheus_build_info",
                "prometheus_engine_query_duration_seconds",
                "go_gc_duration_seconds",
            }  # These are always present in a vanilla Prometheus instance
            metric_names = {m.name for m in metrics}
            assert required_metrics.issubset(metric_names), (
                f"Missing required metrics: {required_metrics - metric_names}"
            )
            return

        except RequestException as e:
            if attempt == max_retries - 1:
                pytest.fail(
                    f"Metrics endpoint failed after {max_retries} attempts: {str(e)}"
                )
            time.sleep(1)


@pytest.mark.integration
def test_alerts_endpoint(prometheus_service):
    """Verify alerts endpoint returns valid data"""
    response = requests.get(
        f"{prometheus_service}/api/v1/alerts", timeout=get_prometheus_config().HEALTH_TIMEOUT
    )
    assert response.status_code == 200
    assert "data" in response.json(), "Invalid alerts response format"


@pytest.mark.performance
def test_metrics_endpoint_performance(prometheus_service):
    """Verify metrics endpoint responds within acceptable time"""
    start_time = time.time()
    response = requests.get(f"{prometheus_service}/metrics")
    response_time = time.time() - start_time

    assert response_time < 1.0, "Metrics endpoint too slow"
    assert response.status_code == 200
