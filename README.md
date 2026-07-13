# Automate Video and Voice AI Agents with n8n

**WSQ course TGS-2024052081 — Tertiary Infotech Academy Pte Ltd**

Courseware for building chatbots, RAG assistants, voice agents and AI avatar/video automations with
**n8n**. Every lab is runnable: a real n8n workflow plus, where it applies, a real web front end.

## Two lab trees — pick one and stay in it

The same ten labs ship twice. They are **not** interchangeable halfway through: the model, the
credential and the webhook base all differ.

| | [`labs_local_n8n/`](labs_local_n8n/) | [`labs_remote_n8n/`](labs_remote_n8n/) |
|---|---|---|
| **n8n** | your own Docker stack ([`lab0/`](labs_local_n8n/lab0/)) | `n8n.tertiarytraining.com` (hosted) |
| **Chat model** | Ollama `gemma4:latest` | OpenAI `gpt-4.1-mini` |
| **Embeddings** | Ollama `nomic-embed-text:latest` | OpenAI `text-embedding-3-small` |
| **n8n credential** | `Ollama local` | `OpenAI account` |
| **Webhook base** | `http://localhost:5678/webhook` | `https://n8n.tertiarytraining.com/webhook` |
| **Runs offline?** | Yes — no API bill, no data leaves your laptop | No |
| **Needs ngrok?** | Yes, when a vendor's servers must call in | **No** — already public |
| **Docker setup** | [`lab0/`](labs_local_n8n/lab0/) | not applicable |

**Local** is the default for the classroom: free, private, and nothing to bill. **Remote** exists for
learners who cannot run Docker, and it removes the single most fragile part of the voice labs — the
ngrok tunnel — because the hosted n8n is already reachable from ElevenLabs and Vapi.

## Learner guides

- [`LEARNER_GUIDE_LOCAL.md`](LEARNER_GUIDE_LOCAL.md) — the Docker/Ollama build. **Includes the
  `docker compose pull` / `docker compose up -d` setup.**
- [`LEARNER_GUIDE_CLOUD.md`](LEARNER_GUIDE_CLOUD.md) — the hosted/OpenAI build. **No Docker.**

## The three topics

| Topic | Theme | Labs |
|---|---|---|
| **1** | **Chatbot** — agents, RAG and grounded answers | Lab 1, Lab 2, Lab 3 |
| **2** | **Voice Agent** — telephony-grade agents that call real tools | Lab 4, Lab 5 |
| **3** | **Video Agent** — lip-sync, avatars and text-to-video | Lab 6 – Lab 10 |

## The ten labs

| Lab | Title | What you build | Key vendor |
|---|---|---|---|
| **0** | Set up n8n locally | Docker + n8n + Postgres + Ollama | *(local tree only)* |
| **1** | AI Agent | Your first n8n AI agent | Ollama / OpenAI |
| **2** | RAG IT Support Chatbot | PDF → embeddings → grounded answers | Ollama / OpenAI |
| **3** | CX Agent with RAG | A customer-facing agent over a brochure knowledge base | Ollama / OpenAI |
| **4** | Voice Booking Agent | Nina books into a real Google Calendar, by voice | **ElevenLabs** |
| **5** | Grounded FAQ Voice Agent | Ava, a prescription-refill assistant that refuses medical advice | **Vapi** |
| **6** | Lip-Sync Face-Off | Digital Human Studio: the same script and portrait through MuseTalk (local) and HeyGen (cloud) | *(local Python)* + **HeyGen** |
| **7** | Avatar News Video | A script agent that drives an avatar presenter | **HeyGen** |
| **7-os** | Avatar News Video, open-source | The same video, rendered on your own machine | *(local Python)* |
| **8** | Interactive Avatar Brain | A low-latency talking avatar in the browser | Ollama / OpenAI |
| **9** | Interactive Avatar Session | An embedded interactive avatar | **LiveAvatar** |
| **10** | AI Video Generation | Idea → shot script → 8-second cinematic clip | **Gemini Veo 3** |

## The lab web apps must be *served*, never opened off the disk

Labs that ship a web front end (notably [Lab 6](labs_local_n8n/lab6/) and
[Lab 7-os](labs_local_n8n/lab7-opensource/)) start with a double-clickable launcher:

| macOS | Windows |
|---|---|
| **`start.command`** | **`start.bat`** |

Each one starts the local server and opens your browser on the right port (Lab 6 → `http://localhost:8137`).

> ⚠️ **Do not double-click `index.html`.** On a `file://` URL the page still paints — images even
> load — but the browser blocks `fetch()`, so sample assets and renderers fail with misleading
> errors (in Lab 6: *"Could not load that sample."*). Always go through the launcher.

## Quick start — local tree

```bash
cd labs_local_n8n/lab0
docker compose pull
docker compose up -d
ollama pull gemma4
ollama pull nomic-embed-text
```

Open n8n at `http://localhost:5678`, create the owner account, and add an **Ollama** credential with
the base URL:

```text
http://host.docker.internal:11434
```

Not `localhost:11434` — n8n runs *inside* a container, where `localhost` means the container itself.
Full walkthrough: [`labs_local_n8n/lab0/LEARNER-GUIDE.md`](labs_local_n8n/lab0/LEARNER-GUIDE.md).

## Quick start — remote tree

No install. Import the flow for the lab into `n8n.tertiarytraining.com`, attach the **OpenAI account**
credential, set the workflow **Active**, and open the lab's website.

## Courseware deliverables

- [PowerPoint deck](courseware/Automate-Video-and-Voice-AI-Agents-with-n8n-v3.0.pptx)
- [Learner Guide DOCX](courseware/LG-Automate-Video-and-Voice-AI-Agents-with-n8n.docx) ·
  [Markdown](courseware/LG-Automate-Video-and-Voice-AI-Agents-with-n8n.md)
- [Lesson Plan DOCX](courseware/LP-Automate-Video-and-Voice-AI-Agents-with-n8n.docx) ·
  [Markdown](courseware/LP-Automate-Video-and-Voice-AI-Agents-with-n8n.md)

> **Note:** the generated deck, Lesson Plan and Learner Guide in `courseware/` are still the **v3.0
> six-topic** build produced by [`scripts/generate_agentic_courseware.py`](scripts/generate_agentic_courseware.py).
> They have **not yet been realigned** to the three-topic structure above. Regenerating them is the next
> change to this repo.

## A workflow will not run until it is Active

A production `/webhook/…` path does not exist in n8n until the workflow is switched **Active**. An
inactive workflow returns `404` and the lab's website will report that it cannot reach n8n. This is
the single most common failure in class.

## Security rule

API keys belong in n8n credentials or a local `.env` (which is gitignored). They must never appear in
browser JavaScript, Markdown examples, screenshots, workflow notes, or committed JSON. The lab websites
are built so the browser only ever receives short-lived tokens — never a vendor key.
