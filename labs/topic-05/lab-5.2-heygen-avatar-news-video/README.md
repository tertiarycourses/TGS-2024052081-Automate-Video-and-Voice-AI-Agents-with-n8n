# Lab 5.2 - Generate an Avatar News Video with HeyGen

> Topic 5 - Approximately 75 minutes - Adult workplace lab

## The build so far

This lab is part of a complete agentic AI automation course. Each lab follows the same engineering loop:

**Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

In this lab you build: **A HeyGen avatar video created from an AI-generated script.**

## What you will build

A HeyGen avatar video created from an AI-generated script. The work is intentionally practical: by the end of the lab you should have an artifact that can be inspected, tested, and reused in the capstone.

## Concepts you will meet

| Concept | In one line |
|---|---|
| Avatar video | Combines script, voice, presenter identity, and scene direction. |
| API credential | Lets n8n call HeyGen without exposing the key in browser code. |
| Generation status | Polls or waits until the video is ready. |
| Result handoff | Stores the generated video URL for review or publishing. |

## Before you start

- Complete the setup in Lab 1.1 or confirm Docker, n8n, Ollama, and your browser are ready.
- Keep n8n executions visible while testing. The execution trace is your evidence.
- Do not place API keys in HTML, JavaScript, Markdown examples, screenshots, or exported workflow notes.
- Commit or export a checkpoint before making large workflow changes.

## Step-by-step instructions

1. Import `lab6/heygen-news-avatar-flow.json`.
2. Create the HeyGen credential or API key variable required by the workflow.
3. Review the script generation node and video generation node.
4. Run the workflow with a short news topic.
5. Wait for the video result and open it for review.
6. Record quality notes: pronunciation, timing, visual relevance, and brand fit.

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
I am completing Generate an Avatar News Video with HeyGen in the course "Automate Video and Voice AI Agents with n8n".
Act as a careful agentic AI workflow reviewer. Review my workflow design against this goal:
A HeyGen avatar video created from an AI-generated script.

Check for:
- missing trigger, input, output, or credential boundary
- weak system prompt or unclear tool description
- missing evaluation case, refusal case, or human review gate
- any place where a secret could leak to browser code or exported notes

Return a concise list of fixes, then give me one improved test case.
```

## Verify

- [ ] The workflow produces a playable HeyGen video URL or file.
- [ ] Credentials remain server-side in n8n.
- [ ] Quality notes identify at least one prompt improvement.

## Reflection questions

1. What did the agent or workflow do correctly on the first attempt?
2. What evidence proves the output was grounded, safe, or complete?
3. Which failure case was most useful for improving the workflow?
4. What should a human still review before this automation is used with real customers?

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| Video generation fails | API key, quota, or payload fields are invalid. | Check credential status and run a shorter test script. |
| Avatar mispronounces names | No pronunciation guidance was supplied. | Add phonetic spelling or choose a more suitable voice. |
| Video is off-brand | Prompt lacks style and brand constraints. | Add tone, audience, and visual rules from the creative brief. |

## Submission evidence

Submit the following:

- Workflow export or screenshot of the main workflow canvas.
- Screenshot or copy of the successful execution output.
- One normal test case and one edge or unsafe test case.
- A short note explaining what you changed after evaluation.

## Lab deliverable

A generated avatar news video and quality review notes.
