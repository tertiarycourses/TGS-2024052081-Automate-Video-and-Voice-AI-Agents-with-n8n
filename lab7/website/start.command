#!/bin/bash
# GG News Studio — one-click launcher (macOS). Right-click → Open the first time.
cd "$(dirname "$0")" || exit 1
PORT=8095
while lsof -iTCP:$PORT -sTCP:LISTEN >/dev/null 2>&1; do PORT=$((PORT + 1)); done
URL="http://localhost:$PORT"
echo "Serving GG News Studio at $URL  (Ctrl+C to stop)"
( sleep 1; open "$URL" ) &
if command -v python3 >/dev/null 2>&1; then python3 -m http.server "$PORT"
elif command -v npx >/dev/null 2>&1; then npx --yes serve -l "$PORT" .
else echo "Install Python or Node, or use VS Code Live Server."; read -r -p "Enter to close."; fi
