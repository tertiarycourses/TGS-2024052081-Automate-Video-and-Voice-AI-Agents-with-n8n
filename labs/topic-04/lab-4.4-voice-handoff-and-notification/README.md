# Lab 4.4 - Add Human Handoff and Notifications

> Topic 4 - Approximately 60 minutes - Adult workplace lab

## The build so far

This lab is part of a complete agentic AI automation course. Each lab follows the same engineering loop:

**Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

In this lab you build: **A voice workflow that notifies staff when a booking or escalation is needed.**

## What you will build

A voice workflow that notifies staff when a booking or escalation is needed. The work is intentionally practical: by the end of the lab you should have an artifact that can be inspected, tested, and reused in the capstone.

## Concepts you will meet

| Concept | In one line |
|---|---|
| Handoff payload | Summarizes caller intent and captured details. |
| Notification channel | Sends the next action to email, chat, or a sheet. |
| Escalation reason | Explains why the human needs to act. |
| SLA thinking | States how quickly the team should respond. |

## Before you start

- Complete the setup in Lab 1.1 or confirm Docker, n8n, Ollama, and your browser are ready.
- Keep n8n executions visible while testing. The execution trace is your evidence.
- Do not place API keys in HTML, JavaScript, Markdown examples, screenshots, or exported workflow notes.
- Commit or export a checkpoint before making large workflow changes.

## Step-by-step instructions

1. Add a handoff branch after the voice call or booking tool branch.
2. Shape a payload with caller summary, captured slots, urgency, and transcript link if available.
3. Send the payload to a simple destination such as email, spreadsheet, or local webhook test endpoint.
4. Create two paths: confirmed booking and escalation.
5. Test both paths with sample call data.
6. Add a workflow note stating the response SLA and owner.

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
I am completing Add Human Handoff and Notifications in the course "Automate Video and Voice AI Agents with n8n".
Act as a careful agentic AI workflow reviewer. Review my workflow design against this goal:
A voice workflow that notifies staff when a booking or escalation is needed.

Check for:
- missing trigger, input, output, or credential boundary
- weak system prompt or unclear tool description
- missing evaluation case, refusal case, or human review gate
- any place where a secret could leak to browser code or exported notes

Return a concise list of fixes, then give me one improved test case.
```

## Verify

- [ ] Confirmed bookings create a staff notification.
- [ ] Escalations include a reason and summary.
- [ ] The notification does not expose unnecessary personal data.

## Reflection questions

1. What did the agent or workflow do correctly on the first attempt?
2. What evidence proves the output was grounded, safe, or complete?
3. Which failure case was most useful for improving the workflow?
4. What should a human still review before this automation is used with real customers?

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| Notification is unreadable | Raw transcript was sent without summary. | Add a concise structured summary before sending. |
| Every call notifies staff | Branch conditions are too broad. | Separate completed self-service calls from handoff cases. |
| Sensitive data is overshared | Payload includes full transcript by default. | Send only fields required for follow-up. |

## Submission evidence

Submit the following:

- Workflow export or screenshot of the main workflow canvas.
- Screenshot or copy of the successful execution output.
- One normal test case and one edge or unsafe test case.
- A short note explaining what you changed after evaluation.

## Lab deliverable

A staff handoff branch for bookings and escalations.
