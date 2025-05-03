# Prometheus Capacity Planning

## Storage Requirements
```
needed_disk_space = retention_time_seconds * ingested_samples_per_second * bytes_per_sample
```

### Recommended Starting Points
- **Scrape Interval**: 15s for critical metrics, 1m for others
- **Retention**: 15d for raw metrics, 365d for recording rules
- **Memory**: 8GB RAM per 1M active series

## Scaling Indicators
```promql
# Memory pressure
process_resident_memory_bytes / machine_memory_bytes > 0.8

# Storage growth rate
predict_linear(prometheus_tsdb_storage_blocks_bytes[6h], 60*60*24*7)
```

## Horizontal Scaling
1. **Sharding Strategy**: Split by service/team
2. **Federation Setup**:
```yaml
- job_name: 'federate'
  scrape_interval: 1m
  honor_labels: true
  metrics_path: '/federate'
  params:
    'match[]':
      - '{__name__=~"..*"}'
  static_configs:
    - targets:
      - 'source-prometheus:9090'
```
