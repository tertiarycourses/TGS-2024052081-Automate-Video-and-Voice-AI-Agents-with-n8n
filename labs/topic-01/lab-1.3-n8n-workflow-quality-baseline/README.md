# Lab 1.3 - Create a Workflow Quality Baseline

> Topic 1 - Approximately 45 minutes - Adult workplace lab

## The build so far

This lab is part of a complete agentic AI automation course. Each lab follows the same engineering loop:

**Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

In this lab you build: **A reusable pre-flight checklist and execution log habit for every n8n workflow.**

## What you will build

A reusable pre-flight checklist and execution log habit for every n8n workflow. The work is intentionally practical: by the end of the lab you should have an artifact that can be inspected, tested, and reused in the capstone.

## Concepts you will meet

| Concept | In one line |
|---|---|
| Execution trace | The evidence trail used to debug an automation. |
| Credential separation | Secrets live in credentials, never in browser code or exported notes. |
| Small test cases | Inputs designed to reveal one behavior at a time. |
| Versioned checkpoints | Saved workflow exports before risky changes. |

## Before you start

- Complete the setup in Lab 1.1 or confirm Docker, n8n, Ollama, and your browser are ready.
- Keep n8n executions visible while testing. The execution trace is your evidence.
- Do not place API keys in HTML, JavaScript, Markdown examples, screenshots, or exported workflow notes.
- Commit or export a checkpoint before making large workflow changes.

## Step-by-step instructions

1. Create a folder named `course-checkpoints` outside the repo for local exported workflows.
2. In n8n, enable execution saving for successful and failed runs while developing.
3. Create a workflow note template with purpose, trigger, inputs, expected outputs, and rollback plan.
4. Run a tiny webhook echo workflow and export it as the first checkpoint.
5. Record three test cases: normal input, missing input, and malicious or irrelevant input.
6. Review the execution data and identify which node proves the expected behavior.

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
I am completing Create a Workflow Quality Baseline in the course "Automate Video and Voice AI Agents with n8n".
Act as a careful agentic AI workflow reviewer. Review my workflow design against this goal:
A reusable pre-flight checklist and execution log habit for every n8n workflow.

Check for:
- missing trigger, input, output, or credential boundary
- weak system prompt or unclear tool description
- missing evaluation case, refusal case, or human review gate
- any place where a secret could leak to browser code or exported notes

Return a concise list of fixes, then give me one improved test case.
```

## Verify

- [ ] A learner can restore from the exported checkpoint.
- [ ] The test cases are specific enough to rerun after every edit.
- [ ] No API keys or secrets appear in notes, browser files, or JSON examples.

## Reflection questions

1. What did the agent or workflow do correctly on the first attempt?
2. What evidence proves the output was grounded, safe, or complete?
3. Which failure case was most useful for improving the workflow?
4. What should a human still review before this automation is used with real customers?

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| No execution data appears | Execution saving is disabled or the workflow did not run. | Enable saving and trigger the workflow again. |
| Export contains secrets | A credential or API key was placed in a regular field. | Move it to n8n credentials and rotate the key if it was exposed. |
| Tests are hard to repeat | Inputs were not recorded. | Save exact sample payloads and expected result text. |

## Submission evidence

Submit the following:

- Workflow export or screenshot of the main workflow canvas.
- Screenshot or copy of the successful execution output.
- One normal test case and one edge or unsafe test case.
- A short note explaining what you changed after evaluation.

## Lab deliverable

A baseline quality checklist plus a saved echo workflow checkpoint.
