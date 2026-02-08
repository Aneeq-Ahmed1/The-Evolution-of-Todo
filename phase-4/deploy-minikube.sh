#!/bin/bash

# Deployment script for Todo Application to Minikube
# This script automates the deployment process described in the guide

set -e  # Exit on any error

echo "🚀 Starting deployment of Todo Application to Minikube..."

# Check if minikube is running
if ! minikube status &>/dev/null; then
    echo "❌ Minikube is not running. Please start minikube first:"
    echo "   minikube start --cpus=4 --memory=8192 --disk-size=20g"
    exit 1
fi

echo "✅ Minikube is running"

# Build Docker images
echo "🏗️  Building Docker images..."
docker build -f helm/todo-app/Dockerfile.backend -t todo-backend:latest . -q
docker build -f helm/todo-app/Dockerfile.frontend -t todo-frontend:latest . -q

echo "✅ Docker images built successfully"

# Load images into minikube
echo "🚚 Loading images into Minikube..."
minikube image load todo-backend:latest
minikube image load todo-frontend:latest

echo "✅ Images loaded into Minikube"

# Enable ingress addon
echo "🔌 Enabling ingress addon..."
minikube addons enable ingress

echo "✅ Ingress addon enabled"

# Create namespace
echo "📦 Creating namespace..."
kubectl create namespace todo-app --dry-run=client -o yaml | kubectl apply -f -

# Create custom values file
echo "📝 Creating custom values file..."
cat <<'EOF' > minikube-values.yaml
# Use locally built images
backend:
  image:
    repository: todo-backend
    tag: "latest"
    pullPolicy: Never  # Since we're using locally loaded images

frontend:
  image:
    repository: todo-frontend
    tag: "latest"
    pullPolicy: Never  # Since we're using locally loaded images

# PostgreSQL configuration for Minikube
postgresql:
  enabled: true
  image:
    registry: docker.io
    repository: postgres
    tag: "15-alpine"
  auth:
    postgresPassword: "postgres-password"
    database: "todo_db"
    username: "todo_user"
    password: "todo-password"
  persistence:
    enabled: true
    size: 8Gi

# Enable ingress for external access
ingress:
  enabled: true
  className: "minikube"
  hosts:
    - host: todo-app.minikube.local
      paths:
        - path: /
          pathType: Prefix
EOF

echo "✅ Custom values file created"

# Deploy using Helm
echo "📦 Deploying application with Helm..."
helm install my-todo-app ./helm/todo-app \
  --namespace todo-app \
  --values minikube-values.yaml \
  --timeout 10m

echo "✅ Application deployed successfully"

# Wait for pods to be ready
echo "⏳ Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=todo-app -n todo-app --timeout=300s

echo "✅ All pods are ready!"

# Get minikube IP
MINIKUBE_IP=$(minikube ip)
echo "🌐 Minikube IP: $MINIKUBE_IP"

echo ""
echo "🎉 Deployment completed successfully!"
echo ""
echo "📝 To access the application:"
echo "   1. Add this line to your hosts file (/etc/hosts on Linux/Mac or C:\\Windows\\System32\\drivers\\etc\\hosts on Windows):"
echo "      $MINIKUBE_IP todo-app.minikube.local"
echo "   2. Access the application at: http://todo-app.minikube.local"
echo ""
echo "🔧 Alternative access (without modifying hosts file):"
echo "   - Start tunnel: minikube tunnel (in another terminal)"
echo "   - Or use port forwarding: kubectl port-forward -n todo-app svc/my-todo-app-frontend-service 3000:3000"
echo ""
echo "📋 Useful commands:"
echo "   - Check pods: kubectl get pods -n todo-app"
echo "   - Check logs: kubectl logs -l app.kubernetes.io/component=backend -n todo-app"
echo "   - Uninstall: helm uninstall my-todo-app -n todo-app"
echo ""