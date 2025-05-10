from typing import Any

from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings


class PrometheusConfig(BaseSettings):
    """
    Prometheus-specific configuration with env support (Pydantic v2).
    All fields can be overridden by environment variables.
    """
    ENABLED: bool = Field(default=True, validation_alias="PROMETHEUS_ENABLED")
    PORT: int = Field(default=9090, validation_alias="PROMETHEUS_PORT")
    SERVICE_URL: str = Field(default="http://localhost:9090", validation_alias="PROMETHEUS_SERVICE_URL")
    HEALTH_TIMEOUT: int = Field(default=30, validation_alias="PROMETHEUS_HEALTH_TIMEOUT")
    METRICS_PREFIX: str = Field(default="lead_ignite_", validation_alias="PROMETHEUS_METRICS_PREFIX")
    SCRAPE_INTERVAL: int = Field(default=15, validation_alias="PROMETHEUS_SCRAPE_INTERVAL")
    DEFAULT_LABELS: dict[str, Any] = Field(default_factory=lambda: {"service": "lead_ignite", "environment": "production"}, validation_alias="PROMETHEUS_DEFAULT_LABELS")

    model_config = ConfigDict(
        env_prefix="",  # No prefix for direct mapping
        extra="ignore"
    )

# Singleton instance for app/tests
_prometheus_config_instance: PrometheusConfig | None = None

def get_prometheus_config() -> PrometheusConfig:
    global _prometheus_config_instance
    if _prometheus_config_instance is None:
        _prometheus_config_instance = PrometheusConfig()
    return _prometheus_config_instance
