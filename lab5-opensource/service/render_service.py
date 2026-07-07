#!/usr/bin/env python3
"""
Local open-source news-avatar render service (free, no cloud, no credits).

POST /render     { "text": "...", "voice": "Daniel" }  -> { "video_path": "/videos/<id>.mp4", "duration": 12.3, "engine": "wav2lip|kenburns" }
GET  /videos/<f> -> serves the rendered mp4

Pipeline:
  text --(macOS `say`)--> speech.wav
  photo + speech.wav --(Wav2Lip if available, else ffmpeg Ken-Burns)--> mp4 (1920x1080)

n8n (in Docker) calls this at http://host.docker.internal:8099/render — it replaces
the HeyGen HTTP node. The browser plays http://localhost:8099/videos/<id>.mp4.
"""
import json, os, subprocess, sys, uuid, http.server, socketserver

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "broadcaster.jpg")
OUT = os.path.join(HERE, "videos")
WAV2LIP = os.path.join(HERE, "wav2lip")
# venv python differs by OS: Windows -> .venv\Scripts\python.exe, else .venv/bin/python
if os.name == "nt":
    VENV_PY = os.path.join(HERE, ".venv", "Scripts", "python.exe")
else:
    VENV_PY = os.path.join(HERE, ".venv", "bin", "python")
PORT = 8099
os.makedirs(OUT, exist_ok=True)


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def tts(text, voice, base):
    """Text -> 16 kHz mono wav, using the OS's built-in TTS (free, no install):
       macOS: `say` · Windows: PowerShell System.Speech · Linux: espeak-ng.
       (Piper is a nicer cross-platform open-source voice — see the README.)"""
    wav = base + ".wav"
    system = sys.platform
    if system == "darwin":                       # macOS
        src = base + ".aiff"
        run(["say", "-v", voice or "Daniel", "-o", src, text])
    elif system.startswith("win"):               # Windows
        src = base + "_sapi.wav"
        ps = ("Add-Type -AssemblyName System.Speech; "
              "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
              f"$s.SetOutputToWaveFile('{src}'); "
              "$s.Speak([Console]::In.ReadToEnd()); $s.Dispose()")
        subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                       input=text, text=True, check=True, capture_output=True)
    else:                                         # Linux
        src = base + "_espeak.wav"
        run(["espeak-ng", "-w", src, text])
    run(["ffmpeg", "-y", "-i", src, "-ar", "16000", "-ac", "1", wav])
    dur = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                     "-of", "csv=p=0", wav]).stdout.strip())
    if os.path.exists(src):
        os.remove(src)
    return wav, dur


def wav2lip_ready():
    return (os.path.exists(VENV_PY)
            and os.path.exists(os.path.join(WAV2LIP, "checkpoints", "wav2lip_gan.pth"))
            and os.path.exists(os.path.join(WAV2LIP, "inference.py")))


def render_wav2lip(wav, out_mp4):
    """Real lip-sync with Wav2Lip (photo's mouth moves to the audio),
    then upscale/pad to 1920x1080 (YouTube)."""
    raw = out_mp4 + ".raw.mp4"
    run([VENV_PY, "inference.py",
         "--checkpoint_path", "checkpoints/wav2lip_gan.pth",
         "--face", IMG, "--audio", wav, "--outfile", raw,
         "--resize_factor", "1", "--nosmooth", "--pads", "0", "15", "0", "0"], cwd=WAV2LIP)
    run(["ffmpeg", "-y", "-i", raw,
         "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,"
                "pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "copy", out_mp4])
    if os.path.exists(raw):
        os.remove(raw)


def render_kenburns(wav, dur, out_mp4):
    """Fallback: gentle Ken-Burns zoom on the photo + the narration (1080p).
    (No text overlay — many ffmpeg builds ship without the drawtext filter.)"""
    frames = max(int(dur * 25) + 25, 50)
    vf = (
        "[0:v]scale=1920:1080:force_original_aspect_ratio=increase,"
        "crop=1920:1080,"
        f"zoompan=z='min(zoom+0.0004,1.12)':d={frames}:s=1920x1080:fps=25[v]"
    )
    run(["ffmpeg", "-y", "-loop", "1", "-i", IMG, "-i", wav,
         "-filter_complex", vf, "-map", "[v]", "-map", "1:a",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
         "-r", "25", "-shortest", out_mp4])


def render(text, voice):
    vid = uuid.uuid4().hex[:12]
    base = os.path.join(OUT, vid)
    wav, dur = tts(text, voice, base)
    out_mp4 = os.path.join(OUT, vid + ".mp4")
    engine = "kenburns"
    if wav2lip_ready():
        try:
            render_wav2lip(wav, out_mp4)
            engine = "wav2lip"
        except Exception as e:
            sys.stderr.write(f"[wav2lip failed, using kenburns] {e}\n")
            render_kenburns(wav, dur, out_mp4)
    else:
        render_kenburns(wav, dur, out_mp4)
    for f in (wav,):
        if os.path.exists(f):
            os.remove(f)
    return {"video_path": f"/videos/{vid}.mp4", "duration": round(dur, 2), "engine": engine}


class Handler(http.server.BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")

    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()

    def do_GET(self):
        if self.path.startswith("/videos/"):
            fp = os.path.join(OUT, os.path.basename(self.path))
            if os.path.exists(fp):
                self.send_response(200); self._cors()
                self.send_header("Content-Type", "video/mp4")
                self.send_header("Content-Length", str(os.path.getsize(fp)))
                self.end_headers()
                with open(fp, "rb") as f:
                    self.wfile.write(f.read())
                return
        self.send_response(404); self._cors(); self.end_headers()

    def do_POST(self):
        if self.path != "/render":
            self.send_response(404); self._cors(); self.end_headers(); return
        n = int(self.headers.get("Content-Length", 0))
        try:
            body = json.loads(self.rfile.read(n) or b"{}")
            text = (body.get("text") or "").strip()
            if not text:
                raise ValueError("no text")
            result = render(text, body.get("voice"))
            payload = json.dumps(result).encode()
            self.send_response(200)
        except Exception as e:
            payload = json.dumps({"error": str(e)}).encode()
            self.send_response(500)
        self._cors(); self.send_header("Content-Type", "application/json"); self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    print(f"Render service on http://localhost:{PORT}  (wav2lip ready: {wav2lip_ready()})")
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("0.0.0.0", PORT), Handler) as httpd:
        httpd.serve_forever()
