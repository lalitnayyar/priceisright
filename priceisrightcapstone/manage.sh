#!/bin/bash
# =============================================================================
# The Price Is Right — Unified Management Script (Linux / macOS / WSL2)
# Author : Lalit Nayyar | lalitnayyar@gmail.com
# Version: 1.3.0
# =============================================================================

set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$APP_DIR"

# ── Colour helpers ────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'

info()    { echo -e "${CYAN}[INFO]${NC}  $*"; }
success() { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error()   { echo -e "${RED}[ERROR]${NC} $*"; }
header()  { echo -e "\n${BOLD}${CYAN}══════════════════════════════════════${NC}"; echo -e "${BOLD}  $*${NC}"; echo -e "${BOLD}${CYAN}══════════════════════════════════════${NC}\n"; }

# ── Docker / docker-compose detection ────────────────────────────────────────
detect_docker() {
    # Check Docker daemon is reachable
    if ! docker info > /dev/null 2>&1; then
        error "Docker daemon is not running or not accessible."
        echo ""
        echo "  If you are on WSL2, please ensure:"
        echo "  1. Docker Desktop is running on Windows."
        echo "  2. Settings → Resources → WSL Integration → Enable for your distro."
        echo "  3. Restart your WSL2 terminal after enabling."
        echo ""
        echo "  Docs: https://docs.docker.com/go/wsl2/"
        exit 1
    fi

    # Prefer 'docker compose' (V2 plugin) over legacy 'docker-compose'
    if docker compose version > /dev/null 2>&1; then
        DC="docker compose"
        info "Using Docker Compose V2 plugin (docker compose)"
    elif command -v docker-compose > /dev/null 2>&1; then
        DC="docker-compose"
        warn "Using legacy docker-compose binary. Consider upgrading to Docker Compose V2."
    else
        error "Neither 'docker compose' nor 'docker-compose' found."
        echo ""
        echo "  Install Docker Compose V2:"
        echo "    sudo apt-get install docker-compose-plugin   # Debian/Ubuntu"
        echo "    brew install docker-compose                  # macOS"
        echo "  Or enable Docker Desktop WSL2 integration."
        exit 1
    fi
}

# ── Helper: ensure .env exists ────────────────────────────────────────────────
ensure_env() {
    if [ ! -f .env ]; then
        warn ".env not found — creating from .env.example"
        cp .env.example .env
        echo ""
        warn "ACTION REQUIRED: Open .env and fill in your API keys before continuing."
        echo "  Required: OPENAI_API_KEY, ANTHROPIC_API_KEY, PUSHOVER_USER, PUSHOVER_TOKEN"
        echo ""
        read -rp "  Press ENTER to continue once you have edited .env, or Ctrl+C to abort: "
    fi
}

# ── Helper: pull latest from GitHub ──────────────────────────────────────────
git_pull() {
    if git remote -v 2>/dev/null | grep -q origin; then
        info "Pulling latest code from GitHub..."
        git pull origin main 2>&1 || warn "Git pull failed — continuing with local files."
    else
        warn "No git remote configured. Skipping pull."
    fi
}

# ── Commands ──────────────────────────────────────────────────────────────────

cmd_deploy() {
    header "Deploying The Price Is Right"
    detect_docker
    git_pull
    ensure_env
    info "Building Docker images (this may take a few minutes on first run)..."
    $DC build
    info "Starting all services..."
    $DC up -d
    echo ""
    success "Deployment complete!"
    echo -e "  Dashboard  → ${BOLD}http://localhost:7860${NC}"
    echo -e "  REST API   → ${BOLD}http://localhost:8001${NC}"
    echo -e "  ChromaDB   → ${BOLD}http://localhost:8000${NC}"
    echo ""
}

cmd_update() {
    header "Updating The Price Is Right"
    detect_docker
    git_pull
    info "Rebuilding images with latest code..."
    $DC build
    info "Restarting services..."
    $DC up -d
    success "Update complete!"
}

cmd_start() {
    header "Starting The Price Is Right"
    detect_docker
    ensure_env
    $DC up -d
    success "All services started."
    echo -e "  Dashboard → ${BOLD}http://localhost:7860${NC}"
}

cmd_stop() {
    header "Stopping The Price Is Right"
    detect_docker
    $DC down
    success "All services stopped."
}

cmd_restart() {
    header "Restarting services"
    detect_docker
    $DC restart
    success "Services restarted."
}

cmd_test() {
    header "Running Test Suite"
    detect_docker
    ensure_env
    mkdir -p tests/reports
    info "Running 118-test suite inside container..."
    $DC run --rm app python scripts/run_tests.py
    success "Tests complete! Reports saved to tests/reports/"
    ls -lh tests/reports/ 2>/dev/null || true
}

cmd_patch() {
    header "Applying Patch"
    detect_docker
    git_pull
    info "Restarting app and api services..."
    $DC restart app api
    success "Patch applied and services restarted."
}

cmd_logs() {
    detect_docker
    SERVICE="${2:-app}"
    info "Streaming logs for service: $SERVICE (Ctrl+C to stop)"
    $DC logs -f "$SERVICE"
}

cmd_status() {
    detect_docker
    header "Container Status"
    $DC ps
}

cmd_diagnose() {
    header "Diagnostic Check"
    echo -e "${BOLD}System:${NC}"
    echo "  OS     : $(uname -a)"
    echo "  Shell  : $SHELL"
    echo ""

    echo -e "${BOLD}Docker:${NC}"
    if docker info > /dev/null 2>&1; then
        echo -e "  Docker daemon  : ${GREEN}RUNNING${NC}"
        docker version --format '  Version        : {{.Server.Version}}' 2>/dev/null || true
    else
        echo -e "  Docker daemon  : ${RED}NOT RUNNING${NC}"
    fi

    if docker compose version > /dev/null 2>&1; then
        echo -e "  Compose V2     : ${GREEN}AVAILABLE${NC} ($(docker compose version --short 2>/dev/null))"
    elif command -v docker-compose > /dev/null 2>&1; then
        echo -e "  Compose legacy : ${YELLOW}AVAILABLE${NC} ($(docker-compose --version))"
    else
        echo -e "  Compose        : ${RED}NOT FOUND${NC}"
    fi
    echo ""

    echo -e "${BOLD}.env file:${NC}"
    if [ -f .env ]; then
        echo -e "  Status : ${GREEN}EXISTS${NC}"
        for key in OPENAI_API_KEY ANTHROPIC_API_KEY PUSHOVER_USER PUSHOVER_TOKEN; do
            val=$(grep "^${key}=" .env 2>/dev/null | cut -d= -f2 || true)
            if [ -n "$val" ] && [ "$val" != "sk-..." ] && [ "$val" != "sk-ant-..." ] && [ "$val" != "..." ]; then
                echo -e "  $key : ${GREEN}SET${NC}"
            else
                echo -e "  $key : ${YELLOW}NOT SET${NC}"
            fi
        done
    else
        echo -e "  Status : ${RED}MISSING${NC} (run ./manage.sh deploy to create)"
    fi
    echo ""

    echo -e "${BOLD}Ports:${NC}"
    for port in 7860 8000 8001; do
        if ss -tlnp 2>/dev/null | grep -q ":$port " || netstat -tlnp 2>/dev/null | grep -q ":$port "; then
            echo -e "  :$port → ${GREEN}IN USE${NC}"
        else
            echo -e "  :$port → ${CYAN}FREE${NC}"
        fi
    done
    echo ""
}

cmd_help() {
    echo ""
    echo -e "${BOLD}${CYAN}The Price Is Right — Management Script v1.3.0${NC}"
    echo -e "  Author: Lalit Nayyar | lalitnayyar@gmail.com"
    echo ""
    echo -e "${BOLD}Usage:${NC}  ./manage.sh <command>"
    echo ""
    echo -e "${BOLD}Commands:${NC}"
    printf "  %-12s %s\n" "deploy"    "Pull from GitHub, build images, start all services"
    printf "  %-12s %s\n" "update"    "Pull latest code, rebuild, and restart services"
    printf "  %-12s %s\n" "start"     "Start all services in the background"
    printf "  %-12s %s\n" "stop"      "Stop all running services"
    printf "  %-12s %s\n" "restart"   "Restart all services"
    printf "  %-12s %s\n" "test"      "Run 118-test suite and generate Markdown report"
    printf "  %-12s %s\n" "patch"     "Git pull and restart app + api services"
    printf "  %-12s %s\n" "logs"      "Stream logs (default: app service)"
    printf "  %-12s %s\n" "status"    "Show container status"
    printf "  %-12s %s\n" "diagnose"  "Run environment diagnostic check"
    printf "  %-12s %s\n" "help"      "Show this help message"
    echo ""
    echo -e "${BOLD}WSL2 Users:${NC}"
    echo "  Ensure Docker Desktop is running and WSL2 integration is enabled."
    echo "  Settings → Resources → WSL Integration → Enable for your distro."
    echo ""
}

# ── Entry point ───────────────────────────────────────────────────────────────
case "${1:-help}" in
    deploy)   cmd_deploy ;;
    update)   cmd_update ;;
    start)    cmd_start ;;
    stop)     cmd_stop ;;
    restart)  cmd_restart ;;
    test)     cmd_test ;;
    patch)    cmd_patch ;;
    logs)     cmd_logs "$@" ;;
    status)   cmd_status ;;
    diagnose) cmd_diagnose ;;
    import-settings) cmd_import_settings "$@" ;;
    help|--help|-h) cmd_help ;;
    *)
        error "Unknown command: ${1}"
        cmd_help
        exit 1
        ;;
esac
