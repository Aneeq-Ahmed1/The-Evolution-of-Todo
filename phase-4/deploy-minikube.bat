@echo off
setlocal enabledelayedexpansion

echo 🚀 Starting deployment of Todo Application to Minikube...

REM Check if minikube is running
minikube status >nul 2>&1
if errorlevel 1 (
    echo ❌ Minikube is not running. Please start minikube first:
    echo    minikube start --cpus=4 --memory=8192 --disk-size=20g
    exit /b 1
)

echo ✅ Minikube is running

REM Build Docker images
echo 🏗️  Building Docker images...
docker build -f helm/todo-app/Dockerfile.backend -t todo-backend:latest .
if errorlevel 1 (
    echo ❌ Failed to build backend image
    exit /b 1
)

docker build -f helm/todo-app/Dockerfile.frontend -t todo-frontend:latest .
if errorlevel 1 (
    echo ❌ Failed to build frontend image
    exit /b 1
)

echo ✅ Docker images built successfully

REM Load images into minikube
echo 🚚 Loading images into Minikube...
minikube image load todo-backend:latest
minikube image load todo-frontend:latest

echo ✅ Images loaded into Minikube

REM Enable ingress addon
echo 🔌 Enabling ingress addon...
minikube addons enable ingress

echo ✅ Ingress addon enabled

REM Create namespace
echo 📦 Creating namespace...
kubectl create namespace todo-app --dry-run=client -o yaml ^| kubectl apply -f -

REM Create custom values file
echo 📝 Creating custom values file...
(
echo # Use locally built images
echo backend:
echo   image:
echo     repository: todo-backend
echo     tag: "latest"
echo     pullPolicy: Never  # Since we're using locally loaded images
echo.
echo frontend:
echo   image:
echo     repository: todo-frontend
echo     tag: "latest"
echo     pullPolicy: Never  # Since we're using locally loaded images
echo.
echo # PostgreSQL configuration for Minikube
echo postgresql:
echo   enabled: true
echo   image:
echo     registry: docker.io
echo     repository: postgres
echo     tag: "15-alpine"
echo   auth:
echo     postgresPassword: "postgres-password"
echo     database: "todo_db"
echo     username: "todo_user"
echo     password: "todo-password"
echo   persistence:
echo     enabled: true
echo     size: 8Gi
echo.
echo # Enable ingress for external access
echo ingress:
echo   enabled: true
echo   className: "minikube"
echo   hosts:
echo     - host: todo-app.minikube.local
echo       paths:
echo         - path: /
echo           pathType: Prefix
) > minikube-values.yaml

echo ✅ Custom values file created

REM Deploy using Helm
echo 📦 Deploying application with Helm...
helm install my-todo-app ./helm/todo-app ^
  --namespace todo-app ^
  --values minikube-values.yaml ^
  --timeout 10m

if errorlevel 1 (
    echo ❌ Failed to deploy application
    exit /b 1
)

echo ✅ Application deployed successfully

REM Wait for pods to be ready
echo ⏳ Waiting for pods to be ready...
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=todo-app -n todo-app --timeout=300s

echo ✅ All pods are ready!

REM Get minikube IP
for /f %%i in ('minikube ip') do set MINIKUBE_IP=%%i
echo 🌐 Minikube IP: !MINIKUBE_IP!

echo.
echo 🎉 Deployment completed successfully!
echo.
echo 📝 To access the application:
echo    1. Add this line to your hosts file (C:\Windows\System32\drivers\etc\hosts):
echo       !MINIKUBE_IP! todo-app.minikube.local
echo    2. Access the application at: http://todo-app.minikube.local
echo.
echo 🔧 Alternative access (without modifying hosts file):
echo    - Start tunnel: minikube tunnel (in another terminal as Administrator)
echo    - Or use port forwarding: kubectl port-forward -n todo-app svc/my-todo-app-frontend-service 3000:3000
echo.
echo 📋 Useful commands:
echo    - Check pods: kubectl get pods -n todo-app
echo    - Check logs: kubectl logs -l app.kubernetes.io/component=backend -n todo-app
echo    - Uninstall: helm uninstall my-todo-app -n todo-app
echo.