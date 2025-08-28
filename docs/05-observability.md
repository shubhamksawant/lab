# Milestone 4: Observability & Monitoring

## 🎯 **Goal**
Deploy a production-grade monitoring stack with Prometheus and Grafana to track application performance, resource usage, and system health.

## ⏱️ **Typical Time: 45-90 minutes**

## Why This Matters

Monitoring isn't optional in production. This milestone teaches you the same observability patterns used by companies like Datadog and New Relic to track application performance and prevent outages before they happen.

ℹ️ **Side Note:** Observability is the ability to understand the internal state of a system by examining its outputs. In Kubernetes, this means collecting metrics (numbers), logs (text), and traces (request flows) to understand how your application is performing and identify issues before they become problems.

## Do This

### Step 1: Deploy Monitoring Infrastructure

```bash
# Create monitoring namespace and RBAC permissions
kubectl apply -f k8s/prometheus-rbac.yaml

**Expected Output:**
```
namespace/monitoring created
serviceaccount/prometheus created
clusterrole.rbac.authorization.k8s.io/prometheus created
clusterrolebinding.rbac.authorization.k8s.io/prometheus created
```

# Deploy Prometheus and Grafana stack
kubectl apply -f k8s/monitoring.yaml

**Expected Output:**
```
configmap/grafana-datasources created
configmap/prometheus-config created
deployment.apps/prometheus created
deployment.apps/grafana created
service/prometheus created
service/grafana created
```

# Wait for monitoring services to be ready (this takes a few minutes)
kubectl wait --for=condition=ready pod -l app=prometheus -n monitoring --timeout=300s
kubectl wait --for=condition=ready pod -l app=grafana -n monitoring --timeout=300s

# Verify monitoring stack is running
kubectl get pods -n monitoring
# Should show prometheus and grafana pods with "1/1 Running"

**Expected Output:**
```
NAME                          READY   STATUS    RESTARTS   AGE
grafana-7d8f9c8f9c-abc12     1/1     Running   0          3m
prometheus-8e9f0d1e2f-def34  1/1     Running   0          3m
```
```

### Step 2: Access Your Monitoring Dashboards

**Option 1: Port-Forwarding (Traditional Method)**
```bash
# Access Prometheus (metrics database)
kubectl port-forward svc/prometheus 9090:9090 -n monitoring &

**Expected Output:**
```
Forwarding from 127.0.0.1:9090 -> 9090
Forwarding from [::1]:9090 -> 9090
```

# Access Grafana (dashboard interface)
kubectl port-forward svc/grafana 3000:3000 -n monitoring &

**Expected Output:**
```
Forwarding from 127.0.0.1:3000 -> 3000
Forwarding from [::1]:3000 -> 3000
```

# Open monitoring interfaces
open http://localhost:9090  # Prometheus UI
open http://localhost:3000  # Grafana UI (login: admin/admin123)
```

**Option 2: Ingress-Based Access (Recommended - No Port-Forwarding)**
```bash
# Run the automated setup script
./scripts/access-monitoring.sh

# Or manually apply the configuration
kubectl apply -f k8s/monitoring-auth.yaml
kubectl apply -f k8s/ingress.yaml
```

**Access URLs (No Port-Forwarding Required):**
- **Prometheus**: http://prometheus.gameapp.local:8080
- **Grafana**: http://grafana.gameapp.local:8080

### Step 3: Explore Prometheus Metrics

Open `http://localhost:9090` and explore the metrics Prometheus is collecting:

**Basic queries to try:**
```bash
# In Prometheus query interface, try these:

# Pod CPU usage
rate(container_cpu_usage_seconds_total[5m])

**Expected Output:**
```
{container="humor-game-backend",namespace="humor-game",pod="humor-game-backend-7d8f9c8f9c-abc12"} 0.001234
{container="humor-game-frontend",namespace="humor-game",pod="humor-game-frontend-8e9f0d1e2f-def34"} 0.000567
```

# Pod memory usage  
container_memory_usage_bytes

**Expected Output:**
```
{container="humor-game-backend",namespace="humor-game",pod="humor-game-backend-7d8f9c8f9c-abc12"} 156789012
{container="humor-game-frontend",namespace="humor-game",pod="humor-game-frontend-8e9f0d1e2f-def34"} 23456789
```

# HTTP requests to your backend
rate(http_requests_total[5m])

**Expected Output:**
```
{method="GET",status="200",endpoint="/api/health"} 0.1
{method="POST",status="200",endpoint="/api/game"} 0.05
```

# Kubernetes pod restarts
increase(kube_pod_container_status_restarts_total[1h])

**Expected Output:**
```
{namespace="humor-game",pod="humor-game-backend-7d8f9c8f9c-abc12"} 0
{namespace="humor-game",pod="humor-game-frontend-8e9f0d1e2f-def34"} 0
```
```

