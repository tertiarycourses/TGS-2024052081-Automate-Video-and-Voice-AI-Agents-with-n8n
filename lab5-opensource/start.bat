@echo off
REM Lab 5 open-source (Windows) - starts the render service + website, opens browser.
cd /d "%~dp0"
echo Starting render service on :8099 ...
start "render-service" cmd /c "cd service && python render_service.py"
timeout /t 3 >nul
set PORT=8096
echo Serving website at http://localhost:%PORT%  (close windows to stop)
start "" http://localhost:%PORT%
cd website && python -m http.server %PORT%
