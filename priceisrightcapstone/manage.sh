#!/usr/bin/env bash
# =============================================================================
#  The Price Is Right — AI Deal Hunter
#  Interactive Management Console
#  Author : Lalit Nayyar  |  lalitnayyar@gmail.com
#  Phone  : +971 508 320 336  |  +91 959 535 3336
#  GitHub : https://github.com/lalitnayyar/priceisright
#  Version: 2.0.0
# =============================================================================

set -euo pipefail
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$APP_DIR"

# ── Terminal colours ──────────────────────────────────────────────────────────
RED='\033[0;31m';    GREEN='\033[0;32m';   YELLOW='\033[1;33m'
CYAN='\033[0;36m';   BLUE='\033[0;34m';    MAGENTA='\033[0;35m'
WHITE='\033[1;37m';  BOLD='\033[1m';       DIM='\033[2m';  NC='\033[0m'
BG_DARK='\033[48;5;232m'

info()    { echo -e "${CYAN}  [INFO]${NC}  $*"; }
ok()      { echo -e "${GREEN}  [ OK ]${NC}  $*"; }
warn()    { echo -e "${YELLOW}  [WARN]${NC}  $*"; }
err()     { echo -e "${RED}  [ERR ]${NC}  $*"; }
sep()     { echo -e "${DIM}  ──────────────────────────────────────────────────────${NC}"; }

