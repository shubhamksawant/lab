# 📊 Monitoring Access Guide

## Overview
This guide shows you how to access Prometheus and Grafana without port-forwarding using Kubernetes Ingress.

## 🚀 Quick Setup

### Option 1: Automated Setup (Recommended)
```bash
# Run the automated setup script
./scripts/access-monitoring.sh
```

### Option 2: Manual Setup
```bash
# 1. Apply monitoring configuration
kubectl apply -f k8s/monitoring.yaml
kubectl apply -f k8s/monitoring-auth.yaml

# 2. Apply ingress configuration
kubectl apply -f k8s/ingress.yaml

# 3. Wait for services to be ready
kubectl wait --for=condition=ready pod -l app=prometheus -n monitoring
kubectl wait --for=condition=ready pod -l app=grafana -n monitoring
```

## 🌐 Access URLs

### Local Development
- **Prometheus**: http://prometheus.gameapp.local
- **Grafana**: http://grafana.gameapp.local

### Production
- **Prometheus**: http://prometheus.gameapp.games
- **Grafana**: http://grafana.gameapp.games

## 🔐 Default Credentials

### Prometheus
- No authentication required (read-only access)

### Grafana
- **Username**: `admin`
- **Password**: `admin123`

## 📱 Local DNS Setup

The setup script automatically adds these entries to your `/etc/hosts` file:

```bash
# Local monitoring access
127.0.0.1 prometheus.gameapp.local
127.0.1 grafana.gameapp.local

# Production monitoring access (update with your actual IP)
YOUR_IP prometheus.gameapp.games
YOUR_IP grafana.gameapp.games
```

## 🔍 Troubleshooting

### Can't Access Services?

1. **Check cluster status**:
   ```bash
   k3d cluster list
   kubectl cluster-info
   ```

2. **Verify ingress is working**:
   ```bash
   kubectl get ingress -A
   kubectl describe ingress monitoring-ingress -n monitoring
   ```

3. **Check service status**:
   ```bash
   kubectl get pods -n monitoring
   kubectl get svc -n monitoring
   ```

4. **Check ingress controller**:
   ```bash
   kubectl get pods -n ingress-nginx
   kubectl get svc -n ingress-nginx
   ```

### Common Issues

#### Issue: "Connection refused"
- **Solution**: Ensure your cluster is running and ingress controller is deployed

#### Issue: "Host not found"
- **Solution**: Check `/etc/hosts` file and verify DNS entries

#### Issue: "Authentication required"
- **Solution**: Use credentials: `admin/admin123`

## 🛠️ Manual Port-Forwarding (Fallback)

If ingress doesn't work, you can still use port-forwarding:

```bash
# Prometheus
kubectl port-forward -n monitoring svc/prometheus 9090:9090

# Grafana
kubectl port-forward -n monitoring svc/grafana 3000:3000
```

Then access:
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

## 🔧 Customization

### Change Default Credentials

1. **Generate new password hash**:
   ```bash
   htpasswd -nb admin your_new_password
   ```

2. **Update the secret**:
   ```bash
   kubectl patch secret monitoring-auth -n monitoring --type='json' -p='[{"op": "replace", "path": "/data/auth", "value": "YOUR_BASE64_HASH"}]'
   ```

### Add SSL/TLS

1. **Create TLS secret**:
   ```bash
   kubectl create secret tls monitoring-tls -n monitoring --cert=your-cert.pem --key=your-key.pem
   ```

2. **Update ingress annotations**:
   ```yaml
   nginx.ingress.kubernetes.io/ssl-redirect: "true"
   nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
   ```

## 📊 Dashboard Features

### Prometheus
- Real-time metrics collection
- Query language (PromQL)
- Alerting rules
- Service discovery

### Grafana
- Pre-configured dashboards
- Custom visualization
- Alert notifications
- Data source management

## 🚨 Security Notes

- **Basic auth** is enabled by default
- **HTTPS** is recommended for production
- **Network policies** can restrict access
- **RBAC** controls Kubernetes access

## 🔄 Updates and Maintenance

### Update Monitoring Stack
```bash
# Pull latest configurations
git pull origin main

# Apply updates
kubectl apply -f k8s/monitoring.yaml
kubectl apply -f k8s/ingress.yaml
```

### Backup Dashboards
```bash
# Export Grafana dashboards
kubectl get configmap grafana-dashboards -n monitoring -o yaml > dashboards-backup.yaml
```

---

**Need help?** Check the troubleshooting section or run the automated setup script!
