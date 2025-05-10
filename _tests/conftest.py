"""
Test Configuration

Sets up fixtures for all Prometheus tests with production-grade reliability
"""

import os
import subprocess
import time

import pytest
import requests

from app.core.prometheus.config import PrometheusConfig


@pytest.fixture(scope="module")
def prometheus_service():
    """
    Ensure Prometheus container is running for tests.
    If not running, start it via docker-compose. Wait for readiness, yield base_url, and clean up if started.
    """
    base_url = PrometheusConfig.SERVICE_URL
    timeout = PrometheusConfig.HEALTH_TIMEOUT
    compose_file = os.path.join(os.path.dirname(__file__), "..", "docker", "docker-compose.prometheus.yml")
    compose_file = os.path.abspath(compose_file)
    container_name = "prometheus"
    started_by_fixture = False

    def is_container_running():
        try:
            result = subprocess.run([
                "docker", "ps", "--filter", f"name={container_name}", "--filter", "status=running", "--format", "{{.Names}}"
            ], capture_output=True, text=True, check=True)
            return container_name in result.stdout
        except Exception:
            return False

    if not is_container_running():
        # Start Prometheus via docker-compose
        subprocess.run([
            "docker-compose", "-f", compose_file, "up", "-d", container_name
        ], check=True)
        started_by_fixture = True

    # Wait for Prometheus to be healthy
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            if requests.get(f"{base_url}/-/ready").status_code == 200:
                yield base_url
                break
        except requests.exceptions.ConnectionError:
            time.sleep(1)
    else:
        # Timed out
        if started_by_fixture:
            subprocess.run([
                "docker-compose", "-f", compose_file, "down"
            ], check=False)
        pytest.fail("Prometheus service is not reachable")

    # Teardown: stop container if started by fixture
    if started_by_fixture:
        subprocess.run([
            "docker-compose", "-f", compose_file, "down"
        ], check=False)
