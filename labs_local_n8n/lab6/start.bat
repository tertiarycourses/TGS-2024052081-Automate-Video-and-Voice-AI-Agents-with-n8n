@echo off
REM Lab 6 - Digital Human Studio (Windows). Double-click this file.
REM
REM Starts the app and opens the browser at http://localhost:8137.
REM On the first run it builds the Python environment, which takes a few minutes.
REM
REM Do NOT double-click index.html. On a file:// URL the browser blocks fetch(),
REM so the sample portraits and the renderers all fail ("Could not load that
REM sample."). The app has to be served over http://.
cd /d "%~dp0"

REM Files extracted from a downloaded ZIP carry Windows' "blocked" flag
REM (Mark-of-the-Web), and blocked scripts/tools silently refuse to run.
REM Clear the flag for this lab's files before doing anything else.
powershell -NoProfile -Command "Get-ChildItem -LiteralPath '.' -Recurse -File -ErrorAction SilentlyContinue | Unblock-File -ErrorAction SilentlyContinue" >nul 2>&1

if not defined PORT set PORT=8137
set PY=python\.venv\Scripts\python.exe

if not exist "%PY%" (
  echo ==^> First run: building the Python environment ^(this takes a few minutes^)...
  python -m venv python\.venv
  "%PY%" -m pip install --upgrade pip
  "%PY%" -m pip install -e .
)

if not exist ".env" (
  echo # Paste your HeyGen API key here to enable HeyGen ^(https://app.heygen.com^)> .env
  echo HEYGEN_API_KEY=>> .env
  echo GEMINI_API_KEY=>> .env
  echo ELEVENLABS_API_KEY=>> .env
  echo OPENAI_API_KEY=>> .env
  echo ==^> Wrote a starter .env - paste your HEYGEN_API_KEY into it to enable HeyGen.
)

echo.
echo Serving Digital Human Studio at http://localhost:%PORT%  (Ctrl+C to stop)
echo Use this URL - do NOT double-click index.html, fetch() is blocked on file://.
start "" http://localhost:%PORT%
"%PY%" python\app.py
