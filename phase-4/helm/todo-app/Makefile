# Helm Chart Makefile for Todo App

CHART_NAME = todo-app
NAMESPACE = todo-app
RELEASE_NAME = my-todo-app
HELM_CHART_PATH = .
VALUES_FILE ?= values.yaml

.PHONY: help lint template install upgrade uninstall test clean

help:
	@echo "Makefile for $(CHART_NAME) Helm Chart"
	@echo ""
	@echo "Usage:"
	@echo "  make lint      - Lint the Helm chart"
	@echo "  make template  - Template the Helm chart locally"
	@echo "  make install   - Install the Helm chart"
	@echo "  make upgrade   - Upgrade the Helm chart"
	@echo "  make uninstall - Uninstall the Helm chart"
	@echo "  make test      - Test the Helm chart"
	@echo "  make clean     - Clean up test resources"

lint:
	helm lint $(HELM_CHART_PATH)

template:
	helm template $(RELEASE_NAME) $(HELM_CHART_PATH) -f $(VALUES_FILE) --namespace $(NAMESPACE)

install:
	helm install $(RELEASE_NAME) $(HELM_CHART_PATH) \
		--namespace $(NAMESPACE) \
		--create-namespace \
		-f $(VALUES_FILE)

upgrade:
	helm upgrade $(RELEASE_NAME) $(HELM_CHART_PATH) \
		--namespace $(NAMESPACE) \
		-f $(VALUES_FILE)

uninstall:
	helm uninstall $(RELEASE_NAME) --namespace $(NAMESPACE)

test: lint template
	@echo "Running chart tests..."
	helm unittest $(HELM_CHART_PATH) || echo "Unit tests not configured or failed"

clean:
	kubectl delete namespace $(NAMESPACE) --ignore-not-found=true

# Dry run without installing
dry-run:
	helm install $(RELEASE_NAME) $(HELM_CHART_PATH) \
		--namespace $(NAMESPACE) \
		--create-namespace \
		--dry-run \
		-f $(VALUES_FILE)

# Get status of release
status:
	helm status $(RELEASE_NAME) --namespace $(NAMESPACE)

# Rollback to previous version
rollback:
	helm rollback $(RELEASE_NAME) --namespace $(NAMESPACE)

# Get values from release
get-values:
	helm get values $(RELEASE_NAME) --namespace $(NAMESPACE)

# Get manifest from release
get-manifest:
	helm get manifest $(RELEASE_NAME) --namespace $(NAMESPACE)

# Diff between current and new release (requires helm-diff plugin)
diff:
	helm diff upgrade $(RELEASE_NAME) $(HELM_CHART_PATH) \
		--namespace $(NAMESPACE) \
		-f $(VALUES_FILE)

# Create a tarball of the chart
package:
	helm package $(HELM_CHART_PATH)

# Push to registry (requires helm-push plugin)
push: package
	helm push $(CHART_NAME)-*.tgz oci://YOUR_REGISTRY