.PHONY: setup install test format lint run clean docker-build docker-up docker-down

# Default target when running just 'make'
all: setup

# Set up the development environment
setup:
	@echo "Setting up development environment..."
	@./scripts/setup.sh

# Explicitly install dependencies (useful for CI/CD)
install:
	@poetry install --no-root

# Run tests
test:
	@echo "Running tests..."
	@pytest

# Format code with black and isort
format:
	@echo "Formatting code..."
	@black .
	@isort .

# Run linting checks
lint:
	@echo "Running linters..."
	@flake8 .
	@mypy .

# Run the development server
run:
	@echo "Starting development server..."
	@docker-compose up -d

# Clean build artifacts and caches
clean:
	@echo "Cleaning project..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +

# Build Docker images
docker-build:
	@echo "Building Docker images..."
	@docker-compose build

# Start Docker containers
docker-up:
	@echo "Starting Docker containers..."
	@docker-compose up -d

# Stop Docker containers
docker-down:
	@echo "Stopping Docker containers..."
	@docker-compose down
