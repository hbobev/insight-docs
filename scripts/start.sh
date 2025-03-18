#!/bin/bash
set -e

# ANSI color codes for pretty output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}====== InsightDocs Service Starter ======${NC}"

# Function to check if Docker is running
check_docker() {
  if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}Docker does not seem to be running. Please start Docker first.${NC}"
    exit 1
  fi
}

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${RED}.env file does not exist. Please run setup.sh first.${NC}"
    exit 1
fi

# Check Docker status
check_docker

# Parse command line options
MODE="docker"
BUILD=false
DETACHED=true
SERVICES=""

function print_usage() {
    echo -e "Usage: ./start.sh [OPTIONS]"
    echo -e "Options:"
    echo -e "  -h, --help        Show this help message"
    echo -e "  -b, --build       Force rebuild containers before starting"
    echo -e "  -f, --foreground  Run in foreground (not detached mode)"
    echo -e "  -s, --services    Specify comma-separated list of services to start"
    echo -e "\nExamples:"
    echo -e "  ./start.sh                         # Start all services in detached mode"
    echo -e "  ./start.sh -b -f                   # Rebuild and start all services in foreground mode"
    echo -e "  ./start.sh -s mongodb,postgres     # Start only MongoDB and PostgreSQL"
}

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -h|--help) print_usage; exit 0 ;;
        -b|--build) BUILD=true ;;
        -f|--foreground) DETACHED=false ;;
        -s|--services) SERVICES="$2"; shift ;;
        *) echo "Unknown parameter: $1"; print_usage; exit 1 ;;
    esac
    shift
done

# Construct Docker Compose command
DOCKER_COMPOSE_CMD="docker compose"

if [ "$BUILD" = true ]; then
    echo -e "${YELLOW}Rebuilding containers before starting...${NC}"
    if [ -z "$SERVICES" ]; then
        $DOCKER_COMPOSE_CMD build
    else
        # Build only specified services
        $DOCKER_COMPOSE_CMD build $(echo $SERVICES | tr ',' ' ')
    fi
fi

# Start services
echo -e "${GREEN}Starting services...${NC}"

if [ "$DETACHED" = true ]; then
    DOCKER_COMPOSE_CMD="$DOCKER_COMPOSE_CMD up -d"
else
    DOCKER_COMPOSE_CMD="$DOCKER_COMPOSE_CMD up"
fi

if [ -z "$SERVICES" ]; then
    # Start all services
    echo -e "${BLUE}Starting all services${NC}"
    eval $DOCKER_COMPOSE_CMD
else
    # Start only specified services
    echo -e "${BLUE}Starting services: $SERVICES${NC}"
    eval "$DOCKER_COMPOSE_CMD $(echo $SERVICES | tr ',' ' ')"
fi

# If detached, show running services
if [ "$DETACHED" = true ]; then
    echo -e "${GREEN}Services started in detached mode.${NC}"
    echo -e "${YELLOW}Running services:${NC}"
    docker compose ps
    
    # Try to get the API Gateway port from .env file
    API_PORT=$(grep -E "^API_GATEWAY_PORT" .env | cut -d= -f2 || echo "8000")
    echo -e "${GREEN}API Gateway should be available at: ${YELLOW}http://localhost:$API_PORT${NC}"
    
    echo -e "\n${BLUE}Useful commands:${NC}"
    echo -e "  ${YELLOW}docker compose logs -f${NC}            # View logs from all services"
    echo -e "  ${YELLOW}docker compose logs -f SERVICE${NC}    # View logs from a specific service"
    echo -e "  ${YELLOW}docker compose stop${NC}               # Stop all services"
    echo -e "  ${YELLOW}docker compose down${NC}               # Stop and remove containers"
fi

echo -e "${BLUE}========================================${NC}"
