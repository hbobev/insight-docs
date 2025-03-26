# Common variables
PROJECT_ROOT := $(shell pwd)
SERVICES := api_gateway document_ingestion document_processing entity_extraction task_orchestration shared

.PHONY: setup install test format lint run clean docker-build docker-up docker-down \
        $(foreach svc,$(SERVICES),$(svc)-test $(svc)-format $(svc)-lint $(svc)-run) \
        format-service lint-service check-service check-all-service \
        format lint check check-all

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

# Simplified command syntax: make format|lint|check|check-all service_name
# Handles positional argument for service name
format-cmd:
	@if [ "$(word 2,$(MAKECMDGOALS))" != "" ] && [ -d "$(word 2,$(MAKECMDGOALS))" ]; then \
		$(MAKE) format-service SERVICE=$(word 2,$(MAKECMDGOALS)); \
	else \
		$(MAKE) format-all; \
	fi
	@true

lint-cmd:
	@if [ "$(word 2,$(MAKECMDGOALS))" != "" ] && [ -d "$(word 2,$(MAKECMDGOALS))" ]; then \
		$(MAKE) lint-service SERVICE=$(word 2,$(MAKECMDGOALS)); \
	else \
		$(MAKE) lint-all; \
	fi
	@true

check-cmd:
	@if [ "$(word 2,$(MAKECMDGOALS))" != "" ] && [ -d "$(word 2,$(MAKECMDGOALS))" ]; then \
		$(MAKE) check-service SERVICE=$(word 2,$(MAKECMDGOALS)); \
	else \
		echo "Running format and lint for all services..."; \
		$(MAKE) format-all; \
		$(MAKE) lint-all; \
	fi
	@true

check-all-cmd:
	@if [ "$(word 2,$(MAKECMDGOALS))" != "" ] && [ -d "$(word 2,$(MAKECMDGOALS))" ]; then \
		$(MAKE) check-all-service SERVICE=$(word 2,$(MAKECMDGOALS)); \
	else \
		echo "Running format, lint, and tests for all services..."; \
		$(MAKE) format-all; \
		$(MAKE) lint-all; \
		$(MAKE) test-all; \
	fi
	@true

# Allow service names as pseudo targets for the positional argument system
$(SERVICES):
	@true

# Convenience targets for specifying service by command-line argument
# Usage: make format-service SERVICE=api_gateway
format-service:
	@if [ -z "$(SERVICE)" ]; then \
		echo "Error: SERVICE parameter is required. Example: make format-service SERVICE=api_gateway"; \
		exit 1; \
	elif ! echo "$(SERVICES)" | grep -w "$(SERVICE)" > /dev/null; then \
		echo "Error: '$(SERVICE)' is not a valid service. Valid services are: $(SERVICES)"; \
		exit 1; \
	else \
		echo "Formatting code for $(SERVICE)..."; \
		cd "$(PROJECT_ROOT)/$(SERVICE)" && poetry run black . && poetry run isort .; \
	fi

# Usage: make lint-service SERVICE=api_gateway
lint-service:
	@if [ -z "$(SERVICE)" ]; then \
		echo "Error: SERVICE parameter is required. Example: make lint-service SERVICE=api_gateway"; \
		exit 1; \
	elif ! echo "$(SERVICES)" | grep -w "$(SERVICE)" > /dev/null; then \
		echo "Error: '$(SERVICE)' is not a valid service. Valid services are: $(SERVICES)"; \
		exit 1; \
	else \
		echo "Running linters for $(SERVICE)..."; \
		cd "$(PROJECT_ROOT)/$(SERVICE)" && poetry run flake8 .; \
		cd "$(PROJECT_ROOT)/$(SERVICE)" && poetry run mypy .; \
	fi

# Usage: make check-service SERVICE=api_gateway
check-service:
	@if [ -z "$(SERVICE)" ]; then \
		echo "Error: SERVICE parameter is required. Example: make check-service SERVICE=api_gateway"; \
		exit 1; \
	elif ! echo "$(SERVICES)" | grep -w "$(SERVICE)" > /dev/null; then \
		echo "Error: '$(SERVICE)' is not a valid service. Valid services are: $(SERVICES)"; \
		exit 1; \
	else \
		echo "Running format and lint for $(SERVICE)..."; \
		$(MAKE) format-service SERVICE=$(SERVICE); \
		$(MAKE) lint-service SERVICE=$(SERVICE); \
	fi

# Usage: make check-all-service SERVICE=api_gateway
check-all-service:
	@if [ -z "$(SERVICE)" ]; then \
		echo "Error: SERVICE parameter is required. Example: make check-all-service SERVICE=api_gateway"; \
		exit 1; \
	elif ! echo "$(SERVICES)" | grep -w "$(SERVICE)" > /dev/null; then \
		echo "Error: '$(SERVICE)' is not a valid service. Valid services are: $(SERVICES)"; \
		exit 1; \
	else \
		echo "Running format, lint, and tests for $(SERVICE)..."; \
		$(MAKE) format-service SERVICE=$(SERVICE) && \
		$(MAKE) lint-service SERVICE=$(SERVICE) && \
		cd "$(PROJECT_ROOT)/$(SERVICE)" && poetry run pytest; \
	fi

# Define service-specific targets
define service_targets
$(1)-test:
	@echo "Running tests for $(1)..."
	@cd "$(PROJECT_ROOT)/$(1)" && poetry run pytest

$(1)-format:
	@echo "Formatting code for $(1)..."
	@cd "$(PROJECT_ROOT)/$(1)" && poetry run black . && poetry run isort .

$(1)-lint:
	@echo "Running linters for $(1)..."
	@cd "$(PROJECT_ROOT)/$(1)" && poetry run flake8 .
	@cd "$(PROJECT_ROOT)/$(1)" && poetry run mypy .

$(1)-check: $(1)-format $(1)-lint

$(1)-run:
	@echo "Starting $(1) service..."
	@cd "$(PROJECT_ROOT)/$(1)" && poetry run uvicorn app:app --reload --port=$$($(1)_PORT)
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
test: 
	@if [ "$(word 2,$(MAKECMDGOALS))" != "" ] && [ -d "$(word 2,$(MAKECMDGOALS))" ]; then \
		$(MAKE) $(word 2,$(MAKECMDGOALS))-test; \
	else \
		$(MAKE) api_gateway-test; \
	fi
	@true

format: format-cmd
lint: lint-cmd
check: check-cmd
run: 
	@if [ "$(word 2,$(MAKECMDGOALS))" != "" ] && [ -d "$(word 2,$(MAKECMDGOALS))" ]; then \
		$(MAKE) $(word 2,$(MAKECMDGOALS))-run; \
	else \
		$(MAKE) run-all; \
	fi
	@true
