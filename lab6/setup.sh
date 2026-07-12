#!/bin/bash
# Lab 6 — Digital Human Studio (Wav2Lip vs MuseTalk vs HeyGen)
#
# The app lives here in the repo — nothing is cloned. This script only builds the
# Python environment and (optionally) downloads the MuseTalk weights.
#
#     ./setup.sh              # app only  → browser preview + Wav2Lip + HeyGen
#     ./setup.sh --musetalk   # also download the MuseTalk weights (~3.5 GB, once)
#
# macOS/Linux: run in Terminal.  Windows: see README.md (PowerShell steps).
set -e
cd "$(dirname "$0")"

PORT="${PORT:-8137}"

# 1. Python environment. uv is fast and handles the 3.11 pin; fall back to venv.
if [ ! -x "python/.venv/bin/python" ]; then
  if command -v uv >/dev/null 2>&1; then
    echo "==> Creating the Python 3.11 environment with uv"
    uv venv --python 3.11 python/.venv
    # shellcheck disable=SC1091
    source python/.venv/bin/activate
    uv pip install -r pyproject.toml
  else
    echo "==> uv not found, using python3 -m venv (slower)"
    python3 -m venv python/.venv
    # shellcheck disable=SC1091
    source python/.venv/bin/activate
    pip install --upgrade pip
    pip install -e .
  fi
else
  echo "==> Python environment already exists"
  # shellcheck disable=SC1091
  source python/.venv/bin/activate
fi

# 2. MuseTalk weights — 3.5 GB, so only on request.
if [ "$1" = "--musetalk" ]; then
  echo "==> Downloading MuseTalk weights (~3.5 GB). Runs once; takes a while."
  ./python/download_models.sh
else
  echo "==> Skipping MuseTalk weights. Re-run with --musetalk for local photoreal rendering."
fi

# 3. Wav2Lip is reused from Lab 7 — no second download of a 400 MB checkpoint.
if [ -f "../lab7-opensource/service/wav2lip/checkpoints/wav2lip_gan.pth" ]; then
  echo "==> Wav2Lip found (reusing the Lab 7 install)"
else
  echo "==> Wav2Lip NOT found. The ⚡ Render Wav2Lip button will be disabled."
  echo "    It expects ../lab7-opensource/service/wav2lip/checkpoints/wav2lip_gan.pth"
fi

# 4. Keys. The app reads .env; the browser is only told WHICH services are configured.
if [ ! -f .env ]; then
  cat > .env <<'ENVEOF'
# HeyGen renders in the cloud and costs credits. Get the key at https://app.heygen.com
# → your avatar (top right) → Settings → API → copy the API token.
HEYGEN_API_KEY=

# Optional, for nicer voices. Everything else works without them.
GEMINI_API_KEY=
ELEVENLABS_API_KEY=
OPENAI_API_KEY=
ENVEOF
  echo "==> Wrote a starter .env — paste your HEYGEN_API_KEY into it to enable HeyGen."
fi

echo
echo "==> Starting Digital Human Studio on http://localhost:$PORT   (Ctrl+C to stop)"
PORT="$PORT" python python/app.py
