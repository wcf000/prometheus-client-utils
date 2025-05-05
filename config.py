from app.core.config import Settings


class PrometheusConfig:
    """Prometheus-specific configuration"""

    @property
    def ENABLED(self) -> bool:
        return Settings.monitoring.PROMETHEUS_ENABLED

    @property
    def PORT(self) -> int:
        return Settings.monitoring.PROMETHEUS_PORT

    @property
    def SERVICE_URL(self) -> str:
        return Settings.monitoring.PROMETHEUS_SERVICE_URL

    # Additional configurations
    HEALTH_TIMEOUT: int = 30
    METRICS_PREFIX: str = "lead_ignite_"
    SCRAPE_INTERVAL: int = 15
    DEFAULT_LABELS: dict = {"service": "lead_ignite", "environment": "production"}
