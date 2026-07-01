<#
.SYNOPSIS
    The Price Is Right — Unified Management Script for Windows PowerShell
.DESCRIPTION
    Provides commands to deploy, update, start, stop, test, patch, diagnose
    and manage the Docker-based AI Deal Hunter application.
    Supports both Docker Compose V2 plugin (docker compose) and legacy
    docker-compose binary, with clear guidance for Docker Desktop / WSL2 users.
.AUTHOR
    Lalit Nayyar | lalitnayyar@gmail.com
.VERSION
    1.3.0
.EXAMPLE
    .\manage.ps1 deploy
    .\manage.ps1 test
    .\manage.ps1 diagnose
#>

param (
    [Parameter(Position=0)]
    [string]$Command = "help",

    [Parameter(Position=1)]
    [string]$Service = "app"
)

$AppDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $AppDir

# ── Colour helpers ─────────────────────────────────────────────────────────────
function Write-Info    { param($msg) Write-Host "[INFO]  $msg" -ForegroundColor Cyan }
function Write-Ok      { param($msg) Write-Host "[OK]    $msg" -ForegroundColor Green }
function Write-Warn    { param($msg) Write-Host "[WARN]  $msg" -ForegroundColor Yellow }
function Write-Err     { param($msg) Write-Host "[ERROR] $msg" -ForegroundColor Red }
function Write-Header  {
    param($msg)
    Write-Host ""
    Write-Host "══════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "  $msg" -ForegroundColor White
    Write-Host "══════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
}

# ── Docker / docker compose detection ─────────────────────────────────────────
$script:DC = $null

function Detect-Docker {
    # Check Docker daemon
    $dockerInfo = docker info 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Err "Docker daemon is not running or not accessible."
        Write-Host ""
        Write-Host "  Please ensure Docker Desktop is running." -ForegroundColor Yellow
        Write-Host "  If using WSL2, also enable WSL Integration in Docker Desktop:" -ForegroundColor Yellow
        Write-Host "    Settings → Resources → WSL Integration → Enable for your distro" -ForegroundColor Yellow
        Write-Host "  Docs: https://docs.docker.com/go/wsl2/" -ForegroundColor Cyan
        Write-Host ""
        exit 1
    }

    # Prefer Docker Compose V2 plugin
    $v2Test = docker compose version 2>&1
    if ($LASTEXITCODE -eq 0) {
        $script:DC = "docker compose"
        Write-Info "Using Docker Compose V2 plugin (docker compose)"
    }
    else {
        $legacyTest = Get-Command docker-compose -ErrorAction SilentlyContinue
        if ($legacyTest) {
            $script:DC = "docker-compose"
            Write-Warn "Using legacy docker-compose binary. Consider upgrading to Docker Compose V2."
        }
        else {
            Write-Err "Neither 'docker compose' nor 'docker-compose' found."
            Write-Host ""
            Write-Host "  Install Docker Desktop (includes Compose V2):" -ForegroundColor Yellow
            Write-Host "    https://www.docker.com/products/docker-desktop/" -ForegroundColor Cyan
            Write-Host ""
            exit 1
        }
    }
}

function Invoke-DC {
    param([string]$Args)
    $fullCmd = "$($script:DC) $Args"
    Write-Info "Running: $fullCmd"
    Invoke-Expression $fullCmd
    if ($LASTEXITCODE -ne 0) {
        Write-Err "Command failed: $fullCmd"
        exit $LASTEXITCODE
    }
}

# ── Helper: ensure .env exists ─────────────────────────────────────────────────
function Ensure-Env {
    if (-not (Test-Path ".env")) {
        Write-Warn ".env not found — creating from .env.example"
        Copy-Item ".env.example" ".env"
        Write-Host ""
        Write-Warn "ACTION REQUIRED: Open .env and fill in your API keys before continuing."
        Write-Host "  Required: OPENAI_API_KEY, ANTHROPIC_API_KEY, PUSHOVER_USER, PUSHOVER_TOKEN" -ForegroundColor Yellow
        Write-Host ""
        Read-Host "  Press ENTER once you have edited .env (Ctrl+C to abort)"
    }
}

