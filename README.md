# FastAPI Prometheus Monitoring Suite

**Production-ready Python/FastAPI Monitoring & Alerting Stack**

This module provides end-to-end metrics, alerting, and monitoring for Python microservices using:

- **Prometheus** (metrics collection, alerting)
- **Service-specific metrics/rules** (Celery, Pulsar, Valkey, etc.)
- **Docker Compose** (orchestration)
- **Pytest & Pydantic** (testing, type safety)

---

## 📁 Folder Structure & Conventions

```
prometheus/
├── _docs/           # Markdown docs, best practices, diagrams, usage
├── _tests/          # Unit/integration tests for all core logic
├── config.py        # Singleton config (class-based, imports from global settings)
├── docker/          # Dockerfile, docker-compose, prometheus.yml, .env.example
├── models/          # Pydantic models or metric schemas
├── exceptions/      # Custom exceptions for monitoring
├── metrics/         # Service-specific metric configs (YAML for celery, pulsar, valkey)
├── rules/           # Alerting and recording rules (YAML, service subfolders)
├── <core>.py        # Main implementation (metrics.py, middleware.py, etc.)
├── README.md        # Main readme (this file)
```

- **_docs/**: All documentation, diagrams, and best practices for this module.
- **_tests/**: All tests for this module, including integration, config, alert, and performance tests.
- **config.py**: Singleton config pattern, imports from global settings, exposes all constants for this module.
- **docker/**: Containerization assets (Dockerfile, docker-compose, prometheus.yml, .env.example, etc).
- **models/**: Pydantic models or metric schemas for input/output validation.
- **exceptions/**: Custom exception classes for robust error handling.
- **metrics/**: YAML metric configs for each service (celery, pulsar, valkey).
- **rules/**: YAML alerting and recording rules for each service.
- **<core>.py**: Main implementation modules (e.g., metrics.py, middleware.py, etc).

---

## 🏗️ Singleton & Config Pattern
- Use a single class (e.g., `PrometheusConfig`) in `config.py` to centralize all env, metric, and integration settings.
- Import from global settings to avoid duplication and ensure DRY config.
- Document all config keys in `_docs/usage.md` and in this README.

---

## 📄 Documentation & Testing
- Place all best practices, diagrams, and usage guides in `_docs/`.
- All tests (unit, integration, smoke, alerting, config) go in `_tests/` with clear naming.
- Use `_tests/_docs/` for test-specific docs if needed.

---

## 🐳 Docker & Prometheus Configs
- Place Dockerfile(s), docker-compose, and Prometheus configs in `docker/`.
- Provide `.env.example` for local/dev/prod setups.
- Place all Prometheus YAML configs in `docker/` (prometheus.yml, prometheus.local.yml, prometheus-ssl.yml).

---

## 📊 Metrics & Alerting Rules
- Place service-specific metric YAMLs in `metrics/` (e.g., `celery/pulsar_alerts.yml`).
- Place alerting and recording rule YAMLs in `rules/`, with subfolders for each service.
- Reference these configs in Prometheus compose files and docs.

---

## 📝 Repeatable Prompt/Template for Future Folders

```
@[<path/to/new_service>] create readme for this folder and suite @[<path/to/new_service/_tests/_docs/alerts.md>]@[<path/to/new_service/_tests/_docs/docker.md>]@[<path/to/new_service/_tests/_docs/infra.md>]@[<path/to/new_service/_tests/_docs/README.md>]  add it to the root, add docker folder, docs folder, tests etc and give me a prompt so I can repeat this action for future folders with the same structure. Include singleton structure and config.
```

- Replace `<path/to/new_service>` with your actual folder path.
- This will scaffold:
  - `README.md` (main)
  - `config.py` (singleton config)
  - `_docs/` (docs, best practices)
  - `_tests/` (tests)
  - `docker/` (container/provisioning)
  - `models/` (schemas)
  - `exceptions/` (custom errors)
  - `metrics/` (service metric configs)
  - `rules/` (service alerting rules)
  - Main implementation modules

---

## 🔐 Required Environment Variables

See `.env.example` for all required environment variables for Prometheus, alerting, and service integration.

---

## 📦 Usage

1. **Clone this repo or add as a submodule.**
2. **Configure environment variables as per `.env.example`.**
3. **Build and start services:**
   ```bash
   docker-compose -f docker/docker-compose.prometheus.yml up --build
   ```
4. **Access Prometheus at:** http://localhost:9090
5. **View metrics and alerting dashboards in Grafana (if integrated).**

---

## 🏷️ Tags

`python, fastapi, prometheus, monitoring, alerting, metrics, docker, pytest, pydantic`
