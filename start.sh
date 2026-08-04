#!/bin/bash

# Dynamic script directory resolution (no hardcoded paths)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

show_help() {
    echo "Usage: ./start.sh [OPTION]"
    echo "Deploys devops-k8s-3tier-app to a local Minikube cluster."
    echo ""
    echo "Options:"
    echo "  --check   Validate Kubernetes manifests without applying"
    echo "  --clean   Delete the assignment3 namespace and resources"
    echo "  --help    Display this help menu"
    exit 0
}

clean_deployment() {
    echo "Cleaning up assignment3 Kubernetes resources..."
    kubectl delete namespace assignment3 --ignore-not-found=true
    echo "Cleanup complete."
    exit 0
}

check_manifests() {
    echo "Validating Kubernetes manifests..."
    for file in k8s/*.yml; do
        echo "Checking $file..."
        kubectl apply --dry-run=client -f "$file" > /dev/null || exit 1
    done
    echo "All manifests passed dry-run validation."
    exit 0
}

case "$1" in
    --help) show_help ;;
    --clean) clean_deployment ;;
    --check) check_manifests ;;
esac

echo "Starting Minikube..."
minikube start --driver=docker --memory=2048 --cpus=2

echo "Waiting for Minikube node to be ready..."
kubectl wait --for=condition=Ready node/minikube --timeout=120s

echo "Applying Kubernetes namespace..."
kubectl apply -f k8s/namespace.yml
sleep 2

echo "Applying ConfigMaps and Secrets..."
if [ -f "k8s/mysql-secret.yml" ]; then
    kubectl apply -f k8s/mysql-secret.yml
else
    echo "Warning: k8s/mysql-secret.yml not found. Copying from example template..."
    cp k8s/mysql-secret.yml.example k8s/mysql-secret.yml
    kubectl apply -f k8s/mysql-secret.yml
fi

kubectl apply -f k8s/flask-configmap.yml
kubectl apply -f k8s/nginx-configmap.yml

echo "Applying Persistence layers..."
kubectl apply -f k8s/mysql-pv.yml
kubectl apply -f k8s/mysql-pvc.yml

echo "Deploying MySQL Database..."
kubectl apply -f k8s/mysql-deployment.yml
kubectl apply -f k8s/mysql-service.yml

echo "Waiting for MySQL pod readiness..."
kubectl wait --for=condition=Ready pod -l app=mysql -n assignment3 --timeout=120s

echo "Deploying Flask API Backend..."
kubectl apply -f k8s/flask-deployment.yml
kubectl apply -f k8s/flask-service.yml

echo "Deploying Nginx Proxy Presentation Tier..."
kubectl apply -f k8s/nginx-deployment.yml
kubectl apply -f k8s/nginx-service.yml

echo "Waiting for all workloads to reach Ready status..."
kubectl wait --for=condition=Ready pod --all -n assignment3 --timeout=180s

echo ""
echo "=== Cluster Deployment Status ==="
kubectl get all -n assignment3

echo ""
echo "=== Service Endpoint URL ==="
minikube service nginx -n assignment3 --url
