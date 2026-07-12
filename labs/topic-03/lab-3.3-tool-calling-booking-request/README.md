# Lab 3.3 - Create a Tool-Calling Booking Request Agent

> Topic 3 - Approximately 60 minutes - Adult workplace lab

## The build so far

This lab is part of a complete agentic AI automation course. Each lab follows the same engineering loop:

**Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

In this lab you build: **An agent that prepares a booking request and calls a mock booking tool.**

## What you will build

An agent that prepares a booking request and calls a mock booking tool. The work is intentionally practical: by the end of the lab you should have an artifact that can be inspected, tested, and reused in the capstone.

## Concepts you will meet

| Concept | In one line |
|---|---|
| Tool calling | Lets the agent request an action through a controlled workflow path. |
| Argument schema | Defines exactly what the tool needs. |
| Confirmation before action | Prevents accidental bookings. |
| Mock integration | Tests business logic before connecting a real system. |

## Before you start

- Complete the setup in Lab 1.1 or confirm Docker, n8n, Ollama, and your browser are ready.
- Keep n8n executions visible while testing. The execution trace is your evidence.
- Do not place API keys in HTML, JavaScript, Markdown examples, screenshots, or exported workflow notes.
- Commit or export a checkpoint before making large workflow changes.

## Step-by-step instructions

1. Create a mock booking tool branch in n8n with fields for service, date, time, name, and contact.
2. Connect the tool to the AI Agent.
3. Write a tool description that clearly states when it should be used.
4. Require the agent to summarize the booking and ask for confirmation before calling the tool.
5. Run one complete booking scenario and one cancellation scenario.
6. Review executions to confirm the tool was called only after confirmation.

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
I am completing Create a Tool-Calling Booking Request Agent in the course "Automate Video and Voice AI Agents with n8n".
Act as a careful agentic AI workflow reviewer. Review my workflow design against this goal:
An agent that prepares a booking request and calls a mock booking tool.

Check for:
- missing trigger, input, output, or credential boundary
- weak system prompt or unclear tool description
- missing evaluation case, refusal case, or human review gate
- any place where a secret could leak to browser code or exported notes

Return a concise list of fixes, then give me one improved test case.
```

## Verify

- [ ] Tool arguments are complete and correctly typed.
- [ ] The agent does not call the tool before user confirmation.
- [ ] The mock branch receives one clean payload per confirmed booking.

## Reflection questions

1. What did the agent or workflow do correctly on the first attempt?
2. What evidence proves the output was grounded, safe, or complete?
3. Which failure case was most useful for improving the workflow?
4. What should a human still review before this automation is used with real customers?

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| Tool called too early | The prompt does not require confirmation. | Add a hard rule: never call the tool until the user says yes. |
| Tool receives missing fields | The schema or prompt does not require all fields. | List required arguments in the tool description. |
| Tool name rejected | The name contains symbols or punctuation. | Use a simple name such as `Create Booking Request`. |

## Submission evidence

Submit the following:

- Workflow export or screenshot of the main workflow canvas.
- Screenshot or copy of the successful execution output.
- One normal test case and one edge or unsafe test case.
- A short note explaining what you changed after evaluation.

## Lab deliverable

A safe mock booking request workflow.
