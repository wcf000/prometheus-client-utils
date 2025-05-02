"""
Configuration Validation Tests

Tests:
- Config class structure
- Type safety of all settings
- Environment variable overrides
- Default value correctness
"""

import os

from app.core.prometheus.config import PrometheusConfig


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

    for attr, attr_type in required_attrs.items():
        assert hasattr(PrometheusConfig, attr), f"Missing config attribute: {attr}"
        assert isinstance(getattr(PrometheusConfig, attr), attr_type), (
            f"Invalid type for {attr}, expected {attr_type}"
        )


def test_environment_overrides():
    """Verify environment variables override defaults"""
    original_enabled = PrometheusConfig.ENABLED
    original_port = PrometheusConfig.PORT

    try:
        os.environ["PROMETHEUS_ENABLED"] = "false"
        os.environ["PROMETHEUS_PORT"] = "9999"

        # Re-import to get fresh config with new env vars
        from importlib import reload
        from app.core.prometheus import config

        reload(config)

        assert config.PrometheusConfig.ENABLED is False
        assert config.PrometheusConfig.PORT == 9999
    finally:
        # Clean up
        os.environ.pop("PROMETHEUS_ENABLED", None)
        os.environ.pop("PROMETHEUS_PORT", None)
        # Restore original values
        from app.core.prometheus import config

        reload(config)


def test_default_labels():
    """Verify default labels contain required keys"""
    required_labels = {"service", "environment"}
    assert all(key in PrometheusConfig.DEFAULT_LABELS for key in required_labels), (
        "Missing required default labels"
    )
