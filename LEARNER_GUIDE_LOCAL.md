# Learner Guide — Local Build

**Automate Video and Voice AI Agents with n8n** · WSQ TGS-2024052081 · Tertiary Infotech Academy Pte Ltd

> **This is the LOCAL build.** n8n runs in Docker on your machine, the models run on your machine
> (Ollama `gemma4` + `nomic-embed-text`), and webhooks live on `http://localhost:5678`. It is free,
> it works offline, and no data leaves your laptop. Labs: [`labs_local_n8n/`](labs_local_n8n/).
>
> For the hosted build — no Docker, OpenAI models, no ngrok — see
> [`LEARNER_GUIDE_CLOUD.md`](LEARNER_GUIDE_CLOUD.md).

---

## How this course is organised

| Topic | Theme | Labs |
|---|---|---|
| **1** | **Chatbot** — agents, RAG, grounded answers | Lab 1, Lab 2, Lab 3 |
| **2** | **Voice Agent** — agents that speak and call real tools | Lab 4, Lab 5 |
| **3** | **Video Agent** — lip-sync, avatars, text-to-video | Lab 6, Lab 7, Lab 7-os, Lab 8, Lab 9, Lab 10 |

Lab 0 comes before all of it: it builds the machine everything else runs on.

## The one rule that explains most failures

**A workflow does nothing until it is Active.** n8n does not create a production `/webhook/…` path
until you flip the workflow to **Active**. Until then the URL returns `404`, and the lab's website
reports that it cannot reach n8n. When something "doesn't work", check this first, every time.

## The second rule: which way does the call go?

Every lab is a set of HTTP calls, and the *direction* decides whether you need a public URL.

| Direction | Example | Public URL needed? |
|---|---|---|
| **Your browser → n8n** | Lab 4's web-call button, Lab 2's chat box | **No.** Your own machine is calling. `localhost` is fine. |
| **A vendor's servers → n8n** | ElevenLabs calling `check_availability`; Vapi calling your Custom LLM | **Yes.** They cannot see your `localhost`. You need **ngrok**. |
| **n8n → your machine** | Lab 7-os calling the render service | No — n8n reaches it at `host.docker.internal`. |

Learners lose more time to this than to anything else in the course. Before you debug a webhook, ask:
*who is dialling?*

---

# Lab 0 — Set up n8n on your computer

**Goal:** Docker + n8n + Postgres + Ollama, all running and talking to each other.
**Folder:** [`labs_local_n8n/lab0/`](labs_local_n8n/lab0/)

## Get the labs

Download the repository from GitHub:
`https://github.com/tertiarycourses/TGS-2024052081-Automate-Video-and-Voice-AI-Agents-with-n8n`
(**Code → Download ZIP**, or `git clone`).

> 🪟 **Windows: unblock the ZIP before extracting.** Downloaded files carry the
> *Mark-of-the-Web* and Windows silently blocks the scripts inside. Right-click the ZIP →
> **Properties** → tick **Unblock** → OK, *then* extract. If you already extracted and
> SmartScreen warns on a `start.bat`, click **More info → Run anyway** — the launcher then
> unblocks the rest of that lab's files itself. `git clone` avoids all of this.

## Install

| Tool | macOS | Windows (PowerShell) |
|---|---|---|
| Docker Desktop | `brew install --cask docker` | `winget install Docker.DockerDesktop` |
| Ollama | `brew install ollama` | `winget install Ollama.Ollama` |
| ffmpeg (labs 6, 7-os) | `brew install ffmpeg` | `winget install Gyan.FFmpeg` |
| ngrok (labs 4, 5) | `brew install ngrok` | `winget install ngrok.ngrok` |

On Windows, **close and reopen PowerShell after installing** — a new program is not on your PATH until
you do. "Command not recognized" is almost always this.

**Docker Desktop must be launched, not just installed.** Open the app and wait for the whale to settle.

## Start the stack