# ── Clear + splash screen ─────────────────────────────────────────────────────
show_splash() {
    clear
    echo ""
    echo -e "${BOLD}${CYAN}"
    echo "  ╔══════════════════════════════════════════════════════════════════╗"
    echo "  ║                                                                  ║"
    echo "  ║    💰  THE PRICE IS RIGHT — AI DEAL HUNTER  💰                  ║"
    echo "  ║         Multi-Agent Price Estimation System                      ║"
    echo "  ║                                                                  ║"
    echo -e "  ╠══════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${BOLD}${WHITE}"
    echo "  ║                                                                  ║"
    echo "  ║   👤  Author  :  Lalit Nayyar                                   ║"
    echo "  ║   📧  Email   :  lalitnayyar@gmail.com                          ║"
    echo "  ║   📱  Mobile  :  +971 508 320 336  |  +91 959 535 3336          ║"
    echo "  ║   🐙  GitHub  :  github.com/lalitnayyar/priceisright             ║"
    echo "  ║   🏷️  Version :  v2.0.0                                          ║"
    echo "  ║                                                                  ║"
    echo -e "  ╠══════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${DIM}${CYAN}"
    echo "  ║  7-Agent AI Framework:  Scanner · Frontier · Specialist · DNN   ║"
    echo "  ║                         Ensemble · Messaging · Planning          ║"
    echo "  ║  Stack: Python · FastAPI · Gradio · ChromaDB · Docker            ║"
    echo -e "  ╚══════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# ── Docker / compose detection ────────────────────────────────────────────────
detect_docker() {
    if ! docker info > /dev/null 2>&1; then
        err "Docker daemon is not running or not accessible."
        echo ""
        echo -e "  ${YELLOW}WSL2 Users — follow these steps:${NC}"
        echo "    1. Open Docker Desktop on Windows"
        echo "    2. Settings → Resources → WSL Integration"
        echo "    3. Enable toggle for your distro (e.g. Ubuntu)"
        echo "    4. Click Apply & Restart"
        echo "    5. Open a new WSL2 terminal and retry"
        echo ""
        echo "    Docs: https://docs.docker.com/go/wsl2/"
        echo ""
        press_any_key
        return 1
    fi
    if docker compose version > /dev/null 2>&1; then
        DC="docker compose"
    elif command -v docker-compose > /dev/null 2>&1; then
        DC="docker-compose"
        warn "Using legacy docker-compose. Consider upgrading to Compose V2."
    else
        err "Neither 'docker compose' nor 'docker-compose' found."
        echo ""
        echo "  Install: sudo apt-get install docker-compose-plugin"
        echo ""
        press_any_key
        return 1
    fi
}

ensure_env() {
    if [ ! -f .env ]; then
        warn ".env not found — creating from .env.example"
        cp .env.example .env
        echo ""
        warn "Please edit .env and set your API keys before running."
        echo "  Required keys: OPENAI_API_KEY, ANTHROPIC_API_KEY"
        echo "  Optional keys: PUSHOVER_USER, PUSHOVER_TOKEN, MODAL_TOKEN_ID"
        echo ""
    fi
}

git_pull() {
    if git rev-parse --git-dir > /dev/null 2>&1; then
        info "Pulling latest code from GitHub..."
        git pull origin main 2>&1 | sed 's/^/    /' || warn "Git pull failed — continuing with local code."
    fi
}

press_any_key() {
    echo ""
    echo -e "  ${DIM}Press any key to continue...${NC}"
    read -n 1 -s -r
}

# ── Status bar ────────────────────────────────────────────────────────────────
show_status_bar() {
    detect_docker 2>/dev/null || true
    local docker_ok="${RED}✗ Stopped${NC}"
    local env_ok="${RED}✗ Missing${NC}"
    local settings_ok="${RED}✗ Not saved${NC}"

    docker info > /dev/null 2>&1 && docker_ok="${GREEN}✓ Running${NC}"
    [ -f .env ] && env_ok="${GREEN}✓ Found${NC}"
    [ -f data/ui_settings.json ] && settings_ok="${GREEN}✓ Saved${NC}"

    echo -e "  ${DIM}Docker: ${docker_ok}${DIM}  |  .env: ${env_ok}${DIM}  |  Settings: ${settings_ok}${NC}"
    sep
}

# ── Main menu ─────────────────────────────────────────────────────────────────
show_main_menu() {
    show_splash
    show_status_bar
    echo ""
    echo -e "  ${BOLD}${WHITE}MAIN MENU${NC}"
    echo ""
    echo -e "  ${BOLD}${GREEN} 1)${NC}  🚀  Deploy          — First-time setup: pull, build, start"
    echo -e "  ${BOLD}${GREEN} 2)${NC}  🔄  Update          — Pull latest code, rebuild, restart"
    echo -e "  ${BOLD}${GREEN} 3)${NC}  ▶️   Start           — Start all services"
    echo -e "  ${BOLD}${GREEN} 4)${NC}  ⏹️   Stop            — Stop all services"
    echo -e "  ${BOLD}${GREEN} 5)${NC}  🔁  Restart         — Restart all services"
    echo -e "  ${BOLD}${CYAN}  6)${NC}  🩹  Patch           — Git pull + restart (no rebuild)"
    echo -e "  ${BOLD}${CYAN}  7)${NC}  🧪  Test            — Run 118-test suite + generate report"
    echo -e "  ${BOLD}${CYAN}  8)${NC}  📋  Status          — Show container status"
    echo -e "  ${BOLD}${CYAN}  9)${NC}  📜  Logs            — Stream service logs"
    echo -e "  ${BOLD}${YELLOW}10)${NC}  🔍  Diagnose        — Pre-flight environment checks"
    echo -e "  ${BOLD}${YELLOW}11)${NC}  📥  Import Settings — Apply a settings.json file"
    echo -e "  ${BOLD}${MAGENTA}12)${NC}  ℹ️   About / Help    — Show full help and documentation"
    echo ""
    echo -e "  ${BOLD}${RED} 0)${NC}  ❌  Exit"
    echo ""
    sep
    echo -ne "  ${BOLD}${WHITE}Select option [0-12]: ${NC}"
}

# ── Sub-menus / parameter info ────────────────────────────────────────────────

info_deploy() {
    clear
    echo ""
    echo -e "  ${BOLD}${GREEN}🚀  DEPLOY — First-Time Setup${NC}"
    sep
    echo ""
    echo -e "  ${BOLD}What it does:${NC}"
    echo "    1. Pulls the latest code from GitHub (main branch)"
    echo "    2. Creates .env from .env.example if missing"
    echo "    3. Builds all Docker images (app, api, rag-init)"
    echo "    4. Starts all 4 services: chromadb, rag-init, api, app"
    echo "    5. Waits for ChromaDB healthcheck to pass"
    echo ""
    echo -e "  ${BOLD}Services started:${NC}"
    echo -e "    ${CYAN}chromadb${NC}   → Vector database (port 8000)"
    echo -e "    ${CYAN}rag-init${NC}   → Initialises ChromaDB with product data (runs once)"
    echo -e "    ${CYAN}api${NC}        → FastAPI REST layer (port 8001)"
    echo -e "    ${CYAN}app${NC}        → Gradio Dashboard (port 7860)"
    echo ""
    echo -e "  ${BOLD}After deploy, open:${NC}"
    echo -e "    Dashboard → ${BOLD}http://localhost:7860${NC}"
    echo -e "    REST API  → ${BOLD}http://localhost:8001/docs${NC}"
    echo ""
    echo -e "  ${BOLD}${YELLOW}Prerequisites:${NC}"
    echo "    • Docker Desktop running with WSL2 integration enabled"
    echo "    • .env file with OPENAI_API_KEY and ANTHROPIC_API_KEY set"
    echo "    • Ports 7860, 8000, 8001 must be free"
    echo ""
    echo -e "  ${BOLD}First build time:${NC} ~8-12 minutes (downloads ~750MB Python packages)"
    echo -e "  ${BOLD}Subsequent builds:${NC} ~30 seconds (uses Docker layer cache)"
    echo ""
    sep
    echo -ne "  ${BOLD}Proceed with Deploy? [y/N]: ${NC}"
    read -r confirm
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        echo ""
        detect_docker || return
        ensure_env
        git_pull
        info "Building Docker images..."
        $DC build
        info "Starting all services..."
        $DC up -d
        echo ""
        ok "Deployment complete!"
        echo ""
        echo -e "    Dashboard → ${BOLD}${CYAN}http://localhost:7860${NC}"
        echo -e "    REST API  → ${BOLD}${CYAN}http://localhost:8001/docs${NC}"
        echo -e "    ChromaDB  → ${BOLD}${CYAN}http://localhost:8000${NC}"
    fi
    press_any_key
}

info_update() {
    clear
    echo ""
    echo -e "  ${BOLD}${GREEN}🔄  UPDATE — Pull Latest + Rebuild${NC}"
    sep
    echo ""
    echo -e "  ${BOLD}What it does:${NC}"
    echo "    1. git pull origin main — fetches latest code"
    echo "    2. docker compose build — rebuilds changed images only"
    echo "    3. docker compose up -d — restarts with new images"
    echo ""
    echo -e "  ${BOLD}When to use:${NC}"
    echo "    • After a new release is published on GitHub"
    echo "    • When you've made local code changes"
    echo ""
    echo -e "  ${BOLD}${YELLOW}Note:${NC} Your data/ volume (settings, ChromaDB) is preserved."
    echo ""
    sep
    echo -ne "  ${BOLD}Proceed with Update? [y/N]: ${NC}"
    read -r confirm
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        echo ""
        detect_docker || return
        ensure_env
        git_pull
        info "Rebuilding images..."
        $DC build
        $DC up -d
        ok "Update complete!"
    fi
    press_any_key
}

info_start() {
    clear
    echo ""
    echo -e "  ${BOLD}${GREEN}▶️   START — Launch All Services${NC}"
    sep
    echo ""
    echo -e "  ${BOLD}What it does:${NC}"
    echo "    Starts all Docker Compose services in detached (background) mode."
    echo "    Uses existing built images — does NOT rebuild."
    echo ""
    echo -e "  ${BOLD}Services:${NC}"
    printf "    %-14s %s\n" "chromadb"  "Vector DB — port 8000"
    printf "    %-14s %s\n" "api"       "FastAPI REST — port 8001"
    printf "    %-14s %s\n" "app"       "Gradio Dashboard — port 7860"
    echo ""
    echo -e "  ${BOLD}${YELLOW}Tip:${NC} Run 'deploy' first if images haven't been built yet."
    echo ""
    sep
    echo -ne "  ${BOLD}Proceed with Start? [y/N]: ${NC}"
    read -r confirm
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        echo ""
        detect_docker || return
        ensure_env
        $DC up -d
        ok "All services started."
        echo -e "    Dashboard → ${BOLD}${CYAN}http://localhost:7860${NC}"
    fi
    press_any_key
}

info_stop() {
    clear
    echo ""
    echo -e "  ${BOLD}${RED}⏹️   STOP — Halt All Services${NC}"
    sep
    echo ""
    echo -e "  ${BOLD}What it does:${NC}"
    echo "    Stops and removes all running containers."
    echo "    Docker volumes (data/, ChromaDB) are preserved."
    echo ""
    echo -e "  ${BOLD}${YELLOW}Note:${NC} Your settings and ChromaDB data are safe."
    echo "    To also delete volumes: docker compose down -v"
    echo ""
    sep
    echo -ne "  ${BOLD}Proceed with Stop? [y/N]: ${NC}"
    read -r confirm
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        echo ""
        detect_docker || return
        $DC down
        ok "All services stopped."
    fi
    press_any_key
}

info_restart() {
    clear
    echo ""
    echo -e "  ${BOLD}${CYAN}🔁  RESTART — Restart All Services${NC}"
    sep
    echo ""
    echo -e "  ${BOLD}What it does:${NC}"
    echo "    Restarts all running containers without rebuilding images."
    echo "    Useful after changing .env or settings."
    echo ""
    echo -e "  ${BOLD}Faster than:${NC} stop + start (no image rebuild)"
    echo ""
    sep
    echo -ne "  ${BOLD}Proceed with Restart? [y/N]: ${NC}"
    read -r confirm
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        echo ""
        detect_docker || return
        $DC restart
        ok "Services restarted."
    fi
    press_any_key
}

info_patch() {
    clear
    echo ""
    echo -e "  ${BOLD}${CYAN}🩹  PATCH — Quick Update (No Rebuild)${NC}"
    sep
    echo ""
    echo -e "  ${BOLD}What it does:${NC}"
    echo "    1. git pull origin main — fetches latest code"
    echo "    2. Restarts only the 'app' and 'api' containers"
    echo "    No Docker image rebuild — fastest way to apply code fixes."
    echo ""
    echo -e "  ${BOLD}When to use:${NC}"
    echo "    • After a bug fix that only changed Python files"
    echo "    • After updating dashboard.py, agents, or config.py"
    echo "    • Does NOT apply changes to Dockerfile or requirements.txt"
    echo "      (use 'update' for those)"
    echo ""
    sep
    echo -ne "  ${BOLD}Proceed with Patch? [y/N]: ${NC}"
    read -r confirm
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        echo ""
        detect_docker || return
        git_pull
        info "Restarting app and api services..."
        $DC restart app api
        ok "Patch applied and services restarted."
    fi
    press_any_key
}

info_test() {
    clear
    echo ""
    echo -e "  ${BOLD}${CYAN}🧪  TEST — Run Test Suite${NC}"
    sep
    echo ""
    echo -e "  ${BOLD}What it does:${NC}"
    echo "    Runs the full 118-test suite inside the app container."
    echo "    Generates a Markdown report in tests/reports/"
    echo ""
    echo -e "  ${BOLD}Test categories:${NC}"
    printf "    %-30s %s\n" "test_config_loading"       "12 tests — Settings and env vars"
    printf "    %-30s %s\n" "test_data_models"          "18 tests — Deal, EnsembleResult models"
    printf "    %-30s %s\n" "test_scanner_agent"        "14 tests — RSS parsing, dedup"
    printf "    %-30s %s\n" "test_frontier_agent"       "16 tests — RAG retrieval, prompting"
    printf "    %-30s %s\n" "test_specialist_agent"     "12 tests — Modal inference"
    printf "    %-30s %s\n" "test_dnn_agent"            "10 tests — PyTorch model"
    printf "    %-30s %s\n" "test_ensemble_agent"       "14 tests — Weight validation"
    printf "    %-30s %s\n" "test_messaging_agent"      "12 tests — Pushover, Claude"
    printf "    %-30s %s\n" "test_planning_agent"       "10 tests — Pipeline orchestration"
    echo ""
    echo -e "  ${BOLD}Output:${NC}  tests/reports/test_report_<timestamp>.md"
    echo ""
    sep
    echo -ne "  ${BOLD}Proceed with Test? [y/N]: ${NC}"
    read -r confirm
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        echo ""
        detect_docker || return
        ensure_env
        mkdir -p tests/reports
        info "Running 118-test suite inside container..."
        $DC run --rm app python scripts/run_tests.py
        ok "Tests complete! Reports saved to tests/reports/"
        ls -lh tests/reports/ 2>/dev/null || true
    fi
    press_any_key
}

info_status() {
    clear
    echo ""
    echo -e "  ${BOLD}${CYAN}📋  STATUS — Container Overview${NC}"
    sep
    echo ""
    detect_docker || return
    $DC ps
    echo ""
    sep
    press_any_key
}

info_logs() {
    clear
    echo ""
    echo -e "  ${BOLD}${CYAN}📜  LOGS — Stream Service Logs${NC}"
    sep
    echo ""
    echo -e "  ${BOLD}Available services:${NC}"
    echo -e "    ${BOLD}${GREEN}1)${NC}  app       — Gradio Dashboard (port 7860)"
    echo -e "    ${BOLD}${GREEN}2)${NC}  api       — FastAPI REST (port 8001)"
    echo -e "    ${BOLD}${GREEN}3)${NC}  chromadb  — ChromaDB Vector DB (port 8000)"
    echo -e "    ${BOLD}${GREEN}4)${NC}  rag-init  — RAG initialisation (one-shot)"
    echo -e "    ${BOLD}${GREEN}5)${NC}  all       — All services combined"
    echo ""
    echo -e "  ${DIM}Press Ctrl+C to stop streaming.${NC}"
    echo ""
    sep
    echo -ne "  ${BOLD}Select service [1-5]: ${NC}"
    read -r svc_choice
    case "$svc_choice" in
        1) SVC="app" ;;
        2) SVC="api" ;;
        3) SVC="chromadb" ;;
        4) SVC="rag-init" ;;
        5) SVC="" ;;
        *) warn "Invalid choice"; press_any_key; return ;;
    esac
    echo ""
    detect_docker || return
    if [ -z "$SVC" ]; then
        $DC logs -f
    else
        $DC logs -f "$SVC"
    fi
}

