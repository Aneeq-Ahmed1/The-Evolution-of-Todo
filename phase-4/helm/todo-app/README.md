# Todo App Helm Chart

This Helm chart deploys the Todo Full-Stack Web Application, which consists of:
- Frontend: Next.js 15 application
- Backend: FastAPI application
- Database: PostgreSQL (optional, can use external DB)

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+
- PV provisioner support in the underlying infrastructure (for PostgreSQL persistence)

## Installing the Chart

To install the chart with the release name `my-todo-app`:

```bash
# Add the chart repository (if hosted)
helm repo add todo-app https://your-repo-url/todo-app

# Install the chart
helm install my-todo-app ./helm/todo-app --namespace todo-app --create-namespace
```

Or install from the local chart directory:

```bash
helm install my-todo-app ./helm/todo-app \
  --namespace todo-app \
  --create-namespace \
  --set backend.image.tag=v1.0.0 \
  --set frontend.image.tag=v1.0.0
```

## Upgrading the Chart

```bash
helm upgrade my-todo-app ./helm/todo-app --namespace todo-app -f values.yaml
```

## Uninstalling the Chart

```bash
helm uninstall my-todo-app --namespace todo-app
```

## Configuration

The following table lists the configurable parameters of the todo-app chart and their default values.

### Global Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `global.imageRegistry` | Global Docker image registry | `""` |
| `global.imagePullSecrets` | Global Docker registry secret names | `[]` |
| `global.storageClass` | Global storage class for dynamic provisioning | `""` |

### Backend Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `backend.enabled` | Enable backend deployment | `true` |
| `backend.image.registry` | Backend image registry | `""` |
| `backend.image.repository` | Backend image repository | `todo-backend` |
| `backend.image.tag` | Backend image tag | `"latest"` |
| `backend.image.pullPolicy` | Backend image pull policy | `"IfNotPresent"` |
| `backend.replicaCount` | Number of backend replicas | `1` |
| `backend.service.type` | Backend service type | `ClusterIP` |
| `backend.service.port` | Backend service port | `8000` |
| `backend.resources.limits.cpu` | CPU limit for backend | `"500m"` |
| `backend.resources.limits.memory` | Memory limit for backend | `"512Mi"` |
| `backend.resources.requests.cpu` | CPU request for backend | `"100m"` |
| `backend.resources.requests.memory` | Memory request for backend | `"256Mi"` |

### Frontend Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `frontend.enabled` | Enable frontend deployment | `true` |
| `frontend.image.registry` | Frontend image registry | `""` |
| `frontend.image.repository` | Frontend image repository | `todo-frontend` |
| `frontend.image.tag` | Frontend image tag | `"latest"` |
| `frontend.image.pullPolicy` | Frontend image pull policy | `"IfNotPresent"` |
| `frontend.replicaCount` | Number of frontend replicas | `1` |
| `frontend.service.type` | Frontend service type | `ClusterIP` |
| `frontend.service.port` | Frontend service port | `3000` |
| `frontend.resources.limits.cpu` | CPU limit for frontend | `"300m"` |
| `frontend.resources.limits.memory` | Memory limit for frontend | `"256Mi"` |
| `frontend.resources.requests.cpu` | CPU request for frontend | `"50m"` |
| `frontend.resources.requests.memory` | Memory request for frontend | `"128Mi"` |

### PostgreSQL Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `postgresql.enabled` | Enable PostgreSQL deployment | `true` |
| `postgresql.image.registry` | PostgreSQL image registry | `"docker.io"` |
| `postgresql.image.repository` | PostgreSQL image repository | `"postgres"` |
| `postgresql.image.tag` | PostgreSQL image tag | `"15-alpine"` |
| `postgresql.auth.postgresPassword` | PostgreSQL superuser password | `"postgres-password"` |
| `postgresql.auth.database` | PostgreSQL database name | `"todo_db"` |
| `postgresql.auth.username` | PostgreSQL username | `"todo_user"` |
| `postgresql.auth.password` | PostgreSQL user password | `"todo-password"` |
| `postgresql.persistence.enabled` | Enable PostgreSQL persistence | `true` |
| `postgresql.persistence.size` | PostgreSQL persistent volume size | `"8Gi"` |

### Ingress Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `ingress.enabled` | Enable ingress resource | `false` |
| `ingress.className` | Ingress class name | `""` |
| `ingress.hosts[0].host` | Hostname for the ingress | `"todo-app.local"` |
| `ingress.hosts[0].paths[0].path` | Path for the ingress | `"/"` |
| `ingress.hosts[0].paths[0].pathType` | Path type for the ingress | `"Prefix"` |

## Custom Values Example

Create a `custom-values.yaml` file:

```yaml
backend:
  image:
    tag: "v1.0.0"
  resources:
    limits:
      cpu: 1000m
      memory: 1Gi
    requests:
      cpu: 200m
      memory: 512Mi

frontend:
  image:
    tag: "v1.0.0"
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 100m
      memory: 256Mi

postgresql:
  auth:
    postgresPassword: "your-secure-password"
    password: "your-secure-user-password"
  persistence:
    size: "16Gi"

ingress:
  enabled: true
  hosts:
    - host: todo.yourdomain.com
      paths:
        - path: /
          pathType: Prefix
```

Deploy with custom values:

```bash
helm install my-todo-app ./helm/todo-app -f custom-values.yaml --namespace todo-app --create-namespace
```

## Secrets Management

⚠️ **Important**: The chart creates secrets for database credentials and API keys. For production use, consider using external secret management solutions like:

- Kubernetes External Secrets
- HashiCorp Vault
- AWS Secrets Manager
- Azure Key Vault

## Security Considerations

- The chart implements security contexts with `runAsNonRoot` and `readOnlyRootFilesystem`
- Resource limits are set to prevent resource exhaustion
- Network policies should be configured separately for additional security
- TLS should be enabled for production deployments

## Persistence

When PostgreSQL persistence is enabled, the chart creates a PersistentVolumeClaim for database storage. The volume is mounted at `/var/lib/postgresql/data`.

## Troubleshooting

Check the status of pods:
```bash
kubectl get pods -n todo-app
```

View logs for backend:
```bash
kubectl logs -l app.kubernetes.io/component=backend -n todo-app
```

View logs for frontend:
```bash
kubectl logs -l app.kubernetes.io/component=frontend -n todo-app
```

## Contributing

Feel free to submit issues and enhancement requests via the GitHub repository.