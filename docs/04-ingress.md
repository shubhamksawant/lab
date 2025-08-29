# Milestone 3: Ingress & External Access

## 🎯 **Goal**
Set up an Ingress Controller to route external traffic to your Kubernetes services, enabling production-style domain access to your application.

## ⏱️ **Typical Time: 20-40 minutes**

## Why This Matters

An Ingress Controller acts like nginx in Docker Compose, routing external traffic to your services. This milestone enables production-style domain access to your Kubernetes application.

ℹ️ **Side Note:** An Ingress Controller is a Kubernetes component that manages external access to services in a cluster, typically HTTP/HTTPS. It acts as a "smart load balancer" that can route traffic based on hostnames, paths, and other rules. Think of it as the "front door" to your Kubernetes cluster.

## Do This

### Step 1: Set Up Ingress Controller for External Access

```bash
# Install nginx-ingress controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/baremetal/deploy.yaml

**Expected Output:**
```bash
namespace/ingress-nginx created
serviceaccount/ingress-nginx created
configmap/ingress-nginx-controller created
clusterrole.rbac.authorization.k8s.io/ingress-nginx created
clusterrolebinding.rbac.authorization.k8s.io/ingress-nginx created
role.rbac.authorization.k8s.io/ingress-nginx created
rolebinding.rbac.authorization.k8s.io/ingress-nginx created
service/ingress-nginx-controller-admission created
service/ingress-nginx-controller created
deployment.apps/ingress-nginx-controller created
validatingwebhookconfiguration.admissionregistration.k8s.io/ingress-nginx-admission created
```

# Wait for ingress controller to be ready
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s

# Deploy your application's ingress rules
kubectl apply -f k8s/ingress.yaml

**Expected Output:**
```bash
ingress.networking.k8s.io/humor-game-ingress created
```

# Verify ingress is configured
kubectl get ingress -n humor-game

**Expected Output:**
```bash
NAME               CLASS                HOSTS           ADDRESS   PORTS   AGE
humor-game-ingress   humor-game-nginx   gameapp.local   80        2m
```
```

### Step 2: Configure Local Domain and Test Access

**Set up local domain for development:**
```bash
# Add local domain to your hosts file
echo "127.0.0.1 gameapp.local" | sudo tee -a /etc/hosts

**Expected Output:**
```bash
127.0.0.1 gameapp.local
```

# Verify DNS resolution works
ping gameapp.local
# Should ping 127.0.0.1 successfully

**Expected Output:**
```bash
PING gameapp.local (127.0.0.1): 56 data bytes
64 bytes from 127.0.0.1: icmp_seq=1 time=0.037 ms
64 bytes from 127.0.0.1: icmp_seq=2 time=0.034 ms
64 bytes from 127.0.0.1: icmp_seq=3 time=0.033 ms
--- gameapp.local ping statistics ---
3 packets transmitted, 3 packets received, 0.0% packet loss
```
```

**Test your Kubernetes application:**
```bash
# Test API health through Ingress
curl -H "Host: gameapp.local" http://localhost:8080/api/health
# Should return: {"status":"healthy",...}

**Expected Output:**
```json
{
  "status": "healthy",
  "services": {
    "database": "connected",
    "redis": "connected"
  },
  "timestamp": "2024-01-15T10:30:00.000Z",
  "uptime": "00:05:23"
}
```

# Open in browser with domain
open http://gameapp.local:8080
```

### Step 3: Verify Ingress Configuration

```bash
# Check ingress status
kubectl get ingress -n humor-game
# Should show: humor-game-ingress with humor-game-nginx class

**Expected Output:**
```bash
NAME               CLASS                HOSTS           ADDRESS   PORTS   AGE
humor-game-ingress   humor-game-nginx   gameapp.local   80        88m
```

# Check ingress controller pods
kubectl get pods -n ingress-nginx
# Should show: nginx-ingress-controller pod with "1/1 Running"

**Expected Output:**
```bash
NAME                                       READY   STATUS    RESTARTS   AGE
nginx-ingress-controller-7c8b7c8b7c8b    1/1     Running   0          88m
```

# Verify ingress rules
kubectl describe ingress humor-game-ingress -n humor-game
# Should show rules for gameapp.local and gameapp.games
```

### Step 4: Test Full Application Functionality

```bash
# Test frontend loads
curl -H "Host: gameapp.local" -I http://localhost:8080/
# Should return: HTTP/1.1 200 OK

**Expected Output:**
```html
HTTP/1.1 200 OK
Server: nginx/1.25.3
Content-Type: text/html
Content-Length: 1234
Date: Mon, 15 Jan 2024 10:30:00 GMT
```

# Test API endpoints
curl -H "Host: gameapp.local" http://localhost:8080/api/health
# Should return: {"status":"healthy",...}

# Test static assets
curl -H "Host: gameapp.local" -I http://localhost:8080/scripts/game.js
# Should return: Content-Type: application/javascript

**Expected Output:**
```bash
HTTP/1.1 200 OK
Server: nginx/1.25.3
Content-Type: application/javascript
Content-Length: 5678
Date: Mon, 15 Jan 2024 10:30:00 GMT
```
```

## You Should See...

**Ingress Status:**
```
NAME               CLASS                HOSTS           ADDRESS   PORTS   AGE
humor-game-ingress   humor-game-nginx   gameapp.local   80        88m
```

