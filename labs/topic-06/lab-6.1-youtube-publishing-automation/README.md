# Lab 6.1 - Publish the Avatar Video to YouTube

> Topic 6 - Approximately 75 minutes - Adult workplace lab

## The build so far

This lab is part of a complete agentic AI automation course. Each lab follows the same engineering loop:

**Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

In this lab you build: **An n8n publishing workflow that uploads a generated video with metadata.**

## What you will build

An n8n publishing workflow that uploads a generated video with metadata. The work is intentionally practical: by the end of the lab you should have an artifact that can be inspected, tested, and reused in the capstone.

## Concepts you will meet

| Concept | In one line |
|---|---|
| Publishing automation | Moves from generated asset to distribution channel. |
| OAuth credential | Authorizes YouTube upload without storing passwords. |
| Metadata | Defines title, description, tags, and visibility. |
| Review gate | Prevents unapproved videos from going public. |

## Before you start

- Complete the setup in Lab 1.1 or confirm Docker, n8n, Ollama, and your browser are ready.
- Keep n8n executions visible while testing. The execution trace is your evidence.
- Do not place API keys in HTML, JavaScript, Markdown examples, screenshots, or exported workflow notes.
- Commit or export a checkpoint before making large workflow changes.

## Step-by-step instructions

1. Create or import the YouTube upload workflow for Lab 6.
2. Configure the YouTube OAuth credential in n8n.
3. Use a generated video file or URL from a previous lab.
4. Prepare title, description, tags, and visibility as workflow fields.
5. Add a manual review gate before upload.
6. Run an unlisted upload test and verify it appears in YouTube Studio.

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
I am completing Publish the Avatar Video to YouTube in the course "Automate Video and Voice AI Agents with n8n".
Act as a careful agentic AI workflow reviewer. Review my workflow design against this goal:
An n8n publishing workflow that uploads a generated video with metadata.

Check for:
- missing trigger, input, output, or credential boundary
- weak system prompt or unclear tool description
- missing evaluation case, refusal case, or human review gate
- any place where a secret could leak to browser code or exported notes

Return a concise list of fixes, then give me one improved test case.
```

## Verify

- [ ] The workflow uploads a video as unlisted or private first.
- [ ] Metadata is populated from workflow fields.
- [ ] A review gate exists before public publishing.

## Reflection questions

1. What did the agent or workflow do correctly on the first attempt?
2. What evidence proves the output was grounded, safe, or complete?
3. Which failure case was most useful for improving the workflow?
4. What should a human still review before this automation is used with real customers?

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| OAuth fails | Consent screen or redirect URL is not configured. | Follow n8n credential instructions and retry authorization. |
| Video upload rejected | File URL is inaccessible or format unsupported. | Download the file locally or provide an MP4 path. |
| Wrong visibility | Default visibility was not set intentionally. | Use private or unlisted during training. |

## Submission evidence

Submit the following:

- Workflow export or screenshot of the main workflow canvas.
- Screenshot or copy of the successful execution output.
- One normal test case and one edge or unsafe test case.
- A short note explaining what you changed after evaluation.

## Lab deliverable

An unlisted YouTube upload test with approved metadata.
