# Lab 6.3 - Monitor, Debug, and Recover AI Workflows

> Topic 6 - Approximately 60 minutes - Adult workplace lab

## The build so far

This lab is part of a complete agentic AI automation course. Each lab follows the same engineering loop:

**Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

In this lab you build: **A monitoring checklist for failed executions, retries, and provider outages.**

## What you will build

A monitoring checklist for failed executions, retries, and provider outages. The work is intentionally practical: by the end of the lab you should have an artifact that can be inspected, tested, and reused in the capstone.

## Concepts you will meet

| Concept | In one line |
|---|---|
| Failure mode | A predictable way a workflow can break. |
| Retry policy | Defines when to try again and when to stop. |
| Fallback provider | Keeps service running with a lower-quality or local option. |
| Runbook | A short procedure another person can follow during an incident. |

## Before you start

- Complete the setup in Lab 1.1 or confirm Docker, n8n, Ollama, and your browser are ready.
- Keep n8n executions visible while testing. The execution trace is your evidence.
- Do not place API keys in HTML, JavaScript, Markdown examples, screenshots, or exported workflow notes.
- Commit or export a checkpoint before making large workflow changes.

## Step-by-step instructions

1. List failure modes for LLM, vector store, Retell, HeyGen, Replicate, and YouTube.
2. For each failure, define retry, fallback, and human notification behavior.
3. Add an error branch to one existing workflow.
4. Simulate a failed API call using a wrong key or test URL, then restore it.
5. Write a runbook with symptoms, first checks, and recovery steps.
6. Review the runbook with another learner and close unclear steps.

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
I am completing Monitor, Debug, and Recover AI Workflows in the course "Automate Video and Voice AI Agents with n8n".
Act as a careful agentic AI workflow reviewer. Review my workflow design against this goal:
A monitoring checklist for failed executions, retries, and provider outages.

Check for:
- missing trigger, input, output, or credential boundary
- weak system prompt or unclear tool description
- missing evaluation case, refusal case, or human review gate
- any place where a secret could leak to browser code or exported notes

Return a concise list of fixes, then give me one improved test case.
```

## Verify

- [ ] At least one workflow has an error branch.
- [ ] The runbook covers credentials, quota, network, payload, and provider status.
- [ ] The fallback decision is explicit, not improvised during failure.

## Reflection questions

1. What did the agent or workflow do correctly on the first attempt?
2. What evidence proves the output was grounded, safe, or complete?
3. Which failure case was most useful for improving the workflow?
4. What should a human still review before this automation is used with real customers?

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| Errors disappear | Failed executions are not saved. | Enable failed execution saving during development. |
| Workflow retries forever | No stop condition exists. | Limit retries and notify a human after threshold. |
| Fallback is unclear | No provider decision was made. | Choose local HyperFrames, open-source avatar, or manual review as fallback. |

## Submission evidence

Submit the following:

- Workflow export or screenshot of the main workflow canvas.
- Screenshot or copy of the successful execution output.
- One normal test case and one edge or unsafe test case.
- A short note explaining what you changed after evaluation.

## Lab deliverable

A monitoring runbook and one tested error branch.
