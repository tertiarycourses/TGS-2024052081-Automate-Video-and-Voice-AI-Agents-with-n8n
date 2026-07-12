# Lab 6.2 - Embed an Interactive HeyGen Avatar

> Topic 6 - Approximately 75 minutes - Adult workplace lab

## The build so far

This lab is part of a complete agentic AI automation course. Each lab follows the same engineering loop:

**Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

In this lab you build: **A real-time avatar website that can speak with a visitor.**

## What you will build

A real-time avatar website that can speak with a visitor. The work is intentionally practical: by the end of the lab you should have an artifact that can be inspected, tested, and reused in the capstone.

## Concepts you will meet

| Concept | In one line |
|---|---|
| Interactive avatar | Supports real-time conversation instead of a pre-rendered video. |
| Session token | Starts the interactive experience securely. |
| Front-end embed | Connects the avatar session to the browser UI. |
| Conversation boundary | Keeps the live avatar within approved topics. |

## Before you start

- Complete the setup in Lab 1.1 or confirm Docker, n8n, Ollama, and your browser are ready.
- Keep n8n executions visible while testing. The execution trace is your evidence.
- Do not place API keys in HTML, JavaScript, Markdown examples, screenshots, or exported workflow notes.
- Commit or export a checkpoint before making large workflow changes.

## Step-by-step instructions

1. Open the Lab 8 website files and identify the token or session endpoint.
2. Configure the n8n or backend side that creates interactive avatar sessions.
3. Load the website locally and start an avatar session.
4. Ask course-related and unrelated questions.
5. Tune the avatar prompt for concise responses and safe boundaries.
6. Document browser, microphone, and account requirements for learners.

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
I am completing Embed an Interactive HeyGen Avatar in the course "Automate Video and Voice AI Agents with n8n".
Act as a careful agentic AI workflow reviewer. Review my workflow design against this goal:
A real-time avatar website that can speak with a visitor.

Check for:
- missing trigger, input, output, or credential boundary
- weak system prompt or unclear tool description
- missing evaluation case, refusal case, or human review gate
- any place where a secret could leak to browser code or exported notes

Return a concise list of fixes, then give me one improved test case.
```

## Verify

- [ ] The browser starts a live avatar session.
- [ ] The avatar stays within the approved course-advisory role.
- [ ] The learner can explain how this differs from a rendered video.

## Reflection questions

1. What did the agent or workflow do correctly on the first attempt?
2. What evidence proves the output was grounded, safe, or complete?
3. Which failure case was most useful for improving the workflow?
4. What should a human still review before this automation is used with real customers?

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| Avatar does not start | Session token creation failed. | Check credential, quota, and endpoint response. |
| Browser blocks audio | Autoplay or microphone permission was blocked. | Interact with the page and allow permissions. |
| Avatar answers outside scope | Prompt lacks boundaries. | Add role, refusal, and escalation instructions. |

## Submission evidence

Submit the following:

- Workflow export or screenshot of the main workflow canvas.
- Screenshot or copy of the successful execution output.
- One normal test case and one edge or unsafe test case.
- A short note explaining what you changed after evaluation.

## Lab deliverable

A working interactive avatar demo and prompt notes.
