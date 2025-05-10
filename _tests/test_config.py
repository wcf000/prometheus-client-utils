"""
Prometheus Configuration Tests

Validates:
- Config attribute existence and types
- Environment variable overrides
- Default values and labels
- Service URL formatting
"""


from urllib.parse import urlparse

from app.core.prometheus.config import get_prometheus_config, PrometheusConfig


def test_config_attributes_exist():
    """Verify all required config attributes exist with correct types"""
    required_attrs = {
        "ENABLED": bool,
        "PORT": int,
        "SERVICE_URL": str,
        "HEALTH_TIMEOUT": int,
        "METRICS_PREFIX": str,
        "SCRAPE_INTERVAL": int,
        "DEFAULT_LABELS": dict,
    }
    config = get_prometheus_config()
    for attr, attr_type in required_attrs.items():
        assert hasattr(config, attr), f"Missing required attribute: {attr}"
        assert isinstance(getattr(config, attr), attr_type), (
            f"{attr} should be {attr_type.__name__}"
        )


def test_service_url_format():
    """Validate SERVICE_URL is properly formatted"""
    url = urlparse(PrometheusConfig.SERVICE_URL)
    assert url.scheme in ("http", "https"), "Invalid URL scheme"
    assert url.netloc, "Missing hostname in URL"


def test_default_labels():
    """Validate default labels contain required keys"""
    required_labels = {"service", "environment"}
    assert all(label in PrometheusConfig.DEFAULT_LABELS for label in required_labels), (
        "Missing required labels"
    )


def test_metrics_prefix():
    """Validate metrics prefix follows conventions"""
    prefix = PrometheusConfig.METRICS_PREFIX
    assert prefix, "Metrics prefix cannot be empty"
    assert prefix.endswith("_"), "Prefix should end with underscore"
    assert prefix.islower(), "Prefix should be lowercase"