info_diagnose() {
    clear
    echo ""
    echo -e "  ${BOLD}${YELLOW}🔍  DIAGNOSE — Pre-Flight Checks${NC}"
    sep
    echo ""

    # Docker
    echo -e "  ${BOLD}Docker Engine:${NC}"
    if docker info > /dev/null 2>&1; then
        echo -e "    Status   : ${GREEN}✓ Running${NC}"
        echo -e "    Version  : $(docker version --format '{{.Server.Version}}' 2>/dev/null || echo 'unknown')"
    else
        echo -e "    Status   : ${RED}✗ Not running${NC}"
        echo "    Fix: Start Docker Desktop and enable WSL2 integration."
    fi
    echo ""

    # Compose
    echo -e "  ${BOLD}Docker Compose:${NC}"
    if docker compose version > /dev/null 2>&1; then
        echo -e "    Plugin V2 : ${GREEN}✓ Available${NC} ($(docker compose version --short 2>/dev/null))"
    elif command -v docker-compose > /dev/null 2>&1; then
        echo -e "    Legacy    : ${YELLOW}⚠ Available${NC} ($(docker-compose --version))"
        echo "    Recommend: Install docker-compose-plugin for V2"
    else
        echo -e "    Status    : ${RED}✗ Not found${NC}"
        echo "    Fix: sudo apt-get install docker-compose-plugin"
    fi
    echo ""

    # .env file
    echo -e "  ${BOLD}.env File:${NC}"
    if [ -f .env ]; then
        echo -e "    Status : ${GREEN}✓ Exists${NC}"
        for key in OPENAI_API_KEY ANTHROPIC_API_KEY PUSHOVER_USER PUSHOVER_TOKEN MODAL_TOKEN_ID; do
            val=$(grep "^${key}=" .env 2>/dev/null | cut -d= -f2- || true)
            if [ -n "$val" ] && [[ "$val" != "sk-..."* ]] && [[ "$val" != "sk-ant-..."* ]] && [[ "$val" != "..."* ]]; then
                echo -e "    $key : ${GREEN}✓ SET${NC}"
            else
                echo -e "    $key : ${YELLOW}⚠ NOT SET${NC}"
            fi
        done
    else
        echo -e "    Status : ${RED}✗ Missing${NC} — run deploy to create"
    fi
    echo ""

    # Saved settings
    echo -e "  ${BOLD}UI Settings (data/ui_settings.json):${NC}"
    if [ -f data/ui_settings.json ]; then
        echo -e "    Status : ${GREEN}✓ Exists${NC}"
        echo -e "    Size   : $(wc -c < data/ui_settings.json) bytes"
    else
        echo -e "    Status : ${YELLOW}⚠ Not yet saved${NC} — fill Settings tab and click Save & Apply"
    fi
    echo ""

    # Ports
    echo -e "  ${BOLD}Port Availability:${NC}"
    for port in 7860 8000 8001; do
        if ss -tlnp 2>/dev/null | grep -q ":${port} " || netstat -tlnp 2>/dev/null | grep -q ":${port} " 2>/dev/null; then
            echo -e "    :$port → ${GREEN}IN USE (service running)${NC}"
        else
            echo -e "    :$port → ${CYAN}FREE${NC}"
        fi
    done
    echo ""

    # Disk
    echo -e "  ${BOLD}Disk Space:${NC}"
    df -h . | awk 'NR==2{printf "    Available: %s / %s (%s used)\n", $4, $2, $5}'
    echo ""

    sep
    press_any_key
}

