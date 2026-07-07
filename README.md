# Automate Video and Voice AI Agents with n8n

**WSQ course · Tertiary Infotech Academy Pte Ltd**

Hands-on courseware for building **AI agents, voice agents, and AI avatar videos** with [n8n](https://n8n.io), local LLMs via [Ollama](https://ollama.com), and cloud AI services. The AI "brain" runs **locally and free** on your machine (Docker + n8n + Ollama/gemma4); the voice and video layers use cloud services (Retell, HeyGen, Replicate) — with a **100% free/local video option** too.

> 🎓 **Register for this course:** [Build a Human–AI Workforce with Autonomous AI Agents](https://www.tertiarycourses.com.sg/wsq-build-a-human-ai-workforce-with-autonomous-ai-agents.html) — **Course Code TGS-2024043854** (WSQ, SkillsFuture-claimable), Tertiary Infotech Academy.

📘 **Start here: [LEARNER_GUIDE.md](LEARNER_GUIDE.md)** — step-by-step, Windows + macOS.

## Labs

| Lab | What you build | Folder |
|-----|----------------|--------|
| 0 | Local environment: Docker, n8n, Ollama, gemma4 | [`lab0/`](lab0/) |
| 1 | Your first AI Agent (chat) with a local Ollama model | [`lab1/`](lab1/) |
| 2 | RAG IT-Support chatbot — upload a PDF, chat over it | [`lab2/`](lab2/) |
| 3 | CX Agent with RAG for a course-academy website | [`lab3/`](lab3/) |
| 4 | Voice AI booking agent (Retell) on a website | [`lab4/`](lab4/) |
| 5 | AI avatar news video — Ollama script → HeyGen video | [`lab5/`](lab5/) |
| 5.5 | Same video, **100% free & local** (Ollama + Wav2Lip) | [`lab5-opensource/`](lab5-opensource/) |
| 6 | Auto-post the avatar video to YouTube | [`lab6/`](lab6/) |
| 7 | Cloud AI avatar with Replicate (Kokoro TTS → SadTalker) | [`lab7/`](lab7/) |
| 8 | Interactive (real-time) HeyGen avatar, vertical, on a website | [`lab8/`](lab8/) |

## What each lab teaches

- **Local AI agents & RAG (Labs 1–3):** AI Agent nodes, the Ollama chat model, in-memory vector stores, embeddings (`nomic-embed-text`), and tool-calling — a chatbot that answers only from your uploaded documents.
- **Voice agent (Lab 4):** a browser voice call, minted through an n8n webhook so the Retell API key never touches the front-end.
- **AI avatar video (Labs 5–7):** Ollama writes a news script; the video is rendered by **HeyGen** (cloud), **Wav2Lip** (free/local), or **Replicate** (cloud, pay-per-second) — all driven by the same n8n flow shape.
- **Publishing & interactivity (Labs 6, 8):** auto-upload to **YouTube** from n8n, and embed a real-time, two-way **interactive avatar**.

## Quick start

1. Install **Docker Desktop** and **Ollama**; pull the models:
   ```bash
   ollama pull gemma4
   ollama pull nomic-embed-text
   ```
2. Start n8n:
   ```bash
   cd lab0 && docker compose up -d      # n8n at http://localhost:5678
   ```
3. In n8n, create the **Ollama** credential with Base URL `http://host.docker.internal:11434` (⚠️ not `localhost` — n8n runs in Docker).
4. Import each lab's workflow JSON and follow **[LEARNER_GUIDE.md](LEARNER_GUIDE.md)**.

> Full setup (Windows + macOS), the "why localhost?" explanation, per-lab steps, and a troubleshooting cheat-sheet are all in the Learner Guide.

## Tech stack

- **Orchestration:** n8n (self-hosted, Docker + Postgres)
- **Local LLM:** Ollama — `gemma4` (chat + tools), `nomic-embed-text` (embeddings)
- **Voice:** Retell AI (WebRTC)
- **Avatar video:** HeyGen · Replicate (Kokoro TTS, SadTalker) · Wav2Lip (free/local) · ffmpeg
- **Publishing:** YouTube Data API v3
- **Web:** plain HTML/CSS/JS lab front-ends

## Repository layout

```
lab0..lab8/            # one folder per lab (workflow JSON + website where applicable)
lab5-opensource/       # free/local video pipeline (render service + n8n flow + website)
LEARNER_GUIDE.md       # the full step-by-step guide
.claude/               # WSQ courseware tooling (skills, agents, hooks)
```

Cloud services (Retell, HeyGen, Replicate) each require the learner's own account and credit; the flows are built to work the moment credit is added. API keys live in a local `.env` (git-ignored) and inside n8n credentials — never in the pushed code.

---

Powered by [Tertiary Infotech Academy Pte Ltd](https://www.tertiaryinfotech.com/)
