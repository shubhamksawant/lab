# Prerequisites: Setting Up Your Development Environment

## 🎯 **Goal**
Set up a production-ready development environment with all required tools and sufficient resources for Kubernetes deployment.

## ⏱️ **Typical Time: 15-30 minutes**

## Why This Matters

Proper tool installation and resource availability prevent hours of troubleshooting later. This milestone ensures your development environment is production-ready before we begin building infrastructure.

## Do This

### Step 1: Install Required Tools

**For macOS (Recommended path):**
```bash
# Install all tools at once using Homebrew
brew install docker docker-compose kubectl k3d helm nodejs jq

# Start Docker Desktop (required for container operations)
# Download from: https://www.docker.com/products/docker-desktop

**Expected Output:**
```
==> Installing docker
==> Installing docker-compose
==> Installing kubectl
==> Installing k3d
==> Installing helm
==> Installing nodejs
==> Installing jq
==> Summary
🍺  /opt/homebrew/Cellar now contains:
  docker, docker-compose, kubectl, k3d, helm, nodejs, jq
```
```

**For Linux (Ubuntu/Debian):**
```bash
# Update your system first
sudo apt-get update

# Install Docker
sudo apt-get install -y docker.io docker-compose
sudo usermod -aG docker $USER
newgrp docker  # Apply group changes immediately

```
**Expected Output:**
Get:1 http://archive.ubuntu.com/ubuntu focal-updates InRelease [114 kB]
Get:2 http://archive.ubuntu.com/ubuntu focal-updates/main amd64 Packages [1,234 kB]
...
Reading package lists... Done
Building dependency tree... Done
docker.io is already the newest version (20.10.21-0ubuntu1~20.04.2).
docker-compose is already the newest version (1.25.0-1).
```

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install kubectl /usr/local/bin/kubectl

# Install k3d (lightweight Kubernetes)
curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash

ℹ️ **Side Note:** k3d is a lightweight Kubernetes distribution that runs inside Docker containers. It's perfect for development and testing because it's fast to start, uses minimal resources, and provides a real Kubernetes experience without the overhead of full cluster management.

# Install Helm (Kubernetes package manager)
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs jq
```

### Step 2: Verify Tools Are Installed

```bash
# Check all tools are properly installed
docker --version        # Should show: Docker version 20.0+
kubectl version --client # Should show: Client Version v1.28+
k3d version            # Should show: k3d version v5.6+
helm version           # Should show: version.BuildInfo
node --version         # Should show: v18+
npm --version          # Should show: 8.0+
jq --version           # Should show: jq-1.6+

**Expected Output:**
```
Docker version 20.10.21, build 20.10.21-0ubuntu1~20.04.2
Client Version: version.Info{Major:"1", Minor:"28", GitVersion:"v1.28.0", GitCommit:"a6eaaf4d6efc7a96940d2d4247e7206c91e14be7", GitTreeState:"clean", BuildDate:"2023-08-28T16:03:32Z", GoVersion:"go1.20.5", Compiler:"gc", Platform:"linux/amd64"}
k3d version v5.6.0
version.BuildInfo{Version:"v3.12.3", GitCommit:"3a31588be33fe7a89b61ea5e2022f9e2a8f2c5c7", GitTreeState:"clean", GoVersion:"go1.20.10"}
v18.17.1
8.19.4
jq-1.6
```
```

### Step 3: Check System Resources

```bash
# Check Docker daemon status
docker info

# Check available memory (macOS)
vm_stat

# Check disk space
df -h

**Expected Output:**
```
Client:
 Context:    default
 Debug Mode: false
 Plugins:
  app: Docker App (Docker Inc., v0.9.1-beta3)
  buildx: Docker Buildx (Docker Inc., v0.10.4)
  compose: Docker Compose (Docker Inc., v2.17.2)
  scan: Docker Scan (Docker Inc., v0.23.0)

Server:
 Containers: 0
  Running: 0
  Paused: 0
  Stopped: 0
 Images: 0
 Server Version: 20.10.21
 Storage Driver: overlay2
 Total Memory: 4.096GiB
```
```

### Step 4: Test Docker Functionality

