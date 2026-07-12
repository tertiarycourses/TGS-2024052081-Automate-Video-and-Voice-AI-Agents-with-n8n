# Lab 3.4 - Add Safety Guardrails and Escalation

> Topic 3 - Approximately 60 minutes - Adult workplace lab

## The build so far

This lab is part of a complete agentic AI automation course. Each lab follows the same engineering loop:

**Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

In this lab you build: **A guardrailed CX agent with refusal, escalation, and audit notes.**

## What you will build

A guardrailed CX agent with refusal, escalation, and audit notes. The work is intentionally practical: by the end of the lab you should have an artifact that can be inspected, tested, and reused in the capstone.

## Concepts you will meet

| Concept | In one line |
|---|---|
| Policy boundary | Defines what the agent must not answer or promise. |
| Escalation trigger | Routes sensitive or high-value requests to a human. |
| Audit note | Records why the workflow took a path. |
| Prompt injection defense | Tells the agent to ignore user attempts to override system rules. |

## Before you start

- Complete the setup in Lab 1.1 or confirm Docker, n8n, Ollama, and your browser are ready.
- Keep n8n executions visible while testing. The execution trace is your evidence.
- Do not place API keys in HTML, JavaScript, Markdown examples, screenshots, or exported workflow notes.
- Commit or export a checkpoint before making large workflow changes.

## Step-by-step instructions

1. List five prohibited actions for the CX agent, such as guaranteeing admission or inventing subsidies.
2. Add the prohibited actions to the system message using direct language.
3. Add escalation wording for complaints, refunds, legal questions, and personal data concerns.
4. Create test prompts that attempt to override the system instruction.
5. Run the tests and record whether the agent refused, answered, or escalated.
6. Revise the prompt until all tests pass.

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
I am completing Add Safety Guardrails and Escalation in the course "Automate Video and Voice AI Agents with n8n".
Act as a careful agentic AI workflow reviewer. Review my workflow design against this goal:
A guardrailed CX agent with refusal, escalation, and audit notes.

Check for:
- missing trigger, input, output, or credential boundary
- weak system prompt or unclear tool description
- missing evaluation case, refusal case, or human review gate
- any place where a secret could leak to browser code or exported notes

Return a concise list of fixes, then give me one improved test case.
```

## Verify

- [ ] Prompt injection attempts do not override the agent role.
- [ ] Sensitive requests are escalated with useful context.
- [ ] The audit note explains the reason for refusal or escalation.

## Reflection questions

1. What did the agent or workflow do correctly on the first attempt?
2. What evidence proves the output was grounded, safe, or complete?
3. Which failure case was most useful for improving the workflow?
4. What should a human still review before this automation is used with real customers?

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| Agent apologizes but still answers | The refusal rule is too soft. | State the prohibited behavior and required alternative response. |
| Everything escalates | Escalation triggers are too broad. | Separate low-risk FAQ from sensitive cases. |
| Audit note is missing | No branch records the decision. | Add a Set node that captures decision type and reason. |

## Submission evidence

Submit the following:

- Workflow export or screenshot of the main workflow canvas.
- Screenshot or copy of the successful execution output.
- One normal test case and one edge or unsafe test case.
- A short note explaining what you changed after evaluation.

## Lab deliverable

A guardrail test set and passing CX workflow.
