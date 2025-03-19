.PHONY: setup install test format lint run clean docker-build docker-up docker-down

# Default target when running just 'make'
all: setup

# Clean build artifacts and caches
clean:
	@echo "Cleaning project..."
	@find . -type d -name "__pycache__" -not -path "./.venv/*" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -not -path "./.venv/*" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -not -path "./.venv/*" -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -not -path "./.venv/*" -delete
	@echo "Python cache files cleaned."

# Deep clean - includes virtual environment
clean-all: clean
	@echo "Performing deep clean..."
	@if [ -d ".venv" ]; then rm -rf .venv && echo "Removed virtual environment."; fi
	@if [ -f "poetry.lock" ]; then echo "Removing poetry.lock file..."; rm poetry.lock && echo "Poetry lock file removed."; fi
	@echo "Environment completely cleaned."

# Set up the development environment
setup:
	@echo "Setting up development environment..."
	@./scripts/setup.sh

# Setup with clean environment
setup-clean: clean-all
	@echo "Setting up clean development environment..."
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
