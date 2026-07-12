# Lab 5.2 - Build a Video Script Agent

> Topic 5 - Approximately 60 minutes - Adult workplace lab

## The build so far

This lab is part of a complete agentic AI automation course. Each lab follows the same engineering loop:

**Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

In this lab you build: **An n8n workflow that turns a topic into a timed presenter video script.**

## What you will build

An n8n workflow that turns a topic into a timed presenter video script. The work is intentionally practical: by the end of the lab you should have an artifact that can be inspected, tested, and reused in the capstone.

## Concepts you will meet

| Concept | In one line |
|---|---|
| Creative brief | Defines audience, goal, length, tone, and call to action. |
| Timed script | Allocates seconds to scenes and narration. |
| Shot list | Converts words into visual direction. |
| Brand constraints | Keeps voice, claims, and style consistent. |

## Before you start

- Complete the setup in Lab 1.1 or confirm Docker, n8n, Ollama, and your browser are ready.
- Keep n8n executions visible while testing. The execution trace is your evidence.
- Do not place API keys in HTML, JavaScript, Markdown examples, screenshots, or exported workflow notes.
- Commit or export a checkpoint before making large workflow changes.

## Step-by-step instructions

1. Create or duplicate a workflow for script generation.
2. Add fields for target audience, duration, message, tone, and required facts.
3. Prompt the local model to output scene number, time range, voiceover, on-screen text, and visual direction.
4. Generate a 60-second script for a course announcement or news update.
5. Review for unsupported claims and timing overrun.
6. Revise the prompt so every scene has a visual purpose and every claim has a source.

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
I am completing Build a Video Script Agent in the course "Automate Video and Voice AI Agents with n8n".
Act as a careful agentic AI workflow reviewer. Review my workflow design against this goal:
An n8n workflow that turns a topic into a timed presenter video script.

Check for:
- missing trigger, input, output, or credential boundary
- weak system prompt or unclear tool description
- missing evaluation case, refusal case, or human review gate
- any place where a secret could leak to browser code or exported notes

Return a concise list of fixes, then give me one improved test case.
```

## Verify

- [ ] The script totals the requested duration.
- [ ] Every scene has narration and visual direction.
- [ ] The script avoids unverifiable promises.

## Reflection questions

1. What did the agent or workflow do correctly on the first attempt?
2. What evidence proves the output was grounded, safe, or complete?
3. Which failure case was most useful for improving the workflow?
4. What should a human still review before this automation is used with real customers?

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| Script is too long | The model was not constrained by time per scene. | Specify words per minute and scene duration. |
| Visuals are generic | The prompt asks only for narration. | Require camera, subject, motion, and background per scene. |
| Claims are risky | No evidence rule was provided. | Add a source and approved-claims constraint. |

## Submission evidence

Submit the following:

- Workflow export or screenshot of the main workflow canvas.
- Screenshot or copy of the successful execution output.
- One normal test case and one edge or unsafe test case.
- A short note explaining what you changed after evaluation.

## Lab deliverable

A timed script and shot list ready for video generation.
