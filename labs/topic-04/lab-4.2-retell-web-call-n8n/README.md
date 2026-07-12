# Lab 4.2 - Connect Retell Web Calls Through n8n

> Topic 4 - Approximately 75 minutes - Adult workplace lab

## The build so far

This lab is part of a complete agentic AI automation course. Each lab follows the same engineering loop:

**Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

In this lab you build: **A browser voice call that mints access through an n8n webhook.**

## What you will build

A browser voice call that mints access through an n8n webhook. The work is intentionally practical: by the end of the lab you should have an artifact that can be inspected, tested, and reused in the capstone.

## Concepts you will meet

| Concept | In one line |
|---|---|
| WebRTC voice call | Runs the real-time audio session in the browser. |
| Server-side token minting | Keeps the Retell API key away from front-end code. |
| Webhook trigger | Lets the website request a call session securely. |
| Credential hygiene | Stores the API key in n8n or local environment only. |

## Before you start

- Complete the setup in Lab 1.1 or confirm Docker, n8n, Ollama, and your browser are ready.
- Keep n8n executions visible while testing. The execution trace is your evidence.
- Do not place API keys in HTML, JavaScript, Markdown examples, screenshots, or exported workflow notes.
- Commit or export a checkpoint before making large workflow changes.

## Step-by-step instructions

1. Import `lab4/retell-web-call-flow.json`.
2. Create the `Retell API` Header Auth credential (`Authorization` = `Bearer key_...`) on the HTTP Request node.
3. Put your own `agent_...` ID into the **Create Retell Web Call** node, or send it from the site in the next step. The shipped fallback is the trainer's demo agent.
4. Activate the workflow and copy the Webhook node's **Production URL** (not the Test URL).
5. Serve the site: double-click `lab4/website/start.command` (macOS) or `start.bat` (Windows). Or by hand: `cd lab4/website` then `python3 -m http.server 8090` on macOS / `python -m http.server 8090` on Windows. Open `http://localhost:8090`.
6. Click **⚙ Settings** on the page, paste your webhook URL and your `agent_...` ID, and Save. Nothing is hardcoded: the values live in your browser, so every learner drives the same site from their own n8n.
7. Start a browser call and complete one short booking conversation.
8. Inspect the n8n execution to confirm the front end never received the API key.

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
I am completing Connect Retell Web Calls Through n8n in the course "Automate Video and Voice AI Agents with n8n".
Act as a careful agentic AI workflow reviewer. Review my workflow design against this goal:
A browser voice call that mints access through an n8n webhook.

Check for:
- missing trigger, input, output, or credential boundary
- weak system prompt or unclear tool description
- missing evaluation case, refusal case, or human review gate
- any place where a secret could leak to browser code or exported notes

Return a concise list of fixes, then give me one improved test case.
```

## Verify

- [ ] The website starts a Retell voice session.
- [ ] The API key is not present in browser JavaScript.
- [ ] n8n records a successful token/session creation execution.

## Reflection questions

1. What did the agent or workflow do correctly on the first attempt?
2. What evidence proves the output was grounded, safe, or complete?
3. Which failure case was most useful for improving the workflow?
4. What should a human still review before this automation is used with real customers?

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| Call button fails | The webhook URL in ⚙ Settings is wrong, or the workflow is not active. | Activate the workflow and paste the production webhook URL into ⚙ Settings. |
| 401 from Retell | API key is missing or invalid. | Update the n8n credential and retest. |
| You reach the trainer's agent | The site sent no agent ID, so the node's fallback was used. | Put your own `agent_...` ID in ⚙ Settings or in the node. |
| Microphone blocked | Browser permission was denied. | Allow microphone access and reload the page. |

## Submission evidence

Submit the following:

- Workflow export or screenshot of the main workflow canvas.
- Screenshot or copy of the successful execution output.
- One normal test case and one edge or unsafe test case.
- A short note explaining what you changed after evaluation.

## Lab deliverable

A secure browser-to-Retell call flow.