info_import_settings() {
    clear
    echo ""
    echo -e "  ${BOLD}${YELLOW}📥  IMPORT SETTINGS — Apply settings.json${NC}"
    sep
    echo ""
    echo -e "  ${BOLD}What it does:${NC}"
    echo "    Copies a settings.json file into data/ui_settings.json"
    echo "    and restarts the app + api containers to apply it."
    echo ""
    echo -e "  ${BOLD}How to get a settings.json:${NC}"
    echo "    1. Open the Dashboard at http://localhost:7860"
    echo "    2. Go to the Settings tab"
    echo "    3. Fill in your API keys and configuration"
    echo "    4. Click 'Export Settings' — saves to data/settings_export.json"
    echo "    5. Copy that file to another machine and run this command"
    echo ""
    echo -e "  ${BOLD}File format (settings.json):${NC}"
    echo '    {'
    echo '      "OPENAI_API_KEY": "sk-...",  '
    echo '      "ANTHROPIC_API_KEY": "sk-ant-...",  '
    echo '      "PUSHOVER_USER": "...",  '
    echo '      "DEAL_THRESHOLD": 50,  '
    echo '      "SCANNER_MODEL": "gpt-4o-mini",  '
    echo '      ...  '
    echo '    }'
    echo ""
    echo -e "  ${BOLD}${YELLOW}Note:${NC} Masked values (***MASKED***) from exports must be"
    echo "    replaced with real values before importing."
    echo ""
    sep
    echo -ne "  ${BOLD}Enter path to settings.json (or press Enter to cancel): ${NC}"
    read -r filepath
    if [ -z "$filepath" ]; then
        info "Cancelled."
        press_any_key
        return
    fi
    if [ ! -f "$filepath" ]; then
        err "File not found: $filepath"
        press_any_key
        return
    fi
    mkdir -p data
    cp "$filepath" data/ui_settings.json
    ok "Settings imported to data/ui_settings.json"
    detect_docker || return
    if $DC ps 2>/dev/null | grep -q "Up"; then
        info "Restarting app and api to apply new settings..."
        $DC restart app api
        ok "Services restarted with new settings."
    else
        info "Run Deploy or Start to launch with the imported settings."
    fi
    press_any_key
}

