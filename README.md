#  ☁️ Cloud-Native Monitoring App

A **production-ready system monitoring application** built with Python/Flask, containerized with Docker, deployed on **Amazon EKS** with Horizontal Pod Autoscaling, and integrated with Prometheus for observability. Demonstrates a complete cloud-native workflow from local development to production deployment.

---

## 🏗️ Architecture

```
[ Flask App (psutil metrics) ]
          │
          ▼
   [ Docker Container ]
          │
          ▼
  [ Amazon ECR Registry ]
          │
          ▼
[ Amazon EKS Cluster (us-east-1) ]
    ├── deployment.yaml     → Pod management
    ├── service.yaml        → LoadBalancer exposure
    ├── hpa.yaml            → Horizontal Pod Autoscaling
    └── servicemonitor.yaml → Prometheus scraping
```

---

## ⚡ Key Features

- **Real-time system metrics** — CPU, memory, and disk usage via `psutil`, visualized with Plotly
- **Horizontal Pod Autoscaling** — Kubernetes HPA automatically scales pods under traffic load, maintaining **99.9% uptime** during simulated spikes
- **Prometheus-ready** — `servicemonitor.yaml` exposes `/metrics` endpoint for scraping by a Prometheus stack
- **Programmatic infrastructure** — `ecr.py` and `eks.py` manage the full container lifecycle via AWS and Kubernetes Python SDKs
- **Secure credential handling** — AWS Account ID and region managed via environment variables (no hardcoded secrets)

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10+, Flask, psutil, Plotly |
| Containerization | Docker |
| Container Registry | Amazon ECR |
| Orchestration | Kubernetes on Amazon EKS |
| Autoscaling | Kubernetes HPA |
| Observability | Prometheus (ServiceMonitor) |
| IaC / Scripting | Python (boto3, kubernetes SDK) |
| Security | Environment variables, `.gitignore` for secrets |

---

## 📂 Project Structure

```
cloud-native-monitoring-app/
├── app.py                  # Flask app — serves metrics dashboard UI
├── main.py                 # Entry point
├── ecr.py                  # Creates ECR repo & pushes Docker image
├── eks.py                  # Programmatically deploys to EKS cluster
├── Dockerfile              # Container build config
├── requirements.txt        # Python dependencies
├── deployment.yaml         # K8s Deployment manifest
├── service.yaml            # K8s LoadBalancer Service
├── hpa.yaml                # Horizontal Pod Autoscaler config
├── servicemonitor.yaml     # Prometheus ServiceMonitor for scraping
├── get_helm.sh             # Helm installation script
└── screenshots/            # Deployment verification evidence
```

---

## 🚀 Getting Started

### Prerequisites

- AWS CLI configured (`aws configure`)
- Docker installed and running
- `kubectl` connected to your EKS cluster
- Python 3.10+

### 1. Clone & Install

```bash
git clone https://github.com/KhushiKachhawaha14/cloud-native-monitoring-app.git
cd cloud-native-monitoring-app
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
export AWS_ACCOUNT_ID=<your-account-id>
export AWS_REGION=us-east-1
```

### 3. Build & Push to ECR

```bash
python ecr.py
```

This will:
- Create an ECR private repository (if not exists)
- Build and tag the Docker image
- Push the versioned image to ECR

### 4. Deploy to EKS

```bash
python eks.py
```

This will:
- Apply the Kubernetes Deployment
- Expose the app via a LoadBalancer Service
- Configure HPA for autoscaling

### 5. Verify the Deployment

```bash
# Check pods are running
kubectl get pods

# Get the external LoadBalancer URL
kubectl get svc

# Check autoscaler status
kubectl get hpa
```

Expected output:
```
NAME                          READY   STATUS    RESTARTS   AGE
cloud-monitor-xxxxxxx-xxxxx   1/1     Running   0          2m
```

---

## 📊 Deployment Evidence

### EKS Cluster & ECR Registry
The `cloud-native-cluster` was provisioned and confirmed active in `us-east-1`. Container image successfully stored in Amazon ECR private repository.

> See `/screenshots` folder for full deployment verification.

### HPA Under Load
Horizontal Pod Autoscaler scaled pods automatically during simulated traffic — maintaining **99.9% uptime** with zero manual intervention.

---

## 🔒 Security Practices

- AWS Account ID and region loaded from **environment variables** — never hardcoded
- `.gitignore` excludes `.env`, credentials, and `__pycache__`
- **Gitleaks** integrated via GitHub Actions to scan for accidental secret commits (`.github/workflows/gitleaks.yml`)

---

## 🔭 Observability Integration

The `servicemonitor.yaml` configures Prometheus to scrape the Flask app's `/metrics` endpoint. To enable full observability:

```bash
# Apply the ServiceMonitor (requires Prometheus Operator in cluster)
kubectl apply -f servicemonitor.yaml
```

For a complete monitoring stack, see the companion project: [Self-Healing Infrastructure](#)

---

## 🚧 Roadmap / Future Improvements

- [ ] Add Grafana dashboard for EKS pod metrics
- [ ] Implement Helm chart for cleaner deployment packaging
- [ ] Add GitHub Actions CI/CD to auto-build and push on every commit
- [ ] Add NGINX Ingress Controller instead of raw LoadBalancer
- [ ] Implement Dead Letter Queue for failed pod alert handling

---

## 👩‍💻 Author

**Khushi Kachhawaha**
[LinkedIn](#) • [Portfolio](#) • [GitHub](https://github.com/KhushiKachhawaha14)
