# Milestone 6: Global Scale and Production Readiness

## 🎯 **Goal**
Transform your local application into a production-ready system with security, scalability, and global access patterns used by enterprise applications.

## ⏱️ **Typical Time: 60-120 minutes**

## Why This Matters

This milestone transforms your local application into one ready for production use, implementing security and scalability patterns used by enterprise applications.

ℹ️ **Side Note:** Production readiness means your application can handle real user traffic, security threats, and operational challenges. This includes implementing security best practices (TLS, network policies), resource management (limits and requests), monitoring (health checks, metrics), and scalability (auto-scaling, load balancing) that enterprise applications require.

## Do This

### Step 1: Verify Current Setup and Add Production Monitoring

```bash
# Verify your current setup from previous milestones
curl -H "Host: gameapp.local" -s http://localhost:8080/api/health
# Should return: {"status":"healthy"}

**Expected Output:**
```json
{
  "status": "healthy",
  "services": {
    "database": "connected",
    "redis": "connected"
  },
  "timestamp": "2024-01-15T10:30:00.000Z",
  "uptime": "00:15:45"
}
```

# Test game functionality
open http://gameapp.local:8080

# Add resource monitoring
kubectl top nodes
kubectl top pods -n humor-game

**Expected Output:**
```
NAME                    CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
k3d-dev-cluster-server-0   45m          2%     1.2Gi          30%
k3d-dev-cluster-agent-0    23m          1%     856Mi          21%
k3d-dev-cluster-agent-1    18m          1%     789Mi          19%

NAME                                    CPU(cores)   MEMORY(bytes)
humor-game-backend-7d8f9c8f9c-abc12    12m           156Mi
humor-game-frontend-8e9f0d1e2f-def34   5m            45Mi
humor-game-postgres-7d8f9c8f9c-abc12   8m            89Mi
humor-game-redis-8e9f0d1e2f-def34      3m            23Mi
```
```

### Step 2: Implement Resource Limits and Requests

**✅ Resource limits are already configured in your deployment files!**

```bash
# Verify resources are applied (they're already there from previous milestones)
kubectl describe deployment backend -n humor-game | grep -A 10 "Limits\|Requests"
kubectl describe deployment frontend -n humor-game | grep -A 10 "Limits\|Requests"

**Expected Output:**
```
    Limits:
      cpu:     500m
      memory:  512Mi
    Requests:
      cpu:     100m
      memory:  128Mi
```
```

### Step 3: Set Up Real Domain Access (Optional but Recommended)

**Option A: Using a Real Domain You Own**
```bash
# If you own a domain like "mycompany.com", create a subdomain
# In your DNS provider, add an A record:
# Name: game.mycompany.com  
# Value: Your public IP or cloud load balancer IP

# ✅ Your ingress is already configured for production!
# The k8s/ingress.yaml already includes both:
# - gameapp.local (for local development)
# - gameapp.games (for production)

# Just apply the existing ingress (no editing needed)
kubectl apply -f k8s/ingress.yaml

# Test with your real domain (replace gameapp.games with your actual domain)
curl -H "Host: yourdomain.com" http://your-public-ip/api/health
```

**Option B: Using ngrok for Testing (No Domain Required)**
```bash
# Install ngrok if you don't have it
# Sign up at ngrok.com for free account

# Expose your local k3d cluster to the internet
ngrok http 8080

# This gives you a public URL like: https://abc123.ngrok.io
# ✅ Your ingress is already configured for production domains!
# Just replace gameapp.games in k8s/ingress.yaml with your ngrok URL
# Then apply: kubectl apply -f k8s/ingress.yaml
```

### Step 4: Add TLS/HTTPS Support

Production applications need encrypted traffic:

