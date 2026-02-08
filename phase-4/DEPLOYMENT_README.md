# Todo Application - Docker and Minikube Deployment

This project includes a complete deployment setup for running the Todo application on Docker and Minikube. The setup includes:

- Helm chart for Kubernetes deployment
- Dockerfiles for both backend (FastAPI) and frontend (Next.js)
- Complete microservices architecture with PostgreSQL database
- Security best practices and resource management

## Prerequisites

Before deploying, ensure you have the following installed:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Helm](https://helm.sh/docs/intro/install/)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)

## Quick Deployment

### Option 1: Using the deployment script (Recommended)

#### On Windows (PowerShell):
```powershell
# Start Minikube
minikube start --cpus=4 --memory=8192 --disk-size=20g

# Run the deployment script
./deploy-minikube.ps1
```

#### On Windows (Command Prompt):
```batch
# Start Minikube
minikube start --cpus=4 --memory=8192 --disk-size=20g

# Run the deployment script
deploy-minikube.bat
```

### Option 2: Manual deployment

1. **Start Minikube:**
   ```bash
   minikube start --cpus=4 --memory=8192 --disk-size=20g
   ```

2. **Build Docker images:**
   ```bash
   docker build -f helm/todo-app/Dockerfile.backend -t todo-backend:latest .
   docker build -f helm/todo-app/Dockerfile.frontend -t todo-frontend:latest .
   ```

3. **Load images into Minikube:**
   ```bash
   minikube image load todo-backend:latest
   minikube image load todo-frontend:latest
   ```

4. **Enable ingress:**
   ```bash
   minikube addons enable ingress
   ```

5. **Deploy with Helm:**
   ```bash
   kubectl create namespace todo-app
   helm install my-todo-app ./helm/todo-app \
     --namespace todo-app \
     --set backend.image.repository=todo-backend \
     --set backend.image.tag=latest \
     --set backend.image.pullPolicy=Never \
     --set frontend.image.repository=todo-frontend \
     --set frontend.image.tag=latest \
     --set frontend.image.pullPolicy=Never
   ```

## Accessing the Application

After deployment, you have several options to access the application:

### Option 1: Using Ingress (Recommended)
1. Get the Minikube IP: `minikube ip`
2. Add an entry to your hosts file (`C:\Windows\System32\drivers\etc\hosts` on Windows or `/etc/hosts` on Mac/Linux):
   ```
   <MINIKUBE_IP> todo-app.minikube.local
   ```
3. Access the application at: http://todo-app.minikube.local

### Option 2: Using minikube tunnel
Open a new terminal as administrator and run:
```bash
minikube tunnel
```

### Option 3: Using port forwarding
```bash
# Forward frontend port
kubectl port-forward -n todo-app svc/my-todo-app-frontend-service 3000:3000

# Forward backend port
kubectl port-forward -n todo-app svc/my-todo-app-backend-service 8000:8000
```

Then access:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

## Application Architecture

The deployed application consists of:

- **Frontend Service**: Next.js application (port 3000)
- **Backend Service**: FastAPI application (port 8000)
- **Database**: PostgreSQL database (port 5432)
- **Ingress Controller**: For external access

## Configuration

The deployment uses the Helm chart located at `helm/todo-app/` with the following key features:

- Security contexts with non-root users
- Resource limits and requests
- Health checks and readiness probes
- Persistent storage for the database
- Environment variable configuration
- Service mesh networking

## Management Commands

### Check deployment status:
```bash
kubectl get pods -n todo-app
kubectl get services -n todo-app
kubectl get ingress -n todo-app
```

### View logs:
```bash
kubectl logs -l app.kubernetes.io/component=backend -n todo-app
kubectl logs -l app.kubernetes.io/component=frontend -n todo-app
kubectl logs -l app.kubernetes.io/component=postgresql -n todo-app
```

### Scale the application:
```bash
kubectl scale deployment my-todo-app-backend -n todo-app --replicas=2
kubectl scale deployment my-todo-app-frontend -n todo-app --replicas=2
```

### Update the application:
```bash
# Build and load new images
docker build -f helm/todo-app/Dockerfile.backend -t todo-backend:v2.0 .
minikube image load todo-backend:v2.0

# Update deployment
helm upgrade my-todo-app ./helm/todo-app \
  --namespace todo-app \
  --set backend.image.tag=v2.0
```

### Cleanup:
```bash
helm uninstall my-todo-app -n todo-app
kubectl delete namespace todo-app
minikube stop
```

## Security Considerations

For production deployments, consider:

1. Using stronger passwords in the values file
2. Enabling TLS/HTTPS for the ingress
3. Implementing network policies
4. Using external secret management systems
5. Configuring proper resource quotas

## Troubleshooting

### Common Issues:

1. **Images not found**: Make sure to use `pullPolicy: Never` when using locally built images
2. **Ingress not working**: Ensure the hosts file entry is correct and ingress addon is enabled
3. **Database connection issues**: Check that the PostgreSQL pod is running and accessible
4. **Resource constraints**: Increase Minikube resources if pods are stuck in pending state

### Debugging Commands:

```bash
# Check all resources in todo-app namespace
kubectl get all -n todo-app

# Describe a specific pod for detailed information
kubectl describe pod <pod-name> -n todo-app

# Check events for troubleshooting
kubectl get events -n todo-app --sort-by='.lastTimestamp'
```

## Project Structure

```
helm/todo-app/           # Helm chart for Kubernetes deployment
├── Chart.yaml          # Chart definition
├── values.yaml         # Default values
├── templates/          # Kubernetes manifests templates
├── Dockerfile.backend  # Backend Dockerfile
├── Dockerfile.frontend # Frontend Dockerfile
└── Makefile           # Convenient deployment commands
```

The deployment leverages your existing architecture while adapting it for containerized deployment on Minikube.