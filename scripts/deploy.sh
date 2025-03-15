#!/bin/bash

# Build Docker images
echo "Building Docker images..."
docker-compose build

# Deploy services
echo "Deploying services..."
docker-compose up -d

echo "Deployment complete!"
