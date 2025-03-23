#!/bin/bash
set -e

# ANSI color codes for pretty output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}====== InsightDocs Dependency Installation ======${NC}"

if ! command -v poetry &> /dev/null; then
    echo -e "${RED}Poetry is required but not installed or not in PATH.${NC}"
    echo -e "Please install Poetry before running this script: https://python-poetry.org/docs/#installation"
    exit 1
else
    echo -e "${GREEN}Poetry is installed.${NC}"
fi

# Portable replacement for realpath
get_abs_path() {
    # $1 : relative filename
    if [[ -d "$1" ]]; then
        # dir
        (cd "$1"; pwd)
    elif [[ -f "$1" ]]; then
        # file
        if [[ $1 == */* ]]; then
            echo "$(cd "${1%/*}"; pwd)/${1##*/}"
        else
            echo "$(pwd)/$1"
        fi
    else
        echo "$1" does not exist! >&2
        return 127
    fi
}

echo -e "${BLUE}Configuring Poetry to use in-project virtual environment...${NC}"
poetry config virtualenvs.in-project true

SERVICES=("api_gateway" "document_ingestion" "document_processing" "entity_extraction" "task_orchestration" "shared")

# Get the project root directory
SCRIPT_PATH=$(get_abs_path "$0")
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")
PROJECT_ROOT=$(dirname "$SCRIPT_DIR")

# Install shared dependencies first
echo -e "${BLUE}Installing shared dependencies...${NC}"
cd "${PROJECT_ROOT}/shared"
poetry install --no-root
echo -e "${GREEN}Shared dependencies installed successfully.${NC}"

# Install dependencies for each service
for service in "${SERVICES[@]}"; do
    if [ "$service" == "shared" ]; then
        continue
    fi
    
    echo -e "${BLUE}Installing dependencies for ${service}...${NC}"
    cd "${PROJECT_ROOT}/${service}"
    
    # Create a symbolic link to the shared directory if it doesn't exist
    if [ ! -L "shared" ] && [ ! -d "shared" ]; then
        echo -e "${YELLOW}Creating symbolic link to shared directory...${NC}"
        ln -sf "../shared" shared
    fi
    
    # Install dependencies with --no-root flag to avoid packaging the current project
    poetry install --no-root
    echo -e "${GREEN}Dependencies for ${service} installed successfully.${NC}"
done

echo -e "${GREEN}All dependencies installed successfully!${NC}"
echo -e "${BLUE}=============================================${NC}"
echo -e "${YELLOW}To activate a service's virtual environment:${NC}"
echo -e "Navigate to the service directory and run: ${GREEN}poetry shell${NC}"
echo -e "Or: ${GREEN}source .venv/bin/activate${NC}"
