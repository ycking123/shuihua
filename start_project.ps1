# start_project.ps1

Write-Host "Starting Water Essence Sprite v4 Project..." -ForegroundColor Green

# Check if conda is available
if (-not (Get-Command "conda" -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Conda not found. Please ensure Conda is installed and in your PATH." -ForegroundColor Red
    exit 1
}

# 1. Start Unified Backend Service (Port 8002)
Write-Host "Launching Unified Backend Service (FastAPI + WeChat Callback)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& {conda activate water_essence_backend; if ($?) { python -m backend.main } else { Write-Host 'Failed to activate conda env'; Read-Host 'Press Enter to exit' }}"

# 2. Start Frontend (Vite)
Write-Host "Launching Frontend..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm run dev"

Write-Host "All services launched!" -ForegroundColor Green
Write-Host "Frontend: http://localhost:5173"
Write-Host "Unified Backend: http://localhost:8002"
Write-Host "WeChat Callback: http://localhost:8002/wecom/callback"
