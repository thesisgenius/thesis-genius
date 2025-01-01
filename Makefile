APP_NAME := thesisgenius-api
VERSION := $(shell git describe --tags --always --dirty)
DOCKERHUB_UN ?= $(shell whoami)

# Supported architectures
LOCAL_ARCH := $(shell $(CURDIR)/build-support/functions/architecture.sh)
ARCHS := amd64 arm64

##@ Build

# Build Docker images for all platforms
.PHONY: docker-dev-api
docker-dev-api:
	@docker buildx use default && docker buildx build \
		--platform linux/$(LOCAL_ARCH) \
		--build-arg APPLICATION_PORT=$(API_APP_PORT) \
		--build-arg VERSION=dev \
		--tag $(API_DEV_IMAGE):local \
		--target dev-api \
		--load .

.PHONY: docker-dev-api-run
docker-dev-api-run:
	@docker run -d -p $(API_APP_PORT):$(API_APP_PORT) --name $(APP_NAME)-dev $(API_DEV_IMAGE):local

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
test: ## Run tests
	@$(PYTHON) -m unittest discover -s tests

##@ Cleanup
clean: ## Clean up pychache and build artifacts
	@echo "Cleaning up pychache..."
	@find . -name "*.pyc" -delete >/dev/null 2>&1 || true
	@find . -name "__pycache__" -delete >/dev/null 2>&1 || true

# ===========> Makefile config
.DEFAULT_GOAL := help
SHELL = bash
PYTHON := python
PIP := $(PYTHON) -m pip

# API Variables
API_DEV_IMAGE ?= $(DOCKERHUB_UN)/$(APP_NAME)-dev
API_APP_PORT ?= 8557

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
