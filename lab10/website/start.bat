@echo off
REM Veo Studio - one-click launcher (Windows)
REM Double-click this file. It serves the site on http://localhost:8098 and opens it.
cd /d "%~dp0"

set PORT=8098
set URL=http://localhost:%PORT%
echo Serving Veo Studio at %URL%
echo Keep this window open while you use the site. Close it to stop.
start "" %URL%

where python >nul 2>nul && (python -m http.server %PORT% & goto :eof)
where npx >nul 2>nul && (npx --yes serve -l %PORT% . & goto :eof)
echo Neither Python nor Node (npx) found. Install one, or use VS Code Live Server.
pause
