# Use official Prometheus image as base
FROM prom/prometheus:latest

# Set working directory
WORKDIR /etc/prometheus

# Copy Prometheus config and rules
COPY ../../prometheus.yml ./prometheus.yml
COPY ../../rules ./rules

# Optional: Copy prometheus-ssl.yml for HTTPS support (if present)
# COPY docker/prometheus-ssl.yml ./prometheus-ssl.yml

# Expose the port (default 9090, but can be overridden by env)
EXPOSE ${PROMETHEUS_PORT:-9090}
EXPOSE ${PROMETHEUS_HTTPS_PORT:-9093}

# Set up data volume for Prometheus TSDB
VOLUME ["/prometheus"]

# Entrypoint and command can be overridden by docker-compose
CMD ["prometheus", \
    "--config.file=/etc/prometheus/prometheus.yml", \
    "--storage.tsdb.path=/prometheus", \
    "--web.console.libraries=/usr/share/prometheus/console_libraries", \
    "--web.console.templates=/usr/share/prometheus/consoles"]
# Notes:
# - PROMETHEUS_PORT can be set in docker-compose or .env
# - prometheus.yml and rules should be kept up to date
# - To enable HTTPS, mount your certs to /etc/prometheus/certs and use the provided prometheus-ssl.yml snippet.
# - Uncomment the COPY line and include prometheus-ssl.yml in your main config under the 'web' section.
# - See https://prometheus.io/docs/prometheus/latest/configuration/configuration/ for advanced HTTPS usage and tuning.