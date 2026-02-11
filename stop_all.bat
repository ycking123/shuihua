@echo off
echo [INFO] Stopping Water Essence Sprite Services...

:: Kill by Window Title (works if started via run_all.bat)
taskkill /FI "WINDOWTITLE eq Main Server*" /T /F
taskkill /FI "WINDOWTITLE eq WeChat Worker*" /T /F
taskkill /FI "WINDOWTITLE eq Frontend*" /T /F

echo [SUCCESS] Services stopped (if they were running).
pause
