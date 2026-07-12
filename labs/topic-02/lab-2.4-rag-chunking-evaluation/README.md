# Lab 2.4 - Improve RAG with Chunking and Evaluation

> Topic 2 - Approximately 60 minutes - Adult workplace lab

## The build so far

This lab is part of a complete agentic AI automation course. Each lab follows the same engineering loop:

**Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

In this lab you build: **A repeatable RAG evaluation sheet with chunking experiments.**

## What you will build

A repeatable RAG evaluation sheet with chunking experiments. The work is intentionally practical: by the end of the lab you should have an artifact that can be inspected, tested, and reused in the capstone.

## Concepts you will meet

| Concept | In one line |
|---|---|
| Chunk size | Controls how much text is retrieved at once. |
| Overlap | Preserves context across chunk boundaries. |
| Golden question | A known test question with an expected evidence-backed answer. |
| Regression test | A test rerun after every prompt or workflow change. |

## Before you start

- Complete the setup in Lab 1.1 or confirm Docker, n8n, Ollama, and your browser are ready.
- Keep n8n executions visible while testing. The execution trace is your evidence.
- Do not place API keys in HTML, JavaScript, Markdown examples, screenshots, or exported workflow notes.
- Commit or export a checkpoint before making large workflow changes.

## Step-by-step instructions

1. Create ten golden questions from `it-faq.pdf`, including two unsupported questions.
2. Record expected answer points and source phrases for each question.
3. Run the current RAG workflow and score each answer from 0 to 2.
4. Change chunk size or overlap in the text splitter and re-upload the PDF.
5. Rerun the same questions and compare score changes.
6. Choose the best setting and document why it is better.

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
I am completing Improve RAG with Chunking and Evaluation in the course "Automate Video and Voice AI Agents with n8n".
Act as a careful agentic AI workflow reviewer. Review my workflow design against this goal:
A repeatable RAG evaluation sheet with chunking experiments.

Check for:
- missing trigger, input, output, or credential boundary
- weak system prompt or unclear tool description
- missing evaluation case, refusal case, or human review gate
- any place where a secret could leak to browser code or exported notes

Return a concise list of fixes, then give me one improved test case.
```

## Verify

- [ ] The evaluation sheet includes question, expected evidence, actual answer, score, and notes.
- [ ] At least two chunking configurations were tested.
- [ ] The final choice is based on scores, not preference.

## Reflection questions

1. What did the agent or workflow do correctly on the first attempt?
2. What evidence proves the output was grounded, safe, or complete?
3. Which failure case was most useful for improving the workflow?
4. What should a human still review before this automation is used with real customers?

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| Scores do not change | The vector store was not refreshed after changing chunking. | Clear or reinsert the documents before retesting. |
| Every answer is too vague | Chunks are too small or top-k is too low. | Increase chunk size or retrieve more chunks. |
| Answers contain irrelevant sections | Chunks are too large or overlap is excessive. | Reduce chunk size and retest. |

## Submission evidence

Submit the following:

- Workflow export or screenshot of the main workflow canvas.
- Screenshot or copy of the successful execution output.
- One normal test case and one edge or unsafe test case.
- A short note explaining what you changed after evaluation.

## Lab deliverable

A RAG evaluation sheet and selected chunking configuration.
