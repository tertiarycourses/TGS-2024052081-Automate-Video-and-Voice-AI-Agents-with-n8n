# Learner Guide — Automate Video and Voice AI Agents with n8n

**Tertiary Infotech Academy Pte Ltd**

This guide walks you through nine hands-on labs. The AI models run **locally and free** on your own machine using Docker, n8n, and Ollama; the voice and video layers use cloud services (Retell for voice; HeyGen / Replicate for avatar video) — with a fully free/local video option in Lab 5.5.

| Lab | What you build | Folder |
|-----|----------------|--------|
| Lab 0 | Local environment: Docker, n8n, Ollama, gemma4 | `lab0/` |
| Lab 1 | Your first AI Agent (chat) with a local Ollama model | `lab1/` |
| Lab 2 | RAG IT-Support chatbot — upload a PDF, chat over it | `lab2/` |
| Lab 3 | CX Agent with RAG for a course academy website | `lab3/` |
| Lab 4 | Voice AI booking agent (Retell) on a website | `lab4/` |
| Lab 5 | AI avatar news video — Ollama script → HeyGen video | `lab5/` |
| Lab 5.5 | Same video, 100% free & local (Ollama + Wav2Lip) | `lab5-opensource/` |
| Lab 6 | Auto-post the avatar video to YouTube | `lab6/` |
| Lab 7 | Cloud AI avatar with Replicate (Kokoro TTS → SadTalker) | `lab7/` |
| Lab 8 | Interactive (real-time) HeyGen avatar, vertical, on a website | `lab8/` |

---

# Lab 0 — Set Up Your Local Environment

You will install **Docker Desktop** (to run n8n), **Ollama** (to run AI models locally), and download the **gemma4** and **nomic-embed-text** models.

### System requirements

- 16 GB RAM recommended (gemma4 is an 8-billion-parameter model, ~9.6 GB on disk)
- ~15 GB free disk space
- Windows 10/11 (64-bit) or macOS 12+

## 0.1 Install Docker Desktop

**Windows**
1. Download Docker Desktop from <https://www.docker.com/products/docker-desktop/> and run `Docker Desktop Installer.exe`.
2. When prompted, keep **"Use WSL 2 instead of Hyper-V"** ticked (WSL 2 is installed automatically on Windows 11; on Windows 10 run `wsl --install` in PowerShell as Administrator first, then reboot).
3. Launch **Docker Desktop** and wait until the whale icon in the taskbar shows "Docker Desktop is running".

**Mac**
1. Download Docker Desktop from <https://www.docker.com/products/docker-desktop/> — pick **Apple Silicon** (M1/M2/M3/M4) or **Intel** to match your Mac (check  → About This Mac).
2. Open the `.dmg` and drag **Docker** into **Applications**, then launch it and grant the permissions it asks for.
3. Wait until the whale icon in the menu bar shows "Docker Desktop is running".

**Verify (both platforms)** — open a terminal (Windows: PowerShell, Mac: Terminal):

```bash
docker --version
docker compose version
```

Both commands should print version numbers.

## 0.2 Start n8n with Docker Compose

The `lab0/docker-compose.yml` starts n8n together with a Postgres database:

```
┌────────────────────── your computer ──────────────────────┐
│                                                           │
│   Docker Desktop                                          │
│   ┌──────────────┐        ┌──────────────┐                │
│   │     n8n      │───────▶│  Postgres 17 │                │
│   │  port 5678   │        │  (n8n data)  │                │
│   └──────┬───────┘        └──────────────┘                │
│          │  host.docker.internal:11434                    │
│          ▼                                                │
│   ┌──────────────┐                                        │
│   │    Ollama    │  gemma4 + nomic-embed-text             │
│   │  port 11434  │  (runs natively, NOT in Docker)        │
│   └──────────────┘                                        │
└───────────────────────────────────────────────────────────┘
```

In a terminal, `cd` into the `lab0` folder and start the stack:

```bash
cd lab0
docker compose up -d
```

The first run downloads the images (a few minutes). Then open **<http://localhost:5678>** in your browser and create your local **owner account** (any email/password — it stays on your machine).

> **Stop / restart later:** `docker compose stop` and `docker compose start` from the same folder. Your workflows are kept in the `postgres_data` volume.

## 0.3 Install Ollama and download the models

**Windows**
1. Download Ollama from <https://ollama.com/download/windows> and run `OllamaSetup.exe`.
2. Ollama starts automatically as a background service (llama icon in the system tray).

**Mac**
1. Download Ollama from <https://ollama.com/download/mac>, open the `.dmg` and drag **Ollama** into Applications, then launch it (llama icon appears in the menu bar).
   - Alternative with Homebrew: `brew install ollama`, then `ollama serve` (or `brew services start ollama`).

**Download the two models (both platforms)** — in PowerShell / Terminal:

```bash
ollama pull gemma4              # chat + tool-calling model, ~9.6 GB
ollama pull nomic-embed-text    # embedding model for RAG, ~274 MB
```

**Verify:**

```bash
ollama list
```

You should see `gemma4:latest` and `nomic-embed-text:latest`. Quick smoke test:

```bash
ollama run gemma4 "Say hello in one sentence."
```

## 0.4 Create the Ollama credential in n8n

⚠️ **This is the #1 gotcha of the whole course.** n8n runs **inside Docker**, so from n8n's point of view `localhost` is the *container*, not your computer. To reach Ollama you must use the special hostname `host.docker.internal`.

