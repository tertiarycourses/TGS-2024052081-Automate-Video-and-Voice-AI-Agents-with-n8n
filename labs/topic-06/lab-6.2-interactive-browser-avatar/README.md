# Lab 6.2 - Build an Interactive Avatar That Renders in the Browser

> Topic 6 - Approximately 75 minutes - Adult workplace lab

## The build so far

This lab is part of a complete agentic AI automation course. Each lab follows the same engineering loop:

**Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

In this lab you build: **A talking avatar that listens, thinks and answers with no cloud avatar, no credits and no render wait - and a measured latency to prove it.**

## What you will build

A talking avatar that listens, thinks and answers with no cloud avatar, no credits and no render wait - and a measured latency to prove it. The work is intentionally practical: by the end of the lab you should have an artifact that can be inspected, tested, and reused in the capstone.

## Concepts you will meet

| Concept | In one line |
|---|---|
| The interactive loop | Speech to text, then the agent, then text to speech, then the mouth - each stage adds latency the learner can measure. |
| Latency engineering | The reply must arrive in about a second, or the conversation feels dead. Every design choice in this lab serves that. |
| Barge-in | The learner can interrupt the avatar mid-sentence, exactly as they would interrupt a person. |
| Drawn mouth vs real pixels | The mouth here is geometry drawn on a photo - free and instant, but not photoreal. Lab 6.3 is the honest comparison. |

## Before you start

- Complete the setup in Lab 1.1 or confirm Docker, n8n, Ollama, and your browser are ready.
- Keep n8n executions visible while testing. The execution trace is your evidence.
- Do not place API keys in HTML, JavaScript, Markdown examples, screenshots, or exported workflow notes.
- Commit or export a checkpoint before making large workflow changes.

## Step-by-step instructions

1. Import `lab8/avatar-chat-flow.json` and publish it.
2. Start the website with `lab8/website/start.command` (Mac) or `start.bat` (Windows), then open `http://localhost:8100` in Chrome or Edge.
3. Open the gear and paste the Production webhook URL of the Lab 6.2 flow.
4. Pick a face, hold the mic, and ask about the academy's courses.
5. Read the latency line under the stage and note where the time actually goes.
6. Open the flow and find the three settings that buy that speed: `think: false`, `keep_alive`, and a small `num_predict`.
7. Interrupt the avatar while it is speaking and confirm it stops and listens.

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
I am completing Build an Interactive Avatar That Renders in the Browser in the course "Automate Video and Voice AI Agents with n8n".
Act as a careful agentic AI workflow reviewer. Review my workflow design against this goal:
A talking avatar that listens, thinks and answers with no cloud avatar, no credits and no render wait - and a measured latency to prove it.

Check for:
- missing trigger, input, output, or credential boundary
- weak system prompt or unclear tool description
- missing evaluation case, refusal case, or human review gate
- any place where a secret could leak to browser code or exported notes

Return a concise list of fixes, then give me one improved test case.
```

## Verify

- [ ] The avatar answers out loud in roughly a second, and the page prints the measured time.
- [ ] Interrupting the avatar cuts it off immediately.
- [ ] The learner can explain why the flow calls Ollama directly instead of using the AI Agent node, and why a thinking model must be told not to think.

## Reflection questions

1. What did the agent or workflow do correctly on the first attempt?
2. What evidence proves the output was grounded, safe, or complete?
3. Which failure case was most useful for improving the workflow?
4. What should a human still review before this automation is used with real customers?

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| The avatar says it did not catch that | gemma4 is a thinking model: left alone it spends the whole token budget on an internal monologue and returns empty content. | Set `think: false` in the Ollama request and give `num_predict` enough room for two spoken sentences. |
| The first reply takes several seconds | The 9.6 GB model was not resident and had to be loaded from disk. | Send a warm-up call when the page loads, and set `keep_alive` so the model stays in memory. |
| No microphone | Speech recognition needs a secure context and a supported browser. | Serve the page from `http://localhost`, not `file://`, and use Chrome or Edge. |

## Submission evidence

Submit the following:

- Workflow export or screenshot of the main workflow canvas.
- Screenshot or copy of the successful execution output.
- One normal test case and one edge or unsafe test case.
- A short note explaining what you changed after evaluation.

## Lab deliverable

A working browser avatar, the measured latency, and a note naming the three settings that produced it.
