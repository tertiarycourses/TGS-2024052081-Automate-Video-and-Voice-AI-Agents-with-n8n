# Lab 4 - Voice Booking Agent with ElevenLabs

A premium hair salon **single-page web app** (`website/` - plain HTML/CSS/JS, no build step) with an
**ElevenLabs Conversational AI** receptionist called **Nina**, who checks a real Google Calendar and books
real appointments.

## The call path

```text
Click "Book by Voice"
  -> browser POSTs to n8n            (https://n8n.tertiarytraining.com/webhook/elevenlabs-web-call)
    -> n8n asks ElevenLabs for a SIGNED URL  (your xi-api-key stays in n8n)
  <- n8n returns { signed_url }
  -> browser opens a WebSocket straight to that signed URL and starts talking
    -> Nina calls her TOOL webhooks back into n8n to check availability / book
```

The key idea: **the browser never sees your ElevenLabs API key.** It receives a short-lived signed URL,
which is the only thing needed to run one conversation.

## Files

```text
lab4/
├── website/                             # the salon storefront (serve it, do not open with file://)
├── knowledge-base/
│   └── gg-hair-salon-handbook.pdf       # upload to the ElevenLabs agent -> Knowledge Base
├── elevenlabs-web-call-flow.json        # n8n: webhook -> ElevenLabs get-signed-url -> respond
└── elevenlabs-booking-tools-flow.json   # n8n: check_availability + book_appointment (Google Calendar)
```

## Setup

1. **Import both flows** into the shared remote n8n (`n8n.tertiarytraining.com`) and set them **Active**.
2. On *ElevenLabs: Get Signed URL*, add a **Header Auth** credential named **`ElevenLabs API`**:
   - Name: `xi-api-key`
   - Value: your ElevenLabs API key
3. On the two **Google Calendar** nodes, connect **your own Google account** (OAuth). This is per-learner -
   the flow ships without a calendar credential on purpose.
4. In the **ElevenLabs dashboard**, create a Conversational AI agent (Nina), then paste its **agent ID**
   into the flow's *Get Signed URL* node (or into the page's ⚙ Settings, which overrides it per learner).
5. Upload `knowledge-base/gg-hair-salon-handbook.pdf` to the agent's **Knowledge Base** so Nina can answer
   questions about prices and services without inventing them.

## The two webhook directions (this is where people get stuck)

| Webhook | Who calls it | Needs to be public? |
|---|---|---|
| `/elevenlabs-web-call` | **your browser** -> n8n | No - your own machine calls it. |
| `check_availability`, `book_appointment` | **ElevenLabs' servers** -> n8n | **Yes.** |

**No tunnel needed.** The remote n8n is already on the public internet, so ElevenLabs' servers can reach
the tool webhooks directly. Use these as the tool URLs in the ElevenLabs agent:

```text
https://n8n.tertiarytraining.com/webhook/check-availability
https://n8n.tertiarytraining.com/webhook/book-appointment
```

This is the single biggest practical difference from the local build — no ngrok, no rotating URL.

## Serve the site

```bash
cd website
python3 -m http.server 8090      # Windows: python -m http.server 8090
```

Open `http://localhost:8090`. Do **not** double-click `index.html` - `file://` blocks both ES modules and
the microphone, and every button dies silently.

## Troubleshooting

| Symptom | Cause |
|---|---|
| Banner: "Cannot reach n8n" | The workflow is not Active, or the ⚙ URL is wrong. |
| "No signed URL received" | The `ElevenLabs API` credential is missing/wrong, or the agent ID does not exist. |
| Nina says she is checking, then stalls | The **tool** webhook is unreachable - the direction that must be public. |
| Mic blocked | The page must be served over `http://localhost`, and the browser must be granted mic access. |
