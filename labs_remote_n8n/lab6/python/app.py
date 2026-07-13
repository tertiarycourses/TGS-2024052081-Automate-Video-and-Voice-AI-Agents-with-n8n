"""Digital Human Studio — the whole backend.

Replaces the old Node server.js: serves the static app, proxies the TTS/HeyGen
APIs the browser can't call directly (no CORS), extracts audio from video for
voice cloning, drafts scripts on a local Ollama, and runs MuseTalk for photoreal
lip sync.

Keys live in .env and never reach the browser — /api/config reports only *which*
services are configured, not what their keys are.
"""

from __future__ import annotations

import asyncio
import base64
import os
import re
import shutil
import struct
import subprocess
import tempfile
import threading
import uuid
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles

ROOT = Path(__file__).parent.parent          # the web app lives one level up
RENDERS = Path(__file__).parent / "renders"
RENDERS.mkdir(exist_ok=True)

app = FastAPI(title="Digital Human Studio")


# ── .env ─────────────────────────────────────────────────────────────────
def load_env() -> dict[str, str]:
    env: dict[str, str] = {}
    path = ROOT / ".env"
    if not path.exists():
        return env
    for line in path.read_text().splitlines():
        if line.strip().startswith("#"):
            continue
        m = re.match(r"^\s*([\w.\-]+)\s*=\s*(.*)$", line)
        if m:
            # Case-insensitive: GEMINI_API_KEY, Google_API_Key, gemini-api-key all work.
            env[m.group(1).lower().replace("-", "_").replace(".", "_")] = m.group(2).strip().strip("\"'")
    return env


ENV = load_env()

KEY_ALIASES = {
    "gemini": ["gemini_api_key", "google_api_key", "google_ai_api_key"],
    "elevenlabs": ["elevenlabs_api_key", "eleven_api_key", "xi_api_key"],
    "openai": ["openai_api_key"],
    "heygen": ["heygen_api_key"],
}


def env_key(service: str) -> str:
    for name in KEY_ALIASES.get(service, []):
        val = ENV.get(name) or os.environ.get(name.upper())
        if val:
            return val
    return ""


def have_ffmpeg() -> bool:
    return shutil.which("ffmpeg") is not None


@app.get("/api/config")
async def config():
    return {
        "gemini": bool(env_key("gemini")),
        "elevenlabs": bool(env_key("elevenlabs")),
        "openai": bool(env_key("openai")),
        "heygen": bool(env_key("heygen")),
        "ffmpeg": have_ffmpeg(),
        "musetalk": (Path(__file__).parent / "models" / "musetalkV15" / "unet.pth").exists(),
        "wav2lip": __import__("wav2lip_engine").available(),
    }


# ── text to speech ───────────────────────────────────────────────────────
@app.post("/api/tts/gemini")
async def tts_gemini(req: Request):
    body = await req.json()
    key = body.get("apiKey") or env_key("gemini")
    if not key:
        raise HTTPException(400, "No Gemini API key — paste one, or set GEMINI_API_KEY in .env")

    model = "gemini-2.5-flash-preview-tts"
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
            headers={"x-goog-api-key": key},
            json={
                "contents": [{"parts": [{"text": body["text"]}]}],
                "generationConfig": {
                    "responseModalities": ["AUDIO"],
                    "speechConfig": {
                        "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": body.get("voice") or "Kore"}}
                    },
                },
            },
        )
    if r.status_code != 200:
        raise HTTPException(r.status_code, r.text[:400])

    data = r.json()
    part = next(
        (p for p in data.get("candidates", [{}])[0].get("content", {}).get("parts", []) if "inlineData" in p),
        None,
    )
    if not part:
        raise HTTPException(502, "Gemini returned no audio")

    mime = part["inlineData"].get("mimeType", "")
    rate = int(re.search(r"rate=(\d+)", mime).group(1)) if re.search(r"rate=(\d+)", mime) else 24000
    pcm = base64.b64decode(part["inlineData"]["data"])
    # Gemini hands back raw PCM, not a playable file — wrap it in a WAV header.
    return Response(content=wav_header(len(pcm), rate) + pcm, media_type="audio/wav")


