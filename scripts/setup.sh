#!/bin/bash
set -e

# ANSI color codes for pretty output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}====== InsightDocs Setup Script ======${NC}"

# Check if Poetry is installed
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

# Get the project root directory
SCRIPT_PATH=$(get_abs_path "$0")
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")
PROJECT_ROOT=$(dirname "$SCRIPT_DIR")

# Configure Poetry to create virtual environment in project directory
echo -e "${BLUE}Configuring Poetry to use in-project virtual environment...${NC}"
poetry config virtualenvs.in-project true

# Install dependencies using the new script
echo -e "${BLUE}Installing project dependencies...${NC}"
bash "$(dirname "$(get_abs_path "$0")")/install_dependencies.sh"

# Display virtual environment activation instructions
echo -e "${YELLOW}To activate a service's virtual environment:${NC}"
echo -e "Navigate to the service directory and run: ${GREEN}poetry shell${NC}"
echo -e "Or: ${GREEN}source .venv/bin/activate${NC}"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed or not in PATH.${NC}"
    echo -e "Please install Docker before continuing: https://docs.docker.com/get-docker/"
else
    echo -e "${GREEN}Docker is installed.${NC}"
fi

# Check if Docker Compose is installed
if ! command -v docker compose &> /dev/null; then
    echo -e "${RED}Docker Compose is not installed or not in PATH.${NC}"
    echo -e "If you're using Docker Desktop, it should be included."
    echo -e "Otherwise, visit: https://docs.docker.com/compose/install/"
else
    echo -e "${GREEN}Docker Compose is installed.${NC}"
fi

# Create .env file from example if it doesn't exist
if [ ! -f "${PROJECT_ROOT}/.env" ]; then
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    cp "${PROJECT_ROOT}/.env.example" "${PROJECT_ROOT}/.env"
    echo -e "${GREEN}.env file created. You may want to edit it with your configuration.${NC}"
else
    echo -e "${YELLOW}.env file already exists. Skipping creation.${NC}"
fi

echo -e "${BLUE}To build and start services:${NC}"
echo -e "${YELLOW}./start.sh${NC}"
echo -e "For more options: ${YELLOW}./start.sh --help${NC}"
echo -e "${GREEN}Setup completed successfully!${NC}"
echo -e "${BLUE}=====================================${NC}"
