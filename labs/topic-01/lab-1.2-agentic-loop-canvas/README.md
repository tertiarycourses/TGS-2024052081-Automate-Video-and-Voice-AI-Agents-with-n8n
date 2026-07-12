# Lab 1.2 - Map the Agentic AI Loop Before Building

> Topic 1 - Approximately 45 minutes - Adult workplace lab

## The build so far

This lab is part of a complete agentic AI automation course. Each lab follows the same engineering loop:

**Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

In this lab you build: **A one-page agent design canvas for a voice and video automation use case.**

## What you will build

A one-page agent design canvas for a voice and video automation use case. The work is intentionally practical: by the end of the lab you should have an artifact that can be inspected, tested, and reused in the capstone.

## Concepts you will meet

| Concept | In one line |
|---|---|
| Goal definition | Names the business outcome before selecting a model or API. |
| Tool boundary | States what the agent may and may not do. |
| Evaluation rubric | Defines what good output means before generation starts. |
| Human handoff | Identifies when the workflow must stop and ask for approval. |

## Before you start

- Complete the setup in Lab 1.1 or confirm Docker, n8n, Ollama, and your browser are ready.
- Keep n8n executions visible while testing. The execution trace is your evidence.
- Do not place API keys in HTML, JavaScript, Markdown examples, screenshots, or exported workflow notes.
- Commit or export a checkpoint before making large workflow changes.

## Step-by-step instructions

1. Choose one workplace scenario: customer support, course advisory, booking, training video, or sales follow-up.
2. Write the agent goal in one measurable sentence.
3. List inputs, tools, outputs, and forbidden actions.
4. Create a five-point evaluation rubric covering accuracy, tone, safety, completion, and traceability.
5. Convert the canvas into an n8n workflow note so the design travels with the automation.
6. Use an AI assistant to challenge the canvas, then revise weak assumptions.

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
I am completing Map the Agentic AI Loop Before Building in the course "Automate Video and Voice AI Agents with n8n".
Act as a careful agentic AI workflow reviewer. Review my workflow design against this goal:
A one-page agent design canvas for a voice and video automation use case.

Check for:
- missing trigger, input, output, or credential boundary
- weak system prompt or unclear tool description
- missing evaluation case, refusal case, or human review gate
- any place where a secret could leak to browser code or exported notes

Return a concise list of fixes, then give me one improved test case.
```

## Verify

- [ ] The canvas has a clear user, trigger, tool list, output, and stop condition.
- [ ] The evaluation rubric can be applied by another learner.
- [ ] At least two risks and two guardrails are documented.

## Reflection questions

1. What did the agent or workflow do correctly on the first attempt?
2. What evidence proves the output was grounded, safe, or complete?
3. Which failure case was most useful for improving the workflow?
4. What should a human still review before this automation is used with real customers?

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| The goal is too broad | It describes a department instead of a task. | Rewrite it as a single trigger-to-output workflow. |
| The agent has unlimited authority | No tool boundary was defined. | Add explicit allow and deny lists. |
| Rubric is vague | Words like good or professional are not testable. | Use observable criteria, examples, and pass or fail thresholds. |

## Submission evidence

Submit the following:

- Workflow export or screenshot of the main workflow canvas.
- Screenshot or copy of the successful execution output.
- One normal test case and one edge or unsafe test case.
- A short note explaining what you changed after evaluation.

## Lab deliverable

An agentic loop canvas ready to guide the remaining labs.
