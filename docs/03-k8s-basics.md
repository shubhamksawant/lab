# Milestone 2: Kubernetes Basics

## 🎯 **Goal**
Transform your Docker Compose application into a Kubernetes deployment, learning core concepts like Pods, Services, Deployments, and ConfigMaps.

## ⏱️ **Typical Time: 30-60 minutes**

## Why This Matters

This milestone teaches you the core Kubernetes concepts that every platform engineer needs to know: Pods, Services, Deployments, and ConfigMaps. You'll transform your Docker Compose application into a Kubernetes deployment.

ℹ️ **Side Note:** Kubernetes is a container orchestration platform that automates the deployment, scaling, and management of containerized applications. Think of it as a "smart scheduler" that can run your containers across multiple machines, handle failures automatically, and provide service discovery.

## Do This

### Step 1: Create Your Kubernetes Cluster

```bash
# Create a local 3-node Kubernetes cluster
k3d cluster create dev-cluster \
  --servers 1 \
  --agents 2 \
  --port "8080:80@loadbalancer" \
  --port "8443:443@loadbalancer"

**Expected Output:**
```bash
INFO[0000] Prep: Network
INFO[0000] Created network 'k3d-dev-cluster'
INFO[0000] Created volume 'k3d-dev-cluster-images'
INFO[0000] Starting cluster 'dev-cluster'
INFO[0000] Starting the server node
INFO[0000] Starting the agent nodes
INFO[0000] Starting load balancer
INFO[0000] Starting helpers
INFO[0000] Cluster 'dev-cluster' created successfully!
```

# Verify cluster is running
kubectl get nodes

kubectl get nodes -o wide
# Should show 3 nodes: 1 server, 2 agents, all "Ready"

**Expected Output:**
```bash
NAME                    STATUS   ROLES                  AGE   VERSION        INTERNAL-IP     EXTERNAL-IP   OS-IMAGE   KERNEL-VERSION   CONTAINER-RUNTIME
k3d-dev-cluster-server-0   Ready    control-plane,master   2m    v1.28.0+k3s1   172.18.0.2     <none>        Alpine Linux v3.18  6.1.0-13-amd64   containerd://1.7.11
k3d-dev-cluster-agent-0    Ready    <none>                 2m    v1.28.0+k3s1   172.18.0.3     <none>        Alpine Linux v3.18  6.1.0-13-amd64   containerd://1.7.11
k3d-dev-cluster-agent-1    Ready    <none>                 2m    v1.28.0+k3s1   172.18.0.4     <none>        Alpine Linux v3.18  6.1.0-13-amd64   containerd://1.7.11
```

# Check cluster health
kubectl cluster-info
# Should show cluster endpoint and DNS

**Expected Output:**
```bash
Kubernetes control plane is running at https://0.0.0.0:6443
CoreDNS is running at https://0.0.0.0:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
Metrics-server is running at https://0.0.0.0:6443/api/v1/namespaces/kube-system/services/metrics-server:https/proxy
```
```

### Step 2: Deploy Your Application Configuration

```bash
# Create the application namespace (organization)
kubectl apply -f k8s/namespace.yaml

**Expected Output:**
```bash
namespace/humor-game created
```

# Create configuration and secrets
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml

**Expected Output:**
```bash
configmap/humor-game-config created
configmap/frontend-config created
secret/humor-game-secrets created
```

# Verify they were created
kubectl get configmap -n humor-game
kubectl get secrets -n humor-game

**Expected Output:**
```bash
NAME                DATA   AGE
frontend-config     1      30s
humor-game-config   5      30s

NAME                  TYPE     DATA   AGE
humor-game-secrets   Opaque   5      30s
```
```

### Step 3: Deploy Database Services

```bash
# Deploy PostgreSQL with persistent storage
kubectl apply -f k8s/postgres.yaml

**Expected Output:**
```bash
deployment.apps/humor-game-postgres created
service/humor-game-postgres created
persistentvolumeclaim/humor-game-postgres-pvc created
```

# Deploy Redis for caching
kubectl apply -f k8s/redis.yaml

**Expected Output:**
```bash
deployment.apps/humor-game-redis created
service/humor-game-redis created
persistentvolumeclaim/humor-game-redis-pvc created
```

# Wait for databases to be ready (this takes time!)
kubectl wait --for=condition=ready pod -l app=postgres -n humor-game --timeout=180s
kubectl wait --for=condition=ready pod -l app=redis -n humor-game --timeout=180s

# Verify databases are running
kubectl get pods -n humor-game
# Should show postgres and redis pods with "1/1 Running"

**Expected Output:**
```bash
NAME                                    READY   STATUS    RESTARTS   AGE
humor-game-postgres-7d8f9c8f9c-abc12   1/1     Running   0          2m
humor-game-redis-8e9f0d1e2f-def34      1/1     Running   0          2m
```
```

### Step 4: Build and Deploy Application Services