show_about() {
    clear
    echo ""
    echo -e "  ${BOLD}${MAGENTA}ℹ️   ABOUT — The Price Is Right AI Deal Hunter${NC}"
    sep
    echo ""
    echo -e "  ${BOLD}Project Overview:${NC}"
    echo "    A 7-agent AI system that monitors RSS deal feeds, estimates"
    echo "    true product prices using RAG + LLMs + DNN, and sends"
    echo "    Pushover notifications for genuine arbitrage opportunities."
    echo ""
    echo -e "  ${BOLD}7-Agent Pipeline:${NC}"
    printf "    ${CYAN}%-18s${NC} %s\n" "Scanner Agent"    "Parses RSS feeds, deduplicates deals"
    printf "    ${CYAN}%-18s${NC} %s\n" "Frontier Agent"   "RAG + GPT-4o price estimation"
    printf "    ${CYAN}%-18s${NC} %s\n" "Specialist Agent" "Fine-tuned Llama via Modal GPU"
    printf "    ${CYAN}%-18s${NC} %s\n" "DNN Agent"        "Deep Residual Neural Network (PyTorch)"
    printf "    ${CYAN}%-18s${NC} %s\n" "Ensemble Agent"   "Weighted combiner (0.8/0.1/0.1)"
    printf "    ${CYAN}%-18s${NC} %s\n" "Messaging Agent"  "Claude + Pushover notifications"
    printf "    ${CYAN}%-18s${NC} %s\n" "Planning Agent"   "Orchestrates the full pipeline"
    echo ""
    echo -e "  ${BOLD}Tech Stack:${NC}"
    printf "    %-20s %s\n" "Language"       "Python 3.11"
    printf "    %-20s %s\n" "Dashboard"      "Gradio 4.x"
    printf "    %-20s %s\n" "REST API"       "FastAPI"
    printf "    %-20s %s\n" "Vector DB"      "ChromaDB 0.4.24"
    printf "    %-20s %s\n" "Embeddings"     "sentence-transformers"
    printf "    %-20s %s\n" "LLMs"           "OpenAI GPT-4o, Anthropic Claude"
    printf "    %-20s %s\n" "GPU Inference"  "Modal (Llama-3.2-3B)"
    printf "    %-20s %s\n" "Notifications"  "Pushover API"
    printf "    %-20s %s\n" "Container"      "Docker + Compose V2"
    echo ""
    echo -e "  ${BOLD}Ports:${NC}"
    printf "    %-20s %s\n" "7860"  "Gradio Dashboard"
    printf "    %-20s %s\n" "8001"  "FastAPI REST API (/docs for Swagger)"
    printf "    %-20s %s\n" "8000"  "ChromaDB Vector DB"
    echo ""
    echo -e "  ${BOLD}Useful Links:${NC}"
    echo "    GitHub  : https://github.com/lalitnayyar/priceisright"
    echo "    Docs    : https://github.com/lalitnayyar/priceisright/blob/main/README.md"
    echo ""
    echo -e "  ${BOLD}Contact:${NC}"
    echo "    Lalit Nayyar  |  lalitnayyar@gmail.com"
    echo "    +971 508 320 336  |  +91 959 535 3336"
    echo ""
    sep
    press_any_key
}

