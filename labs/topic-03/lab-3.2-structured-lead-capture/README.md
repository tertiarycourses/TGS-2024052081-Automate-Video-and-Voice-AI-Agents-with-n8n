# Lab 3.2 - Add Structured Lead Capture

> Topic 3 - Approximately 60 minutes - Adult workplace lab

## The build so far

This lab is part of a complete agentic AI automation course. Each lab follows the same engineering loop:

**Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

In this lab you build: **A CX agent that extracts name, email, course interest, and urgency into a structured payload.**

## What you will build

A CX agent that extracts name, email, course interest, and urgency into a structured payload. The work is intentionally practical: by the end of the lab you should have an artifact that can be inspected, tested, and reused in the capstone.

## Concepts you will meet

| Concept | In one line |
|---|---|
| Structured output | Turns conversation into fields another system can use. |
| Validation | Checks required fields before handoff. |
| Consent | Asks permission before storing or sending contact data. |
| CRM handoff | Passes clean data to a downstream node or sheet. |

## Before you start

- Complete the setup in Lab 1.1 or confirm Docker, n8n, Ollama, and your browser are ready.
- Keep n8n executions visible while testing. The execution trace is your evidence.
- Do not place API keys in HTML, JavaScript, Markdown examples, screenshots, or exported workflow notes.
- Commit or export a checkpoint before making large workflow changes.

## Step-by-step instructions

1. Duplicate the course advisory workflow.
2. Add an Edit Fields or Set node after the agent to shape lead fields.
3. Prompt the agent to ask for missing required fields one at a time.
4. Add a consent question before collecting email or phone.
5. Test with a learner who gives incomplete information.
6. Inspect the final JSON payload and revise field names for clarity.

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
I am completing Add Structured Lead Capture in the course "Automate Video and Voice AI Agents with n8n".
Act as a careful agentic AI workflow reviewer. Review my workflow design against this goal:
A CX agent that extracts name, email, course interest, and urgency into a structured payload.

Check for:
- missing trigger, input, output, or credential boundary
- weak system prompt or unclear tool description
- missing evaluation case, refusal case, or human review gate
- any place where a secret could leak to browser code or exported notes

Return a concise list of fixes, then give me one improved test case.
```

## Verify

- [ ] The workflow does not hand off a lead until required fields are present.
- [ ] The agent asks for consent before contact capture.
- [ ] The resulting payload has stable field names and no extra prose.

## Reflection questions

1. What did the agent or workflow do correctly on the first attempt?
2. What evidence proves the output was grounded, safe, or complete?
3. Which failure case was most useful for improving the workflow?
4. What should a human still review before this automation is used with real customers?

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| Lead payload contains paragraphs | The agent was not instructed to separate conversation from data. | Use a structured output instruction and post-process with fields. |
| Agent asks too many questions | Required fields are not prioritized. | Collect only the minimum needed for follow-up. |
| Consent is skipped | It was placed after data capture. | Move consent before requesting contact details. |

## Submission evidence

Submit the following:

- Workflow export or screenshot of the main workflow canvas.
- Screenshot or copy of the successful execution output.
- One normal test case and one edge or unsafe test case.
- A short note explaining what you changed after evaluation.

## Lab deliverable

A structured lead capture branch ready for CRM or spreadsheet integration.
