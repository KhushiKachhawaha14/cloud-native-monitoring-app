import os
from dotenv import load_dotenv
from kubernetes import client, config
from kubernetes.client.rest import ApiException

# 1. Load environment variables from .env file
load_dotenv()

# Get Account ID from environment variable
# Use a fallback or raise an error if not found
account_id = os.getenv('AWS_ACCOUNT_ID')

if not account_id:
    print("Error: AWS_ACCOUNT_ID not found in .env file.")
    exit(1)

# Construct the Image URI dynamically
image_uri = f"{account_id}.dkr.ecr.us-east-1.amazonaws.com/my-cloud-native-repo:latest"

# 2. Load Kubernetes configuration
# This connects to your current context (EKS/Minikube)
config.load_kube_config()

# Create a Kubernetes API client
api_client = client.ApiClient()

# Define the Deployment
deployment = client.V1Deployment(
    api_version="apps/v1",
    kind="Deployment",
    metadata=client.V1ObjectMeta(name="my-flask-app"),
    spec=client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(
            match_labels={"app": "my-flask-app"}
        ),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(
                labels={"app": "my-flask-app"}
            ),
            spec=client.V1PodSpec(
                image_pull_secrets=[client.V1LocalObjectReference(name="ecr-registry-helper")],
                containers=[
                    client.V1Container(
                        name="my-flask-container",
                        image=image_uri,  # Using the dynamic URI here
                        ports=[client.V1ContainerPort(container_port=5000)]
                    )
                ]
            )
        )
    ))

# Create the deployment
api_instance_apps = client.AppsV1Api(api_client)
print("Creating Deployment...")
try:
    api_instance_apps.create_namespaced_deployment(
        namespace="default",
        body=deployment)
    print("Deployment 'my-flask-app' created successfully.")
except ApiException as e:
    print(f"Note: {e.reason} ({e.status})")

# Define the Service
service = client.V1Service(
    api_version="v1",
    kind="Service",
    metadata=client.V1ObjectMeta(name="my-flask-service"),
    spec=client.V1ServiceSpec(
        selector={"app": "my-flask-app"},
        ports=[client.V1ServicePort(port=5000)],
        type="ClusterIP" 
    ))

# Create the service
api_instance_core = client.CoreV1Api(api_client)
print("Creating Service...")
try:
    api_instance_core.create_namespaced_service(
        namespace="default",
        body=service)
    print("Service 'my-flask-service' created successfully.")
except ApiException as e:
    print(f"Note: {e.reason} ({e.status})")

print("Deployment and Service creation sequence complete.")