```bash
# Install cert-manager for automatic TLS certificates
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

**Expected Output:**
```
namespace/cert-manager created
customresourcedefinition.apiextensions.k8s.io/certificaterequests.cert-manager.io created
customresourcedefinition.apiextensions.k8s.io/certificates.cert-manager.io created
customresourcedefinition.apiextensions.k8s.io/challenges.acme.cert-manager.io created
customresourcedefinition.apiextensions.k8s.io/clusterissuers.cert-manager.io created
customresourcedefinition.apiextensions.k8s.io/issuers.cert-manager.io created
customresourcedefinition.apiextensions.k8s.io/orders.acme.cert-manager.io created
deployment.apps/cert-manager created
deployment.apps/cert-manager-cainjector created
deployment.apps/cert-manager-webhook created
```

# Wait for cert-manager to be ready
kubectl wait --for=condition=ready pod -l app=cert-manager -n cert-manager --timeout=120s

# Apply TLS configuration to your ingress
kubectl apply -f k8s/cluster-issuer.yaml

# Verify certificate is issued
kubectl get certificate -n humor-game
kubectl describe certificate game-tls -n humor-game

**Expected Output:**
```
NAME       READY   SECRET     AGE
game-tls   True    game-tls   5m
```

**Certificate Details:**
```
Name:         game-tls
Namespace:    humor-game
Labels:       <none>
Annotations:  <none>
API Version:  cert-manager.io/v1
Kind:         Certificate
Spec:
  Secret Name:  game-tls
  Issuer Ref:
    Name:  letsencrypt-prod
    Kind:  ClusterIssuer
Status:
  Conditions:
    Last Transition Time:  2024-01-15T10:35:00Z
    Message:               Certificate is up to date and has not expired
    Reason:                Ready
    Status:                True
    Type:                  Ready
```
```

### Step 5: Implement Health Checks and Monitoring

**✅ Health checks are already configured in your deployments!**

```bash
# Verify health checks are working
kubectl describe deployment backend -n humor-game | grep -A 5 "Liveness\|Readiness"

# Install simple monitoring stack (beginner-friendly)
kubectl apply -f k8s/simple-monitoring.yaml

# Wait for monitoring pods to be ready
kubectl wait --for=condition=ready pod -l app=prometheus -n monitoring --timeout=120s

# Check monitoring is working
kubectl get pods -n monitoring

# Access monitoring dashboards
kubectl port-forward -n monitoring svc/prometheus 9090:9090 &
kubectl port-forward -n monitoring svc/grafana 3000:3000 &

# Open in browser:
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000 (admin/admin123)
```

### Step 6: Configure Horizontal Pod Autoscaling

Let your application scale automatically based on load:

```bash
# Apply HPA configuration
kubectl apply -f k8s/hpa.yaml

# Verify HPA is working
kubectl get hpa -n humor-game

# Generate some load to test autoscaling
kubectl run load-test --image=busybox --rm -i --tty -- sh
# Inside the pod:
while true; do wget -q -O- http://gameapp.local:8080/; done
```

### Step 7: Production Security Hardening

Implement security best practices:

```bash
# Apply network policies to restrict pod communication
kubectl apply -f k8s/network-policies.yaml

# Apply pod security standards
kubectl apply -f k8s/security-context.yaml

# Verify security policies
kubectl get networkpolicy -n humor-game
kubectl describe networkpolicy -n humor-game

# Test if application still functions with policies
curl -H "Host: gameapp.local" -s http://localhost:8080/api/health
```

## You Should See...

**Resource Limits Applied:**
```
Limits:
  cpu:     500m
  memory:  256Mi
Requests:
  cpu:     100m
  memory:  128Mi
```

**HPA Status:**
```
NAME           REFERENCE             TARGETS                                     MINPODS   MAXPODS   REPLICAS   AGE
backend-hpa    Deployment/backend    cpu: <unknown>/70%, memory: <unknown>/80%   1         5         1          14s
frontend-hpa   Deployment/frontend   cpu: <unknown>/70%                          1         3         1          14s
```

**Network Policies:**
```
NAME                      POD-SELECTOR   AGE
backend-network-policy    app=backend    56s
database-network-policy   app=postgres   56s
frontend-network-policy   app=app=frontend   56s
redis-network-policy      app=redis      56s
```

**Monitoring Stack:**
```
NAME                       READY   STATUS    RESTARTS   AGE
prometheus-7c8b7c8b7c8b   1/1     Running   0          15m
grafana-9d8e7d6c5b-def34  1/1     Running   0          20m
```

## ✅ Checkpoint