def wav_header(data_len: int, rate: int, channels: int = 1, bits: int = 16) -> bytes:
    byte_rate = rate * channels * bits // 8
    return (
        b"RIFF" + struct.pack("<I", 36 + data_len) + b"WAVE"
        + b"fmt " + struct.pack("<IHHIIHH", 16, 1, channels, rate, byte_rate, channels * bits // 8, bits)
        + b"data" + struct.pack("<I", data_len)
    )


@app.post("/api/tts/elevenlabs")
async def tts_elevenlabs(req: Request):
    body = await req.json()
    key = body.get("apiKey") or env_key("elevenlabs")
    if not key:
        raise HTTPException(400, "No ElevenLabs API key — paste one, or set ELEVENLABS_API_KEY in .env")

    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{body['voiceId']}",
            headers={"xi-api-key": key, "Accept": "audio/mpeg"},
            json={
                "text": body["text"],
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {"stability": 0.45, "similarity_boost": 0.75},
            },
        )
    if r.status_code != 200:
        raise HTTPException(r.status_code, r.text[:400])
    return Response(content=r.content, media_type="audio/mpeg")


@app.post("/api/tts/openai")
async def tts_openai(req: Request):
    body = await req.json()
    key = body.get("apiKey") or env_key("openai")
    if not key:
        raise HTTPException(400, "No OpenAI API key — paste one, or set OPENAI_API_KEY in .env")

    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(
            "https://api.openai.com/v1/audio/speech",
            headers={"Authorization": f"Bearer {key}"},
            json={"model": "tts-1", "voice": body.get("voice", "alloy"),
                  "input": body["text"], "response_format": "mp3"},
        )
    if r.status_code != 200:
        raise HTTPException(r.status_code, r.text[:400])
    return Response(content=r.content, media_type="audio/mpeg")


@app.post("/api/tts/piper")
async def tts_piper(req: Request):
    body = await req.json()
    base = (body.get("baseUrl") or os.environ.get("PIPER_URL") or "http://localhost:5000").rstrip("/")
    url = f"{base}/?voice={body['voice']}" if body.get("voice") else base
    try:
        async with httpx.AsyncClient(timeout=120) as client:
            r = await client.post(url, content=body["text"].encode(),
                                  headers={"Content-Type": "text/plain"})
    except httpx.RequestError:
        raise HTTPException(502, f"Cannot reach Piper at {base}")
    if r.status_code != 200:
        raise HTTPException(r.status_code, r.text[:300])
    return Response(content=r.content, media_type="audio/wav")


# ── voice cloning ────────────────────────────────────────────────────────
@app.post("/api/voice/clone")
async def clone_voice(req: Request):
    """Video in, voice out. ffmpeg strips the audio locally, so the video itself
    never leaves this machine — only the speech ElevenLabs needs."""
    key = req.headers.get("x-api-key") or env_key("elevenlabs")
    if not key:
        raise HTTPException(400, "No ElevenLabs API key — paste one, or set ELEVENLABS_API_KEY in .env")

    name = req.headers.get("x-voice-name", "Cloned voice")
    ctype = req.headers.get("content-type", "")
    raw = await req.body()
    if not raw:
        raise HTTPException(400, "Empty clip")

    tmp = Path(tempfile.mkdtemp(prefix="dh-clone-"))
    try:
        src = tmp / "clip"
        src.write_bytes(raw)

        if ctype.startswith("video/"):
            if not have_ffmpeg():
                raise HTTPException(400, "ffmpeg is required to pull audio out of a video (brew install ffmpeg).")
            audio = tmp / "sample.mp3"
            # -t 180: ElevenLabs wants ~1 minute of clean speech and ignores the rest.
            proc = subprocess.run(
                ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-vn",
                 "-ac", "1", "-ar", "44100", "-b:a", "128k", "-t", "180", str(audio)],
                capture_output=True,
            )
            if proc.returncode != 0:
                raise HTTPException(400, f"Could not extract audio: {proc.stderr.decode()[:200]}")
            payload, filename, mime = audio.read_bytes(), "sample.mp3", "audio/mpeg"
        else:
            payload, filename, mime = raw, "sample.mp3", ctype or "audio/mpeg"

        async with httpx.AsyncClient(timeout=300) as client:
            r = await client.post(
                "https://api.elevenlabs.io/v1/voices/add",
                headers={"xi-api-key": key},
                data={"name": name},
                files={"files": (filename, payload, mime)},
            )
        return JSONResponse(status_code=r.status_code, content=r.json())
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ── script drafting on a local Ollama ────────────────────────────────────
@app.post("/api/script/ollama")
async def script_ollama(req: Request):
    """Ollama writes the script; it cannot speak it. Gemma/Qwen/Llama are text
    models with no audio output — Piper is the offline *speech* engine, this is
    the offline *scriptwriting* one."""
    body = await req.json()
    base = (body.get("baseUrl") or os.environ.get("OLLAMA_URL") or "http://localhost:11434").rstrip("/")
    prompt = (
        "Write a short spoken script for a talking-head video presenter.\n\n"
        f"Brief: {body['brief']}\n\n"
        "Rules: 60-110 words. Plain spoken English, first person, no stage directions, "
        "no markdown, no headings, no quotes around the text. Short sentences that are "
        "easy to say aloud. Output ONLY the script itself."
    )
    try:
        async with httpx.AsyncClient(timeout=300) as client:
            r = await client.post(f"{base}/api/generate",
                                  json={"model": body.get("model") or "gemma4",
                                        "prompt": prompt, "stream": False})
    except httpx.RequestError:
        raise HTTPException(502, f"Cannot reach Ollama at {base}. Is it running?")
    if r.status_code != 200:
        raise HTTPException(r.status_code, r.text[:300])
    return {"script": r.json().get("response", "").strip().strip("\"'")}


