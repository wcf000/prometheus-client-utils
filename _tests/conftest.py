"""
Test Configuration

Sets up fixtures for all Prometheus tests with production-grade reliability
"""

import time

import pytest
import requests

from app.core.prometheus.config import PrometheusConfig


@pytest.fixture(scope="module")
def prometheus_service():
    """Connect to existing Prometheus service with health checks"""
    base_url = PrometheusConfig.SERVICE_URL
    timeout = PrometheusConfig.HEALTH_TIMEOUT

    # Verify service is reachable
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            if requests.get(f"{base_url}/-/ready").status_code == 200:
                yield base_url
                return
        except requests.exceptions.ConnectionError:
            time.sleep(1)

    pytest.fail("Prometheus service is not reachable")
