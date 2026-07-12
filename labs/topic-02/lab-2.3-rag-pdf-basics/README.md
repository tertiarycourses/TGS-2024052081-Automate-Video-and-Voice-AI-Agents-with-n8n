# Lab 2.3 - Build a PDF RAG IT Support Agent

> Topic 2 - Approximately 75 minutes - Adult workplace lab

## The build so far

This lab is part of a complete agentic AI automation course. Each lab follows the same engineering loop:

**Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

In this lab you build: **A document-grounded chatbot over the sample IT FAQ PDF.**

## What you will build

A document-grounded chatbot over the sample IT FAQ PDF. The work is intentionally practical: by the end of the lab you should have an artifact that can be inspected, tested, and reused in the capstone.

## Concepts you will meet

| Concept | In one line |
|---|---|
| RAG | Retrieves relevant document chunks before generating an answer. |
| Embeddings | Convert text chunks into vectors for similarity search. |
| Vector store | Stores and retrieves document chunks. |
| Grounded refusal | Answers only from available evidence and declines unsupported questions. |

## Before you start

- Complete the setup in Lab 1.1 or confirm Docker, n8n, Ollama, and your browser are ready.
- Keep n8n executions visible while testing. The execution trace is your evidence.
- Do not place API keys in HTML, JavaScript, Markdown examples, screenshots, or exported workflow notes.
- Commit or export a checkpoint before making large workflow changes.

## Step-by-step instructions

1. Import `lab2/rag-flow.json` into n8n.
2. Select the Ollama credential in both chat and embedding nodes.
3. Open `lab2/index.html` in a browser.
4. Upload `lab2/it-faq.pdf` through the page and confirm the insert path runs.
5. Ask three questions that are answered in the PDF.
6. Ask one unrelated question and tune the system prompt so the agent refuses politely.

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
I am completing Build a PDF RAG IT Support Agent in the course "Automate Video and Voice AI Agents with n8n".
Act as a careful agentic AI workflow reviewer. Review my workflow design against this goal:
A document-grounded chatbot over the sample IT FAQ PDF.

Check for:
- missing trigger, input, output, or credential boundary
- weak system prompt or unclear tool description
- missing evaluation case, refusal case, or human review gate
- any place where a secret could leak to browser code or exported notes

Return a concise list of fixes, then give me one improved test case.
```

## Verify

- [ ] The PDF upload execution inserts chunks into the vector store.
- [ ] The chat path calls the retrieval tool before answering.
- [ ] Unsupported questions are refused instead of invented.

## Reflection questions

1. What did the agent or workflow do correctly on the first attempt?
2. What evidence proves the output was grounded, safe, or complete?
3. Which failure case was most useful for improving the workflow?
4. What should a human still review before this automation is used with real customers?

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| Answers are invented | The system prompt does not require document grounding. | Add an evidence-only answer rule and a refusal phrase. |
| Upload succeeds but chat finds nothing | The vector store was cleared or n8n restarted. | Upload the PDF again and rerun the chat test. |
| Browser cannot call webhook | Workflow is inactive or URL is wrong. | Activate the workflow and use the production webhook URL. |

## Submission evidence

Submit the following:

- Workflow export or screenshot of the main workflow canvas.
- Screenshot or copy of the successful execution output.
- One normal test case and one edge or unsafe test case.
- A short note explaining what you changed after evaluation.

## Lab deliverable

A RAG chatbot that answers from the IT FAQ and refuses unrelated questions.
