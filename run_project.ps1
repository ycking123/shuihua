# Windows Startup Script for Water Essence Sprite
$ScriptDir = $PSScriptRoot
$LogDir = "$ScriptDir\logs"
if (!(Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir }

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "   Water Essence Sprite - Windows Startup Script" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# Check Python
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "❌ Python not found. Please activate your Conda environment first (e.g., conda activate water-essence-sprite)."
    exit 1
}

# Set PYTHONPATH to include project root and server directory
$env:PYTHONPATH = "$ScriptDir;$ScriptDir\server;$env:PYTHONPATH"
Write-Host "✅ PYTHONPATH set." -ForegroundColor Green

# 1. Start Main Backend (Port 8000)
Write-Host "[1/3] Starting Main Backend (server.main)..." -ForegroundColor Yellow
try {
    Start-Process python -ArgumentList "-m server.main" -WorkingDirectory $ScriptDir
    Write-Host "   -> Started in new window." -ForegroundColor Green
} catch {
    Write-Error "Failed to start Main Backend."
}

# 2. Start WeChat Backend (Port 8080)
Write-Host "[2/3] Starting WeChat Backend (backend.server_receive)..." -ForegroundColor Yellow
try {
    Start-Process python -ArgumentList "-m backend.server_receive" -WorkingDirectory $ScriptDir
    Write-Host "   -> Started in new window." -ForegroundColor Green
} catch {
    Write-Error "Failed to start WeChat Backend."
}

# 3. Start Frontend
Write-Host "[3/3] Starting Frontend..." -ForegroundColor Yellow
if (Get-Command npm -ErrorAction SilentlyContinue) {
    try {
        Start-Process npm -ArgumentList "run dev" -WorkingDirectory $ScriptDir
        Write-Host "   -> Started in new window." -ForegroundColor Green
    } catch {
        Write-Error "Failed to start Frontend."
    }
} else {
    Write-Warning "⚠️ npm not found. Skipping Frontend start."
}

Write-Host "`n✅ All services launch initiated." -ForegroundColor Cyan
Write-Host "Please check the opened windows for logs."
