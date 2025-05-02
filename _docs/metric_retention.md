# Metric Retention Policy

## Retention Tiers
| Metric Type | Retention | Compression |
|-------------|-----------|-------------|
| High-resolution | 7d | Snappy |
| Medium-resolution | 30d | Zstd |
| Long-term | 1y | Downsampled |

## Configuration
```yaml
# prometheus.yml
global:
  retention: 15d
  retentionSize: 100GB

# Downsampling rules
rule_files:
  - '/etc/prometheus/recording_rules.yml'
```

## Recording Rules Example
```yaml
- record: instance:http_requests:rate5m
expr: rate(http_requests_total[5m])

- record: cluster:http_requests:rate1h
expr: rate(http_requests_total[1h])
```

## Lifecycle Management
1. **Critical Metrics**: Keep raw data for 15d
2. **Business Metrics**: Downsample after 7d
3. **Debug Metrics**: Drop after 24h