1. In n8n, open the left sidebar → **Credentials** (or, inside any Ollama node, click the **Credential** dropdown → *Create new credential*).
2. Click **Add credential**, search for **Ollama**, select **Ollama** (credential type `Ollama API`).
3. Fill in:

   | Field | Value |
   |---|---|
   | **Base URL** | `http://host.docker.internal:11434` |
   | **API Key** | *(leave empty — not needed for local Ollama)* |

4. Name it **`Ollama local`** and click **Save** — n8n tests the connection and should show a green "Connection tested successfully".

> ❌ If you enter `http://localhost:11434` you will get **"fetch failed"** errors when workflows run. Always use `host.docker.internal` (works on Docker Desktop for both Windows and Mac).

## 0.5 Import the lab workflows into n8n

Each lab folder contains the workflow as a `.json` file. To import one:

1. In n8n click **+ New workflow** (top right) → open the **⋯** menu (top right) → **Import from File…**
2. Choose the lab's `.json` file (e.g. `lab1/ai-agent-ollama.json`).
3. Click **Save**. If the flow has webhooks, also switch the **Active** toggle (top right) to **on**.

Import all four now, or import each at the start of its lab:

- `lab1/ai-agent-ollama.json`
- `lab2/rag-flow.json`
- `lab3/CX Agent with RAG.json`
- `lab4/retell-web-call-flow.json`

> After importing, open each **Ollama Chat Model** / **Embeddings Ollama** node once and make sure your **Ollama local** credential is selected, then Save.

---

# Lab 1 — Your First AI Agent with Ollama

**Flow:** `lab1/ai-agent-ollama.json` &nbsp;·&nbsp; **Goal:** a chat AI agent powered 100% by your local gemma4 model.

```
Chat Trigger ──▶ AI Agent ──▶ reply
                   │
        Ollama Chat Model (gemma4)
```

### Steps

1. Import `lab1/ai-agent-ollama.json` (see 0.5) and open it.
2. Double-click **Ollama Chat Model**:
   - **Credential**: select **Ollama local**.
   - **Model**: `gemma4:latest`.
3. (Optional) Double-click **AI Agent** → *Options* → add a **System Message** such as `You are a helpful AI assistant running locally via Ollama. Answer clearly and concisely.`
4. Click **Save**, then click **Open chat** (bottom of the canvas) and send:
   > *Hello! In one sentence, introduce yourself.*
5. Watch the nodes light up — the answer is generated locally; no cloud API is used.

### Checkpoint ✅

- The agent replies in the chat panel.
- In **Executions** (left sidebar) you can open the run and inspect each node's input/output.