**⚠️ CRITICAL: Build Images Locally AND Import to k3d!**

```bash
# Build your application images locally
docker build -t humor-game-frontend:latest ./frontend
docker build -t humor-game-backend:latest ./backend

**Expected Output:**
```bash
Building frontend
Step 1/8 : FROM nginx:alpine
 ---> 1234567890ab
Step 2/8 : COPY nginx.conf /etc/nginx/nginx.conf
 ---> Using cache
 ---> 1234567890ab
...
Successfully built 1234567890ab
Successfully tagged humor-game-frontend:latest

Building backend
Step 1/12 : FROM node:18-alpine
 ---> 0987654321cd
...
Successfully built 0987654321cd
Successfully tagged humor-game-backend:latest
```

# Verify images were built
docker images | grep humor-game
# Should show: humor-game-frontend:latest and humor-game-backend:latest

**Expected Output:**
```bash
humor-game-backend    latest    0987654321cd   2 minutes ago   156MB
humor-game-frontend   latest    1234567890ab   2 minutes ago   23.4MB
```

# Import images to k3d (CRITICAL STEP!)
k3d image import humor-game-frontend:latest -c dev-cluster
k3d image import humor-game-backend:latest -c dev-cluster

**Expected Output:**
```bash
Importing image 'humor-game-frontend:latest' into cluster 'dev-cluster'
Importing image 'humor-game-backend:latest' into cluster 'dev-cluster'
```
```

**Deploy your services:**
```bash
# Deploy backend API service
kubectl apply -f k8s/backend.yaml

**Expected Output:**
```bash
deployment.apps/humor-game-backend created
service/humor-game-backend created
```

# Deploy frontend web service  
kubectl apply -f k8s/frontend.yaml

**Expected Output:**
```bash
deployment.apps/humor-game-frontend created
service/humor-game-frontend created
```

# Wait for applications to be ready
kubectl wait --for=condition=ready pod -l app=backend -n humor-game --timeout=120s
kubectl wait --for=condition=ready pod -l app=frontend -n humor-game --timeout=60s

# Check all pods are running
kubectl get pods -n humor-game
# Should show 4 pods all with "1/1 Running" status

**Expected Output:**
```bash
NAME                                    READY   STATUS    RESTARTS   AGE
humor-game-backend-7d8f9c8f9c-abc12    1/1     Running   0          3m
humor-game-frontend-8e9f0d1e2f-def34   1/1     Running   0          2m
humor-game-postgres-7d8f9c8f9c-abc12   1/1     Running   0          5m
humor-game-redis-8e9f0d1e2f-def34      1/1     Running   0          5m
```
```

### Step 5: Verify Service Discovery

```bash
# Check services are created
kubectl get svc -n humor-game
# Should show 4 services: postgres, redis, backend, frontend

# Test backend health via Service
kubectl port-forward -n humor-game svc/backend 3001:3001 >/dev/null 2>&1 &
echo $! > /tmp/pf_backend.pid
sleep 2
curl -sf http://127.0.0.1:3001/health
kill $(cat /tmp/pf_backend.pid)

# Test frontend static via Service
kubectl port-forward -n humor-game svc/frontend 8088:80 >/dev/null 2>&1 &
echo $! > /tmp/pf_frontend.pid
sleep 2
curl -sI http://127.0.0.1:8088/ | grep -q "200"
kill $(cat /tmp/pf_frontend.pid)
```

## You Should See...

**Cluster Status:**
```
NAME                    STATUS   ROLES                  AGE   VERSION
k3d-dev-cluster-server-0   Ready    control-plane,master   2m    v1.28.0+k3s1
k3d-dev-cluster-agent-0    Ready    <none>                 2m    v1.28.0+k3s1
k3d-dev-cluster-agent-1    Ready    <none>                 2m    v1.28.0+k3s1
```

**Namespace Creation:**
```
namespace/humor-game created
configmap/humor-game-config created
secret/humor-game-secrets created
```

**Pod Status:**
```
NAME                       READY   STATUS    RESTARTS   AGE
backend-675577fbf8-rb77b   1/1     Running   0          15m
frontend-5977b4874d-hfddb  1/1     Running   0          20m
postgres-7d8f9b8c5d-abc12  1/1     Running   0          25m
redis-9f8e7d6c5b-def34    1/1     Running   0          25m
```

**Service Status:**
```
NAME      TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
backend   ClusterIP   10.43.244.239   <none>        3001/TCP   88m
frontend  ClusterIP   10.43.201.170   <none>        80/TCP     88m
postgres  ClusterIP   10.43.201.172   <none>        5432/TCP   88m
redis     ClusterIP   10.43.201.171   <none>        6379/TCP   88m
```

**Backend Health Check:**
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