# ── HeyGen (v3) ──────────────────────────────────────────────────────────
# v1/v2 are on the sunset path (31 Oct 2026) and reject the new `sk_` keys, so
# everything here talks to v3: POST /v3/videos, GET /v3/videos/{id}.
HEYGEN = "https://api.heygen.com/v3"


def heygen_headers(req: Request) -> dict:
    key = req.headers.get("x-api-key") or env_key("heygen")
    if not key:
        raise HTTPException(400, "No HeyGen API key — paste one, or set HEYGEN_API_KEY in .env")
    return {"X-Api-Key": key}


OWN_ID = re.compile(r"^[0-9a-f]{32}$")   # avatars you own carry 32-hex ids
_avatar_cache: list | None = None         # /v2/avatars is ~500 KB and slow; fetch once


@app.get("/api/heygen/avatars")
async def heygen_avatars(req: Request):
    """Only the avatars v3 will actually render — which is the ones you own.

    This needs both lists, and neither alone is right:
      · /v3/avatars  returns *stock* avatar groups (Annie, Yara, …) whose ids v3
        then rejects with `avatar_not_found`, plus your photo avatars (looks_count 1).
      · /v2/avatars  returns 1200+ look-level entries: stock ones have readable ids
        ("Abigail_standing_office_front") that v3 rejects with `invalid_parameter`,
        while your own avatars carry 32-hex ids that v3 accepts.
    So: photo avatars from v3, custom avatars from v2, stock from neither. Listing a
    stock avatar would just be offering a button that always errors.
    """
    global _avatar_cache
    if _avatar_cache is not None:
        return _avatar_cache

    headers = heygen_headers(req)
    out, seen = [], set()

    async with httpx.AsyncClient(timeout=90) as client:
        v3, v2 = await asyncio.gather(
            client.get(f"{HEYGEN}/avatars", headers=headers),
            client.get("https://api.heygen.com/v2/avatars", headers=headers),
            return_exceptions=True,
        )

    if not isinstance(v3, Exception) and v3.status_code == 200:
        for a in v3.json().get("data", []):
            if a.get("looks_count") == 1 and a["id"] not in seen:   # photo avatar
                seen.add(a["id"])
                out.append({"id": a["id"], "name": a.get("name", "?"),
                            "kind": "photo", "preview": a.get("preview_image_url")})

    if not isinstance(v2, Exception) and v2.status_code == 200:
        data = v2.json().get("data") or {}
        for a in data.get("avatars", []):
            aid = a.get("avatar_id", "")
            if OWN_ID.match(aid) and aid not in seen:
                seen.add(aid)
                out.append({"id": aid, "name": a.get("avatar_name", "?"),
                            "kind": "avatar", "preview": a.get("preview_image_url")})
        for t in data.get("talking_photos", []):
            tid = t.get("talking_photo_id", "")
            if tid and tid not in seen:
                seen.add(tid)
                out.append({"id": tid, "name": t.get("talking_photo_name") or "Photo avatar",
                            "kind": "photo", "preview": t.get("preview_image_url")})

    if not out:
        raise HTTPException(404, "No usable avatars. HeyGen v3 renders only avatars you own — "
                                 "create an avatar or upload a photo avatar in HeyGen first.")
    _avatar_cache = out
    return out


