@echo off
echo [INFO] Starting Water Essence Sprite Services...

:: 1. Start Main Server (Port 8000)
echo Starting Main Server...
start "Main Server" /min cmd /k "python -m server.main"

:: 2. Start WeChat Worker
echo Starting WeChat Worker...
start "WeChat Worker" /min cmd /k "python -m backend.server_receive"

:: 3. Start Frontend (Port 5173)
echo Starting Frontend...
start "Frontend" /min cmd /k "npm run dev"

echo [SUCCESS] All services are running in the background (minimized windows).
echo You can close this window now.
