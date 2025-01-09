APP_NAME := thesisgenius-backend
VERSION := $(shell git describe --tags --always --dirty)
DOCKERHUB_UN ?= $(shell whoami)

# Supported architectures
LOCAL_ARCH := $(shell $(CURDIR)/build-support/functions/architecture.sh)
ARCHS := amd64 arm64

# ============> FRONTEND Variables
FRONTEND_DEV_IMAGE ?= $(DOCKERHUB_UN)/$(APP_NAME)-frontend-dev
FRONTEND_PORT ?= 5173

# ============> BACKEND Variables
BACKEND_DEV_IMAGE ?= $(DOCKERHUB_UN)/$(APP_NAME)-dev
BACKEND_APP_PORT ?= 8557

##@ Build
.PHONY: docker-dev-backend
docker-dev-backend: ## Build the backend development Docker image
	@docker buildx use default && docker buildx build \
		--platform linux/$(LOCAL_ARCH) \
		--build-arg APPLICATION_PORT=$(BACKEND_APP_PORT) \
		--build-arg VERSION=dev \
		--tag $(BACKEND_DEV_IMAGE):local \
		--target dev-backend \
		--load \
		$(CURDIR)/backend

.PHONY: docker-dev-frontend
docker-dev-frontend: ## Build the frontend development Docker image
	@docker buildx use default && docker buildx build \
		--platform linux/$(LOCAL_ARCH) \
		--build-arg FRONTEND_PORT=$(FRONTEND_PORT)
		--tag $(FRONTEND_DEV_IMAGE):local \
		--target dev-frontend \
		--load \
		$(CURDIR)/frontend

.PHONY: docker-dev-backend-run
docker-dev-backend-run: ## Run the backend development Docker container
	@docker run -d -p $(BACKEND_APP_PORT):$(BACKEND_APP_PORT) --name $(APP_NAME)-dev-backend $(BACKEND_DEV_IMAGE):local

.PHONY: docker-dev-frontend-run
docker-dev-frontend-run: ## Run the frontend development Docker container
	@docker run -d -p $(FRONTEND_PORT):$(FRONTEND_PORT) --name $(APP_NAME)-dev-frontend $(FRONTEND_DEV_IMAGE):local

.PHONY: docker-stop
docker-stop: ## Stop all running development Docker containers
	@docker stop $(APP_NAME)-dev-backend $(APP_NAME)-dev-frontend || true

.PHONY: docker-clean
docker-clean: ## Remove all development Docker containers and images
	@docker rm -f $(APP_NAME)-dev-backend $(APP_NAME)-dev-frontend || true
	@docker rmi -f $(BACKEND_DEV_IMAGE):local $(FRONTEND_DEV_IMAGE):local || true

##@ Linting
.PHONY: lint
lint: ## Run black, isort, and ruff Python code linters
	@black .
	@isort .
	@ruff check .

.PHONY: check
check: ## Lint check formatting
	@black --check .
	@isort --check-only .
	@ruff check .

##@ Tools
.PHONY: tools
tools: ## Installs various supporting Python development tools.
	@$(SHELL) $(CURDIR)/build-support/scripts/devtools.sh

.PHONY: lint-tools
lint-tools: ## Install tools for linting
	@$(SHELL) $(CURDIR)/build-support/scripts/devtools.sh -lint

##@ Testing
.PHONY: test
test: ## Run tests
	@$(PYTHON) -m unittest discover -s tests

##@ Cleanup
.PHONY: clean
clean: ## Clean up pychache and build artifacts
	@echo "Cleaning up pychache..."
	@find . -name "*.pyc" -delete >/dev/null 2>&1 || true
	@find . -name "__pycache__" -delete >/dev/null 2>&1 || true

##@ Help
.PHONY: help
help: ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

%:
	@:
