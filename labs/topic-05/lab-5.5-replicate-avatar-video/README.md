# Lab 5.5 - Generate Cloud Avatar Video with Replicate

> Topic 5 - Approximately 60 minutes - Adult workplace lab

## The build so far

This lab is part of a complete agentic AI automation course. Each lab follows the same engineering loop:

**Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

In this lab you build: **A Replicate-based avatar video using TTS and talking-head generation.**

## What you will build

A Replicate-based avatar video using TTS and talking-head generation. The work is intentionally practical: by the end of the lab you should have an artifact that can be inspected, tested, and reused in the capstone.

## Concepts you will meet

| Concept | In one line |
|---|---|
| Model API | Calls hosted models for speech or talking-head generation. |
| Cost control | Uses short tests before longer renders. |
| Polling | Checks job status until completion. |
| Provider comparison | Compares speed, quality, price, and setup complexity. |

## Before you start

- Complete the setup in Lab 1.1 or confirm Docker, n8n, Ollama, and your browser are ready.
- Keep n8n executions visible while testing. The execution trace is your evidence.
- Do not place API keys in HTML, JavaScript, Markdown examples, screenshots, or exported workflow notes.
- Commit or export a checkpoint before making large workflow changes.

## Step-by-step instructions

1. Import `lab8/replicate-avatar-flow.json`.
2. Create the Replicate API credential in n8n.
3. Run a 10-second test script before a full render.
4. Inspect job status and final video URL.
5. Record render time and approximate cost.
6. Compare output against HeyGen and local HyperFrames on a three-column scorecard.

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
I am completing Generate Cloud Avatar Video with Replicate in the course "Automate Video and Voice AI Agents with n8n".
Act as a careful agentic AI workflow reviewer. Review my workflow design against this goal:
A Replicate-based avatar video using TTS and talking-head generation.

Check for:
- missing trigger, input, output, or credential boundary
- weak system prompt or unclear tool description
- missing evaluation case, refusal case, or human review gate
- any place where a secret could leak to browser code or exported notes

Return a concise list of fixes, then give me one improved test case.
```

## Verify

- [ ] The workflow returns a playable video URL.
- [ ] The test run is short enough to control cost.
- [ ] The scorecard states when Replicate is the right provider.

## Reflection questions

1. What did the agent or workflow do correctly on the first attempt?
2. What evidence proves the output was grounded, safe, or complete?
3. Which failure case was most useful for improving the workflow?
4. What should a human still review before this automation is used with real customers?

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| Prediction fails | Model input schema changed or API key is invalid. | Open the node output and compare required fields. |
| Cost is higher than expected | The test script was too long. | Use a 5 to 10 second smoke test first. |
| Output quality varies | The model is stochastic and input image quality matters. | Use a clear face image and rerun only after prompt fixes. |

## Submission evidence

Submit the following:

- Workflow export or screenshot of the main workflow canvas.
- Screenshot or copy of the successful execution output.
- One normal test case and one edge or unsafe test case.
- A short note explaining what you changed after evaluation.

## Lab deliverable

A Replicate avatar video and provider comparison scorecard.
