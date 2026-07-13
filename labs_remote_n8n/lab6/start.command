#!/bin/bash
# Lab 6 — Digital Human Studio (macOS). Double-click this file in Finder.
#
# Starts the app and opens the browser at http://localhost:8137.
# On the first run there is no Python environment yet, so this hands over to
# ./setup.sh, which builds it and then starts the app.
#
# Do NOT double-click index.html. On a file:// URL the browser blocks fetch(),
# so the sample portraits and the renderers all fail ("Could not load that
# sample."). The app has to be served over http://.
cd "$(dirname "$0")" || exit 1

PORT="${PORT:-8137}"
PY="python/.venv/bin/python"

# First run: no environment yet — setup.sh builds it and starts the app itself.
if [ ! -x "$PY" ]; then
  echo "==> First run: building the Python environment (this takes a few minutes)…"
  exec ./setup.sh
fi

# If the port is busy, walk up until we find a free one, like Lab 7 does.
while lsof -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; do PORT=$((PORT+1)); done

echo "Serving Digital Human Studio at http://localhost:$PORT  (Ctrl+C to stop)"
echo "Use this URL — do NOT double-click index.html, fetch() is blocked on file://."

# Open the browser once the server actually answers.
(
  for _ in $(seq 1 60); do
    if curl -fs -o /dev/null "http://localhost:$PORT/"; then break; fi
    sleep 0.5
  done
  open "http://localhost:$PORT"
) &

PORT="$PORT" exec "$PY" python/app.py