```bash
# Test Docker is working
docker run hello-world

# Should show: "Hello from Docker!" message

**Expected Output:**
```
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
2db29710123e: Pull complete
Digest: sha256:7d0ee538c6de6c5f71c0b0c83f6c466e77e7f1b5c8b5c8b5c8b5c8b5c8b5c8b5
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.
```
```

## You Should See...

**Tool Versions:**
```
Docker version 20.0+
Client Version: v1.28+
k3d version v5.6+
version.BuildInfo{Version:v3.18+}
v18+
8.0+
jq-1.6+
```

**Docker Info:**
```
Server:
 Containers: 0
 Server Version: 20.0+
 Total Memory: 4GB+
 Name: colima (or docker-desktop)
```

**System Resources:**
```
Filesystem: At least 10GB available
Memory: At least 4GB available
```

## ✅ Checkpoint

Your environment is ready when:
- ✅ All 7 required tools show version numbers
- ✅ Docker daemon is running and accessible
- ✅ At least 4GB RAM available
- ✅ At least 10GB disk space available
- ✅ No permission or PATH errors
- ✅ `docker run hello-world` succeeds

## If It Fails

### Symptom: Docker permission errors
**Cause:** User not in docker group
**Command to confirm:** `docker run hello-world`
**Fix:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Test again
docker run hello-world
```

### Symptom: kubectl not found
**Cause:** kubectl not in PATH
**Command to confirm:** `which kubectl`
**Fix:**
```bash
# Ensure kubectl is in your PATH
echo $PATH

# If missing, add to your shell profile:
echo 'export PATH=$PATH:/usr/local/bin' >> ~/.bashrc
source ~/.bashrc
```

### Symptom: Docker Desktop missing (macOS)
**Cause:** Docker Desktop not installed
**Command to confirm:** `docker --version`
**Fix:**
```bash
# Alternative: Use Colima (already configured)
brew install colima
colima start --cpu 2 --memory 4 --disk 20

# Or install Docker Desktop from:
# https://www.docker.com/products/docker-desktop
```

### Symptom: Insufficient resources
**Cause:** System doesn't meet minimum requirements
**Command to confirm:** `docker info` and `df -h`
**Fix:**
```bash
# For low RAM systems, use minimal cluster:
k3d cluster create dev-cluster \
  --servers 1 \
  --agents 1 \
  --k3s-arg --disable=traefik@server:0

# Monitor resource usage:
kubectl top nodes
kubectl top pods --all-namespaces
```

## 💡 **Reset/Rollback Commands**

If you need to start over or fix a broken installation:

```bash
# Remove all Docker containers and images (nuclear option)
docker system prune -a --volumes

# Reset Docker Desktop to factory defaults (macOS)
# Docker Desktop → Settings → Troubleshoot → Reset to factory defaults

# Remove specific tools and reinstall
brew uninstall docker docker-compose kubectl k3d helm nodejs jq
brew install docker docker-compose kubectl k3d helm nodejs jq

# Reset user groups (Linux)
sudo gpasswd -d $USER docker
sudo usermod -aG docker $USER
newgrp docker
```

## Common Issues & Fixes

**Docker Permission Errors:**
```bash
# If you get "permission denied" errors:
sudo usermod -aG docker $USER
newgrp docker
# Then test: docker run hello-world
```

**kubectl Not Found:**
```bash
# Ensure kubectl is in your PATH
echo $PATH
# If missing, add to your shell profile:
echo 'export PATH=$PATH:/usr/local/bin' >> ~/.bashrc
source ~/.bashrc
```

## What You Learned

You've verified your development environment readiness:
- **Tool availability** for container orchestration and development
- **Resource constraints** that may impact Kubernetes performance
- **Alternative solutions** like Colima for Docker backend
- **Troubleshooting approaches** for common installation issues

## Professional Skills Gained

- **Environment validation** before starting complex deployments
- **Resource planning** for development and production workloads
- **Tool chain management** across multiple technologies
- **Problem prevention** through systematic verification

---

*Environment setup completed. All tools verified, resources assessed, ready for [02-compose.md](02-compose.md).*
