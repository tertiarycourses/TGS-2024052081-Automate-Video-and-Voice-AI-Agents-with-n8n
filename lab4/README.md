# GG Hair Salon — Voice AI Agent (Lab 4)

A premium hair salon **single-page web app** (`website/` — plain HTML/CSS/JS, no build step) with **AI voice booking**. The Retell voice call is triggered through an **n8n flow**, so no API key ever touches the browser.

- **AI Voice Booking** — talk to Nina, the AI salon assistant, to check availability and book appointments via natural conversation (**Retell AI**, WebRTC, triggered via n8n)
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
├── retell-web-call-flow.json    # n8n flow: webhook → Retell create-web-call
└── .env                         # reference copy of the Retell keys
```

## Prerequisites

- Local n8n (Lab 0) with:
  - the **`retell-web-call-flow.json`** workflow imported and **Active**
  - a **Header Auth** credential named `Retell API` on its HTTP Request node
    (Name: `Authorization`, Value: `Bearer key_…` — your Retell API key)

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
