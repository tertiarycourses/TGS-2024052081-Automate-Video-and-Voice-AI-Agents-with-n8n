@echo off
REM GG News Studio - one-click launcher (Windows). Double-click this file.
cd /d "%~dp0"
set PORT=8095
set URL=http://localhost:%PORT%
echo Serving GG News Studio at %URL%  (close window to stop)
start "" %URL%
where python >nul 2>nul && (python -m http.server %PORT% & goto :eof)
where npx >nul 2>nul && (npx --yes serve -l %PORT% . & goto :eof)
echo Install Python or Node, or use VS Code Live Server.
pause
