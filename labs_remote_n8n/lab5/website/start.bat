@echo off
REM MediRefill - one-click launcher (Windows)
REM Double-click this file. It serves the website on http://localhost:8096
REM (so the browser trusts it for the microphone) and opens it for you.
REM Uses Python if available, else Node (npx).
cd /d "%~dp0"

REM Files extracted from a downloaded ZIP carry Windows' "blocked" flag
REM (Mark-of-the-Web), and blocked scripts/tools silently refuse to run.
REM Clear the flag for this lab's files before doing anything else.
powershell -NoProfile -Command "Get-ChildItem -LiteralPath '.' -Recurse -File -ErrorAction SilentlyContinue | Unblock-File -ErrorAction SilentlyContinue" >nul 2>&1

set PORT=8096
set URL=http://localhost:%PORT%
echo Serving MediRefill at %URL%
echo Keep this window open while you use the site. Close it to stop.
start "" %URL%

where python >nul 2>nul && (python -m http.server %PORT% & goto :eof)
where npx >nul 2>nul && (npx --yes serve -l %PORT% . & goto :eof)
echo Neither Python nor Node (npx) found. Install one, or use VS Code Live Server.
pause