Your Kubernetes deployment is working when:
- ✅ All 4 pods show "1/1 Running" status
- ✅ Services are created and accessible
- ✅ Backend health endpoint responds via port-forward
- ✅ Frontend serves content via port-forward
- ✅ No pod restart loops or error states

## If It Fails

### Symptom: Pods stuck in "Pending" status
**Cause:** Insufficient resources or image pull issues
**Command to confirm:** `kubectl describe pod <pod-name> -n humor-game`
**Fix:**
```bash
# Check what's wrong
kubectl describe pod <pod-name> -n humor-game

# Common cause: Insufficient resources
kubectl top nodes  # Check resource usage

# If using k3d, increase cluster resources
k3d cluster delete dev-cluster
k3d cluster create dev-cluster --servers 1 --agents 2 --k3s-arg --disable=traefik@server:0
```

### Symptom: Backend can't connect to database
**Cause:** Database service not ready or network issues
**Command to confirm:** `kubectl logs -l app=backend -n humor-game`
**Fix:**
```bash
# Check backend logs
kubectl logs -l app=backend -n humor-game

# Verify database service exists
kubectl get svc postgres -n humor-game

# Test database connectivity
kubectl exec -it deployment/postgres -n humor-game -- psql -U gameuser -d humor_memory_game -c "SELECT 1;"
```

### Symptom: Image pull errors (ErrImagePull/ImagePullBackOff)
**Cause:** Kubernetes trying to pull images from external registries
**Command to confirm:** `kubectl describe pod <pod-name> -n humor-game`
**Fix:**
```bash
# Problem: Kubernetes trying to pull images from external registries
# Solution: Use local images with imagePullPolicy: Never

# Rebuild and import images
docker build -t humor-game-frontend:latest ./frontend
docker build -t humor-game-backend:latest ./backend

# Import to k3d (CRITICAL!)
k3d image import humor-game-frontend:latest -c dev-cluster
k3d image import humor-game-backend:latest -c dev-cluster

# Restart deployments
kubectl rollout restart deployment/frontend -n humor-game
kubectl rollout restart deployment/backend -n humor-game
```

### Symptom: Frontend not loading correctly
**Cause:** nginx configuration or static asset serving issues
**Command to confirm:** `kubectl logs -l app=frontend -n humor-game`
**Fix:**
```bash
# Check frontend logs
kubectl logs -l app=frontend -n humor-game

# Verify nginx configuration
kubectl exec -it deployment/frontend -n humor-game -- cat /etc/nginx/nginx.conf

# Test static asset serving
kubectl port-forward -n humor-game svc/frontend 8088:80 &
curl -I http://127.0.0.1:8088/scripts/game.js
kill %1
```

## 💡 **Reset/Rollback Commands**

If you need to start over or fix issues:

```bash
# Delete specific deployments
kubectl delete deployment humor-game-backend -n humor-game
kubectl delete deployment humor-game-frontend -n humor-game

# Delete all resources in namespace
kubectl delete all --all -n humor-game

# Reset entire cluster (nuclear option)
k3d cluster delete dev-cluster
k3d cluster create dev-cluster --servers 1 --agents 2 --port "8080:80@loadbalancer" --port "8443:443@loadbalancer"

# Rollback to previous deployment version
kubectl rollout undo deployment/humor-game-backend -n humor-game
kubectl rollout undo deployment/humor-game-frontend -n humor-game

# Check rollout history
kubectl rollout history deployment/humor-game-backend -n humor-game
```

## Understanding the Hybrid Image Strategy

**Why this approach works:**
- **`imagePullPolicy: Never`** tells Kubernetes: "Don't try to pull from external registries"
- **Local Docker daemon** provides the base images
- **k3d import** ensures the cluster context is updated
- **No external registry complexity** - perfect for development and learning

**The complete workflow:**
1. **Build locally**: `docker build -t humor-game-frontend:latest ./frontend`
2. **Import to k3d**: `k3d image import humor-game-frontend:latest -c dev-cluster`
3. **Deploy to K8s**: `kubectl apply -f k8s/frontend.yaml`
4. **K8s uses local image**: No pulling, no registry errors

## What You Learned

You've successfully migrated a multi-service application from Docker Compose to Kubernetes, understanding:
- **Pod orchestration** and how containers run in Kubernetes
- **Service discovery** and how applications find each other
- **Configuration management** with ConfigMaps and Secrets
- **Persistent storage** for stateful applications like databases
- **Universal image strategy** that works in both Docker Compose and Kubernetes without conflicts

## Professional Skills Gained

- **Kubernetes fundamentals** that form the foundation of container orchestration
- **Service mesh basics** through Kubernetes service discovery
- **Configuration as code** practices for managing application settings
- **Infrastructure debugging** skills for troubleshooting complex deployments
- **Multi-environment compatibility** ensuring Docker Compose and Kubernetes work seamlessly together

---

*Kubernetes basics milestone completed successfully. All 4 pods running and healthy, ready for [04-ingress.md](04-ingress.md).*