```bash
cd labs_local_n8n/lab0
docker compose pull
docker compose up -d
```

- **`docker compose pull`** downloads the `n8nio/n8n` and `postgres:17` images. A few hundred MB the
  first time. Doing it as its own step means the download shows you a progress bar instead of looking
  like a hang.
- **`docker compose up -d`** starts both containers in the background (`-d` = detached) and gives you
  your terminal back.

Check both are up:

```bash
docker compose ps        # want lab0-n8n-1 and lab0-postgres-1, both "running"
```

## Pull the models

```bash
ollama pull gemma4
ollama pull nomic-embed-text
ollama list              # both must appear
```

Two models, two jobs. **`gemma4`** is the *chat* model — it writes and reasons. **`nomic-embed-text`**
is the *embedding* model — it turns text into vectors so the RAG labs can search by meaning. Neither
can do the other's job.

## Connect n8n to Ollama

Open **http://localhost:5678**, create the owner account (local only — but there is no password reset,
so write it down). Then create an **Ollama** credential named **`Ollama local`**:

```text
http://host.docker.internal:11434
```

**Not `localhost:11434`.** n8n runs *inside a container*, and inside that container `localhost` means
*the container itself*, where nothing is listening. `host.docker.internal` is how a container says
"the computer hosting me". Press **Test** — it must pass before you go on.

## Everyday commands

| Task | Command |
|---|---|
| Start | `docker compose up -d` |
| Stop, keep data | `docker compose stop` |
| Logs | `docker compose logs -f n8n` |
| Update n8n | `docker compose pull` then `docker compose up -d` |
| Remove containers, **keep** workflows | `docker compose down` |
| Remove containers **and erase everything** | `docker compose down -v` |

`-v` deletes the `n8n_data` and `postgres_data` volumes — every workflow and credential you have built.
There is no undo.

## Checkpoint

- [ ] `docker compose ps` shows n8n and postgres running.
- [ ] n8n opens at `http://localhost:5678`.
- [ ] `ollama list` shows `gemma4` and `nomic-embed-text`.
- [ ] The `Ollama local` credential test passes.
- [ ] You can say why the credential must not use `localhost:11434`.

---

# Topic 1 — Chatbot

Agents, retrieval, and the discipline of making a model answer only from what it was given.

---

## Lab 1 — Your first AI Agent

**Goal:** the smallest possible working agent.
**Flow:** `lab1/ai-agent.json` · **Credential:** `Ollama local`

Three nodes, and that is the whole point:

| Node | Job |
|---|---|
| **When chat message received** | n8n's built-in chat trigger — it gives you a chat window, no website needed |
| **AI Agent** | the agent: system prompt, memory, and (later) tools |
| **Ollama Chat Model** | the brain — `gemma4:latest`, running on your machine |

### Steps

1. Import the flow. Open the **Ollama Chat Model** node; confirm the credential is `Ollama local` and
   the model is `gemma4:latest`.
2. Click **Chat** at the bottom of the canvas and say hello.
3. Open the **AI Agent** node and give it a system prompt — e.g. *"You are a terse assistant. Never use
   more than two sentences."*
4. Ask again. Watch the reply change.

### Verify

- [ ] The agent replies in the chat panel.
- [ ] The execution list shows a run, and you can open it and read what the model received.
- [ ] Changing the system prompt visibly changes the behaviour.

> **The habit this lab teaches:** open the execution and read what the model *actually* got. A fluent
> answer is not evidence. The execution trace is evidence.

---

## Lab 2 — RAG IT Support Chatbot

**Goal:** a chatbot that answers from a PDF you upload, and admits when the answer is not in it.
**Flow:** `lab2/rag-flow.json` · **Site:** `lab2/index.html`
**Webhooks:** `POST /rag-upload`, `POST /rag-chat` · **Credential:** `Ollama local`

### What RAG actually is

The model does not "learn" your PDF. Instead:

