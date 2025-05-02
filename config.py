from app.core.config import Settings


class PrometheusConfig:
    """Prometheus-specific configuration"""

    # Import from main settings
    ENABLED: bool = Settings.PROMETHEUS_ENABLED
    PORT: int = Settings.PROMETHEUS_PORT
    SERVICE_URL: str = Settings.PROMETHEUS_SERVICE_URL

    # Additional configurations
    HEALTH_TIMEOUT: int = 30
    METRICS_PREFIX: str = "lead_ignite_"
    SCRAPE_INTERVAL: int = 15
    DEFAULT_LABELS: dict = {"service": "lead_ignite", "environment": "production"}