Your production-grade setup is working when:
- ✅ **Resource limits applied** - pods have CPU/memory limits
- ✅ **Health checks enhanced** - liveness and readiness probes active
- ✅ **Monitoring deployed** - Prometheus and Grafana running and accessible
- ✅ **Autoscaling configured** - HPA created and monitoring resource usage
- ✅ **Real domain access** - Ingress configured for both local and production domains
- ✅ **TLS/HTTPS** - Optional: requires cert-manager setup
- ✅ **Security hardening** - Network policies implemented, security contexts configured

## If It Fails

### Symptom: HPA shows "<unknown>" targets
**Cause:** Metrics server not fully configured in k3d
**Command to confirm:** `kubectl get hpa -n humor-game`
**Fix:**
```bash
# This is expected behavior for k3d - HPA is working, just waiting for metrics data
# HPA is working, just waiting for metrics data

# To verify HPA is working:
kubectl describe hpa backend-hpa -n humor-game
# Should show HPA configuration and status
```

### Symptom: Network policies block application functionality
**Cause:** Overly restrictive network policies
**Command to confirm:** `curl -H "Host: gameapp.local" -s http://localhost:8080/api/health`
**Fix:**
```bash
# Check network policy configuration
kubectl describe networkpolicy -n humor-game

# If too restrictive, modify k8s/network-policies.yaml
# Ensure frontend can reach backend (port 3001)
# Ensure backend can reach postgres (port 5432) and redis (port 6379)
```

### Symptom: Security contexts cause pods to fail
**Cause:** Container trying to run as non-root without proper configuration
**Command to confirm:** `kubectl describe pod <pod-name> -n humor-game`
**Fix:**
```bash
# Check security context configuration
kubectl describe deployment frontend -n humor-game | grep -A 5 "Security Context"

# Verify containers are running as non-root users
kubectl exec -it deployment/frontend -n humor-game -- whoami
kubectl exec -it deployment/backend -n humor-game -- whoami

# Expected output: Should show non-root users (e.g., "nginx", "backend")
```

### Symptom: Monitoring stack won't start
**Cause:** Resource constraints or RBAC issues
**Command to confirm:** `kubectl get pods -n monitoring`
**Fix:**
```bash
# Check resource usage
kubectl top nodes

# If resources are low, use minimal monitoring
kubectl apply -f k8s/simple-monitoring.yaml

# Check RBAC configuration
kubectl get serviceaccount -n monitoring
kubectl get clusterrole | grep prometheus
```

## 💡 **Reset/Rollback Commands**

If you need to start over or fix issues:

```bash
# Remove HPA (Horizontal Pod Autoscaler)
kubectl delete hpa backend-hpa -n humor-game
kubectl delete hpa frontend-hpa -n humor-game

# Remove network policies
kubectl delete networkpolicy --all -n humor-game

# Remove cert-manager (if causing issues)
kubectl delete namespace cert-manager

# Reset to basic monitoring
kubectl delete -f k8s/simple-monitoring.yaml
kubectl apply -f k8s/simple-monitoring.yaml

# Rollback deployments to previous versions
kubectl rollout undo deployment/backend -n humor-game
kubectl rollout undo deployment/frontend -n humor-game

# Check current status
kubectl get all -n humor-game
kubectl get hpa -n humor-game
kubectl get networkpolicy -n humor-game
```

## Understanding Production Security

**Security features now active:**
- **Network isolation**: Only allowing necessary communication between pods
- **Non-root execution**: Preventing containers from running as root users
- **Capability restrictions**: Removing unnecessary system privileges
- **Security contexts**: Enforcing security policies at the pod level

**Why it matters:**
- **Prevents attacks**: If one pod is compromised, others are protected
- **Compliance**: Meets enterprise security standards
- **Best practices**: Industry-standard security configurations

## What You Learned

You've implemented enterprise-grade production features:
- **Resource management** preventing resource starvation
- **Automatic scaling** handling traffic spikes
- **Security hardening** protecting against threats
- **TLS termination** encrypting user traffic
- **Comprehensive monitoring** observing system health

## Professional Skills Gained

- **Production readiness** patterns used by major platforms
- **Auto-scaling strategies** for handling variable load
- **Security best practices** for multi-tenant environments
- **Certificate management** for encrypted communications
- **Monitoring and observability** for operational excellence

---

*Production milestone completed successfully. Application hardened, monitoring active, autoscaling configured, ready for global deployment.*