**Ingress Controller Status:**
```
NAME                                       READY   STATUS    RESTARTS   AGE
nginx-ingress-controller-7c8b7c8b7c8b    1/1     Running   0          88m
```

**Host Resolution:**
```
PING gameapp.local (127.0.0.1): 56 data bytes
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.045 ms
```

**Frontend Response:**
```
HTTP/1.1 200 OK
Content-Type: text/html
```

**API Health Response:**
```json
{
  "status": "healthy",
  "services": {
    "database": "connected",
    "redis": "connected"
  },
  "timestamp": "2024-08-21T10:00:00.000Z"
}
```

## ✅ Checkpoint

Your Ingress setup is working when:
- ✅ Ingress controller pods are running in ingress-nginx namespace
- ✅ Ingress rules are configured for gameapp.local and gameapp.games
- ✅ Frontend loads at `http://gameapp.local:8080` through Ingress
- ✅ You can start a game and play without errors
- ✅ Backend API responds to health checks through Ingress
- ✅ Ingress routes traffic correctly to both frontend and backend

## If It Fails

### Symptom: Ingress controller pods not starting
**Cause:** Resource constraints or image pull issues
**Command to confirm:** `kubectl get pods -n ingress-nginx`
**Fix:**
```bash
# Check ingress controller logs
kubectl logs -n ingress-nginx -l app.kubernetes.io/component=controller

# Check resource usage
kubectl top nodes

# If resources are low, use minimal cluster
k3d cluster delete dev-cluster
k3d cluster create dev-cluster --servers 1 --agents 1 --k3s-arg --disable=traefik@server:0
```

### Symptom: Ingress not routing /api/* requests to backend
**Cause:** Ingress routing correct but backend missing /api/* routes
**Command to confirm:** `curl -H "Host: gameapp.local" -s http://localhost:8080/api/health`
**Fix:**
```bash
# Problem: Ingress routing correct but backend missing /api/* routes
# Error: {"error":"Not Found","message":"API endpoint not found! 🔍"}

# Solution: Add /api/* routes to backend server.js
# Fix: Ensure backend has app.get('/api/health', ...) and app.use('/api/*', ...)

# Verify fix:
curl -H "Host: gameapp.local" -s http://localhost:8080/api/health
# Should return: {"status":"healthy",...}
```

### Symptom: Frontend not loading correctly (static assets served as index.html)
**Cause:** Frontend nginx catch-all location block overriding static asset paths
**Command to confirm:** `curl -H "Host: gameapp.local" -I http://localhost:8080/scripts/game.js`
**Fix:**
```bash
# Problem: Frontend nginx catch-all location block overriding static asset paths
# Solution: Reorder nginx location blocks with ^~ prefix matching
# Fix: Update frontend/nginx.conf to prioritize /scripts/, /styles/, /components/

# Verify fix:
curl -H "Host: gameapp.local" -I http://localhost:8080/scripts/game.js
# Should return: Content-Type: application/javascript, not text/html
```

### Symptom: Backend Redis connection failing with malformed URL
**Cause:** Kubernetes sets REDIS_PORT=tcp://host:port instead of just port
**Command to confirm:** `kubectl logs -l app=backend -n humor-game | grep "Redis"`
**Fix:**
```bash
# Problem: Kubernetes sets REDIS_PORT=tcp://host:port instead of just port
# Error: redis://:password@redis:tcp://10.43.201.171:6379/0 (ERR_INVALID_URL)

# Solution: Universal Redis connection logic for both environments
# Fix: Update backend/utils/redis.js to handle tcp:// prefix in REDIS_PORT

# Verify fix:
kubectl logs -l app=backend -n humor-game | grep "Redis: Connected"
# Should show: ✅ Redis: Connected and ready!
```

## 💡 **Reset/Rollback Commands**

If you need to start over or fix issues:

```bash
# Remove ingress rules
kubectl delete ingress humor-game-ingress -n humor-game

# Remove ingress controller (nuclear option)
kubectl delete namespace ingress-nginx

# Reset hosts file
sudo sed -i '/gameapp.local/d' /etc/hosts

# Restart ingress controller
kubectl rollout restart deployment/ingress-nginx-controller -n ingress-nginx

# Check ingress controller status
kubectl get pods -n ingress-nginx
kubectl logs -n ingress-nginx -l app.kubernetes.io/component=controller
```

## Understanding the URL Patterns

The documentation shows different URLs for different purposes:

- **`localhost:8080`** - For direct service testing and curl commands with Host headers
- **`gameapp.local:8080`** - For actual user access through the browser  
- **`Host: gameapp.local`** - For testing Ingress routing

This gives you **both development and production access patterns**:

- **Developers**: Use `localhost:8080` for direct testing and debugging
- **Users**: Access via `gameapp.local:8080` through Ingress (production-style)
- **DevOps Engineers**: Can test both patterns to verify routing works correctly

**Why both?** `localhost:8080` is the local port that k3d exposes, while `gameapp.local:8080` is the domain that Ingress routes to your services.

## What You Learned

You've implemented production networking with Ingress routing:
- **External access** to your Kubernetes application through domain names
- **Traffic routing** from Ingress controller to appropriate services
- **Production patterns** used by enterprise applications
- **Domain management** for both development and production environments

## Professional Skills Gained

- **Ingress controller setup** and configuration
- **Domain routing** and traffic management
- **Production networking** patterns
- **Service discovery** through external access points

---

*Ingress milestone completed successfully. Application accessible via gameapp.local:8080, ready for [05-observability.md](05-observability.md).*
