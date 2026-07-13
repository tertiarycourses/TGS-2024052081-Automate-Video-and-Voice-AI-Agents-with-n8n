@echo off
REM MediRefill - one-click launcher (Windows)
REM Double-click this file. It serves the website on http://localhost:8096
REM (so the browser trusts it for the microphone) and opens it for you.
REM Uses Python if available, else Node (npx).
cd /d "%~dp0"

set PORT=8096
set URL=http://localhost:%PORT%
echo Serving MediRefill at %URL%
echo Keep this window open while you use the site. Close it to stop.
start "" %URL%

where python >nul 2>nul && (python -m http.server %PORT% & goto :eof)
where npx >nul 2>nul && (npx --yes serve -l %PORT% . & goto :eof)
echo Neither Python nor Node (npx) found. Install one, or use VS Code Live Server.
pause
