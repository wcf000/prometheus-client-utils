# Prometheus Integration & Testing Guide

This guide explains how to run and validate Prometheus integration in the Lead Ignite backend.

---

## 1. Prerequisites
- Docker & Docker Compose installed
- Poetry environment set up (`poetry install`)
- Prometheus config files in `app/core/prometheus/docker/`

---

## 2. Start Prometheus Locally

Use the provided Docker Compose configuration for local testing:

```bash
cd backend
# Start Prometheus with local config
docker compose -f app/core/prometheus/docker/docker-compose.prometheus.yml up -d
```
- Prometheus will be available at [http://localhost:9090](http://localhost:9090)

---

## 3. Run Integration Tests

Make sure your Poetry virtual environment is active, then run:

```bash
poetry run pytest app/core/prometheus/_tests/
```

Tests include:
- **Base endpoint checks**: `/metrics` and `/api/v1/alerts` must return expected structure and default metrics
- **Config validation**: Ensures Prometheus config is correct and environment overrides work
- **Performance**: Metrics endpoint responds quickly and handles concurrent requests

---

## 4. Test File Overview
- `test_integration.py`: End-to-end checks for Prometheus endpoints
- `test_alerts.py`: Alerts endpoint and metrics presence
- `test_metrics.py`: Naming, labels, and value conventions for metrics
- `test_performance.py`: Scrape and load performance
- `test_config.py`: Configuration and environment variable overrides

---

## 5. Troubleshooting
- If tests fail, check Prometheus logs:
  ```bash
  docker compose -f app/core/prometheus/docker/docker-compose.prometheus.yml logs prometheus
  ```
- Ensure no other service is using port 9090
- Make sure environment variables are set if you want to override defaults

---

## 6. Customizing
- To test your own metrics, add your service as a scrape target in `prometheus.local.yml`
- Update tests to check for your application's custom metrics if needed

---

## 7. Cleanup
To stop Prometheus after testing:
```bash
docker compose -f app/core/prometheus/docker/docker-compose.prometheus.yml down
```

---

*For more details, see the `_tests` folder and Prometheus documentation: https://prometheus.io/docs/.*