@app.get("/api/heygen/voices")
async def heygen_voices(req: Request):
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.get(f"{HEYGEN}/voices", headers=heygen_headers(req))
    if r.status_code != 200:
        raise HTTPException(r.status_code, r.text[:200])
    items = r.json().get("data", [])
    return [
        {"id": v["voice_id"], "name": (v.get("name") or "").strip(),
         "gender": v.get("gender"), "language": v.get("language")}
        for v in items if v.get("voice_id")
    ]


@app.post("/api/heygen/upload")
async def heygen_upload(req: Request):
    """Turn the uploaded portrait into a photo avatar. Note HeyGen caps how many
    photo avatars an account may hold (3 on lower plans) and returns a 400 — we
    pass that message straight through rather than dressing it up."""
    raw = await req.body()
    async with httpx.AsyncClient(timeout=300) as client:
        r = await client.post(
            "https://upload.heygen.com/v1/talking_photo",
            headers={**heygen_headers(req),
                     "Content-Type": req.headers.get("content-type", "image/jpeg")},
            content=raw,
        )
    if r.status_code == 200:
        global _avatar_cache
        _avatar_cache = None   # a new photo avatar exists now
    return JSONResponse(status_code=r.status_code, content=r.json())


@app.post("/api/heygen/render")
async def heygen_render(req: Request):
    """Submit a v3 render and poll it in the background, so the browser just
    watches one job like it does for MuseTalk."""
    body = await req.json()
    headers = heygen_headers(req)

    payload = {
        "type": "avatar",
        "avatar_id": body["avatar_id"],
        "script": body["text"],
        "voice_id": body["voice_id"],
    }

    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(f"{HEYGEN}/videos", headers=headers, json=payload)
    if r.status_code != 200:
        raise HTTPException(r.status_code, r.text[:300])

    video_id = r.json()["data"]["video_id"]
    job_id = f"hg_{video_id[:10]}"
    JOBS[job_id] = {"status": "running", "pct": 5, "message": "submitted to HeyGen", "url": None}

    def poll():
        import time, httpx as hx
        started = time.time()
        while time.time() - started < 900:
            try:
                resp = hx.get(f"{HEYGEN}/videos/{video_id}", headers=headers, timeout=30)
                data = resp.json().get("data", {})
            except Exception as exc:
                JOBS[job_id].update(status="error", message=str(exc))
                return

            status = data.get("status")
            secs = int(time.time() - started)
            if status == "completed":
                JOBS[job_id].update(status="done", pct=100, message="done",
                                    url=data.get("video_url"))
                return
            if status == "failed":
                JOBS[job_id].update(status="error",
                                    message=f"HeyGen failed: {data.get('error') or 'unknown'}")
                return
            # HeyGen has no progress %, only a state — show elapsed instead of a fake bar.
            JOBS[job_id].update(status="running", pct=min(90, 10 + secs),
                                message=f"{status} · {secs}s elapsed")
            time.sleep(5)
        JOBS[job_id].update(status="error", message="timed out after 15 minutes")

    threading.Thread(target=poll, daemon=True).start()
    return {"job_id": job_id}


# ── MuseTalk: photoreal lip sync ─────────────────────────────────────────
JOBS: dict[str, dict] = {}
_render_lock = threading.Lock()   # the model is big; one render at a time


@app.post("/api/render/musetalk")
async def render_musetalk(
    image: UploadFile = File(...),
    audio: UploadFile = File(...),
    bbox_shift: int = Form(0),
):
    job_id = uuid.uuid4().hex[:12]
    work = Path(tempfile.mkdtemp(prefix=f"dh-render-{job_id}-"))
    img_path = work / f"portrait{Path(image.filename or 'x.png').suffix or '.png'}"
    aud_path = work / f"audio{Path(audio.filename or 'x.wav').suffix or '.wav'}"
    img_path.write_bytes(await image.read())
    aud_path.write_bytes(await audio.read())

    out = RENDERS / f"{job_id}.mp4"
    JOBS[job_id] = {"status": "queued", "pct": 0, "message": "queued", "url": None}

    def run():
        def progress(msg, pct):
            JOBS[job_id].update(status="running", message=msg, pct=pct)

        try:
            with _render_lock:
                from musetalk_engine import get_engine
                progress("loading MuseTalk (first run takes a minute)", 1)
                engine = get_engine()
                engine.load()
                engine.render(str(img_path), str(aud_path), str(out),
                              bbox_shift=bbox_shift, progress=progress)
            JOBS[job_id].update(status="done", pct=100, message="done",
                                url=f"/api/render/file/{job_id}.mp4")
        except Exception as exc:  # surfaced to the UI verbatim — don't swallow it
            JOBS[job_id].update(status="error", message=f"{type(exc).__name__}: {exc}")
        finally:
            shutil.rmtree(work, ignore_errors=True)

    threading.Thread(target=run, daemon=True).start()
    return {"job_id": job_id}


