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
# Backend virtual environment directory
BACKEND_VENV := $(CURDIR)/backend/.venv
PYTHON_BIN := $(BACKEND_VENV)/bin

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
lint: lint-backend lint-frontend

.PHONY: lint-backend
lint-backend: check-venv ## Run black, isort, and ruff Python code linters
	@echo "==> Linting Python backend..."
	@$(PYTHON_BIN)/black .
	@$(PYTHON_BIN)/isort .
	@$(PYTHON_BIN)/ruff check .

.PHONY: lint-frontend
lint-frontend:
	@echo "==> Linting React frontend..."
	cd frontend && npm install && npm run lint

.PHONY: lint-fix-backend
lint-fix-backend: check-venv ## Run black, isort, and ruff Python code linters
	@$(PYTHON_BIN)/black . --fix
	@$(PYTHON_BIN)/isort . --fix
	@$(PYTHON_BIN)/ruff check . --fix

.PHONY: lint-fix-frontend
lint-fix-frontend:
	@echo "==> Running lint + fix (React frontend)..."
	cd frontend && npm install && npm run lint:fix

.PHONY: check
check: check-venv ## Lint check formatting
	@$(PYTHON_BIN)/black --check .
	@$(PYTHON_BIN)/isort --check-only .
	@$(PYTHON_BIN)/ruff check .

.PHONY: check-venv
check-venv: ## Ensure the virtual environment and tools are set up
	@if [ ! -d "$(BACKEND_VENV)" ]; then \
		echo "Error: Virtual environment not found at $(BACKEND_VENV). Run 'make setup-venv' to create it."; \
		exit 1; \
	fi
	@if [ ! -x "$(PYTHON_BIN)/black" ] || [ ! -x "$(PYTHON_BIN)/isort" ] || [ ! -x "$(PYTHON_BIN)/ruff" ]; then \
		echo "Error: One or more linters are missing in the virtual environment. Run 'make setup-venv' to install them."; \
		exit 1; \
	fi

.PHONY: setup-venv
setup-venv: ## Create the virtual environment and install linters
	@if [ ! -d "$(BACKEND_VENV)" ]; then \
		python3 -m venv $(BACKEND_VENV); \
	fi
	@$(PYTHON_BIN)/pip install --upgrade pip
	@$(PYTHON_BIN)/pip install black isort ruff
	@echo "Virtual environment set up with linters."

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

SHELL=bash
.DEFAULT_GOAL := help
##@ Help

# The help target prints out all targets with their descriptions organized
# beneath their categories. The categories are represented by '##@' and the
# target descriptions by '##'. The awk commands is responsible for reading the
# entire set of makefiles included in this invocation, looking for lines of the
# file as xyz: ## something, and then pretty-format the target and help. Then,
# if there's a line with ##@ something, that gets pretty-printed as a category.
# More info on the usage of ANSI control characters for terminal formatting:
# https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_parameters
# More info on the awk command:
# http://linuxcommand.org/lc3_adv_awk.php
.PHONY: help
help: ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

%:
	@:
