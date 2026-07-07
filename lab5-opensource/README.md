# Lab 5 (Open-Source) — Free, Local AI Avatar News

The same idea as Lab 5, but with **zero cloud and zero credits**. Everything runs on your machine:

```
Website → n8n webhook (os-generate)
            → Write Script (Ollama gemma4)
            → HTTP → local render service (http://host.docker.internal:8099/render)
                       • macOS `say`  → speech.wav        (TTS)
                       • Wav2Lip      → lip-synced video   (talking mouth)
                       • ffmpeg       → 1920×1080 (YouTube)
            → Respond { video_url, script, engine }
Website plays the finished video.
```

**HeyGen vs this:** in `lab5/` the video is rendered by HeyGen (cloud, needs API credits). Here the *same n8n flow shape* points at a local render service instead — no account, no credits. Ollama still writes the script in both.

## What's inside

```
lab5-opensource/
├── os-news-avatar-flow.json     # n8n flow: Ollama → local render → respond
├── service/
│   ├── render_service.py        # HTTP render service on :8099
│   ├── broadcaster.jpg          # the anchor photo (the "avatar")
│   ├── wav2lip/                 # Wav2Lip repo + checkpoints (lip-sync)
│   └── .venv/                   # Python env for Wav2Lip
├── website/                     # the news-studio UI
└── start.command               # one-click: starts service + website
```

## Requirements

- **ffmpeg** on `PATH` (`brew install ffmpeg` / `winget install Gyan.FFmpeg`), Python 3, and the Wav2Lip env (`service/.venv`).
- Local **n8n** (Lab 0) with the **Ollama local** credential.
- **TTS is built into the OS** — the service auto-selects: macOS `say`, Windows PowerShell *System.Speech* (SAPI), Linux `espeak-ng`. Optional upgrade: open-source **Piper**.

## Run

1. Import `os-news-avatar-flow.json` into n8n and set it **Active** (it uses the existing **Ollama local** credential).
2. Start the render service (:8099) + website and open the browser:
   - **Mac:** double-click **`start.command`**
   - **Windows:** double-click **`start.bat`**
   - **Manually** (two terminals):

     | | macOS / Linux | Windows |
     |---|---|---|
     | Service | `cd service && python3 render_service.py` | `cd service && python render_service.py` |
     | Website | `cd website && python3 -m http.server 8096` | `cd website && python -m http.server 8096` |
3. Open **http://localhost:8096**, enter a topic, click **Generate News Video**. Ollama writes the script; the service renders a lip-synced 1080p video locally (~30–60s).

## The render engines

`render_service.py` picks the best available:

- **`wav2lip`** — real lip-sync: the anchor's mouth moves to the speech. Used when `service/.venv` + `wav2lip/checkpoints/wav2lip_gan.pth` + the s3fd face detector are present.
- **`kenburns`** — fallback if Wav2Lip isn't set up: a gentle zoom on the photo with the narration (no mouth movement).

### Re-creating the Wav2Lip env (if needed)

```bash
cd service
uv venv --python 3.11 .venv
.venv/bin/python -m pip install "numpy<2" "librosa==0.9.2" opencv-python torch torchvision tqdm numba scipy
git clone https://github.com/Rudrabha/Wav2Lip.git wav2lip
# checkpoints:
#   wav2lip/checkpoints/wav2lip_gan.pth   (Wav2Lip GAN model, ~416 MB)
#   wav2lip/face_detection/detection/sfd/s3fd.pth  (face detector, ~86 MB,
#     e.g. https://www.adrianbulat.com/downloads/python-fan/s3fd-619a316812.pth)
```

## Swapping the "camera"

The n8n flow is agnostic — it just POSTs `{text}` and gets back a video URL. To use a different free renderer (SadTalker, MuseTalk) or a cheap hosted API (Replicate SadTalker), change **only** `render_service.py`; the flow and website stay the same.
