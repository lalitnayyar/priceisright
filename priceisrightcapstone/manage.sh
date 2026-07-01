#!/bin/bash

# The Price Is Right - Unified Management Script

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$APP_DIR"

function show_help {
    echo "The Price Is Right - Management Script"
    echo "Usage: ./manage.sh [command]"
    echo ""
    echo "Commands:"
    echo "  deploy   - Pull latest from GitHub, build and start containers"
    echo "  update   - Pull latest from GitHub and restart containers"
    echo "  start    - Start all containers in background"
    echo "  stop     - Stop all containers"
    echo "  test     - Run unit tests and generate markdown report"
    echo "  patch    - Apply a quick patch and restart"
    echo "  status   - Show container status"
    echo ""
}

function deploy {
    echo "Deploying The Price Is Right..."
    git pull origin main || echo "Git pull failed, continuing with local files..."
    if [ ! -f .env ]; then
        echo "Creating .env from .env.example..."
        cp .env.example .env
    fi
    docker-compose build
    docker-compose up -d
    echo "Deployment complete! Dashboard available at http://localhost:7860"
}

function update {
    echo "Updating application..."
    git pull origin main
    docker-compose build
    docker-compose up -d
    echo "Update complete!"
}

function start {
    echo "Starting application..."
    docker-compose up -d
    echo "Application started!"
}

function stop {
    echo "Stopping application..."
    docker-compose down
    echo "Application stopped!"
}

function run_tests {
    echo "Running test suite..."
    docker-compose run --rm app python scripts/run_tests.py
    echo "Tests complete! Check tests/reports/ directory for markdown reports."
}

function patch {
    echo "Applying patch..."
    git pull origin main
    docker-compose restart app api
    echo "Patch applied and services restarted!"
}

function status {
    docker-compose ps
}

case "$1" in
    deploy) deploy ;;
    update) update ;;
    start) start ;;
    stop) stop ;;
    test) run_tests ;;
    patch) patch ;;
    status) status ;;
    *) show_help ;;
esac
