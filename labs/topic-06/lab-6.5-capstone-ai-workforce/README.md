# Lab 6.5 - Capstone - Build a Human-AI Workforce Automation

> Topic 6 - Approximately 120 minutes - Adult workplace lab

## The build so far

This lab is part of a complete agentic AI automation course. Each lab follows the same engineering loop:

**Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

In this lab you build: **An end-to-end workflow that combines RAG, voice, video, publishing, and monitoring.**

## What you will build

An end-to-end workflow that combines RAG, voice, video, publishing, and monitoring. The work is intentionally practical: by the end of the lab you should have an artifact that can be inspected, tested, and reused in the capstone.

## Concepts you will meet

| Concept | In one line |
|---|---|
| System integration | Combines multiple agents and tools into one business process. |
| Human-in-the-loop | Places review gates where quality or risk requires judgement. |
| Operational handoff | Documents ownership, monitoring, and improvement process. |
| Portfolio evidence | Packages screenshots, exports, rubrics, and demo outputs. |

## Before you start

- Complete the setup in Lab 1.1 or confirm Docker, n8n, Ollama, and your browser are ready.
- Keep n8n executions visible while testing. The execution trace is your evidence.
- Do not place API keys in HTML, JavaScript, Markdown examples, screenshots, or exported workflow notes.
- Commit or export a checkpoint before making large workflow changes.

## Step-by-step instructions

1. Choose a capstone scenario such as course advisory, appointment booking, or training content production.
2. Draw the workflow from trigger to final output, including human review gates.
3. Reuse at least three previous lab components.
4. Add a quality rubric and run three test cases.
5. Fix the highest-risk failure discovered by testing.
6. Package the exported workflow, screenshots, video or call output, and a one-page operating guide.

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
I am completing Capstone - Build a Human-AI Workforce Automation in the course "Automate Video and Voice AI Agents with n8n".
Act as a careful agentic AI workflow reviewer. Review my workflow design against this goal:
An end-to-end workflow that combines RAG, voice, video, publishing, and monitoring.

Check for:
- missing trigger, input, output, or credential boundary
- weak system prompt or unclear tool description
- missing evaluation case, refusal case, or human review gate
- any place where a secret could leak to browser code or exported notes

Return a concise list of fixes, then give me one improved test case.
```

## Verify

- [ ] The capstone completes a realistic business process end to end.
- [ ] At least three agentic loop components are integrated.
- [ ] Evidence includes test cases, evaluation results, and improvement notes.

## Reflection questions

1. What did the agent or workflow do correctly on the first attempt?
2. What evidence proves the output was grounded, safe, or complete?
3. Which failure case was most useful for improving the workflow?
4. What should a human still review before this automation is used with real customers?

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| Capstone is too broad | It tries to automate an entire department. | Reduce it to one trigger, one primary user, and one output. |
| No review gate | The workflow publishes or contacts people automatically. | Add approval before external publishing or customer communication. |
| Demo is fragile | It depends on many paid services at once. | Prepare a fallback path and a recorded output. |

## Submission evidence

Submit the following:

- Workflow export or screenshot of the main workflow canvas.
- Screenshot or copy of the successful execution output.
- One normal test case and one edge or unsafe test case.
- A short note explaining what you changed after evaluation.

## Lab deliverable

A capstone package suitable for trainer assessment and learner portfolio.
