# HomeMart — FAQ Voice Agent with Vapi (Lab 5)

A one-page HomeMart storefront (`website/` — plain HTML/CSS/JS, no build step) with **Ava**,
a FAQ voice assistant built on **Vapi**. It is the counterpart to the Retell lab: same job,
different platform, deliberately different architecture.

## Why this lab exists — n8n is the BRAIN

| | Retell (Lab 4) | Vapi (this lab) |
|---|---|---|
| Who runs the model | **Retell** does | **your n8n workflow** does (Vapi "Custom LLM") |
| n8n's job | mint the call token; answer tool calls | **think** — every conversational turn |
| Call path | browser → n8n → Retell API → token → WebRTC | browser → Vapi (public key), then Vapi → n8n each turn |
| Key in the browser | none — the **private** key stays in n8n | the **public** key (it can only start calls) |

Vapi handles the ears (speech-to-text) and the mouth (text-to-speech). Everything in between —
the actual answer — is your workflow. Vapi POSTs an OpenAI-shaped chat request to your webhook
on every turn, and **expects an OpenAI `chat.completion` object back**. Return anything else and
the assistant goes quiet mid-call with no browser error. That is the classic failure of this lab.

```
caller speaks → Vapi (STT) → POST /webhook/vapi-faq
                                 → Prepare Prompt → FAQ Agent (Ollama) → Build OpenAI Response
                             ← { object: "chat.completion", choices:[{ message:{ content }}] }
              → Vapi (TTS) → caller hears the answer
```

## Project structure

```
├── website/
│   ├── index.html            # one-page storefront + FAQ + voice modal
│   ├── main.js               # Vapi Web SDK call, live transcript, ⚙ settings
│   └── styles.css            # HomeMart look (green / Manrope)
├── vapi-faq-flow.json        # n8n: the agent's brain (custom-LLM endpoint)
├── ava-assistant-prompt.md   # system prompt + first message + the 6-question test set
└── README.md
```

## Prerequisites

- Local n8n with **`vapi-faq-flow.json`** imported, the `Ollama local` credential selected, and the workflow **published/active**
- A tunnel (`ngrok http 5678`) — Vapi's servers cannot reach `localhost`
- A **Vapi** account, an assistant whose **Model → Custom LLM** points at `https://<tunnel>/webhook/vapi-faq`, its **assistant ID**, and your **public** key

> ⚠️ The **private** key manages your account and must never appear in browser code.
> The page only ever asks for the **public** key.

## Test the brain before you test the voice

HTTP is far easier to debug than audio:

```bash
curl -X POST http://localhost:5678/webhook/vapi-faq \
  -H 'Content-Type: application/json' \
  -d '{"model":"gpt-4o","messages":[{"role":"user","content":"How long is the warranty on a Dyson?"}]}'
```

You should get a `chat.completion` object whose content says **two years** (not the 1-year default).
Then ask *"Do you sell nail polish?"* — it must offer a colleague follow-up, not invent a product.

## Run

The site must be served over `http://localhost` — browsers block module scripts and the
microphone on `file://`.

```bash
cd website
python3 -m http.server 8096
```

Open `http://localhost:8096`, click **⚙ Settings**, paste your **public key** and **assistant ID**
(saved in your browser only — nothing is hardcoded), then click **Ask Ava** and allow the microphone.

## The test that matters

Ava knows six FAQ topics and nothing else. Work through the test set at the end of
[`ava-assistant-prompt.md`](ava-assistant-prompt.md) — the last question is the point:

> **"Do you sell nail polish?"**

It is not in the FAQ. Ava must offer a colleague follow-up rather than invent an answer.
An agent that is confidently wrong is worse than one that says "I don't know".

## License

MIT
