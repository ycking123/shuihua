# start_project.ps1

Write-Host "Starting Water Essence Sprite v4 Project..." -ForegroundColor Green

# Check if conda is available
if (-not (Get-Command "conda" -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Conda not found. Please ensure Conda is installed and in your PATH." -ForegroundColor Red
    exit 1
}

# 1. Start Backend Main Service (Port 8002)
Write-Host "Launching Backend Main Service (FastAPI)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& {conda activate water_essence_backend; if ($?) { cd backend; python main.py } else { Write-Host 'Failed to activate conda env'; Read-Host 'Press Enter to exit' }}"

# 2. Start Backend WeChat Callback Service (Port 8080)
Write-Host "Launching WeChat Callback Service (Flask)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& {conda activate water_essence_backend; if ($?) { cd backend; python server_receive.py } else { Write-Host 'Failed to activate conda env'; Read-Host 'Press Enter to exit' }}"

# 3. Start Frontend (Vite)
Write-Host "Launching Frontend..." -ForegroundColor Cyan
# Using current window for frontend or new window? Let's use current window to keep one visible log, or new window to keep script clean.
# Let's use a new window for consistency so this script finishes.
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm run dev"

Write-Host "All services launched!" -ForegroundColor Green
Write-Host "Frontend: http://localhost:5173"
Write-Host "Backend Main: http://localhost:8002"
Write-Host "Backend WeChat: http://localhost:8080"
