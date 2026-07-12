# Lab 3.1 - Build a Course Advisory CX Agent

> Topic 3 - Approximately 75 minutes - Adult workplace lab

## The build so far

This lab is part of a complete agentic AI automation course. Each lab follows the same engineering loop:

**Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

In this lab you build: **A customer-facing course advisory chatbot over 20 academy brochures.**

## What you will build

A customer-facing course advisory chatbot over 20 academy brochures. The work is intentionally practical: by the end of the lab you should have an artifact that can be inspected, tested, and reused in the capstone.

## Concepts you will meet

| Concept | In one line |
|---|---|
| Domain grounding | Restricts answers to approved business documents. |
| Customer context | Keeps tone practical and service oriented. |
| Brochure ingestion | Loads multiple text documents into a vector store. |
| Session continuity | Supports follow-up questions in a website chat. |

## Before you start

- Complete the setup in Lab 1.1 or confirm Docker, n8n, Ollama, and your browser are ready.
- Keep n8n executions visible while testing. The execution trace is your evidence.
- Do not place API keys in HTML, JavaScript, Markdown examples, screenshots, or exported workflow notes.
- Commit or export a checkpoint before making large workflow changes.

## Step-by-step instructions

1. Import `lab3/CX Agent with RAG.json`.
2. Activate the workflow and confirm the brochure upload webhook URL.
3. Open `lab3/upload-brochures.html` and upload all 20 brochure text files.
4. Open `lab3/website/index.html` and start a customer chat.
5. Ask about course fees, duration, campus, and suitable learner profile.
6. Refine the system prompt so answers are concise, polite, and grounded in brochure facts.

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
I am completing Build a Course Advisory CX Agent in the course "Automate Video and Voice AI Agents with n8n".
Act as a careful agentic AI workflow reviewer. Review my workflow design against this goal:
A customer-facing course advisory chatbot over 20 academy brochures.

Check for:
- missing trigger, input, output, or credential boundary
- weak system prompt or unclear tool description
- missing evaluation case, refusal case, or human review gate
- any place where a secret could leak to browser code or exported notes

Return a concise list of fixes, then give me one improved test case.
```

## Verify

- [ ] The website chatbot returns exact details from the brochures.
- [ ] Follow-up questions work within the same browser session.
- [ ] The agent refuses to invent discounts, schedules, or policies not in the documents.

## Reflection questions

1. What did the agent or workflow do correctly on the first attempt?
2. What evidence proves the output was grounded, safe, or complete?
3. Which failure case was most useful for improving the workflow?
4. What should a human still review before this automation is used with real customers?

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| Tool call fails | Tool node name contains special characters. | Rename tool nodes using letters, numbers, and spaces only. |
| All courses sound the same | Retrieval is not specific enough. | Ask for exact course code or increase retrieval specificity in the prompt. |
| CORS or webhook error | The workflow is inactive or URL is not production webhook. | Activate and copy the production webhook path. |

## Submission evidence

Submit the following:

- Workflow export or screenshot of the main workflow canvas.
- Screenshot or copy of the successful execution output.
- One normal test case and one edge or unsafe test case.
- A short note explaining what you changed after evaluation.

## Lab deliverable

A working course advisory chatbot embedded in the sample website.