### Step 4: Create Your First Grafana Dashboard

Open `http://localhost:3000` and login with `admin/admin123`.

**Create a new dashboard:**
1. Click the "+" icon and select "Create Dashboard"
2. Click "Add a new panel"
3. Add these panels one by one:

**Panel 1: Pod CPU Usage**
```bash
# Query: 
rate(container_cpu_usage_seconds_total{namespace="humor-game"}[5m])

# Panel title: "Pod CPU Usage"
# Unit: "percent (0.0-1.0)"
```

**Panel 2: Pod Memory Usage**
```bash
# Query:
container_memory_usage_bytes{namespace="humor-game"}

# Panel title: "Pod Memory Usage"  
# Unit: "custom units: bytes"
```

**Panel 3: HTTP Request Rate**
```bash
# Query:
rate(nginx_ingress_controller_requests[5m])

# Panel title: "HTTP Requests per Second"
# Unit: "reqps"
```

**Panel 4: Pod Status**
```bash
# Query:
kube_pod_status_phase{namespace="humor-game"}

# Panel title: "Pod Status"
# Visualization: "Stat"
```

### Step 5: Import Advanced Custom Dashboards

Instead of building dashboards from scratch, import our pre-built production-ready dashboards:

**Option 1: Import Basic Custom Dashboard**
```bash
# 1. In Grafana, click the "+" icon → "Import"
# 2. Click "Upload JSON file"
# 3. Select: k8s/custom-dashboard.json
# 4. Click "Load"
# 5. Verify Data Source: Should show "Prometheus (default)"
# 6. Click "Import"
```

**Option 2: Import Advanced Production Dashboard**
```bash
# 1. In Grafana, click the "+" icon → "Import"
# 2. Click "Upload JSON file"
# 3. Select: k8s/advanced-custom-dashboard.json
# 4. Click "Load"
# 5. Verify Data Source: Should show "Prometheus (default)"
# 6. Click "Import"
```

### Step 6: Generate Load to See Metrics

Create some traffic to populate your dashboards using our production-ready metrics test scripts:

**Option 1: Local Port-Forward (Traditional)**
```bash
# Start backend port-forward
kubectl port-forward -n humor-game svc/backend 3001:3001 &

# Run the metrics test script
./scripts/production-metrics-test.sh

# Expected output: 100+ successful API calls, metrics generated
```

**Option 2: Ingress-Based (Recommended)**
```bash
# No port-forward needed! Use ingress directly
./scripts/production-metrics-test-ingress.sh

# Expected output: Same metrics, but using gameapp.local:8080
```

## You Should See...

**Monitoring Stack Status:**
```
NAME                       READY   STATUS    RESTARTS   AGE
prometheus-7c8b7c8b7c8b   1/1     Running   0          15m
grafana-9d8e7d6c5b-def34  1/1     Running   0          20m
```

**Prometheus Targets Page (`/targets`):**
- Should show multiple `kubernetes-pods` targets
- All targets should display "UP" status
- Namespace should show `humor-game` for your app pods

**Grafana Dashboard with 4 Panels:**
- **Panel 1**: Pod CPU Usage showing real-time data
- **Panel 2**: Pod Memory Usage with stable values
- **Panel 3**: HTTP Request Rate with traffic spikes
- **Panel 4**: Pod Status showing all pods as healthy

**Expected Output:**
```
✅ Prometheus: 5+ targets UP
✅ Grafana: All 4 panels showing data
✅ Metrics: Real-time updates during load testing
✅ RBAC: No permission errors in logs
```

## ✅ Checkpoint

Your monitoring is working when:
- ✅ Prometheus collects metrics at `http://localhost:9090`
- ✅ Grafana shows dashboards at `http://localhost:3000`
- ✅ CPU and memory panels show data for your pods
- ✅ HTTP request panels show traffic spikes during load tests
- ✅ You can create and modify dashboard panels
- ✅ Metrics update in real-time as you use the application