@app.post("/api/render/wav2lip")
async def render_wav2lip(
    image: UploadFile = File(...),
    audio: UploadFile = File(...),
):
    """Wav2Lip: fast (96x96 mouth model), local, no GPU strictly required.
    Same job/progress contract as MuseTalk so the front end treats them alike."""
    job_id = uuid.uuid4().hex[:12]
    work = Path(tempfile.mkdtemp(prefix=f"dh-w2l-{job_id}-"))
    img_path = work / f"portrait{Path(image.filename or 'x.png').suffix or '.png'}"
    aud_path = work / f"audio{Path(audio.filename or 'x.wav').suffix or '.wav'}"
    img_path.write_bytes(await image.read())
    aud_path.write_bytes(await audio.read())

    out = RENDERS / f"{job_id}.mp4"
    JOBS[job_id] = {"status": "queued", "pct": 0, "message": "queued", "url": None}

    def run():
        def progress(msg, pct):
            JOBS[job_id].update(status="running", message=msg, pct=pct)

        try:
            with _render_lock:
                import wav2lip_engine
                progress("starting Wav2Lip", 1)
                wav2lip_engine.render(str(img_path), str(aud_path), str(out), progress=progress)
            JOBS[job_id].update(status="done", pct=100, message="done",
                                url=f"/api/render/file/{job_id}.mp4")
        except Exception as exc:
            JOBS[job_id].update(status="error", message=f"{type(exc).__name__}: {exc}")
        finally:
            shutil.rmtree(work, ignore_errors=True)

    threading.Thread(target=run, daemon=True).start()
    return {"job_id": job_id}


@app.post("/api/models/download/{engine}")
async def download_weights(engine: str):
    """Fetch an engine's weights (MuseTalk ~3.5 GB, Wav2Lip ~440 MB) with live progress.
    A learner should not need a terminal to fix a greyed-out button."""
    import weights

    if engine not in weights.DOWNLOADERS:
        raise HTTPException(404, f"Unknown engine: {engine}")

    job_id = uuid.uuid4().hex[:12]
    JOBS[job_id] = {"status": "queued", "pct": 0, "message": "queued", "url": None}

    def run():
        def progress(msg, pct):
            JOBS[job_id].update(status="running", message=msg, pct=int(pct))

        try:
            weights.DOWNLOADERS[engine](progress)
            JOBS[job_id].update(status="done", pct=100, message=f"{engine} is ready — reload the page")
        except Exception as exc:
            JOBS[job_id].update(status="error", message=f"{type(exc).__name__}: {exc}")

    threading.Thread(target=run, daemon=True).start()
    return {"job_id": job_id}


@app.get("/api/render/status/{job_id}")
async def render_status(job_id: str):
    job = JOBS.get(job_id)
    if not job:
        raise HTTPException(404, "Unknown job")
    return job


@app.get("/api/render/file/{name}")
async def render_file(name: str):
    path = RENDERS / Path(name).name          # basename only — no path traversal
    if not path.exists():
        raise HTTPException(404, "No such render")
    return FileResponse(path, media_type="video/mp4")


# ── static app (must be mounted last, it catches everything) ─────────────
app.mount("/", StaticFiles(directory=ROOT, html=True), name="static")


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", "8137"))
    host = os.environ.get("HOST", "127.0.0.1")   # Docker/Coolify set HOST=0.0.0.0
    print(f"\n  Digital Human Studio → http://{'localhost' if host == '127.0.0.1' else host}:{port}\n")
    uvicorn.run(app, host=host, port=port, log_level="warning")
