@echo off
REM Nova — Interactive Avatar (LiveAvatar) - one-click launcher (Windows)
REM The microphone only works over http://localhost, never on file://.
cd /d "%~dp0"

set PORT=8099
set URL=http://localhost:%PORT%
echo Serving Nova — Interactive Avatar (LiveAvatar) at %URL%
echo Keep this window open. Close it to stop.
start "" %URL%

where python >nul 2>nul && (python -m http.server %PORT% & goto :eof)
where npx >nul 2>nul && (npx --yes serve -l %PORT% . & goto :eof)
echo Neither Python nor Node (npx) found. Install one, or use VS Code Live Server.
pause