# ── Helper: git pull ───────────────────────────────────────────────────────────
function Git-Pull {
    $remotes = git remote -v 2>&1
    if ($LASTEXITCODE -eq 0 -and $remotes -match "origin") {
        Write-Info "Pulling latest code from GitHub..."
        git pull origin main 2>&1
        if ($LASTEXITCODE -ne 0) { Write-Warn "Git pull failed — continuing with local files." }
    }
    else {
        Write-Warn "No git remote configured. Skipping pull."
    }
}

# ── Commands ───────────────────────────────────────────────────────────────────

function Deploy-App {
    Write-Header "Deploying The Price Is Right"
    Detect-Docker
    Git-Pull
    Ensure-Env
    Write-Info "Building Docker images (this may take a few minutes on first run)..."
    Invoke-DC "build"
    Write-Info "Starting all services..."
    Invoke-DC "up -d"
    Write-Host ""
    Write-Ok "Deployment complete!"
    Write-Host "  Dashboard  → http://localhost:7860" -ForegroundColor Cyan
    Write-Host "  REST API   → http://localhost:8001" -ForegroundColor Cyan
    Write-Host "  ChromaDB   → http://localhost:8000" -ForegroundColor Cyan
    Write-Host ""
}

function Update-App {
    Write-Header "Updating The Price Is Right"
    Detect-Docker
    Git-Pull
    Write-Info "Rebuilding images with latest code..."
    Invoke-DC "build"
    Invoke-DC "up -d"
    Write-Ok "Update complete!"
}

function Start-App {
    Write-Header "Starting The Price Is Right"
    Detect-Docker
    Ensure-Env
    Invoke-DC "up -d"
    Write-Ok "All services started."
    Write-Host "  Dashboard → http://localhost:7860" -ForegroundColor Cyan
}

function Stop-App {
    Write-Header "Stopping The Price Is Right"
    Detect-Docker
    Invoke-DC "down"
    Write-Ok "All services stopped."
}

function Restart-App {
    Write-Header "Restarting services"
    Detect-Docker
    Invoke-DC "restart"
    Write-Ok "Services restarted."
}

function Run-Tests {
    Write-Header "Running Test Suite"
    Detect-Docker
    Ensure-Env
    New-Item -ItemType Directory -Force -Path "tests/reports" | Out-Null
    Write-Info "Running 118-test suite inside container..."
    Invoke-DC "run --rm app python scripts/run_tests.py"
    Write-Ok "Tests complete! Reports saved to tests/reports/"
    Get-ChildItem "tests/reports/" -ErrorAction SilentlyContinue | Format-Table Name, Length, LastWriteTime
}

function Patch-App {
    Write-Header "Applying Patch"
    Detect-Docker
    Git-Pull
    Write-Info "Restarting app and api services..."
    Invoke-DC "restart app api"
    Write-Ok "Patch applied and services restarted."
}

function Show-Logs {
    Detect-Docker
    Write-Info "Streaming logs for service: $Service (Ctrl+C to stop)"
    Invoke-DC "logs -f $Service"
}

function Show-Status {
    Detect-Docker
    Write-Header "Container Status"
    Invoke-DC "ps"
}

