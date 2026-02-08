# Deployment script for Todo Application to Minikube
# This script automates the deployment process described in the guide

Write-Host "🚀 Starting deployment of Todo Application to Minikube..." -ForegroundColor Green

# Check if minikube is running
try {
    $minikubeStatus = minikube status 2>$null
    if (-not $minikubeStatus) {
        Write-Host "❌ Minikube is not running. Please start minikube first:" -ForegroundColor Red
        Write-Host "   minikube start --cpus=4 --memory=8192 --disk-size=20g" -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "❌ Minikube is not running. Please start minikube first:" -ForegroundColor Red
    Write-Host "   minikube start --cpus=4 --memory=8192 --disk-size=20g" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Minikube is running" -ForegroundColor Green

# Build Docker images
Write-Host "🏗️  Building Docker images..." -ForegroundColor Cyan
docker build -f helm/todo-app/Dockerfile.backend -t todo-backend:latest . 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to build backend image" -ForegroundColor Red
    exit 1
}

docker build -f helm/todo-app/Dockerfile.frontend -t todo-frontend:latest . 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to build frontend image" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Docker images built successfully" -ForegroundColor Green

# Load images into minikube
Write-Host "🚚 Loading images into Minikube..." -ForegroundColor Cyan
minikube image load todo-backend:latest
minikube image load todo-frontend:latest

Write-Host "✅ Images loaded into Minikube" -ForegroundColor Green

# Enable ingress addon
Write-Host "🔌 Enabling ingress addon..." -ForegroundColor Cyan
minikube addons enable ingress

Write-Host "✅ Ingress addon enabled" -ForegroundColor Green

# Create namespace
Write-Host "📦 Creating namespace..." -ForegroundColor Cyan
kubectl create namespace todo-app --dry-run=client -o yaml | kubectl apply -f -

Write-Host "📝 Creating custom values file..." -ForegroundColor Cyan

# Create custom values file
@"
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
"@ | Out-File -FilePath minikube-values.yaml -Encoding UTF8

Write-Host "✅ Custom values file created" -ForegroundColor Green

# Deploy using Helm
Write-Host "📦 Deploying application with Helm..." -ForegroundColor Cyan
helm install my-todo-app ./helm/todo-app `
  --namespace todo-app `
  --values minikube-values.yaml `
  --timeout 10m

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to deploy application" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Application deployed successfully" -ForegroundColor Green

# Wait for pods to be ready
Write-Host "⏳ Waiting for pods to be ready..." -ForegroundColor Cyan
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=todo-app -n todo-app --timeout=300s

Write-Host "✅ All pods are ready!" -ForegroundColor Green

# Get minikube IP
$MINIKUBE_IP = $(minikube ip).Trim()
Write-Host "🌐 Minikube IP: $MINIKUBE_IP" -ForegroundColor Cyan

Write-Host ""
Write-Host "🎉 Deployment completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 To access the application:" -ForegroundColor Yellow
Write-Host "   1. Add this line to your hosts file (C:\Windows\System32\drivers\etc\hosts):" -ForegroundColor White
Write-Host "      $MINIKUBE_IP todo-app.minikube.local" -ForegroundColor White
Write-Host "   2. Access the application at: http://todo-app.minikube.local" -ForegroundColor White
Write-Host ""
Write-Host "🔧 Alternative access (without modifying hosts file):" -ForegroundColor Yellow
Write-Host "   - Start tunnel: minikube tunnel (in another terminal as Administrator)" -ForegroundColor White
Write-Host "   - Or use port forwarding: kubectl port-forward -n todo-app svc/my-todo-app-frontend-service 3000:3000" -ForegroundColor White
Write-Host ""
Write-Host "📋 Useful commands:" -ForegroundColor Yellow
Write-Host "   - Check pods: kubectl get pods -n todo-app" -ForegroundColor White
Write-Host "   - Check logs: kubectl logs -l app.kubernetes.io/component=backend -n todo-app" -ForegroundColor White
Write-Host "   - Uninstall: helm uninstall my-todo-app -n todo-app" -ForegroundColor White
Write-Host ""