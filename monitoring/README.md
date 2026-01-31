# Monitoring Setup

This directory contains the monitoring infrastructure for VendorFind platform using Prometheus and Grafana.

## Components

### 1. Prometheus

- **URL (local)**: http://localhost:9090
- **URL (staging)**: https://prometheus.staging.vendorfind.ru
- **URL (production)**: https://prometheus.vendorfind.ru
- **Purpose**: Metrics collection and storage
- **Retention**: 30 days

### 2. Grafana

- **URL (local)**: http://localhost:3001
- **URL (staging)**: https://grafana.staging.vendorfind.ru
- **URL (production)**: https://grafana.vendorfind.ru
- **Purpose**: Metrics visualization and dashboards
- **Note**: Port 3001 is used locally to avoid conflict with frontend on port 3000

### 3. Exporters

#### PostgreSQL Exporter

- Collects database metrics (connections, transactions, cache hit ratio)
- Automatically configured to connect to the main database

#### Node Exporter

- Collects system metrics (CPU, memory, disk, network)
- Monitors the host system resources

#### Traefik Metrics

- Built-in Prometheus metrics from Traefik
- Tracks HTTP requests, response times, and errors

#### FastAPI Metrics

- Provided by `prometheus-fastapi-instrumentator`
- Tracks API endpoint performance, request rates, and response times

## Metrics Endpoints

- **Backend**: http://backend/metrics
- **PostgreSQL**: http://postgres-exporter:9187/metrics
- **Node**: http://node-exporter:9100/metrics
- **Traefik**: http://traefik:8080/metrics

## Pre-configured Dashboards

### 1. FastAPI Overview

- Request rate by endpoint
- Response time percentiles (p95, p99)
- Error rate
- Active requests

### 2. PostgreSQL Overview

- Database connections
- Transaction rate (commits/rollbacks)
- Database size
- Cache hit ratio

### 3. System Overview

- CPU usage
- Memory usage
- Disk usage
- Network traffic

## Local Development

```bash
# Start all services including monitoring
# Note: docker-compose.override.yml is automatically loaded for local development
docker compose up -d

# Access Grafana (port 3001 to avoid conflict with frontend on 3000)
open http://localhost:3001

# Access Prometheus
open http://localhost:9090

# Access backend metrics directly
curl http://localhost:8000/metrics
```

## Configuration Files

- `prometheus.yml` - Prometheus scrape configuration
- `grafana/provisioning/datasources/` - Auto-configured data sources
- `grafana/provisioning/dashboards/` - Auto-configured dashboards

## Setting Up Alerts (TODO)

To set up alerts:

1. Go to Grafana → Alerting → Alert rules
2. Create alert rules for critical metrics:

   - High error rate (>5% for 5 minutes)
   - High response time (p95 >2s for 5 minutes)
   - High CPU usage (>80% for 5 minutes)
   - High memory usage (>90% for 5 minutes)
   - Database connection pool near limit (>80% for 5 minutes)

3. Configure notification channels:
   - Telegram
   - Slack
   - Email
   - PagerDuty (for production)

## Production Setup

1. Update `.env.staging` and `.env.production`:

   ```bash
   GRAFANA_ADMIN_PASSWORD=STRONG_PASSWORD_HERE
   ```

2. Add GitHub Secrets:

   - `GRAFANA_ADMIN_PASSWORD`
   - `USERNAME` (for Traefik dashboard)
   - `HASHED_PASSWORD` (for Traefik dashboard)

3. Access is restricted by IP whitelist (set in `ALLOWED_IPS`)

## Useful Queries

### Backend Performance

```promql
# Request rate
rate(http_requests_total{job="backend"}[5m])

# 95th percentile response time
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job="backend"}[5m]))

# Error rate
rate(http_requests_total{job="backend",status=~"5.."}[5m])
```

### Database Performance

```promql
# Active connections
pg_stat_database_numbackends

# Transaction rate
rate(pg_stat_database_xact_commit[5m])

# Cache hit ratio
rate(pg_stat_database_blks_hit[5m]) / (rate(pg_stat_database_blks_hit[5m]) + rate(pg_stat_database_blks_read[5m]))
```

### System Resources

```promql
# CPU usage
100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory usage
100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))

# Disk usage
100 - ((node_filesystem_avail_bytes{mountpoint="/"} * 100) / node_filesystem_size_bytes{mountpoint="/"})
```

## Troubleshooting

### Prometheus can't scrape targets

- Check if services are running: `docker compose ps`
- Verify network connectivity: `docker compose exec prometheus wget -O- http://backend/metrics`

### Grafana shows no data

- Check if Prometheus datasource is configured correctly
- Verify Prometheus is collecting data: visit http://prometheus:9090/targets

### High memory usage

- Reduce Prometheus retention time in `docker-compose.yml`
- Limit number of metrics being collected

## Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [FastAPI Instrumentator](https://github.com/trallnag/prometheus-fastapi-instrumentator)
- [PostgreSQL Exporter](https://github.com/prometheus-community/postgres_exporter)
- [Node Exporter](https://github.com/prometheus/node_exporter)
