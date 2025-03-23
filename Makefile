# Common variables
PROJECT_ROOT := $(shell pwd)
SERVICES := api_gateway document_ingestion document_processing entity_extraction task_orchestration shared

.PHONY: setup install test format lint run clean docker-build docker-up docker-down \
        $(foreach svc,$(SERVICES),$(svc)-test $(svc)-format $(svc)-lint $(svc)-run)

# Default target when running just 'make'
all: setup

# Clean build artifacts and caches
clean:
	@echo "Cleaning project..."
	@find . -type d -name "__pycache__" -not -path "*/\.venv/*" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -not -path "*/\.venv/*" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -not -path "*/\.venv/*" -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -not -path "*/\.venv/*" -delete
	@echo "Python cache files cleaned."

# Deep clean - includes virtual environments
clean-all: clean
	@echo "Performing deep clean..."
	@for svc in $(SERVICES); do \
		if [ -d "$$svc/.venv" ]; then rm -rf $$svc/.venv && echo "Removed $$svc virtual environment."; fi; \
		if [ -f "$$svc/poetry.lock" ]; then rm $$svc/poetry.lock && echo "Removed $$svc poetry.lock file."; fi; \
	done
	@echo "All environments completely cleaned."

# Set up the development environment
setup:
	@echo "Setting up development environment..."
	@./scripts/setup.sh

# Setup with clean environment
setup-clean: clean-all
	@echo "Setting up clean development environment..."
	@./scripts/setup.sh

# Define service-specific targets
define service_targets
$(1)-test:
	@echo "Running tests for $(1)..."
	@cd $(1) && poetry run pytest

$(1)-format:
	@echo "Formatting code for $(1)..."
	@cd $(1) && poetry run black . && poetry run isort .

$(1)-lint:
	@echo "Running linters for $(1)..."
	@cd $(1) && poetry run flake8 .
	@cd $(1) && poetry run mypy -p $(1) || poetry run mypy .

$(1)-check: $(1)-format $(1)-lint

$(1)-run:
	@echo "Starting $(1) service..."
	@cd $(1) && poetry run uvicorn app:app --reload --port=$$($(1)_PORT)
endef

$(foreach svc,$(SERVICES),$(eval $(call service_targets,$(svc))))

# Service environment variables for ports
api_gateway_PORT := 8000
document_ingestion_PORT := 8001
document_processing_PORT := 8002
entity_extraction_PORT := 8003
task_orchestration_PORT := 8004

# Run tests for all services
test-all:
	@echo "Running tests for all services..."
	@for svc in $(SERVICES); do \
		echo "\n=== Testing $$svc ==="; \
		(cd $$svc && poetry run pytest) || exit 1; \
	done

# Format code across all services
format-all:
	@echo "Formatting code for all services..."
	@for svc in $(SERVICES); do \
		echo "\n=== Formatting $$svc ==="; \
		(cd $$svc && poetry run black . && poetry run isort .) || exit 1; \
	done

# Run linting across all services
lint-all:
	@echo "Running linters for all services..."
	@for svc in $(SERVICES); do \
		echo "\n=== Linting $$svc ==="; \
		if [ "$$svc" = "shared" ]; then \
			(cd $$svc && poetry run flake8 . && poetry run mypy .) || exit 1; \
		else \
			(cd $$svc && poetry run flake8 . && poetry run mypy .) || exit 1; \
		fi; \
	done

# Format and lint all services
check-all: format-all lint-all

# Start all services
run-all:
	@echo "Starting all services..."
	@for svc in $(filter-out shared,$(SERVICES)); do \
		$(MAKE) $$svc-run & \
	done

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

# Legacy targets for backward compatibility
test: api_gateway-test
format: format-all
lint: lint-all
check: check-all
run: run-all