## If It Fails

### Symptom: No metrics showing in Grafana
**Cause:** Prometheus not scraping targets or data source not configured
**Command to confirm:** Go to http://localhost:9090/targets
**Fix:**
```bash
# Check Prometheus is scraping targets
# Go to http://localhost:9090/targets
# All targets should show "UP" status

# Check ServiceMonitor configuration
kubectl get servicemonitor -n monitoring

# Verify pods have metric endpoints
kubectl get endpoints -n humor-game
```

### Symptom: Grafana shows "No data"
**Cause:** Prometheus data source not working or no metrics collected
**Command to confirm:** Test Prometheus data source in Grafana
**Fix:**
```bash
# Test Prometheus data source in Grafana
# Go to Configuration -> Data Sources -> Test
# Should show "Data source is working"

# Check Prometheus has data
# In Prometheus UI, try query: up
# Should return 1 for healthy targets
```

### Symptom: Dashboards are empty
**Cause:** Incorrect namespace in queries or no traffic generated
**Command to confirm:** Verify correct namespace in queries
**Fix:**
```bash
# Verify correct namespace in queries
# Query should include: {namespace="humor-game"}

# Check metric names are correct
# In Prometheus, use "Metrics" dropdown to see available metrics

# Generate some traffic to create data
curl -H "Host: gameapp.local" http://localhost:8080/api/health
```

### Symptom: Prometheus pod won't start
**Cause:** RBAC configuration issues or resource constraints
**Command to confirm:** `kubectl get pods -n monitoring`
**Fix:**
```bash
# Check RBAC configuration
kubectl get serviceaccount -n monitoring
kubectl get clusterrole | grep prometheus

# If missing, apply RBAC
kubectl apply -f k8s/prometheus-rbac.yaml
```

### Symptom: Port-forwarding not working
**Cause:** Port conflicts or processes already using ports
**Command to confirm:** `lsof -i :3000` and `lsof -i :9090`
**Fix:**
```bash
# Kill conflicting processes
lsof -ti:3000 | xargs kill -9
lsof -ti:9090 | xargs kill -9

# Restart port-forwards
kubectl port-forward -n monitoring svc/grafana 3000:3000 &
kubectl port-forward -n monitoring svc/prometheus 9090:9090 &
```

## 💡 **Reset/Rollback Commands**

If you need to start over or fix issues:

```bash
# Remove monitoring stack
kubectl delete namespace monitoring

# Remove specific monitoring components
kubectl delete deployment prometheus -n monitoring
kubectl delete deployment grafana -n monitoring

# Reset Grafana to factory defaults
kubectl exec -it deployment/grafana -n monitoring -- rm -rf /var/lib/grafana/*

# Restart monitoring services
kubectl rollout restart deployment/prometheus -n monitoring
kubectl rollout restart deployment/grafana -n monitoring

# Check monitoring status
kubectl get pods -n monitoring
kubectl logs -n monitoring -l app=prometheus
kubectl logs -n monitoring -l app=grafana
```

## Understanding Production Monitoring

**The Three Pillars of Observability:**
1. **Metrics:** Numerical data over time (CPU, memory, request rates)
2. **Logs:** Event records with context (error messages, user actions)  
3. **Traces:** Request flow through distributed services

**Key Metrics Categories:**
- **RED Metrics:** Rate, Errors, Duration (user-facing performance)
- **USE Metrics:** Utilization, Saturation, Errors (resource health)
- **Business Metrics:** Game sessions, user signups, revenue

## What You Learned

You've implemented enterprise observability:
- **Metrics collection** with Prometheus for time-series data
- **Data visualization** with Grafana for operational dashboards  
- **Custom dashboards** tailored to your application's needs
- **Load testing** to validate monitoring under stress
- **Production monitoring patterns** used by major technology companies

## Professional Skills Gained

- **Observability architecture** that scales to thousands of services
- **Dashboard creation** for different stakeholder audiences
- **Metrics-driven debugging** to identify performance bottlenecks
- **Capacity planning** using historical resource utilization data
- **Troubleshooting complex monitoring issues** with systematic approaches

---

*Observability milestone completed successfully. Prometheus and Grafana running, dashboards populated, ready for [06-gitops.md](06-gitops.md).*
