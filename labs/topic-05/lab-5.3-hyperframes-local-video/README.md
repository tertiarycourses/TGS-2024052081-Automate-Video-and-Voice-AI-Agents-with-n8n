# Lab 5.3 - Create a Local Cinematic Video with HyperFrames

> Topic 5 - Approximately 75 minutes - Adult workplace lab

## The build so far

This lab is part of a complete agentic AI automation course. Each lab follows the same engineering loop:

**Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

In this lab you build: **A local HTML-rendered MP4 video using HyperFrames, audio, and a timed scene plan.**

## What you will build

A local HTML-rendered MP4 video using HyperFrames, audio, and a timed scene plan. The work is intentionally practical: by the end of the lab you should have an artifact that can be inspected, tested, and reused in the capstone.

## Concepts you will meet

| Concept | In one line |
|---|---|
| HTML composition | Defines scenes, layers, timing, and animation in a renderable document. |
| Timeline validation | Checks text, layout, and runtime errors before rendering. |
| Local render | Creates MP4 output without a cloud video API. |
| Contact sheet | Reviews key frames before committing to a long render. |

## Before you start

- Complete the setup in Lab 1.1 or confirm Docker, n8n, Ollama, and your browser are ready.
- Keep n8n executions visible while testing. The execution trace is your evidence.
- Do not place API keys in HTML, JavaScript, Markdown examples, screenshots, or exported workflow notes.
- Commit or export a checkpoint before making large workflow changes.

## Step-by-step instructions

1. Install or run the HyperFrames CLI with `npx hyperframes --help`.
2. Create a composition project for a 60-second training or commercial video.
3. Translate the script into timed layers: background, subject, product, captions, and closing card.
4. Run `npx hyperframes lint`, `validate`, `inspect`, and `snapshot`.
5. Review the contact sheet and fix text overflow or contrast problems.
6. Render the final MP4 and verify duration, resolution, and audio with `ffprobe`.

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
I am completing Create a Local Cinematic Video with HyperFrames in the course "Automate Video and Voice AI Agents with n8n".
Act as a careful agentic AI workflow reviewer. Review my workflow design against this goal:
A local HTML-rendered MP4 video using HyperFrames, audio, and a timed scene plan.

Check for:
- missing trigger, input, output, or credential boundary
- weak system prompt or unclear tool description
- missing evaluation case, refusal case, or human review gate
- any place where a secret could leak to browser code or exported notes

Return a concise list of fixes, then give me one improved test case.
```

## Verify

- [ ] Lint, validation, and layout inspection pass.
- [ ] The contact sheet shows the intended opening, middle, product, and closing frames.
- [ ] The final MP4 is 16:9 and close to the target duration.

## Reflection questions

1. What did the agent or workflow do correctly on the first attempt?
2. What evidence proves the output was grounded, safe, or complete?
3. Which failure case was most useful for improving the workflow?
4. What should a human still review before this automation is used with real customers?

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| Audio is silent | Timed audio elements lack stable IDs or paths are wrong. | Add IDs and verify local asset paths. |
| Text is clipped | Text sits inside a transformed or undersized container. | Move it to its own layer or increase the text box. |
| Render is slow | Resolution, frame rate, or effects are heavy. | Use draft quality for tests, then standard or high for final. |

## Submission evidence

Submit the following:

- Workflow export or screenshot of the main workflow canvas.
- Screenshot or copy of the successful execution output.
- One normal test case and one edge or unsafe test case.
- A short note explaining what you changed after evaluation.

## Lab deliverable

A local MP4 video plus contact sheet and validation results.