1. **Ingest** — split the PDF into chunks, run each chunk through the *embedding* model
   (`nomic-embed-text`), and store the resulting vectors.
2. **Retrieve** — embed the user's question the same way, and find the chunks whose vectors sit closest
   to it. This is search by **meaning**, not keyword.
3. **Generate** — hand those chunks to `gemma4` and tell it: *answer only from this*.

The flow has both halves: an **upload** webhook that ingests, and a **chat** webhook that retrieves and
answers. Both sides use the *same* embedding model — they must, or the vectors are not comparable.

### Steps

1. Import the flow, set it **Active**.
2. Serve the page:
   ```bash
   cd labs_local_n8n/lab2
   python3 -m http.server 8092       # Windows: python -m http.server 8092
   ```
3. Open `http://localhost:8092`, upload `it-faq.pdf`, wait for the confirmation.
4. Ask something the PDF answers. Then ask something it does **not** — *"What is the CEO's salary?"*

### Verify

- [ ] A question covered by the PDF gets a grounded, correct answer.
- [ ] A question **not** covered gets a refusal, not an invention. **This is the graded behaviour.**
- [ ] You can point to the retrieved chunks in the execution trace.

> **Do not open with `file://`.** Serve it over `http://localhost`, or the browser blocks the requests
> and every button dies silently.

---

## Lab 3 — CX Agent with RAG (Cook & Bake Academy)

**Goal:** the same RAG idea, but as a customer-facing chat widget on a real-looking website.
**Flow:** `lab3/CX Agent with RAG.json`
**Webhooks:** `POST /cx-agent`, `POST /brochure-upload` · **Credential:** `Ollama local`

This is Lab 2 grown up. The knowledge base is a set of **course brochures**; the agent is a course
advisor for a cooking school; the front end is a chat widget bolted onto a marketing site.

### Steps

1. Import the flow, set it **Active**.
2. Open `lab3/upload-brochures.html` and upload the PDFs from `lab3/brochures/` — this hits
   `/brochure-upload` and fills the vector store.
3. Serve the site:
   ```bash
   cd labs_local_n8n/lab3/website
   python3 -m http.server 8093
   ```
4. Open the chat widget and ask about a course, a price, a schedule.

The widget already points at `http://localhost:5678/webhook/cx-agent`. The ⚙ panel still lets you
override it (for ngrok), but you should not need to touch it.

### Verify

- [ ] The agent answers from the brochures, with specifics.
- [ ] Asked about a course that does not exist, it says so rather than inventing one.
- [ ] The chat has memory — a follow-up like *"how much is that one?"* resolves correctly.

---

# Topic 2 — Voice Agent

Two vendors, two architectures. The contrast *is* the lesson.

|  | **Lab 4 — ElevenLabs** | **Lab 5 — Vapi** |
|---|---|---|
| Who runs the model | **ElevenLabs** | **your n8n workflow** (Vapi "Custom LLM") |
| What n8n does | mints a signed URL, and serves the tools | **is the brain** |
| Call path | browser → n8n → signed URL → WebSocket | browser → Vapi, then Vapi → your n8n |

---

## Lab 4 — Voice Booking Agent with ElevenLabs (GG Hair Salon)

**Goal:** Nina takes a phone-style call, checks a **real Google Calendar**, and books a **real** appointment.
**Flows:** `lab4/elevenlabs-web-call-flow.json` · `lab4/elevenlabs-booking-tools-flow.json`
**Webhooks:** `POST /elevenlabs-web-call` · `POST /check-availability` · `POST /book-appointment`
**Credentials:** `ElevenLabs API` (Header Auth, name `xi-api-key`) + **your own Google Calendar** (OAuth)

### How the key stays safe

ElevenLabs does not hand the browser a raw token. Your n8n asks ElevenLabs for a short-lived
**signed URL** — server-side, using the `xi-api-key` — and returns *only that* to the page. The browser
opens a WebSocket to the signed URL and talks. **Your API key never reaches the browser.**

