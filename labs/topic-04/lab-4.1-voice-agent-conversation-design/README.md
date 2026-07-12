# Lab 4.1 - Design a Voice Agent Conversation

> Topic 4 - Approximately 60 minutes - Adult workplace lab

## The build so far

This lab is part of a complete agentic AI automation course. Each lab follows the same engineering loop:

**Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

In this lab you build: **A voice-agent script with opening, slot filling, repair, and closing paths.**

## What you will build

A voice-agent script with opening, slot filling, repair, and closing paths. The work is intentionally practical: by the end of the lab you should have an artifact that can be inspected, tested, and reused in the capstone.

## Concepts you will meet

| Concept | In one line |
|---|---|
| Voice turn-taking | Keeps prompts short so callers know when to speak. |
| Slot filling | Collects required booking details naturally. |
| Repair strategy | Handles unclear or missing caller responses. |
| Persona | Defines tone without overloading the voice model. |

## Before you start

- Complete the setup in Lab 1.1 or confirm Docker, n8n, Ollama, and your browser are ready.
- Keep n8n executions visible while testing. The execution trace is your evidence.
- Do not place API keys in HTML, JavaScript, Markdown examples, screenshots, or exported workflow notes.
- Commit or export a checkpoint before making large workflow changes.

## Step-by-step instructions

1. Choose the service scenario for the Retell voice agent.
2. Write a one-sentence persona and three behavior rules.
3. List required slots: name, service, date, time, and contact method.
4. Write the opening line, slot questions, repair prompts, confirmation, and closing.
5. Read the script aloud and remove long sentences.
6. Create a test call checklist for normal, noisy, and incomplete caller behavior.

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
I am completing Design a Voice Agent Conversation in the course "Automate Video and Voice AI Agents with n8n".
Act as a careful agentic AI workflow reviewer. Review my workflow design against this goal:
A voice-agent script with opening, slot filling, repair, and closing paths.

Check for:
- missing trigger, input, output, or credential boundary
- weak system prompt or unclear tool description
- missing evaluation case, refusal case, or human review gate
- any place where a secret could leak to browser code or exported notes

Return a concise list of fixes, then give me one improved test case.
```

## Verify

- [ ] The script can be spoken naturally in under one minute for a simple booking.
- [ ] Every required slot has a question and a repair prompt.
- [ ] The agent confirms before creating the booking request.

## Reflection questions

1. What did the agent or workflow do correctly on the first attempt?
2. What evidence proves the output was grounded, safe, or complete?
3. Which failure case was most useful for improving the workflow?
4. What should a human still review before this automation is used with real customers?

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| Caller gets interrupted | Prompts are too long or multi-part. | Ask one question at a time. |
| Agent sounds robotic | Persona has too many adjectives. | Use two or three concrete behavior rules. |
| Booking details are incomplete | Slot list and confirmation are not aligned. | Confirm every required field before handoff. |

## Submission evidence

Submit the following:

- Workflow export or screenshot of the main workflow canvas.
- Screenshot or copy of the successful execution output.
- One normal test case and one edge or unsafe test case.
- A short note explaining what you changed after evaluation.

## Lab deliverable

A tested voice conversation design script.
