# Lab 4.8 - Build a FAQ Voice Agent with Vapi

> Topic 4 - Approximately 75 minutes - Adult workplace lab

## The build so far

This lab is part of a complete agentic AI automation course. Each lab follows the same engineering loop:

**Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

In this lab you build: **A second voice agent on a different platform, where n8n is the BRAIN of the call: Vapi speaks, n8n thinks.**

## What you will build

A second voice agent on a different platform, where n8n is the BRAIN of the call: Vapi speaks, n8n thinks. The work is intentionally practical: by the end of the lab you should have an artifact that can be inspected, tested, and reused in the capstone.

## Concepts you will meet

| Concept | In one line |
|---|---|
| Custom LLM | Vapi delegates every turn to your own endpoint instead of its built-in model. |
| OpenAI-shaped response | n8n must reply in chat-completion format or the agent goes silent. |
| Public vs private key | A public key can only start calls, so it is safe in the browser. |
| Refusal testing | The question the FAQ cannot answer is the most important test. |

## Before you start

- Complete the setup in Lab 1.1 or confirm Docker, n8n, Ollama, and your browser are ready.
- Keep n8n executions visible while testing. The execution trace is your evidence.
- Do not place API keys in HTML, JavaScript, Markdown examples, screenshots, or exported workflow notes.
- Commit or export a checkpoint before making large workflow changes.

## Step-by-step instructions

1. Understand the difference before you build. **Retell (Lab 4.2)**: Retell owns the model; n8n only mints the call token and answers tool calls. **Vapi (this lab)**: Vapi owns the ears and the voice, but every turn of thinking is handed to *your* n8n workflow through its **Custom LLM** setting. n8n is the brain.
2. Import `lab5/vapi-faq-flow.json`. Read it left to right: **Vapi Webhook** receives an OpenAI-shaped chat request -> **Prepare Prompt** pulls out the caller's latest turn and the transcript -> **FAQ Agent** (Ollama) answers from the HomeMart FAQ in its system message -> **Build OpenAI Response** wraps the answer as a `chat.completion` object -> **Respond to Vapi**.
3. That last step is the one that breaks silently: Vapi expects a valid OpenAI chat-completion object. Return anything else and the assistant just stops talking mid-call, with no error in the browser.
4. Select the `Ollama local` credential in the model node, then **Publish/Activate** the workflow and copy the Webhook's **Production URL** (`.../webhook/vapi-faq`).
5. Test the brain BEFORE any voice - HTTP is far easier to debug than audio: `curl -X POST <url> -H 'Content-Type: application/json' -d '{"model":"gpt-4o","messages":[{"role":"user","content":"How long is the warranty on a Dyson?"}]}'`. You must get back a `chat.completion` object whose content says **two years** - not one.
6. Run the refusal test the same way: ask *"Do you sell nail polish?"*. The reply must offer a colleague follow-up, NOT invent a product. If it invents one, tighten the grounding rule in the agent's system message and re-run.
7. Start a tunnel (`ngrok http 5678`) - Vapi's servers cannot reach localhost.
8. In Vapi, create an assistant named `Ava - HomeMart FAQ`. Set **Model -> Custom LLM** and paste `https://<tunnel>/webhook/vapi-faq` as the URL. Set the **First Message** so Ava speaks first (see `lab5/ava-assistant-prompt.md`). Save, then copy the **assistant ID**.
9. In **API Keys** you will see a **public** and a **private** key. You need the PUBLIC one - it can only start calls. The private key must never appear in front-end code.
10. Serve the site: double-click `lab5/website/start.command` (macOS) or `start.bat` (Windows) - or `cd lab5/website` then `python3 -m http.server 8096` (macOS) / `python -m http.server 8096` (Windows). Open `http://localhost:8096`, click **⚙ Settings** and paste your public key and assistant ID. Nothing is hardcoded: the values live in your browser, so every learner drives the same page with their own assistant.
11. Click **Ask Ava**, allow the microphone, and work through the six-question test set in `ava-assistant-prompt.md` while watching the n8n executions list - one execution per conversational turn. That list IS the agent thinking.
12. Write three sentences comparing Vapi and Retell: where the model runs, where the secret lives, and which you would choose for a client - and why.

## Agentic AI loop checklist

1. **Define** the user, trigger, input, tool boundary, and output.
2. **Build** the smallest workflow that proves the behavior.
3. **Observe** the execution trace, model output, and external service response.
4. **Evaluate** with normal, edge, and unsafe inputs.
5. **Improve** one thing at a time and rerun the same tests.
6. **Guardrail** credentials, refusal behavior, human handoff, and publishing actions.
7. **Document** the final setup, test evidence, and rollback step.

## Vibe / agent prompt

Paste this into your coding or workflow agent after you have a first draft:

```text
I am completing Build a FAQ Voice Agent with Vapi in the course "Automate Video and Voice AI Agents with n8n".
Act as a careful agentic AI workflow reviewer. Review my workflow design against this goal:
A second voice agent on a different platform, where n8n is the BRAIN of the call: Vapi speaks, n8n thinks.

Check for:
- missing trigger, input, output, or credential boundary
- weak system prompt or unclear tool description
- missing evaluation case, refusal case, or human review gate
- any place where a secret could leak to browser code or exported notes

Return a concise list of fixes, then give me one improved test case.
```

## Verify

- [ ] A curl to the webhook returns a valid `chat.completion` object, and the Dyson answer says two years.
- [ ] The site starts a Vapi call and the live transcript appears.
- [ ] Ava answers the *exception* correctly (opened personal-care items cannot be returned).
- [ ] She REFUSES the nail-polish question instead of inventing a product.
- [ ] One n8n execution appears per conversational turn, and the private key appears nowhere in the browser.

## Reflection questions

1. What did the agent or workflow do correctly on the first attempt?
2. What evidence proves the output was grounded, safe, or complete?
3. Which failure case was most useful for improving the workflow?
4. What should a human still review before this automation is used with real customers?

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| Ava connects then goes silent | n8n did not return a valid OpenAI chat-completion object. | Check the Build OpenAI Response node; the reply must have object, choices[0].message.content. |
| No n8n execution during the call | Vapi cannot reach your n8n. | Start the tunnel and use the https URL in Custom LLM - not localhost. |
| Call fails immediately | The private key was pasted instead of the public key. | Use the PUBLIC key from Vapi -> API Keys. |
| Ava invents a product | The grounding rule is missing or too soft. | State the exact refusal sentence in the agent's system message, then re-test. |
| Model errors with 401 | The OpenAI credential is expired. | Use the Ollama local credential - this course runs the model locally. |

## Submission evidence

Submit the following:

- Workflow export or screenshot of the main workflow canvas.
- Screenshot or copy of the successful execution output.
- One normal test case and one edge or unsafe test case.
- A short note explaining what you changed after evaluation.

## Lab deliverable

A working Vapi FAQ voice agent whose brain is an n8n workflow, proven by a curl test, a live call and one honest refusal.