**Try:** add a **Simple Memory** node (connect it to the AI Agent's *Memory* port), tell the bot your name, and confirm it remembers it in the next message.

---

# Lab 2 — RAG IT-Support Chatbot (PDF → Vector Store → Webhook Chatbot)

**Flow:** `lab2/rag-flow.json` &nbsp;·&nbsp; **Web page:** `lab2/index.html` &nbsp;·&nbsp; **Sample document:** `lab2/it-faq.pdf`

You build **Retrieval-Augmented Generation (RAG)**: documents are converted to embeddings and stored in a vector store; when a user asks a question, the agent retrieves the most relevant chunks and answers **only from them**.

```
UPLOAD PATH   Upload Webhook ─▶ Edit Fields ─▶ Simple Vector Store (insert)
(rag-upload)                                       ▲            ▲
                                        Embeddings Ollama   Data Loader
                                        (nomic-embed-text)

CHAT PATH     Chat Webhook ─▶ AI Agent ─▶ Respond to Webhook
(rag-chat)                     │  │  │
              Ollama Chat Model│  │  └─ knowledge_base tool (vector store, retrieve)
              (gemma4)         │  └──── Simple Memory (per sessionId)
```

### Steps

1. Import `lab2/rag-flow.json`, open every Ollama node and select the **Ollama local** credential, then **Save** and switch **Active** ON.
   - The **Upload Webhook** listens at `http://localhost:5678/webhook/rag-upload`
   - The **Chat Webhook** listens at `http://localhost:5678/webhook/rag-chat`
2. Open `lab2/index.html` by double-clicking it (it opens in your browser as a local file — no web server needed).
3. **Step 1 on the page**: the upload webhook URL is pre-filled with `http://localhost:5678/webhook/rag-upload`. Click **Test** — you should see *Connected*.
4. **Step 2**: drag **`it-faq.pdf`** into the drop zone. The page extracts the text in your browser, then click **Send to Vector Store**. n8n chunks the text, embeds each chunk with `nomic-embed-text`, and fills the in-memory vector store.
5. **Step 3**: use the **built-in IT Support chatbot** at the bottom of the page. Ask:
   > *How do I reset my password?*
   > *What is the wifi policy?*
6. The agent calls its `knowledge_base` tool, retrieves the matching chunks, and answers from the PDF only.

### Checkpoint ✅

- The chatbot quotes details that exist only in `it-faq.pdf` (e.g. the SSPR portal, the 90-day password expiry).
- Ask something *not* in the PDF — it should answer: *"I couldn't find that in the uploaded documents."*

> **Note:** the vector store is **in-memory** — restarting the n8n container empties it. Just re-upload the PDF. Each upload also **replaces** the previous content (Clear Store is on).

---

# Lab 3 — CX Agent with RAG (Cook & Bake Academy)

**Flow:** `lab3/CX Agent with RAG.json` &nbsp;·&nbsp; **Uploader:** `lab3/upload-brochures.html` &nbsp;·&nbsp; **Website:** `lab3/website/index.html` &nbsp;·&nbsp; **Knowledge:** `lab3/brochures/` (20 course brochures)

A realistic customer-experience (CX) agent embedded in a business website. Customers chat with the site widget; the agent answers from the 20 course brochures.

```
INGESTION   Brochure Upload Webhook ─▶ Split Out (20 docs) ─▶ Vector Store (insert)
            (brochure-upload)                                  ▲           ▲
                                                    Embeddings Ollama   Data Loader

CHAT        Webhook ─▶ AI Agent ─▶ Respond to Webhook ─▶ website chat widget
                        │  │  │
       Ollama Chat Model│  │  └─ course_brochures tool (vector store, retrieve)
       (gemma4)         │  └──── Simple Memory (per visitor session)
```

### Steps

1. Import `lab3/CX Agent with RAG.json`, select the **Ollama local** credential in all three Ollama nodes, **Save**, switch **Active** ON.
2. Open **`lab3/upload-brochures.html`** in your browser:
   - The webhook URL is pre-filled with `http://localhost:5678/webhook/brochure-upload`.
   - Click the drop zone, browse into `lab3/brochures/`, select **all 20 `.txt` files** (Ctrl+A / Cmd+A), and click **Upload to Vector Store**.
3. Open **`lab3/website/index.html`** — the Cook & Bake Academy site. Click the **chat bubble** (bottom right) and ask:
   > *How much is the sourdough bread course and how long does it run?*
   > *Which campus runs the sushi course?*
4. The website widget POSTs to the n8n webhook; the agent retrieves from the brochures and answers with exact fees (S$), durations and campuses.

### Checkpoint ✅

- Answers match the brochures (e.g. **Artisan Sourdough Bread Baking = S$680, 4 weeks**).
- The chat remembers context within your browser session (follow-up questions work).

> ⚠️ **Naming tip (learned the hard way):** when you rename AI *tool* nodes in n8n, avoid parentheses or other special characters — e.g. `Brochure Vector Store (Tool)` breaks tool-calling with Ollama models (the model receives an invalid tool name and returns empty responses until "Max iterations reached"). Stick to letters, numbers and spaces: `Brochure Knowledge Base`.

---

# Lab 4 — Voice AI Booking Agent (GG Hair Salon)

**Website:** `lab4/website/` (single-page HTML/CSS/JS) &nbsp;·&nbsp; **Flow:** `lab4/retell-web-call-flow.json`

Unlike Labs 1–3, this lab uses a cloud service: **Retell AI** hosts the voice agent (speech-to-text → LLM → text-to-speech over WebRTC). The website has no backend — clicking **Book by Voice** triggers the call through an **n8n flow**, which keeps your Retell API key out of the browser.

```
"Book by Voice" ─▶ n8n webhook (retell-web-call)
                     │  n8n calls Retell API with the key stored in n8n
                     ▼
   browser ◀── access_token ── Respond to Webhook
   browser ◀──── WebRTC voice session ────▶ Retell agent "Nina"
                                             │ check_availability / book_appointment
                                             ▼
                                n8n webhooks → Google Calendar
```

### Prerequisites

- A **Retell AI** account (<https://retellai.com>) — free to sign up, with trial minutes.
- Your local **n8n** running (from Lab 0) to trigger the call.

### 4.1 Build your voice agent on Retell

Retell hosts the voice agent — the part that listens (speech-to-text), thinks (an LLM), and talks back (text-to-speech). You build and configure it entirely in the Retell dashboard.

#### A. Create the account

1. Go to <https://retellai.com> and click **Sign up** (Google login works).
2. New accounts get **free trial minutes**. When they run out you'll see *"Trial over quota, please add payment"* on every call — add a card under **Billing** to continue.

#### B. Create the agent

1. In the dashboard, open the left sidebar → **Agents** → **+ Add Agent** (or **Create an Agent**).
2. Choose a starting point:
   - **Single Prompt** — simplest; one system prompt drives the whole conversation. Best for this lab.
   - **Conversation Flow** — a visual node graph for multi-step calls. More powerful, more setup.
3. Give the agent a name, e.g. **`GG Hair Salon - Nina`**.

#### C. Configure voice, model and prompt

On the agent's page:

1. **Voice** — pick a voice (e.g. *Cimo*). Click the play icon to preview it.
2. **Model** — choose the LLM that runs the conversation (e.g. GPT-4.1 / GPT-4o-mini). This is Retell's own cloud LLM — it is **not** your local Ollama (Retell's servers can't reach your machine).
3. **Welcome / Begin message** — the first thing the agent says, e.g.
   *"Thanks for calling GG Hair Salon, this is Nina! How can I help you today?"*
4. **General prompt** — paste the agent's instructions. For the salon, include the hours, the service price list, and how to book (collect service + day/time + name, then confirm). Keep replies short since it's a phone call. Example opening:

   ```
   You are Nina, the friendly AI voice receptionist for GG Hair Salon.
   Hours: Mon–Sat 8am–9pm. Every appointment is a 1-hour slot.
   Services & prices: Women's Cut $65, Men's Cut $35, Full Color $120,
   Highlights/Balayage $180, Keratin $250, Blowout $45 … (etc).
   To book: collect the service, preferred day and time, and the caller's
   name, then confirm the details back. Keep replies short and natural.
   ```
5. Click **Save**. Use the **Test** panel (microphone icon / "Test Call") on the right to talk to your agent right in the browser.

#### D. Upload files to a Knowledge Base (give the agent documents)

Instead of pasting everything into the prompt, you can upload files (menus, FAQs, policies) and let the agent retrieve from them — this is RAG, just like Labs 2–3, but hosted by Retell.

1. In the sidebar → **Knowledge Base** → **+ Create Knowledge Base**. Name it e.g. **`GG Salon Docs`**.
2. Add sources — Retell accepts several types:
   - **Upload files** — PDF, TXT, DOCX, etc. (e.g. a `services.pdf` price list, an `faq.txt`). Drag them in.
   - **Add web pages** — paste a URL and Retell crawls it.
   - **Add text** — paste raw text directly.
3. Click **Save / Create** — Retell ingests and indexes the documents (embeddings) automatically. Wait until each source shows **Ready / Completed**.
4. **Attach it to your agent:** go back to your agent → find the **Knowledge Base** setting → select **GG Salon Docs** → **Save**.
5. In the prompt, tell the agent to use it, e.g. *"Answer questions about services, prices and policies using the knowledge base."* Test again — the agent now answers from your uploaded files.

> When you update a document, re-upload it to the Knowledge Base; the agent picks up the new version after it re-indexes. One Knowledge Base can be attached to many agents.

#### E. Get your API key and Agent ID

The website triggers the agent through n8n, which needs two things from Retell:

1. **API key** — sidebar → **API Keys** → **Create API Key** (or copy the default). It starts with **`key_`**. Copy it.
   > Treat this like a password — anyone with it can make paid calls on your account. Never commit it to Git or paste it into front-end code (this is exactly why the lab keeps it inside n8n, not the browser).
2. **Agent ID** — open your agent; the **Agent ID** (`agent_…`) is shown near the top of its page. Copy it.

### 4.2 Add the Retell key to n8n as a credential

The n8n flow calls `https://api.retellai.com/v2/create-web-call`, which expects the HTTP header `Authorization: Bearer key_…`. In n8n this is stored as a **Header Auth** credential:

1. In n8n, left sidebar → **Credentials** → **Add credential**.
2. Search for and select **Header Auth**.
3. Fill in:

   | Field | Value |
   |---|---|
   | **Name** (header name) | `Authorization` |
   | **Value** | `Bearer key_xxxxxxxxxxxx` — the word `Bearer`, **one space**, then your API key |

4. Rename the credential to **`Retell API`** (click the name at the top) and **Save**.

> ⚠️ The two most common mistakes: forgetting the word `Bearer ` before the key, or having a trailing space/newline after the key. The header value must be exactly `Bearer key_…`.

### 4.3 Import and wire up the flow

1. **Import the n8n flow** `lab4/retell-web-call-flow.json` (see 0.5). It has three nodes:
   `Webhook (retell-web-call)` → `Create Retell Web Call (HTTP Request)` → `Respond to Webhook`.
2. Open the **Create Retell Web Call** node:
   - **Authentication** is set to *Generic Credential Type → Header Auth* — select your **Retell API** credential in the dropdown.
   - In the **JSON body**, replace the default `agent_id` with **your** Agent ID from step 4.1E.
3. **Save** and switch the workflow **Active** ON.
4. **Test it** (optional) — in a terminal:

   ```bash
   curl -X POST http://localhost:5678/webhook/retell-web-call
   ```

   A working setup returns JSON containing an `access_token`. If you get `"Trial over quota, please add payment."` the key works but the Retell account needs credits.

### 4.4 Run the website

The website is **voice only** — click **Book by Voice** to talk to Nina.

**⚠️ You must open the site through `http://localhost`, not by double-clicking `index.html`.** See *"Why localhost?"* below for the reason. Two ways to start it:

**Option A — one-click launcher (easiest)**

In `lab4/website/`, double-click:
- **`start.command`** on **Mac** (the first time: right-click → Open, to get past Gatekeeper)
- **`start.bat`** on **Windows**

A terminal window opens, serves the site, and launches your browser automatically. Keep that window open while you use the site; close it (or press Ctrl+C) to stop.

**Option B — start a server yourself** (any one of these; they all just serve the folder over `http://localhost`)

| You have… | Command (run inside `lab4/website/`) | Opens at |
|---|---|---|
| **VS Code** | Install the **Live Server** extension, then right-click `index.html` → **Open with Live Server** (no terminal, no Python) | `http://localhost:5500` |
| **Node.js** | `npx serve` &nbsp;(or `npx http-server -p 8090`) | shown in the terminal |
| **Python** | `python3 -m http.server 8090` &nbsp;(Windows: `python -m http.server 8090`) | `http://localhost:8090` |
| **PHP** | `php -S localhost:8090` | `http://localhost:8090` |

Then open the URL it prints. Any of these works — pick whichever you already have installed.

**Use it:** click **Book by Voice**, allow microphone access when the browser asks, and talk to **Nina** — ask about services or book an appointment. The page calls the n8n webhook → n8n creates the Retell web call → the WebRTC voice session starts. During the call the Retell agent can invoke its `check_availability` / `book_appointment` tools (n8n webhooks writing to Google Calendar).

### Why localhost? (and why `file://` won't work)

Opening `index.html` directly (so the address bar shows `file:///…`) leaves the page dead — buttons do nothing. Two browser rules are the reason:

1. **JavaScript modules are blocked on `file://`.** The page loads its code with `<script type="module">`, and browsers refuse to load module scripts from a `file://` origin (a CORS restriction). So `main.js` never runs and no button is wired up. (When this happens the page shows a red warning banner reminding you to use `http://localhost:8090`.)
2. **The microphone needs a "secure context."** A voice call needs mic access (`getUserMedia`), which browsers only grant on a secure origin: `https://…` or **`http://localhost`**. `file://` is not trusted for the mic, so even if the code ran, the call couldn't start.

`http://localhost` satisfies both — it's a real HTTP origin *and* it's treated as secure — with no HTTPS certificate needed. That's why every browser-based voice/mic app is served over localhost during development.

### Checkpoint ✅

- The site opens at `http://localhost:8090` with images and services.
- Clicking **Book by Voice** shows the call modal, connects, and Nina responds to your voice.

### Known limitations (read before troubleshooting!)

- **Retell trial quota:** if the call fails with *"Trial over quota, please add payment"*, the Retell account has used up its free minutes — add a payment method in the Retell dashboard, or use a fresh trial account and update the **Retell API** credential in n8n (4.2) and the `agent_id` in the flow (4.3).
- **Booking tools:** the Retell agent's `check_availability` / `book_appointment` tools are webhooks that must point to a **publicly reachable** n8n (Retell's cloud cannot call your `localhost`). Build those flows on a hosted n8n or a tunnel (ngrok / Cloudflare) and set the tool URLs in the Retell dashboard → your agent → **Tools**. Without them the conversation still works; only live availability/booking replies fail.
- The Retell **voice LLM runs in Retell's cloud** (e.g. GPT-4.1) — it cannot use your local Ollama, because Retell's servers can't reach your machine. (Labs 1–3 are where the local Ollama models are used.)

---

# Lab 5 — AI Avatar News Video (Ollama script → HeyGen)

**Website:** `lab5/website/` &nbsp;·&nbsp; **Flow:** `lab5/heygen-news-avatar-flow.json` &nbsp;·&nbsp; **Anchor photo:** `lab5/newsbroadcaster.png`

You turn a **news topic** into a talking-head video: **Ollama** writes a short anchor script, then **HeyGen** animates a still photo of a news anchor speaking it (rendered in YouTube 1920×1080). n8n orchestrates both.

```
POST /webhook/heygen-generate {topic}
   → Write Script (Ollama gemma4)  → ~20-second anchor script
   → HeyGen: Create Video (HTTP)   → returns video_id (1920×1080)
   → Respond { video_id, script }

POST /webhook/heygen-status {video_id}
   → HeyGen: Get Status (HTTP)      → status + video_url when done
   → Respond { status, video_url }

Website: enter topic → generate → poll status → play the finished video
```

### Prerequisites

- A **HeyGen** account (<https://heygen.com>) and its **API key** (dashboard → **Settings → API**). It looks like `sk_…` / a long token.
- **⚠️ HeyGen API rendering needs paid *API credits*.** Free-plan credits are for the HeyGen web studio, not the API — an API render with no API credits fails with *"Insufficient credit. This operation requires 'api' credits."* Everything up to the render still works (script + job submission); add API credits (dashboard → **Subscriptions / API**) to get the finished MP4.

### 5.1 Upload the anchor photo as a HeyGen "Talking Photo"

HeyGen animates a still image via a **talking_photo_id**. Upload the anchor image once (any clear front-facing photo works):

```bash
curl -X POST https://upload.heygen.com/v1/talking_photo \
  -H "X-Api-Key: YOUR_HEYGEN_KEY" \
  -H "Content-Type: image/jpeg" \
  --data-binary "@lab5/website/broadcaster.jpg"
```

Copy the returned `talking_photo_id`. (The provided flow already uses one; replace it with yours to use a different face.)

### 5.2 Add the HeyGen key to n8n

HeyGen authenticates with the header `X-Api-Key: <key>` — store it as a **Header Auth** credential (same idea as Lab 4):

1. n8n → **Credentials** → **Add credential** → **Header Auth**.
2. **Name:** `X-Api-Key` &nbsp; **Value:** your HeyGen key (no "Bearer" prefix here).
3. Rename it **`HeyGen API`** and **Save**.

### 5.3 Import and wire the flow

1. Import `lab5/heygen-news-avatar-flow.json`. Nodes:
   `Generate Webhook → Write Script (Ollama) → HeyGen: Create Video → Respond` and `Status Webhook → HeyGen: Get Status → Respond`.
2. In **Write Script (Ollama)** make sure the **Ollama Chat Model** uses your **Ollama local** credential (Lab 0).
3. In **HeyGen: Create Video** and **HeyGen: Get Status**, select the **HeyGen API** credential. In *Create Video*, set the `talking_photo_id` (5.1) and, if you like, a different `voice_id` (list voices: `GET https://api.heygen.com/v2/voices`). The dimension is `1920×1080` (YouTube).
4. **Save** and switch **Active** ON.

### 5.4 Run the website

Serve `lab5/website/` (double-click **`start.command`** / **`start.bat`**, or `python3 -m http.server 8095`) and open **http://localhost:8095**. Enter a topic (a FIFA 2026 example is pre-filled) and click **Generate News Video**:

- The teleprompter fills with the **Ollama-written** script.
- The status pill shows **Rendering…**, then plays the finished video when HeyGen completes.
- With no API credits it shows **No API credits** and explains how to add them — the script is still produced.

> **Checkpoint ✅** — the script is written by local Ollama, HeyGen returns a `video_id`, and (with API credits) the 1080p anchor video plays in the page.

### 5.5 Free / open-source variant (no cloud, no credits) — `lab5-opensource/`

HeyGen renders in the cloud and needs paid API credits. You can render the **same kind of video 100% locally and free** by swapping the "camera": Ollama still writes the script, but a **local render service** turns it into a lip-synced 1080p video on your machine. The n8n flow shape is identical — only the HTTP target changes.

```
Website → n8n (os-generate) → Ollama script → HTTP → local render service (:8099)
                                                        • macOS `say`  → speech (TTS)
                                                        • Wav2Lip      → lip-synced mouth
                                                        • ffmpeg       → 1920×1080
                                                → play the video
```

**Open-source pieces used:**
- **TTS (built-in, no install):** the render service auto-picks the OS voice — **macOS** `say`, **Windows** PowerShell *System.Speech* (SAPI), **Linux** `espeak-ng`. For a nicer cross-platform voice, install open-source **Piper**.
- **Talking head (lip-sync):** **Wav2Lip** — animates the anchor photo's mouth to the audio. (Alternatives: **SadTalker**, **MuseTalk** for higher quality; all free.)
- **Video muxing / scaling:** **ffmpeg**.

**One-time setup** (both platforms) — create the Wav2Lip environment inside `lab5-opensource/service/` (details in that folder's `README.md`):

```bash
cd lab5-opensource/service
uv venv --python 3.11 .venv
# install deps into the venv, then:
git clone https://github.com/Rudrabha/Wav2Lip.git wav2lip
#   wav2lip/checkpoints/wav2lip_gan.pth              (~416 MB)
#   wav2lip/face_detection/detection/sfd/s3fd.pth    (~86 MB)
```
The service auto-detects the venv path (`.venv/bin/python` on Mac/Linux, `.venv\Scripts\python.exe` on Windows).

**Run it:**
1. Import `lab5-opensource/os-news-avatar-flow.json` into n8n (uses the **Ollama local** credential) and set **Active**.
2. Start the render service **and** the website:
   - **Mac:** double-click `lab5-opensource/start.command`
   - **Windows:** double-click `lab5-opensource/start.bat`
   - **Or manually** (two terminals):

     | | macOS / Linux | Windows |
     |---|---|---|
     | Render service | `cd lab5-opensource/service && python3 render_service.py` | `cd lab5-opensource\service && python render_service.py` |
     | Website | `cd lab5-opensource/website && python3 -m http.server 8096` | `cd lab5-opensource\website && python -m http.server 8096` |
3. Open **http://localhost:8096**, enter a topic, click **Generate**. Ollama writes the script; the local service renders a **lip-synced** 1080p video in ~30–60s — no account, no API key, no credits.

> **Windows note:** the mic-free TTS uses the voices already built into Windows (Control Panel → *Speech Recognition* → *Text to Speech* lists them). `ffmpeg` must be on your `PATH` (install via `winget install Gyan.FFmpeg` or `choco install ffmpeg`). Wav2Lip runs fine on Windows CPU, and much faster on an NVIDIA GPU.

> The service auto-selects its engine: **`wav2lip`** (real lip-sync) when the Wav2Lip model + face detector are installed, otherwise a **`kenburns`** fallback (zoom + narration, no mouth movement). The n8n flow is renderer-agnostic — to use SadTalker/MuseTalk or a cheap hosted API (e.g. Replicate SadTalker) instead, change only `render_service.py`.

> **No GPU needed here** — Wav2Lip runs on the Apple-Silicon CPU/MPS in about real-time for short clips. Heavier models (SadTalker, Hallo2) look better but want a proper GPU.

---

# Lab 6 — Auto-Post the Video to YouTube

**Goal:** extend the Lab 5 flow so a finished HeyGen video is **uploaded to YouTube automatically** — no manual download/upload.

n8n has a built-in **YouTube** node that calls the YouTube Data API v3. You add three things to the end of Lab 5: **download the MP4 → upload to YouTube → (optional) confirm**.

### 6.1 Enable the YouTube Data API (one-time Google setup)

1. Go to the **Google Cloud Console** (<https://console.cloud.google.com>) and create (or pick) a project.
2. **APIs & Services → Library →** search **YouTube Data API v3 → Enable**.
3. **APIs & Services → OAuth consent screen:** set it up (External is fine for testing), and under **Test users** add the Google account that owns the YouTube channel.
4. **APIs & Services → Credentials → Create credentials → OAuth client ID → Web application.**
   - Add this **Authorized redirect URI** (n8n shows the exact one on the credential screen): `http://localhost:5678/rest/oauth2-credential/callback`
   - Copy the **Client ID** and **Client secret**.

### 6.2 Create the YouTube (OAuth2) credential in n8n

1. n8n → **Credentials → Add credential → YouTube OAuth2 API**.
2. Paste the **Client ID** and **Client secret** from 6.1.
3. Click **Sign in with Google**, choose the channel's account, and grant access. n8n stores the token.

### 6.3 Extend the flow

Open the Lab 5 flow (or a copy) and, on the branch that runs **after the video is `completed`** (i.e. once `HeyGen: Get Status` returns `status = completed` with a `video_url`), add:

1. **IF** node — continue only when `{{ $json.status }}` equals `completed` (so you upload only finished renders).
2. **HTTP Request** node — **GET** the `video_url`, and set **Response → Response Format = File** (this puts the MP4 into the item's **binary** data).
3. **YouTube** node — **Resource: Video → Operation: Upload**:
   - **Binary Property:** `data` (the download from the previous node)
   - **Title:** e.g. `={{ 'FIFA 2026 Update — ' + $now.format('yyyy-LL-dd') }}`
   - **Description:** `={{ $('Write Script (Ollama)').item.json.output }}` (reuse the anchor script!)
   - **Region/Category:** e.g. *News & Politics*; **Tags:** `FIFA, World Cup 2026, AI news`
   - **Privacy:** start with **unlisted** or **private** while testing, then **public**.
   - Credential: the **YouTube OAuth2** from 6.2.
4. (Optional) **Respond to Webhook / Set** node to return the new YouTube video URL (`https://youtu.be/{{ $json.id }}`).

```
… HeyGen: Get Status ──▶ IF status = completed ──▶ HTTP GET video_url (as File)
                                                    ──▶ YouTube: Upload video ──▶ YouTube URL
```

### 6.4 Automate the trigger (optional)

To make it fully hands-off, replace the manual webhook trigger with a **Schedule Trigger** (e.g. every morning): Schedule → Ollama writes a fresh script from a daily topic → HeyGen renders → **Wait** (or poll) until completed → YouTube upload. You now have a **daily AI news channel** running from n8n.

> **Notes**
> - The first upload opens the Google consent popup once; after that it's automatic.
> - YouTube's API has a daily upload quota — fine for a few videos/day.
> - HeyGen API credits are still required for the render (Lab 5).

---

# Lab 7 — Cloud AI Avatar with Replicate (Kokoro TTS → SadTalker)

**Website:** `lab7/website/` &nbsp;·&nbsp; **Flow:** `lab7/replicate-avatar-flow.json`

Lab 5 used HeyGen; Lab 5.5 ran everything locally. **Lab 7 renders in the cloud on [Replicate](https://replicate.com)** — which hosts thousands of open-source models and bills per second (no GPU of your own, no HeyGen plan). Ollama still writes the script; Replicate runs **Kokoro** (TTS) then **SadTalker** (talking head).

```
POST /webhook/replicate-generate {topic}
   → Write Script (Ollama gemma4)
   → Replicate: Kokoro TTS      (text → speech URL)      [Prefer: wait]
   → Replicate: SadTalker create (photo + speech → video prediction)
   → Respond { prediction_id, script }

POST /webhook/replicate-status {prediction_id}
   → Replicate: Get prediction  → { status, video_url }

Website: enter topic → generate → poll status → play the video
```

### 7.1 Get your Replicate token and add credit

1. Sign up at <https://replicate.com> → **Account → API tokens** → copy the token (starts with `r8_`).
2. **⚠️ Replicate requires purchased credit.** With none you'll get `402 Insufficient credit` on every run — add a card at **replicate.com/account/billing**. Predictions are cheap (SadTalker ≈ a few cents per short clip). Everything up to the render (the Ollama script) still works without credit.

### 7.2 Add the token to n8n

Store it as a **Header Auth** credential named **`Replicate API`** — **Name:** `Authorization`, **Value:** `Bearer r8_…` (note the `Bearer ` prefix, unlike HeyGen's `X-Api-Key`).

### 7.3 Import the flow and run

1. Import `lab7/replicate-avatar-flow.json`, select the **Ollama local** and **Replicate API** credentials, set **Active**.
2. The `source_image` in the *SadTalker* node points at the anchor photo on GitHub (`raw.githubusercontent.com/.../lab7/website/broadcaster.jpg`) so Replicate's cloud can fetch it — change it to any public image URL to use a different face.
3. Serve `lab7/website/` (`python3 -m http.server 8097`) → open **http://localhost:8097** → enter a topic → **Generate**. Ollama writes the script; Replicate renders; the video plays when the prediction succeeds.

> **Model versions** are pinned in the flow (Kokoro `f559560e…`, SadTalker `a519cc0c…`). Swap to any other Replicate talking-head model (e.g. `devxpy/cog-wav2lip`, `zsxkib/hallo`) by changing the `version` and `input` fields — the flow shape stays the same.

> **Checkpoint ✅** — the script comes from local Ollama, Replicate returns a `prediction_id`, and (with credit) the SadTalker video plays in the page.

---

# Lab 8 — Interactive (Real-Time) HeyGen Avatar — Vertical

**Website:** `lab8/website/`

Labs 4–7 are *one-way* (you send input, you get output). An **Interactive Avatar** is *two-way*: a live, streaming avatar you **talk to** and it answers in real time (WebRTC video), like a video call with an AI — shown here in **vertical (9:16)** format for phones and social. See HeyGen's overview: <https://www.heygen.com/blog/interactive-ai-avatar>.

> **Heads-up on the API:** HeyGen's classic *Streaming Avatar* API (`/v1/streaming.*`) is **being sunset** and has moved to the new **LiveAvatar API** (<https://docs.liveavatar.com>). Interactive/streaming avatars also require a HeyGen plan with **streaming/API credits**. The two routes below reflect this.

### Option A — Embed a shared Interactive Avatar (no code, works today)

The fastest way to put a talking, listening avatar on a page:

1. Open HeyGen → **Interactive Avatar** (<https://labs.heygen.com/interactive-avatar>).
2. Pick an avatar and (optionally) give it a **Knowledge Base** or connect an LLM so it answers about your topic.
3. Click **Share / Embed** and copy the link (or `<iframe>` embed code).
4. Open `lab8/website/` (serve it over `http://localhost` — see Lab 4's *Why localhost?*), paste the share URL into the field, and click **Load Avatar**. The avatar is embedded in the page's **9:16 vertical frame**; allow the microphone and start talking.

This is what `lab8/website/index.html` does — it drops your HeyGen share URL into a vertical `<iframe>`, so the avatar (video, mic, and its LLM) all run on HeyGen while it's embedded in your site.

### Option B — Drive it yourself with n8n + the LiveAvatar SDK (advanced)

For a fully custom widget (your own UI, and answers powered by **local Ollama**), the shape mirrors Lab 4's token pattern:

1. **n8n mints a session token** — a webhook → HTTP Request to the LiveAvatar "create session token" endpoint (auth `X-Api-Key: <HeyGen key>`) → returns the short-lived token to the browser. This keeps the API key out of the front-end (exactly like the Retell token in Lab 4).
2. **Browser starts the avatar** — load the LiveAvatar / Streaming-Avatar SDK (from its CDN), call `createStartAvatar({ token, avatarName })`, and attach the returned media stream to a `<video>` element for live WebRTC playback.
3. **Make it answer with Ollama** — when the user speaks/types, send the text to an **n8n chat webhook** that runs the **Ollama AI Agent** (as in Labs 1–3), get the reply, then tell the avatar to say it (`avatar.speak({ text })`). Now the *brain* is your local model and the *face/voice* is HeyGen.

```
browser ──▶ n8n webhook (mint token) ──▶ LiveAvatar API ──▶ token
browser ──▶ LiveAvatar SDK (WebRTC) ──▶ live avatar video/audio
user text ─▶ n8n webhook (Ollama) ──▶ reply ─▶ avatar.speak(reply)
```

> Follow the current endpoint names and SDK version from the LiveAvatar docs (the classic `streaming.create_token` endpoint returns an `endpoint_sunset` notice). Both options need HeyGen streaming credits to actually connect.

---

# Troubleshooting Cheat-Sheet

| Symptom | Cause | Fix |
|---|---|---|
| `fetch failed` on any Ollama node | Credential uses `localhost` | Base URL must be `http://host.docker.internal:11434` |
| *"Workflow could not be published"* with a Telegram trigger | Telegram needs a **public HTTPS** webhook; local n8n has none | Use a Chat Trigger / Webhook instead, or expose n8n with a tunnel (ngrok / Cloudflare) and set `WEBHOOK_URL` |
| Agent replies empty, then *"Max iterations (10) reached"* | AI tool node name contains `(` `)` or other special characters | Rename tool nodes to plain names (letters/numbers/spaces only) |
| Chatbot says it can't find anything after n8n restart | In-memory vector store was cleared | Re-upload the PDF / brochures |
| Lab 4 site is blank / buttons do nothing | Opened as `file://` — module script blocked | Serve over `http://localhost` (launcher, Live Server, or `npx serve`) — never double-click the HTML |
| Lab 4 "Book by Voice" won't access the microphone | Page not on a secure origin | Use `http://localhost` (it's a secure context); `file://` is not trusted for the mic |
| Lab 4 port 8090 already in use | Another app uses the port | Use any other port, e.g. `python3 -m http.server 8091` or `npx serve -l 8091` |
| Ollama credential test fails | Ollama not running | Start the Ollama app (tray/menu-bar icon), check `ollama list` works |
| Lab 5/7 HeyGen render fails: *"Insufficient credit… requires 'api' credits"* | Account has no **API** credits (free credits are studio-only) | Add API credits in HeyGen → **Subscriptions / API**; the Ollama script still works without them |
| Lab 7 `streaming.create_token` returns `endpoint_sunset` | Classic Streaming Avatar API retired | Use the new **LiveAvatar API** (docs.liveavatar.com), or embed a shared Interactive Avatar (Lab 7 Option A) |
| Lab 6 YouTube node "unauthorized" / no channel | OAuth consent not completed or wrong account | Re-run **Sign in with Google** on the YouTube OAuth2 credential; add your account under **Test users** in the Google consent screen |
| Lab 7 Replicate returns `402 Insufficient credit` | Replicate account has no credit | Add a card at **replicate.com/account/billing**; the Ollama script still works without it |
| Lab 7 SadTalker can't read the image | `source_image` URL not publicly reachable | Use a public URL (e.g. the GitHub raw link) — Replicate's cloud can't fetch `localhost` |
| Model download very slow / disk full | gemma4 is ~9.6 GB | Free up space; models live in `~/.ollama/models` (Mac) / `C:\Users\<you>\.ollama\models` (Windows) |

---

*© Tertiary Infotech Academy Pte Ltd — TGS-2024052081 Automate Video and Voice AI Agents with n8n*
