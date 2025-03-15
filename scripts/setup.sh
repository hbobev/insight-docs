#!/bin/bash

echo "Setting up InsightDocs development environment..."

# Only upgrade pip and install Poetry if not already installed
if ! command -v poetry &> /dev/null; then
    echo "Installing Poetry..."
    pip install --upgrade pip
    pip install poetry
else
    echo "Poetry already installed, skipping installation."
fi

# Install dependencies
echo "Installing project dependencies..."
poetry install --no-root

# Create .env file from example if it doesn't exist
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file from .env.example"
fi

echo "Setup complete!"
