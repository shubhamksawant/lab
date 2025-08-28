# Production Kubernetes Homelab

*A beginner-friendly guide to deploying production-grade applications using Kubernetes, monitoring, and DevOps best practices*

## 🚀 Quick Start

1. **Setup Environment** → [01-prereqs.md](docs/01-prereqs.md)
2. **Verify Docker Compose** → [02-compose.md](docs/02-compose.md)  
3. **Deploy to Kubernetes** → [03-k8s-basics.md](docs/03-k8s-basics.md)
4. **Add Ingress** → [04-ingress.md](docs/04-ingress.md)
5. **Enable Monitoring** → [05-observability.md](docs/05-observability.md)
6. **Implement GitOps** → [06-gitops.md](docs/06-gitops.md)
7. **Production Hardening** → [07-global.md](docs/07-global.md)

## 🎯 What You'll Build

A complete production application stack featuring:
- **Multi-service application** running on Kubernetes
- **Production networking** with Ingress and TLS termination  
- **Comprehensive monitoring** with Prometheus and Grafana dashboards
- **Database persistence** with PostgreSQL and Redis
- **Professional DevOps workflows** using GitOps and automation

## 📚 Complete Documentation

- **[Overview & Architecture](docs/00-overview.md)** - Project overview and learning path
- **[Prerequisites](docs/01-prereqs.md)** - Tool installation and setup
- **[Milestone Guides](docs/)** - Step-by-step learning for each milestone
- **[Troubleshooting](docs/08-troubleshooting.md)** - Common issues and solutions
- **[FAQ](docs/09-faq.md)** - Frequently asked questions
- **[Glossary](docs/10-glossary.md)** - Technical terms and definitions

## 🚨 Important Notes

**⚠️ CRITICAL:** This project uses a demo domain (`gameapp.games`) that you MUST replace with your own domain before beginning. See [Domain Replacement Guide](docs/domain-replacement-guide.md) for details.

## 🛠️ Prerequisites

- 4GB+ RAM available
- 10GB+ disk space  
- macOS or Linux (Windows via WSL2)
- Docker, kubectl, k3d, Helm, Node.js, jq

## 🔧 Need Help?

- **Stuck on a step?** → [Troubleshooting Guide](docs/08-troubleshooting.md)
- **Confused by terms?** → [Glossary](docs/10-glossary.md)
- **Have questions?** → [FAQ](docs/09-faq.md)

## 🎉 Success Metrics

**By the end, you'll have:**
- ✅ **4 pods running** in humor-game namespace
- ✅ **Monitoring stack** with Prometheus and Grafana
- ✅ **GitOps automation** with ArgoCD
- ✅ **Production security** with network policies
- ✅ **Global access** via Cloudflare CDN

---

*This guide teaches the same infrastructure patterns used by companies like Netflix, Airbnb, and GitHub. Start with [01-prereqs.md](docs/01-prereqs.md) to begin your journey!*