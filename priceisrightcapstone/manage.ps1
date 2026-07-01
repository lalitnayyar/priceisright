<#
.SYNOPSIS
The Price Is Right - Unified Management Script for PowerShell

.DESCRIPTION
Provides commands to deploy, update, start, stop, test, and patch the application.

.EXAMPLE
.\manage.ps1 deploy
#>

param (
    [Parameter(Position=0)]
    [ValidateSet("deploy", "update", "start", "stop", "test", "patch", "status", "help")]
    [string]$Command = "help"
)

$AppDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $AppDir

function Show-Help {
    Write-Host "The Price Is Right - Management Script" -ForegroundColor Cyan
    Write-Host "Usage: .\manage.ps1 [command]"
    Write-Host ""
    Write-Host "Commands:"
    Write-Host "  deploy   - Pull latest from GitHub, build and start containers"
    Write-Host "  update   - Pull latest from GitHub and restart containers"
    Write-Host "  start    - Start all containers in background"
    Write-Host "  stop     - Stop all containers"
    Write-Host "  test     - Run unit tests and generate markdown report"
    Write-Host "  patch    - Apply a quick patch and restart"
    Write-Host "  status   - Show container status"
    Write-Host ""
}

function Deploy-App {
    Write-Host "Deploying The Price Is Right..." -ForegroundColor Green
    try { git pull origin main } catch { Write-Host "Git pull failed, continuing with local files..." -ForegroundColor Yellow }
    
    if (-not (Test-Path ".env")) {
        Write-Host "Creating .env from .env.example..." -ForegroundColor Yellow
        Copy-Item ".env.example" ".env"
    }
    
    docker-compose build
    docker-compose up -d
    Write-Host "Deployment complete! Dashboard available at http://localhost:7860" -ForegroundColor Green
}

function Update-App {
    Write-Host "Updating application..." -ForegroundColor Green
    git pull origin main
    docker-compose build
    docker-compose up -d
    Write-Host "Update complete!" -ForegroundColor Green
}

function Start-App {
    Write-Host "Starting application..." -ForegroundColor Green
    docker-compose up -d
    Write-Host "Application started!" -ForegroundColor Green
}

function Stop-App {
    Write-Host "Stopping application..." -ForegroundColor Yellow
    docker-compose down
    Write-Host "Application stopped!" -ForegroundColor Green
}

function Run-Tests {
    Write-Host "Running test suite..." -ForegroundColor Cyan
    docker-compose run --rm app python scripts/run_tests.py
    Write-Host "Tests complete! Check tests/reports/ directory for markdown reports." -ForegroundColor Green
}

function Patch-App {
    Write-Host "Applying patch..." -ForegroundColor Green
    git pull origin main
    docker-compose restart app api
    Write-Host "Patch applied and services restarted!" -ForegroundColor Green
}

function Show-Status {
    docker-compose ps
}

switch ($Command) {
    "deploy" { Deploy-App }
    "update" { Update-App }
    "start" { Start-App }
    "stop" { Stop-App }
    "test" { Run-Tests }
    "patch" { Patch-App }
    "status" { Show-Status }
    "help" { Show-Help }
    default { Show-Help }
}
