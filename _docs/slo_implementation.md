# SLO/SLI Implementation Guide

## Core Service Level Indicators
- **Availability**: `sum(rate(http_requests_total{status=~"2.."}[5m])) / sum(rate(http_requests_total[5m]))`
- **Latency**: `histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))`
- **Error Rate**: `sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))`

## Target SLOs
```yaml
availability: 99.95% (30d rolling)
latency_p99: 500ms 
error_budget: 0.1% (monthly)
```

## Alerting Rules
```yaml
alert: HighErrorRate
expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.01
for: 5m
labels:
  severity: critical
annotations:
  summary: "High error rate on {{ $labels.instance }}"
```

## Implementation Checklist
- [ ] Define SLIs for all critical user journeys
- [ ] Configure Prometheus recording rules for SLI metrics
- [ ] Set up Grafana SLO dashboards
- [ ] Implement error budget burn rate alerts
