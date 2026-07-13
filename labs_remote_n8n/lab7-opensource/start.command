#!/bin/bash
# Lab 5 open-source — starts the local render service + the website, opens browser.
cd "$(dirname "$0")" || exit 1
echo "Starting render service on :8099 …"
( cd service && python3 render_service.py ) &
SVC=$!
sleep 2
PORT=8097
while lsof -iTCP:$PORT -sTCP:LISTEN >/dev/null 2>&1; do PORT=$((PORT+1)); done
echo "Serving website at http://localhost:$PORT  (Ctrl+C to stop both)"
( sleep 1; open "http://localhost:$PORT" ) &
trap "kill $SVC 2>/dev/null" EXIT
( cd website && python3 -m http.server "$PORT" )
