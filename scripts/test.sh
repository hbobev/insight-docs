#!/bin/bash

# Run unit tests
echo "Running unit tests..."
python -m pytest tests/unit -v

# Run integration tests
echo "Running integration tests..."
python -m pytest tests/integration -v

# Run end-to-end tests
echo "Running end-to-end tests..."
python -m pytest tests/e2e -v
