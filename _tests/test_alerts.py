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


