# Lab 6 — Lip-Sync Face-Off: MuseTalk (local) vs HeyGen (cloud)

Write a news script with **gemma4** running locally in Ollama, feed the *same* script and the
*same* portrait to two very different lip-sync engines, and judge the result with your eyes
instead of the marketing page.

- **MuseTalk** — a neural model that inpaints real mouth pixels, running **on your machine**. Free, private, ~75 s per clip on Apple Silicon. Mouth only: the head does not move.
- **HeyGen** — a **cloud** renderer that costs credits. ~40 s. The only one of the two that also moves the head and blinks.

The demo app is [alfredang/lipsyncdemo](https://github.com/alfredang/lipsyncdemo) (*Digital Human
Studio*). It also ships an instant in-browser preview — geometry, not a face — which is useful
for timing a script before you spend a cent.

## Install

**macOS / Linux (or Git Bash on Windows):**

```bash
cd lab6
./setup.sh                # app only  → browser preview + HeyGen
./setup.sh --musetalk     # also download MuseTalk weights (~3.5 GB, once)
```

**Windows (PowerShell), by hand:**

```powershell
cd lab6
git clone https://github.com/alfredang/lipsyncdemo.git
cd lipsyncdemo
python -m venv python\.venv
python\.venv\Scripts\Activate.ps1
pip install -e .
python python\app.py          # → http://localhost:8137
```

Then open **http://localhost:8137**.

> **MuseTalk needs a GPU** — Apple Silicon (MPS) or NVIDIA. On a plain CPU it is not slow,
> it is unusable (many minutes per clip), and the app will correctly disable the *Render
> photoreal* button rather than offer you a failure. On a CPU-only machine, compare the
> **browser preview** against **HeyGen** instead — the lesson survives intact.

## Get your HeyGen API key

1. Sign in at **https://app.heygen.com** (the free tier includes credits — enough for a couple of short clips).
2. Click your **avatar / initials, top right → Settings**.
3. Open the **API** tab (also reachable at `https://app.heygen.com/settings?nav=API`).
4. Click **Copy** under *API Token*. It is a long string; HeyGen shows it once.
5. Paste it into `lab6/lipsyncdemo/.env`:

   ```
   HEYGEN_API_KEY=<your token>
   ```
6. **Restart the app** — the key is read at startup. Reload `http://localhost:8137` and the
   HeyGen renderer stops being greyed out.

> **Costs credits.** Each HeyGen render burns credits from your account. Keep the script to
> two or three sentences while you experiment.
>
> **The v3 API only renders avatars you own.** Stock avatars are rejected, so the picker
> lists only *your* avatars and photo avatars. Upload a portrait first if the list is empty.

## Write the script with gemma4 (local, free)

Do not hand-write the news copy — generate it, the same way Lab 7 will:

```bash
ollama run gemma4 "Write a 3-sentence TV news bulletin about Singapore's MRT expansion. \
Spoken style, no headings, no markdown, under 60 words."
```

Paste the result into the app's script box. Keep it short: every extra second of audio is
extra render time on MuseTalk and extra credits on HeyGen.

Pick a voice, click **Speak**, and use the **instant browser preview** to check the timing
*before* you render anything. It is free and immediate — that is the whole point of it.

## The comparison

Render the **same script** and the **same portrait** through both engines, then score them.

| | MuseTalk (local) | HeyGen (cloud) |
|---|---|---|
| Where it runs | your machine | HeyGen's servers |
| Cost | free | credits |
| Privacy | the photo never leaves your laptop | photo + audio are uploaded |
| Speed | ~75 s (Apple M4) | ~40 s |
| Mouth | real inpainted pixels — teeth, lips, shadow | photoreal |
| Head / blinks | **no** — the head is frozen | **yes** |
| Fails when | no GPU | no credits / no network |

Score each render 0–2 on: **lip accuracy** (do the consonants land?), **mouth realism**
(teeth and shadow, or a smear?), **head motion** (alive, or a mannequin?), and **artefacts**
(flicker at the jaw line, colour mismatch at the crop edge).

Then answer the question that actually matters in a workplace: **which would you ship, and
why?** A frozen head that is free and private, or a moving head that costs money and uploads
your customer's face to a vendor? There is no single right answer — there is a defensible one,
and that is what you write down.

## Files

```
lab6/
├── setup.sh      # clone + venv + optional model weights + run
└── README.md
```

The demo itself is cloned into `lab6/lipsyncdemo/` and is **not** committed to this repo —
it is 3.5 GB of weights once you enable MuseTalk.
