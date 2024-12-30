#!/usr/bin/env bash

# devtools.sh: Sets up the development environment for the project

set -e  # Exit immediately if a command exits with a non-zero status
set -u  # Treat unset variables as an error and exit immediately
set -o pipefail  # Return the exit status of the last command in the pipe that failed

command -v git >/dev/null 2>&1 || {
   error "Git not installed, please install git prior to installing development tools..."
}

# Constants
REPO_ROOT="$(git rev-parse --show-toplevel)"
SCRIPT_DIR="$(dirname "${BASH_SOURCE[0]}")"
VENV_DIR="${REPO_ROOT}/venv"
REQUIREMENTS_FILE="${REPO_ROOT}/requirements.txt"
DEV_REQUIREMENTS_FILE="${REPO_ROOT}/dev-requirements.txt"
PYTHON_EXEC="python3"

source "${SCRIPT_DIR}/functions.sh"

# Function to check if a command exists
function command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install Homebrew if not present
function install_homebrew() {
    if ! command_exists brew; then
        warn "Homebrew is not installed. Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    else
        info "Homebrew is already installed."
    fi
}

# Install Python 3 via Homebrew if not present
function install_python3() {
    if ! command_exists "${PYTHON_EXEC}"; then
        warn "Python 3 is not installed. Installing Python 3 via Homebrew..."
        brew install python
    else
        info "Python 3 is already installed."
    fi
}

# Create or activate virtual environment
function setup_virtualenv() {
    if [ ! -d "${VENV_DIR}" ]; then
        info "Creating virtual environment in ${VENV_DIR}..."
        ${PYTHON_EXEC} -m venv "${VENV_DIR}"
    fi

    info "Activating virtual environment..."
    # shellcheck disable=SC1091
    source "${VENV_DIR}/bin/activate"
}

# Install pip dependencies
function install_dependencies() {
    info "Upgrading pip..."
    pip install --upgrade pip

    if [ -f "${REQUIREMENTS_FILE}" ]; then
        info "Installing dependencies from ${REQUIREMENTS_FILE}..."
        pip install -r "${REQUIREMENTS_FILE}"
    else
        warn "No ${REQUIREMENTS_FILE} file found. Skipping."
    fi

    if [ -f "${DEV_REQUIREMENTS_FILE}" ]; then
        info "Installing development dependencies from ${DEV_REQUIREMENTS_FILE}..."
        pip install -r "${DEV_REQUIREMENTS_FILE}"
    else
        warn "No ${DEV_REQUIREMENTS_FILE} file found. Skipping."
    fi
}

# Ensure required dev tools are installed
function install_devtools() {
    local devtools=("black" "ruff" "isort" "pyinstaller")

    local tool
    for tool in "${devtools[@]}"; do
        if ! command_exists "${tool}"; then
            info "Installing ${tool}..."
            pip install "${tool}"
        else
            info "${tool} is already installed."
        fi
    done
}


# Display usage information
function usage() {
    echo -e "${GREEN}Usage:${RESET} $0 [options]"
    echo -e "\nOptions:"
    echo -e "  -python, -p   Set up Python environment (install Python, virtualenv, and dependencies)"
    echo -e "  -lint,   -l   Install linting and formatting tools (black, ruff, isort, pyinstaller)"
    echo -e "  -all,    -a   Perform all setup tasks (Python environment and linting tools)"
    echo -e "  -help,   -h   Show this help message and exit"
}

# Main script execution with flags
function main() {
    local install_python=false
    local install_lint=false
    local all=true

    # Parse flags
    while [[ "$#" -gt 0 ]]; do
        case "$1" in
            -python|--python|-p)
                install_python=true
                all=false
                shift
                ;;
            -lint|--lint|-l)
                install_lint=true
                all=false
                shift
                ;;
            -all|--all|-a)
                all=true
                shift
                ;;
            -help|--help|-h)
                usage
                exit 0
                ;;
            *)
                error "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
    done

    if [[ "$all" == true ]]; then
        install_python=true
        install_lint=true
    fi

    if [[ "$install_python" == true ]]; then
        info "Setting up Python environment..."
        if [[ "$OSTYPE" == "darwin"* ]]; then
            info "Detected macOS environment."
            install_homebrew
            install_python3
        else
            error "This script is primarily designed for macOS. Other platforms are not yet supported."
            exit 1
        fi
        setup_virtualenv
        install_dependencies
    fi

    if [[ "$install_lint" == true ]]; then
        info "Installing linting and formatting tools..."
        setup_virtualenv  # Activate the virtual environment
        install_devtools
    fi

    if [[ "$install_python" == false && "$install_lint" == false ]]; then
        warn "No flags provided. Use -python, -lint, or -all to specify what to install."
        usage
    fi

    info "Setup complete. Activate your virtual environment using: source ${VENV_DIR}/bin/activate"
}

main "$@"
