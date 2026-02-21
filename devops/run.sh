#!/bin/bash

echo "🚀 Starting DevOps Test App..."

if ! command -v docker &> /dev/null
then
    echo "❌ Docker is not installed"
    exit 1
fi

if docker compose version &> /dev/null
then
    COMPOSE_CMD="docker compose"
elif docker-compose version &> /dev/null
then
    COMPOSE_CMD="docker-compose"
else
    echo "❌ Docker Compose not found"
    exit 1
fi

echo "📦 Using: $COMPOSE_CMD"

$COMPOSE_CMD down -v 
$COMPOSE_CMD up --build

echo "✅ App is running at: http://localhost:5000"
