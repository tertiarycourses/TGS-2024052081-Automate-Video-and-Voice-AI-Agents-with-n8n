# Lab 6.3 - Embed an Interactive HeyGen Avatar with LiveAvatar

> Topic 6 - Approximately 75 minutes - Adult workplace lab

## The build so far

This lab is part of a complete agentic AI automation course. Each lab follows the same engineering loop:

**Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

In this lab you build: **The same conversation as Lab 6.2, but with a photoreal streaming avatar - and a clear-eyed comparison of what that costs.**

## What you will build

The same conversation as Lab 6.2, but with a photoreal streaming avatar - and a clear-eyed comparison of what that costs. The work is intentionally practical: by the end of the lab you should have an artifact that can be inspected, tested, and reused in the capstone.

## Concepts you will meet

| Concept | In one line |
|---|---|
| Streaming avatar | A real face, streamed from the cloud, that moves its head and holds eye contact. |
| The ticket pattern | n8n exchanges the API key for a short-lived embed URL. The browser gets the ticket, never the key. |
| Persona (context) | One face, several personalities - the context decides what the avatar knows and how it behaves. |
| The honest trade-off | Photoreal costs credits, a network round trip and an account. Drawn geometry costs nothing. Neither is simply better. |

## Before you start

- Complete the setup in Lab 1.1 or confirm Docker, n8n, Ollama, and your browser are ready.
- Keep n8n executions visible while testing. The execution trace is your evidence.
- Do not place API keys in HTML, JavaScript, Markdown examples, screenshots, or exported workflow notes.
- Commit or export a checkpoint before making large workflow changes.

## Step-by-step instructions

1. Import `lab9/liveavatar-session-flow.json` and publish it.
2. Create the LiveAvatar API credential in n8n as a header credential and select it on both HTTP nodes.
3. Start the website with `lab9/website/start.command` (Mac) or `start.bat` (Windows), then open `http://localhost:8099`.
4. Open the gear and paste the Production webhook URL of the Lab 6.3 session flow.
5. Pick a persona from the dropdown - the page lists them by calling the flow, not by hardcoding ids.
6. Start the session and hold the same conversation you held with Aria in Lab 6.2.
7. Fill in a two-column scorecard: latency, realism, cost per minute, and setup effort.

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
I am completing Embed an Interactive HeyGen Avatar with LiveAvatar in the course "Automate Video and Voice AI Agents with n8n".
Act as a careful agentic AI workflow reviewer. Review my workflow design against this goal:
The same conversation as Lab 6.2, but with a photoreal streaming avatar - and a clear-eyed comparison of what that costs.

Check for:
- missing trigger, input, output, or credential boundary
- weak system prompt or unclear tool description
- missing evaluation case, refusal case, or human review gate
- any place where a secret could leak to browser code or exported notes

Return a concise list of fixes, then give me one improved test case.
```

## Verify

- [ ] The browser starts a live photoreal avatar session.
- [ ] The learner can show that the API key is nowhere in the page source - only the short-lived embed URL is.
- [ ] The scorecard states, in the learner's own words, when to reach for a streaming avatar and when the browser-rendered one is enough.

## Reflection questions

1. What did the agent or workflow do correctly on the first attempt?
2. What evidence proves the output was grounded, safe, or complete?
3. Which failure case was most useful for improving the workflow?
4. What should a human still review before this automation is used with real customers?

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| The avatar does not start | The session flow returned no embed URL - usually a bad key or an avatar id the account cannot use. | Open the flow's last execution and read the LiveAvatar error message, then check the key and the avatar id. |
| The persona dropdown is empty | The contexts webhook is not published, or the account has no contexts yet. | Publish the flow and confirm the contexts endpoint returns a list. |
| The browser blocks the audio | Autoplay is blocked until the user interacts with the page. | Click into the page before starting the session, and allow the microphone. |

## Submission evidence

Submit the following:

- Workflow export or screenshot of the main workflow canvas.
- Screenshot or copy of the successful execution output.
- One normal test case and one edge or unsafe test case.
- A short note explaining what you changed after evaluation.

## Lab deliverable

A working streaming avatar session plus the two-column scorecard comparing it against the browser-rendered avatar.
