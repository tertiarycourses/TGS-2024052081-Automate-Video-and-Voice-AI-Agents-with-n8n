# Lab 5.5 - Build the Free Local Avatar Video Pipeline

> Topic 5 - Approximately 90 minutes - Adult workplace lab

## The build so far

This lab is part of a complete agentic AI automation course. Each lab follows the same engineering loop:

**Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

In this lab you build: **A local avatar video path using Ollama, generated speech, Wav2Lip-style rendering, and ffmpeg.**

## What you will build

A local avatar video path using Ollama, generated speech, Wav2Lip-style rendering, and ffmpeg. The work is intentionally practical: by the end of the lab you should have an artifact that can be inspected, tested, and reused in the capstone.

## Concepts you will meet

| Concept | In one line |
|---|---|
| Open-source pipeline | Keeps video generation possible without cloud video credits. |
| Render service | Separates heavy video work from the n8n orchestration flow. |
| Audio-video sync | Aligns speech and face movement. |
| Fallback strategy | Lets a production workflow continue when a paid provider is unavailable. |

## Before you start

- Complete the setup in Lab 1.1 or confirm Docker, n8n, Ollama, and your browser are ready.
- Keep n8n executions visible while testing. The execution trace is your evidence.
- Do not place API keys in HTML, JavaScript, Markdown examples, screenshots, or exported workflow notes.
- Commit or export a checkpoint before making large workflow changes.

## Step-by-step instructions

1. Open `lab7-opensource/README.md` and review the service architecture.
2. Start the local render service using the provided start script for your platform.
3. Import `lab7-opensource/os-news-avatar-flow.json` into n8n.
4. Run a short script generation and render test.
5. Open the website front end and play the generated output.
6. Compare the local output against the HeyGen output using a quality rubric.

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
I am completing Build the Free Local Avatar Video Pipeline in the course "Automate Video and Voice AI Agents with n8n".
Act as a careful agentic AI workflow reviewer. Review my workflow design against this goal:
A local avatar video path using Ollama, generated speech, Wav2Lip-style rendering, and ffmpeg.

Check for:
- missing trigger, input, output, or credential boundary
- weak system prompt or unclear tool description
- missing evaluation case, refusal case, or human review gate
- any place where a secret could leak to browser code or exported notes

Return a concise list of fixes, then give me one improved test case.
```

## Verify

- [ ] The local service accepts a render request.
- [ ] The workflow returns a playable local video file.
- [ ] The learner can explain quality and cost trade-offs versus HeyGen.

## Reflection questions

1. What did the agent or workflow do correctly on the first attempt?
2. What evidence proves the output was grounded, safe, or complete?
3. Which failure case was most useful for improving the workflow?
4. What should a human still review before this automation is used with real customers?

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| Service does not start | Python dependencies or paths are missing. | Use the README setup commands and verify Python version. |
| Video has no lip sync | The audio or image input was not passed to the renderer. | Check the render request payload and service logs. |
| ffmpeg error | ffmpeg is not installed or not on PATH. | Install ffmpeg and reopen the terminal. |

## Submission evidence

Submit the following:

- Workflow export or screenshot of the main workflow canvas.
- Screenshot or copy of the successful execution output.
- One normal test case and one edge or unsafe test case.
- A short note explaining what you changed after evaluation.

## Lab deliverable

A free local avatar video and comparison notes.
