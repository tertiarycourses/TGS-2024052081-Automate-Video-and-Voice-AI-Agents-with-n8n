# GG Hair Salon — Voice AI Agent (Lab 4)

A premium hair salon **single-page web app** (`website/` — plain HTML/CSS/JS, no build step) with **AI voice booking**. The Retell voice call is triggered through an **n8n flow**, so no API key ever touches the browser.

- **AI Voice Booking** — talk to Nina, the AI salon assistant, to check availability and book appointments via natural conversation (**Retell AI**, WebRTC, triggered via n8n)
- **Grounded answers** — a **Retell Knowledge Base** (`knowledge-base/`) lets Nina answer questions on prices, stylists and policies from a source document instead of guessing
- **Services Menu** — salon services across Haircuts, Coloring, Treatments, and Styling
- **Fully Responsive** — desktop, tablet, and mobile

## Architecture

```
User clicks "Book by Voice"
  → browser POSTs to n8n webhook  (http://localhost:5678/webhook/retell-web-call)
    → n8n "Retell Web Call Trigger" flow calls the Retell API
      (API key stored as an n8n credential) → returns access_token
  → browser starts WebRTC voice session via Retell Web SDK
    → Retell agent "Nina" calls its n8n webhook tools to check availability / book
  → appointment confirmed in Google Calendar
```

## Project structure

```
├── website/
│   ├── index.html               # single-page salon website
│   ├── main.js                  # voice call (via n8n) + UI
│   ├── styles.css               # rose gold/mauve salon theme
│   ├── start.command            # one-click launcher (macOS)
│   └── start.bat                # one-click launcher (Windows)
├── knowledge-base/
│   ├── gg-hair-salon-handbook.pdf  # upload this to Retell → Knowledge Base
│   └── build_kb_pdf.py             # regenerates the PDF (pip install reportlab)
├── retell-web-call-flow.json    # n8n flow: webhook → Retell create-web-call
└── .env                         # reference copy of the Retell keys
```

## Prerequisites

- Local n8n (Lab 0) with:
  - the **`retell-web-call-flow.json`** workflow imported and **Active**
  - a **Header Auth** credential named `Retell API` on its HTTP Request node
    (Name: `Authorization`, Value: `Bearer key_…` — your Retell API key)
- A Retell agent (Nina), **published**, with its `agent_…` ID set in the flow's
  *Create Retell Web Call* node (it ships with the trainer's ID as a fallback)

## The two webhooks — which goes where

They point in **opposite directions**, and only one of them is configured inside Retell:

| Webhook | Direction | Where you set the URL | Public? |
|---|---|---|---|
| `/webhook/retell-web-call` | browser → n8n → Retell API | On the page: **⚙ Settings** (nothing is hardcoded — saved per browser) | No — `localhost` is fine |
| `check_availability`, `book_appointment` | **Retell cloud → n8n** | Retell agent → **Functions** → *Custom Function* → URL | **Yes — needs a tunnel** |

The ⚙ Settings panel also takes an optional **Retell agent ID**, so each learner drives the
same page with their own agent (the flow falls back to its configured agent if left blank).

Retell's servers cannot reach your `localhost`, so the agent's function URLs must be public:

```bash
ngrok http 5678      # use https://<id>.ngrok-free.app/webhook/check-availability in Retell
```

Symptom guide: *call never starts* → browser→n8n webhook. *Nina greets you, then stalls
while "checking availability"* → Retell→n8n function URL (tunnel down or a localhost URL).

## Knowledge Base (grounded answers)

Upload `knowledge-base/gg-hair-salon-handbook.pdf` in the Retell dashboard under
**Knowledge Base → +**, then attach it to the agent in the agent's **Knowledge Base**
panel and **publish** the agent again. Nina can then answer prices, stylists, parking
and the cancellation policy from the document instead of guessing. See Lab 4.5 in the
Learner Guide for the full walkthrough and the grounding test.

## Run

The site **must be served over `http://localhost`** (not opened as a `file://` page) — browsers block module scripts and microphone access on `file://`.

- **Easiest:** double-click **`website/start.command`** (Mac) or **`website/start.bat`** (Windows). It serves the site and opens your browser. Uses Python if present, otherwise Node (`npx serve`).
- **Or serve it yourself** (any one):
  ```bash
  cd website
  python3 -m http.server 8090     # Python
  npx serve                       # Node
  php -S localhost:8090           # PHP
  ```
  …or in VS Code: right-click `index.html` → **Open with Live Server**.

Then open the printed `http://localhost:…` URL, click **Book by Voice**, allow microphone access, and talk to Nina.

## License

MIT
