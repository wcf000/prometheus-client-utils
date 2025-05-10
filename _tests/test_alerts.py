"""
Configuration Validation Tests

Tests:
- Config class structure
- Type safety of all settings
- Environment variable overrides
- Default value correctness
"""

import os

from app.core.prometheus.config import get_prometheus_config, PrometheusConfig


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


def test_environment_overrides():
    """Verify environment variables override defaults"""
    from importlib import reload
    import app.core.prometheus.config as prom_config_mod

    orig_enabled = get_prometheus_config().ENABLED
    orig_port = get_prometheus_config().PORT

    try:
        os.environ["PROMETHEUS_ENABLED"] = "false"
        os.environ["PROMETHEUS_PORT"] = "9999"

        # Reset singleton and reload config to pick up env changes
        if hasattr(prom_config_mod, '_prometheus_config_instance'):
            prom_config_mod._prometheus_config_instance = None
        config = prom_config_mod.get_prometheus_config()

        assert config.ENABLED is False
        assert config.PORT == 9999
    finally:
        os.environ.pop("PROMETHEUS_ENABLED", None)
        os.environ.pop("PROMETHEUS_PORT", None)
        # Restore original values
        if hasattr(prom_config_mod, '_prometheus_config_instance'):
            prom_config_mod._prometheus_config_instance = None



def test_default_labels():
    """Verify default labels contain required keys"""
    required_labels = {"service", "environment"}
    assert all(key in PrometheusConfig.DEFAULT_LABELS for key in required_labels), (
        "Missing required default labels"
    )
