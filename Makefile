APP_NAME_BACKEND := thesisgenius-api
VERSION := $(shell git describe --tags --always --dirty)
DOCKER_IMAGE := ghcr.io/$(GITHUB_USERNAME)/$(APP_NAME)
DIST_DIR := dist

# Supported architectures
ARCHS := amd64 arm64

##@ Build

.PHONY: install
install: ## Install dependencies (requirements.txt)
	@$(PIP) install -r requirements.txt

##@ Linting
.PHONY: black
black:
	@black .

.PHONY: isort
isort:
	@isort .

.PHONY: ruff
ruff:
	@ruff check .

.PHONY: lint
lint: black isort ruff ## Run black, isort, and ruff Python code linters

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
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	rm -rf $(DIST_DIR)

# ===========> Makefile config
.DEFAULT_GOAL := help
SHELL = bash
PYTHON := python
PIP := $(PYTHON) -m pip

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
