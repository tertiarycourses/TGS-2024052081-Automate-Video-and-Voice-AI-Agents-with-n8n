# Learner Guide — Cloud Build

> **This is the CLOUD build.** No Docker, no Ollama, nothing to install. You use the hosted n8n at
> **`n8n.tertiarytraining.com`** and OpenAI models. Labs live in [`labs_remote_n8n/`](labs_remote_n8n/).
>
> For the local build — n8n in Docker, models on your own machine, free and offline — see
> [`LEARNER_GUIDE_LOCAL.md`](LEARNER_GUIDE_LOCAL.md). **The Docker setup lives there, not here.**

## What is different in this build

| | Local build | **Cloud build (this one)** |
|---|---|---|
| n8n | Docker on your laptop | **`n8n.tertiarytraining.com`** |
| Chat model | Ollama `gemma4:latest` | **OpenAI `gpt-4.1-mini`** |
| Embeddings | Ollama `nomic-embed-text:latest` | **OpenAI `text-embedding-3-small`** |
| n8n credential | `Ollama local` | **`OpenAI account`** |
| Webhook base | `http://localhost:5678/webhook` | **`https://n8n.tertiarytraining.com/webhook`** |
| Cost | free | metered against your OpenAI key |
| Install time | ~45 min | **none** |
| **ngrok tunnel** | required for the voice labs | **never required** |

That last row is the reason this build exists. In the local build, ElevenLabs and Vapi have to call
*into* your laptop, which they cannot do — so you run an ngrok tunnel, and the URL changes every time
it restarts. The hosted n8n is already on the public internet, so those vendors reach it directly.
The single most fragile step in the voice labs simply disappears.

## Setup — the whole thing

1. Sign in to **`https://n8n.tertiarytraining.com`**.
2. Create one credential named **`OpenAI account`** (Credentials → Add → OpenAI) and paste your
   OpenAI API key. Every lab's chat and embedding nodes already point at this name.
3. For each lab: **Import from File** the flow in `labs_remote_n8n/labN/`, then set the workflow
   **Active**.
4. Open the lab's `website/` folder and serve it:

   ```bash
   cd labs_remote_n8n/lab4/website
   python3 -m http.server 8090      # Windows: python -m http.server 8090
   ```

   Open `http://localhost:8090`. Do **not** double-click the HTML file — `file://` blocks both ES
   modules and the microphone, and every button dies silently.

The websites already point at `https://n8n.tertiarytraining.com/webhook/…`. There is nothing to paste.

### About n8n's free OpenAI credits

n8n gives **100 free OpenAI credits** to new sign-ups, but they are an **n8n Cloud** perk — they appear
as a ready-made credential inside a new *n8n Cloud* account. `n8n.tertiarytraining.com` is **self-hosted**,
so those credits do not apply here: on this instance you bring your own OpenAI key. If you want the free
credits, sign up at n8n.io for a Cloud workspace and import the same `labs_remote_n8n/` flows there —
they will run unchanged.

## A workflow does nothing until it is Active

A production `/webhook/…` path does not exist in n8n until you switch the workflow **Active**. Before
that, n8n returns `404` and the lab's page reports that it cannot reach n8n. This is the most common
failure in class, in both builds.

## The labs

| Lab | Flow to import | Webhook(s) | Extra credential |
|---|---|---|---|
| 1 | `lab1/ai-agent.json` | — | `OpenAI account` |
| 2 | `lab2/rag-flow.json` | `/rag-upload`, `/rag-chat` | `OpenAI account` |
| 3 | `lab3/CX Agent with RAG.json` | `/cx-agent`, `/brochure-upload` | `OpenAI account` |
| 4 | `lab4/elevenlabs-web-call-flow.json`<br>`lab4/elevenlabs-booking-tools-flow.json` | `/elevenlabs-web-call`<br>`/check-availability`, `/book-appointment` | `ElevenLabs API` (header `xi-api-key`) + your Google Calendar |
| 5 | `lab5/vapi-faq-flow.json` | `/vapi-faq` | `OpenAI account` |
| 6 | *(no n8n flow — local Python lip-sync studio)* | — | — |
| 7 | `lab7/heygen-news-avatar-flow.json` | `/heygen-generate`, `/heygen-status` | `HeyGen API` |
| 7-os | `lab7-opensource/os-news-avatar-flow.json` | `/os-generate` | see the caveat below |
| 8 | `lab8/avatar-chat-flow.json` | `/avatar-chat` | `OpenAI account` |
| 9 | `lab9/liveavatar-session-flow.json` | `/liveavatar-session`, `/liveavatar-contexts` | `LiveAvatar API` |
| 10 | `lab10/veo3-video-flow.json` | `/veo-generate`, `/veo-status`, `/veo-file` | `Gemini API` |

### Two labs still need your own machine

The cloud build removes the *n8n* install, not every install.

- **Lab 6** renders lip-sync locally (Wav2Lip / MuseTalk). It has no n8n flow at all — it is a Python
  app on your laptop. It is identical in both builds.
- **Lab 7 (open-source)** asks the hosted n8n to call a **render service running on your machine**, and
  a hosted n8n cannot reach your laptop. Its flow ships with the render URL set to
  `https://REPLACE-WITH-YOUR-NGROK-URL` on purpose. To run it you must tunnel your local render service:

  ```bash
  ngrok http 8099
  ```

  then paste the ngrok address into the flow's render node. This is the one lab where the cloud build
  is *harder* than the local build — which is itself worth understanding: the direction of the call is
  what decides whether a tunnel is needed.

## Voice labs — which way does the call go?

This decides everything about setup, and it is the thing learners get wrong.

| Call | Direction | Public URL needed? |
|---|---|---|
| Lab 4 web call | **your browser** → n8n | No |
| Lab 4 booking tools | **ElevenLabs' servers** → n8n | Yes — and the hosted n8n already is public ✅ |
| Lab 5 custom LLM | **Vapi's servers** → n8n | Yes — already public ✅ |
| Lab 7-os render | **n8n** → *your machine* | Yes — **you** must tunnel (see above) |

## Security rule

Your API keys live in **n8n credentials**, never in the browser. The lab websites are built so the page
only ever receives a short-lived token — a signed URL in Lab 4, a public key in Lab 5. If you ever find
yourself pasting a secret key into a web page, stop: that page is visible to every visitor.