function Run-Diagnose {
    Write-Header "Diagnostic Check"

    Write-Host "System:" -ForegroundColor White
    Write-Host "  OS      : $([System.Environment]::OSVersion.VersionString)"
    Write-Host "  PS Ver  : $($PSVersionTable.PSVersion)"
    Write-Host ""

    Write-Host "Docker:" -ForegroundColor White
    $dockerInfo = docker info 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  Docker daemon  : " -NoNewline; Write-Host "RUNNING" -ForegroundColor Green
        $ver = docker version --format '{{.Server.Version}}' 2>&1
        Write-Host "  Version        : $ver"
    } else {
        Write-Host "  Docker daemon  : " -NoNewline; Write-Host "NOT RUNNING" -ForegroundColor Red
    }

    $v2 = docker compose version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  Compose V2     : " -NoNewline; Write-Host "AVAILABLE" -ForegroundColor Green
    } elseif (Get-Command docker-compose -ErrorAction SilentlyContinue) {
        Write-Host "  Compose legacy : " -NoNewline; Write-Host "AVAILABLE" -ForegroundColor Yellow
    } else {
        Write-Host "  Compose        : " -NoNewline; Write-Host "NOT FOUND" -ForegroundColor Red
    }
    Write-Host ""

    Write-Host ".env file:" -ForegroundColor White
    if (Test-Path ".env") {
        Write-Host "  Status : " -NoNewline; Write-Host "EXISTS" -ForegroundColor Green
        $envContent = Get-Content ".env"
        foreach ($key in @("OPENAI_API_KEY","ANTHROPIC_API_KEY","PUSHOVER_USER","PUSHOVER_TOKEN")) {
            $line = $envContent | Where-Object { $_ -match "^${key}=(.+)" }
            $val = if ($line) { ($line -split "=",2)[1] } else { "" }
            if ($val -and $val -notmatch "^\.\.\.$|^sk-\.\.\.$|^sk-ant-\.\.\.$") {
                Write-Host "  ${key} : " -NoNewline; Write-Host "SET" -ForegroundColor Green
            } else {
                Write-Host "  ${key} : " -NoNewline; Write-Host "NOT SET" -ForegroundColor Yellow
            }
        }
    } else {
        Write-Host "  Status : " -NoNewline; Write-Host "MISSING" -ForegroundColor Red
        Write-Host "  Run '.\manage.ps1 deploy' to create it."
    }
    Write-Host ""

    Write-Host "Ports:" -ForegroundColor White
    foreach ($port in @(7860, 8000, 8001)) {
        $conn = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
        if ($conn) {
            Write-Host "  :$port → " -NoNewline; Write-Host "IN USE" -ForegroundColor Green
        } else {
            Write-Host "  :$port → " -NoNewline; Write-Host "FREE" -ForegroundColor Cyan
        }
    }
    Write-Host ""
}

function Show-Help {
    Write-Host ""
    Write-Host "The Price Is Right — Management Script v1.3.0" -ForegroundColor Cyan
    Write-Host "  Author: Lalit Nayyar | lalitnayyar@gmail.com"
    Write-Host ""
    Write-Host "Usage:  .\manage.ps1 <command> [service]" -ForegroundColor White
    Write-Host ""
    Write-Host "Commands:" -ForegroundColor White
    $cmds = @(
        @("deploy",   "Pull from GitHub, build images, start all services"),
        @("update",   "Pull latest code, rebuild, and restart services"),
        @("start",    "Start all services in the background"),
        @("stop",     "Stop all running services"),
        @("restart",  "Restart all services"),
        @("test",     "Run 118-test suite and generate Markdown report"),
        @("patch",    "Git pull and restart app + api services"),
        @("logs",     "Stream logs (default: app, pass service name as 2nd arg)"),
        @("status",   "Show container status"),
        @("diagnose", "Run environment diagnostic check"),
        @("help",     "Show this help message")
    )
    foreach ($c in $cmds) {
        Write-Host ("  {0,-12} {1}" -f $c[0], $c[1])
    }
    Write-Host ""
    Write-Host "Docker Desktop / WSL2 Users:" -ForegroundColor Yellow
    Write-Host "  Ensure Docker Desktop is running and WSL2 integration is enabled."
    Write-Host "  Settings → Resources → WSL Integration → Enable for your distro."
    Write-Host "  Docs: https://docs.docker.com/go/wsl2/"
    Write-Host ""
}

# ── Entry point ────────────────────────────────────────────────────────────────
switch ($Command.ToLower()) {
    "deploy"   { Deploy-App }
    "update"   { Update-App }
    "start"    { Start-App }
    "stop"     { Stop-App }
    "restart"  { Restart-App }
    "test"     { Run-Tests }
    "patch"    { Patch-App }
    "logs"     { Show-Logs }
    "status"   { Show-Status }
    "diagnose" { Run-Diagnose }
    "help"     { Show-Help }
    default    {
        Write-Err "Unknown command: $Command"
        Show-Help
        exit 1
    }
}
