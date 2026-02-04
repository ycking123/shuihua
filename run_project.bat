@echo off
echo Starting Water Essence Sprite Project...
powershell -ExecutionPolicy Bypass -File "%~dp0run_project.ps1"
if %errorlevel% neq 0 (
    echo.
    echo ❌ Script failed with error code %errorlevel%.
    echo Please make sure you have activated the conda environment.
    echo.
    pause
)
