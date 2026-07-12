# Lab 2.2 - Add Memory and Session Design

> Topic 2 - Approximately 45 minutes - Adult workplace lab

## The build so far

This lab is part of a complete agentic AI automation course. Each lab follows the same engineering loop:

**Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

In this lab you build: **A chat agent that remembers context within a learner session and forgets across sessions.**

## What you will build

A chat agent that remembers context within a learner session and forgets across sessions. The work is intentionally practical: by the end of the lab you should have an artifact that can be inspected, tested, and reused in the capstone.

## Concepts you will meet

| Concept | In one line |
|---|---|
| Conversation memory | Stores recent turns so follow-up questions make sense. |
| Session ID | Separates one user conversation from another. |
| Memory window | Limits cost and prevents old irrelevant context from dominating. |
| Privacy boundary | Defines what should not be stored. |

## Before you start

- Complete the setup in Lab 1.1 or confirm Docker, n8n, Ollama, and your browser are ready.
- Keep n8n executions visible while testing. The execution trace is your evidence.
- Do not place API keys in HTML, JavaScript, Markdown examples, screenshots, or exported workflow notes.
- Commit or export a checkpoint before making large workflow changes.

## Step-by-step instructions

1. Duplicate the Lab 2.1 workflow and rename it with `memory` in the title.
2. Add a Simple Memory node to the AI Agent memory port.
3. Set a session key using the chat session or a fixed learner test ID.
4. Tell the agent your name and role, then ask a follow-up question without repeating them.
5. Start a second session and confirm the first session details do not leak.
6. Add a note listing what data is acceptable to remember during training.

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
I am completing Add Memory and Session Design in the course "Automate Video and Voice AI Agents with n8n".
Act as a careful agentic AI workflow reviewer. Review my workflow design against this goal:
A chat agent that remembers context within a learner session and forgets across sessions.

Check for:
- missing trigger, input, output, or credential boundary
- weak system prompt or unclear tool description
- missing evaluation case, refusal case, or human review gate
- any place where a secret could leak to browser code or exported notes

Return a concise list of fixes, then give me one improved test case.
```

## Verify

- [ ] Follow-up questions work inside the same session.
- [ ] A separate session does not receive the first user's details.
- [ ] The workflow note describes memory scope and privacy limits.

## Reflection questions

1. What did the agent or workflow do correctly on the first attempt?
2. What evidence proves the output was grounded, safe, or complete?
3. Which failure case was most useful for improving the workflow?
4. What should a human still review before this automation is used with real customers?

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| The agent forgets immediately | Memory is not connected to the AI Agent memory port. | Reconnect the Simple Memory node and rerun. |
| Sessions leak together | All users share the same session key. | Use a per-user or per-browser session ID. |
| Old messages dominate | Memory window is too large for the task. | Reduce the number of retained turns. |

## Submission evidence

Submit the following:

- Workflow export or screenshot of the main workflow canvas.
- Screenshot or copy of the successful execution output.
- One normal test case and one edge or unsafe test case.
- A short note explaining what you changed after evaluation.

## Lab deliverable

A memory-enabled agent and a privacy note.
