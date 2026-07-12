#!/bin/bash
# Nova — Interactive Avatar (LiveAvatar) — one-click launcher (macOS)
# Double-click in Finder (first time: right-click → Open to pass Gatekeeper).
# The microphone only works over http://localhost, never on file://.
cd "$(dirname "$0")" || exit 1

PORT=8099
while lsof -iTCP:$PORT -sTCP:LISTEN >/dev/null 2>&1; do PORT=$((PORT + 1)); done

URL="http://localhost:$PORT"
echo "Serving Nova — Interactive Avatar (LiveAvatar) at $URL"
echo "Keep this window open. Press Ctrl+C to stop."
( sleep 1; open "$URL" ) &

if command -v python3 >/dev/null 2>&1; then
  python3 -m http.server "$PORT"
elif command -v python >/dev/null 2>&1; then
  python -m http.server "$PORT"
elif command -v npx >/dev/null 2>&1; then
  npx --yes serve -l "$PORT" .
else
  echo "Neither Python nor Node (npx) found. Install one, or use VS Code Live Server."
  read -r -p "Press Enter to close."
fi
