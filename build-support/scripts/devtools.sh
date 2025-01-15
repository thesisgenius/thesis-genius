#!/usr/bin/env bash

# devtools.sh: Sets up the development environment for the project

set -e  # Exit immediately if a command exits with a non-zero status
set -u  # Treat unset variables as an error and exit immediately
set -o pipefail  # Return the exit status of the last command in the pipe that failed

SCRIPT_DIR="$(dirname "${BASH_SOURCE[0]}")"
source "${SCRIPT_DIR}/functions.sh"

command -v git >/dev/null 2>&1 || {
   error "Git not installed, please install git prior to installing development tools..."
   exit
}

# Constants
REPO_ROOT="$(git rev-parse --show-toplevel)"
VENV_DIR="${REPO_ROOT}/backend/.venv"
REQUIREMENTS_FILE="${REPO_ROOT}/backend/requirements.txt"
PYTHON_EXEC="python3"



if [[ "$OSTYPE" == "darwin"* ]]; then
    info "Detected macOS environment"; ok
else
    error "This script is primarily designed for macOS. Other platforms are not yet supported."
    exit 1
fi

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
        info "Homebrew is already installed"; ok
        return 0
    fi
    ok
}

# Install act via Homebrew if not present
function install_act() {
    if ! command_exists act; then
        warn "act (local GH actions) is not installed. Installing act via Homebrew..."
        brew install act
    else
        info "act is already installed"; ok
        return 0
    fi
    ok
}

# Install Node.js and Yarn
function install_node_and_yarn() {
    if ! command_exists node; then
        info "Node.js is not installed. Installing Node.js via Homebrew..."
        brew install node >/dev/null 2>&1 || error "Failed to install node!" && exit
        ok
    else
        info "Node.js is already installed"; ok
    fi

    if ! command_exists yarn; then
        info "Yarn is not installed. Installing Yarn..."
        npm install --global yarn >/dev/null 2>&1 || error "Failed to install yarn!" && exit
        ok
    else
        info "Yarn is already installed"
    fi
    ok
}

# Set up frontend dependencies for Vite
function setup_frontend() {
    if [ ! -d "${REPO_ROOT}/frontend" ]; then
        error "Frontend directory not found. Please ensure the Vite project is initialized."
        exit
    fi

    cd "${REPO_ROOT}/frontend"

    info "Installing dependencies from ${REPO_ROOT}/frontend"
    npm install >/dev/null 2>&1 || {
        error "Failed to install frontend dependencies!"
        exit
    }; ok
}

# Install Python 3 via Homebrew if not present
function install_python3() {
    if ! command_exists "${PYTHON_EXEC}"; then
        warn "Python 3 is not installed. Installing Python 3 via Homebrew..."
        brew install python
    else
        info "Python 3 is already installed"; ok
        return 0
    fi
    ok
}

# Create or activate virtual environment
function setup_virtualenv() {
    if [ ! -d "${VENV_DIR}" ]; then
        info "Creating virtual environment in ${VENV_DIR}..."
        ${PYTHON_EXEC} -m venv "${VENV_DIR}"; ok
    fi

    info "Activating virtual environment"
    # shellcheck disable=SC1091
    source "${VENV_DIR}/bin/activate"
    ok
}

# Install pip dependencies
function install_dependencies() {
    info "Upgrading pip"
    pip install --upgrade pip >/dev/null 2>&1 || {
        warn "Failed to upgrade ${PYTHON_EXEC} pip version!"
    }; ok

    if [ -f "${REQUIREMENTS_FILE}" ]; then
        info "Installing dependencies from ${REQUIREMENTS_FILE}"
        pip install -r "${REQUIREMENTS_FILE}" >/dev/null 2>&1 || {
            error "Failed to install pip requirements packages from ${REQUIREMENTS_FILE}!"
            exit
        }; ok
    else
        warn "No ${REQUIREMENTS_FILE} file found. Skipping."
    fi
}

# Ensure required dev tools are installed
function install_devtools() {
    local devtools=("black" "ruff" "isort")

    local tool
    for tool in "${devtools[@]}"; do
        if ! command_exists "${tool}"; then
            info "Installing ${tool}..."
            pip install "${tool}" >/dev/null 2>&1 || error "Failed to install ${tool}!" && exit
            ok
        else
            info "${tool} is already installed"; ok
        fi
    done
}


# Display usage information
function usage() {
    echo -e "${GREEN}Usage:${RESET} $0 [options]"
    echo -e "\nOptions:"
    echo -e "  -docker,   -d   Install Docker Desktop environment for macOS"
    echo -e "  -act            Install act (Local GH Actions) for macOS"
    echo -e "  -python,   -p   Set up Python environment (install Python, virtualenv, and dependencies)"
    echo -e "  -frontend, -f   Set up JavaScript (React) environment (install npm, yarn, and dependencies)"
    echo -e "  -lint,     -l   Install linting and formatting tools (black, ruff, isort)"
    echo -e "  -all,      -a   Perform all setup tasks (Python environment and linting tools)"
    echo -e "  -help,     -h   Show this help message and exit"
}

# Main script execution with flags
function main() {
    local install_docker=false
    local install_act=false
    local install_python=false
    local install_lint=false
    local install_frontend=false
    local configure_frontend=false
    local all=true

    # Parse flags
    while [[ "$#" -gt 0 ]]; do
        case "$1" in
            -docker|--docker|-d)
                install_docker=true
                all=false
                shift
                ;;
            -act|--act)
                install_act=true
                all=false
                shift
                ;;
            -python|--python|-p)
                install_python=true
                all=false
                shift
                ;;
            -frontend|--frontend|-f)
                install_frontend=true
                configure_frontend=true
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
        install_docker=true
        install_act=true
        install_python=true
        install_lint=true
        install_frontend=true
        configure_frontend=true
    fi

    if [[ "$install_docker" == true ]]; then
        install_docker_desktop
    fi

    if [[ "$install_act" == true ]]; then
      install_act
    fi

    if [[ "$install_python" == true ]]; then
        install_homebrew
        install_python3
        setup_virtualenv
        install_dependencies
    fi

    if [[ "$install_lint" == true ]]; then
        setup_virtualenv  # Activate the virtual environment
        install_devtools
    fi

    if [[ "$install_python" == false && "$install_lint" == false && "$install_frontend" == false && "$configure_frontend" == false ]]; then
        warn "No flags provided. Use -python, -lint, or -all to specify what to install."
        usage
    fi

    if [[ "$install_frontend" == true ]]; then
        install_node_and_yarn
    fi

    if [[ "$configure_frontend" == true ]]; then
        setup_frontend
    fi

    info "Development dependency setup complete!"
}

main "$@"