### Setup

1. Import **both** flows; set both **Active**.
2. On *ElevenLabs: Get Signed URL*, add a **Header Auth** credential named `ElevenLabs API`:
   Name `xi-api-key`, Value = your key.
3. On the two **Google Calendar** nodes, connect **your own** Google account. The flow ships with no
   calendar credential on purpose — it is yours.
4. In the ElevenLabs dashboard, create a Conversational AI agent (Nina). Put her **agent ID** into the
   *Get Signed URL* node (or in the page's ⚙ Settings).
5. Upload `knowledge-base/gg-hair-salon-handbook.pdf` to the agent's **Knowledge Base**, so she quotes
   real prices instead of inventing them.

### The tunnel — and why only half of it needs one

```bash
ngrok http 5678
```

| Webhook | Who calls it | Tunnel? |
|---|---|---|
| `/elevenlabs-web-call` | your **browser** | **No** |
| `check_availability`, `book_appointment` | **ElevenLabs' servers** | **Yes** |

Register the tools in the ElevenLabs agent as
`https://<id>.ngrok-free.app/webhook/check-availability` and `…/book-appointment`.

If you skip the tunnel, the call *appears* to work: Nina says "let me check that for you" — and then
stalls forever, because her tool call went to a `localhost` that her servers cannot see.

### Run it

```bash
cd labs_local_n8n/lab4/website
python3 -m http.server 8090
```

### Verify

- [ ] Nina answers by voice.
- [ ] Asked for a taken slot, she offers an alternative.
- [ ] A booking **appears in your Google Calendar**. That event is your evidence.

---

## Lab 5 — Grounded FAQ Voice Agent with Vapi (MediRefill)

**Goal:** Ava answers refill questions from a fixed FAQ — and **refuses to give medical advice**.
**Flow:** `lab5/vapi-faq-flow.json` · **Webhook:** `POST /vapi-faq`
**Credential:** `Ollama local` · **Prompt:** `lab5/ava-assistant-prompt.md`

Here **n8n is the model**. Vapi does speech-to-text and the voice, then calls *your* workflow as its
**Custom LLM**. The intelligence — and the guardrail — is yours.

### Why a pharmacy

Because the interesting failure is not a wrong delivery date. Ava has two rules, and the second is the
one that matters:

1. **Grounding** — answer only from the six FAQ topics.
2. **A hard safety boundary** — never advise on a dose, an interaction, a substitution, or a symptom.
   Every such question gets one fixed sentence and a **pharmacist callback**.

A confident wrong answer in retail costs a refund. In a pharmacy it is a safety incident. That is why
the refusal is *fixed wording in the prompt*, not left to the model's judgement.

### Setup

1. Import the flow, set it **Active**.
2. Tunnel — Vapi's servers must reach your n8n:
   ```bash
   ngrok http 5678
   ```
   Custom LLM URL = `https://<id>.ngrok-free.app/webhook/vapi-faq`
3. In Vapi, create an assistant whose **model** is that Custom LLM.
4. Serve the site and paste your Vapi **public** key + assistant ID into ⚙ Settings:
   ```bash
   cd labs_local_n8n/lab5/website
   python3 -m http.server 8091
   ```

**Never paste your *private* key into the page.** A public key can only start calls; a private key
manages your account, and anything in a web page is visible to every visitor.

### Verify — the grade is in the refusals

| Say | Ava must |
|---|---|
| "When will my refill arrive?" | Answer: two to three working days, free above sixty dollars |
| **"Can I take two instead of one?"** | **Refuse** + pharmacist callback |
| **"Is it safe with my other medicine?"** | **Refuse** — interactions are clinical |
| **"I'm having chest pains."** | **Escalate** — 995 / A&E |
| "Who is your CEO?" | "I don't have that in front of me…" |

If Ava gives medical content on any **bold** row — even hedged, even with a disclaimer — the guardrail
failed. Capture the transcript; that transcript is your assessment evidence.

---

# Topic 3 — Video Agent

From a script, to a mouth that moves, to a face that talks back, to video from nothing but a sentence.

---

## Lab 6 — Lip-Sync Face-Off: MuseTalk (local) vs HeyGen (cloud)

**Goal:** feed the *same* script and the *same* portrait to two engines and judge with your eyes.
**Folder:** `lab6/` · **No n8n flow** — this one is a local Python app.

| | **MuseTalk** | **HeyGen** |
|---|---|---|
| Runs | on your machine | in the cloud |
| Cost | free | credits |
| Speed | ~75 s (Apple Silicon) | ~40 s |
| Moves | **mouth only** | mouth **+ head + blinks** |
| Privacy | your face never leaves | uploaded |

### Steps

```bash
cd labs_local_n8n/lab6
./setup.sh                # app only → browser preview + HeyGen
./setup.sh --musetalk     # also download MuseTalk weights (~3.5 GB, once)
```

`gemma4` writes the news script; the same script and portrait go to both engines.

### Verify

- [ ] Both clips render from the identical script and portrait.
- [ ] You can state, in one sentence each, when you would choose each engine — and back it with what
      you saw, not the marketing page.

---

## Lab 7 — Avatar News Video with HeyGen (GG News Studio)

**Goal:** facts in → spoken script → a presenter reads it on camera.
**Flow:** `lab7/heygen-news-avatar-flow.json`
**Webhooks:** `POST /heygen-generate`, `POST /heygen-status` · **Credentials:** `HeyGen API`, `Ollama local`

Video rendering is **slow** — far too slow to hold an HTTP request open. So the flow is split, and this
shape is worth learning because every long-running API works this way:

- **`/heygen-generate`** — `gemma4` writes ~55–70 words of *spoken* copy, sends it to HeyGen, and
  immediately returns a **video ID**.
- **`/heygen-status`** — the page polls this until the video is `completed`, then plays it.

### Verify

- [ ] The script *sounds* spoken — no bullets, no URLs, no markdown. The avatar reads it aloud; a stray
      asterisk becomes an audible "asterisk".
- [ ] The page polls and eventually plays the finished video.

---

## Lab 7 (Open-Source) — the same video, free and local

**Goal:** the same flow shape, with **zero cloud and zero credits**.
**Flow:** `lab7-opensource/os-news-avatar-flow.json`
**Webhook:** `POST /os-generate` · **Credential:** `Ollama local`

```text
Website → n8n /os-generate
            → Write Script (Ollama gemma4)
            → HTTP → your render service at host.docker.internal:8099/render
                       • TTS       → speech.wav
                       • Wav2Lip   → lip-synced video
                       • ffmpeg    → 1920×1080
            → Respond { video_url }
```

Start the render service first (`start.command` on macOS, `start.bat` on Windows), then run the flow.
Note the direction: **n8n calls out to your machine**, so `host.docker.internal` works and no tunnel is
needed — the exact opposite of Lab 4's tools.

### Verify

- [ ] A finished MP4 plays in the page, produced entirely on your machine.
- [ ] You can name one quality difference versus HeyGen, and one reason you would still pick this.

---

## Lab 8 — Interactive Avatar Brain (Aria, in-browser)

**Goal:** a talking avatar you can **interrupt** — latency is the feature.
**Flow:** `lab8/avatar-chat-flow.json`
**Webhook:** `POST /avatar-chat` · **Model:** AI Agent + `gemma4` (`Ollama local`)

The flow is the same pair you met in Lab 1 — **AI Agent + Ollama Chat Model** — now behind a
webhook instead of a chat window, so it is one credential to attach and nothing else to configure:

```text
Webhook → Build Prompt → AI Agent (gemma4) → Make It Speakable → Respond
```

Three details worth reading in the flow:

- **The system prompt** (in the AI Agent node) carries Aria's voice rules — one or two spoken
  sentences, no markdown, say numbers in words — plus the facts she is allowed to state. It also
  tells her to *always answer helpfully* and never claim she "didn't catch" a message: the text
  always arrives perfectly; only a model hiccup can fail.
- **Stateless by design** — the browser sends the recent transcript with every turn, folded into
  the system message. No memory node, no session store.
- **Make It Speakable** strips whatever must never be spoken aloud: markdown (a stray asterisk
  becomes an audible "asterisk"), URLs, and a thinking model's private `<think>` reasoning.

### Verify

- [ ] Aria answers helpfully by voice — never "I did not catch that" when the message arrived.
- [ ] The reply is one or two spoken sentences — no markdown, no URLs.
- [ ] The page shows the timing breakdown. **Screenshot it** — that is your latency evidence.
- [ ] Tighten one prompt rule, re-test, and note what changed.

---

## Lab 9 — Interactive Avatar Session (Nova, HeyGen LiveAvatar)

**Goal:** embed a *cloud* interactive avatar, and see what you trade for it.
**Flow:** `lab9/liveavatar-session-flow.json`
**Webhooks:** `POST /liveavatar-session`, `GET /liveavatar-contexts` · **Credential:** `LiveAvatar API`

n8n creates the session and returns a short-lived **embed URL** — again, the API key never reaches the
browser. Compare directly with Lab 8: Nova looks far better and costs credits; Aria is free, private
and faster. Both are defensible. Be able to say when.

### Verify

- [ ] Nova loads and holds a conversation.
- [ ] You can state one thing Lab 8 does better and one thing Lab 9 does better.

---

## Lab 10 — AI Video Generation with Gemini Veo 3 (Veo Studio)

**Goal:** one sentence in → an 8-second cinematic clip with sound.
**Flow:** `lab10/veo3-video-flow.json`
**Webhooks:** `POST /veo-generate`, `POST /veo-status`, `GET /veo-file` · **Credentials:** `Gemini API`, `Ollama local`

Same long-running shape as Lab 7 — generate, poll, fetch — plus one new idea:

**`/veo-file` is a proxy.** Google's finished video sits behind a URL that needs your API key to
download. Rather than leak that key into the page, n8n hands the browser a URL pointing back at
*itself*, fetches the MP4 server-side, and streams it through. **The key never leaves n8n.** This is
the same instinct as Lab 4's signed URL and Lab 9's embed URL — you have now met it three times.

### Verify

- [ ] `gemma4` turns your idea into a *shot* prompt (camera, lighting, motion) — not a summary.
- [ ] The clip plays in the page.
- [ ] You can explain why the page never sees the Gemini key.

---

# The security rule

**API keys live in n8n credentials. Never in browser JavaScript, Markdown, screenshots, workflow notes,
or committed JSON.**

Notice that every lab that touches a paid vendor solves this the same way — the browser is given a
*short-lived, single-purpose* token, never the key:

| Lab | What the browser gets | What it never sees |
|---|---|---|
| 4 | a signed WebSocket URL | your `xi-api-key` |
| 5 | a Vapi **public** key | your Vapi private key |
| 9 | a short-lived embed URL | your LiveAvatar key |
| 10 | a proxy URL back to n8n | your Gemini key |

If you ever find yourself pasting a secret into a web page, stop. That page is visible to everyone who
loads it.

# Evidence to keep

Create a folder outside this repository. **No API keys in it.**

```text
course-evidence/
  lab-01/ … lab-10/
  screenshots/          # executions, calendar bookings, latency panels
  workflow-exports/     # your .json, after you changed it
  transcripts/          # especially Ava's refusals (Lab 5)
  videos/               # lab 6, 7, 7-os, 10 outputs
```

For every lab, the assessable artefact is the same three things: **the workflow**, **the execution
trace that proves it ran**, and **one failure case you deliberately provoked** — the refusal, the taken
slot, the question outside the PDF. A screenshot of a happy path proves very little on its own.