# ── Non-interactive mode (direct command) ─────────────────────────────────────
run_direct() {
    detect_docker 2>/dev/null || true
    case "${1:-}" in
        deploy)           ensure_env; git_pull; $DC build; $DC up -d; ok "Deployed." ;;
        update)           ensure_env; git_pull; $DC build; $DC up -d; ok "Updated." ;;
        start)            ensure_env; $DC up -d; ok "Started." ;;
        stop)             $DC down; ok "Stopped." ;;
        restart)          $DC restart; ok "Restarted." ;;
        patch)            git_pull; $DC restart app api; ok "Patched." ;;
        test)             ensure_env; mkdir -p tests/reports; $DC run --rm app python scripts/run_tests.py ;;
        status)           $DC ps ;;
        logs)             $DC logs -f "${2:-app}" ;;
        diagnose)         info_diagnose ;;
        import-settings)
            if [ -z "${2:-}" ]; then err "Usage: ./manage.sh import-settings <file>"; exit 1; fi
            mkdir -p data; cp "$2" data/ui_settings.json; ok "Imported."
            $DC ps 2>/dev/null | grep -q "Up" && $DC restart app api || true ;;
        help|--help|-h)   show_about ;;
        *)  err "Unknown command: ${1:-}"; echo "  Run ./manage.sh for interactive menu."; exit 1 ;;
    esac
}

# ── Entry point ───────────────────────────────────────────────────────────────
# If called with arguments, run non-interactively (backward compatible)
if [ $# -gt 0 ]; then
    detect_docker 2>/dev/null || true
    run_direct "$@"
    exit 0
fi

# Interactive menu loop
while true; do
    show_main_menu
    read -r choice

    case "$choice" in
        1)  info_deploy ;;
        2)  info_update ;;
        3)  info_start ;;
        4)  info_stop ;;
        5)  info_restart ;;
        6)  info_patch ;;
        7)  info_test ;;
        8)  info_status ;;
        9)  info_logs ;;
        10) info_diagnose ;;
        11) info_import_settings ;;
        12) show_about ;;
        0)
            clear
            echo ""
            echo -e "  ${BOLD}${CYAN}Thank you for using The Price Is Right AI Deal Hunter!${NC}"
            echo -e "  ${DIM}Lalit Nayyar | lalitnayyar@gmail.com${NC}"
            echo ""
            exit 0
            ;;
        *)
            warn "Invalid option. Please select 0-12."
            sleep 1
            ;;
    esac
done
