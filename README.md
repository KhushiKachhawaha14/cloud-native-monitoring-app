**Cloud-Native Monitoring Application**
A robust, cloud-native monitoring solution built with Python and Flask, containerized with Docker, and deployed on Amazon EKS (Elastic Kubernetes Service). This project demonstrates a full CI/CD-ready workflow for deploying applications to AWS using infrastructure-as-code principles in Python.

*🚀 Features*
Flask Web App: Lightweight backend for monitoring services.
Dockerized Architecture: Fully containerized for environment consistency.
AWS ECR Integration: Automated image management via Amazon Elastic Container Registry.
Kubernetes Orchestration: Automated deployment and scaling using Amazon EKS.
Helm Support: Ready for package management via Helm charts.

*🛠️ Tech Stack*
Backend: Python 3.x, Flask
Containerization: Docker
Cloud Provider: AWS (ECR, EKS)
Orchestration: Kubernetes (Boto3 & Kubernetes Python Client)
Package Management: uv / pip

*📋 Prerequisites*
Before running this project, ensure you have the following installed and configured:
AWS CLI: Configured with your credentials (aws configure).
Docker: To build and push images.
kubectl: To interact with the EKS cluster.
Python 3.10+

🔧 Installation & Setup
Clone the repository:

Bash

git clone https://github.com/KhushiKachhawaha14/cloud-native-monitoring-app.git
cd cloud-native-monitoring-app
Set up virtual environment:

Bash

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
🚢 Deployment Guide
1. Create ECR Repository & Push Image
Run the ECR script to create your repository and push the Docker image:

Bash

python ecr.py
2. Deploy to Amazon EKS
Once the image is in ECR, deploy the application to your Kubernetes cluster:

Bash

python eks.py
3. Verify Deployment
Check the status of your pods and services:

Bash

kubectl get pods
kubectl get svc

*📂 Project Structure*
app.py: Main Flask application logic.
ecr.py: Script to handle AWS ECR operations.
eks.py: Kubernetes deployment script using the Python client.
deployment.yaml: K8s Deployment manifest.
service.yaml: K8s Service manifest for load balancing.

Dockerfile: Instructions for building the application image.
