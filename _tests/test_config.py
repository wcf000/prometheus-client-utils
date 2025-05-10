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
    config = get_prometheus_config()
    url = urlparse(config.SERVICE_URL)
    assert url.scheme in ("http", "https"), "SERVICE_URL must have valid scheme"
    assert url.hostname, "SERVICE_URL must have a hostname"


def test_default_labels():
    """Validate default labels contain required keys"""
    required_labels = {"service", "environment"}
    config = get_prometheus_config()
    assert all(label in config.DEFAULT_LABELS for label in required_labels), (
        "Missing required labels"
    )


def test_metrics_prefix():
    """Validate metrics prefix follows conventions"""
    config = get_prometheus_config()
    prefix = config.METRICS_PREFIX
    assert prefix, "Metrics prefix cannot be empty"
    assert prefix.endswith("_"), "Prefix should end with underscore"
    assert prefix.islower(), "Prefix should be lowercase"



def test_config_structure():
    """Verify all required config attributes exist"""
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
        assert hasattr(config, attr), f"Missing config attribute: {attr}"
        assert isinstance(getattr(config, attr), attr_type), (
            f"Invalid type for {attr}, expected {attr_type}"
        )




def test_environment_overrides(monkeypatch):
    """Verify environment variables override defaults"""
    monkeypatch.setenv("PROMETHEUS_ENABLED", "false")
    monkeypatch.setenv("PROMETHEUS_PORT", "9999")

    # Import config module and reset singleton AFTER setting env
    import app.core.prometheus.config as prom_config_mod
    if hasattr(prom_config_mod, '_prometheus_config_instance'):
        prom_config_mod._prometheus_config_instance = None

    config = prom_config_mod.get_prometheus_config()

    import os
    print("PROMETHEUS_ENABLED env:", os.environ.get("PROMETHEUS_ENABLED"))
    print("Config ENABLED:", config.ENABLED)
    print("Config dict:", config.model_dump())

    assert config.ENABLED is False, f"ENABLED should be False, got {config.ENABLED!r}"
    assert config.PORT == 9999, f"PORT should be 9999, got {config.PORT!r}"

    # Clean up (monkeypatch handles env cleanup automatically)
    if hasattr(prom_config_mod, '_prometheus_config_instance'):
        prom_config_mod._prometheus_config_instance = None

