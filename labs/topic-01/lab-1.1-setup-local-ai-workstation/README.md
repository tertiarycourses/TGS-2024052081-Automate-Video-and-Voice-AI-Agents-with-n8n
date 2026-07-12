# Lab 1.1 - Set Up the Local AI Automation Workstation

> Topic 1 - Approximately 60 minutes - Adult workplace lab

## The build so far

This lab is part of a complete agentic AI automation course. Each lab follows the same engineering loop:

**Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

In this lab you build: **A working Docker, n8n, Postgres, Ollama, and browser test environment.**

## What you will build

A working Docker, n8n, Postgres, Ollama, and browser test environment. The work is intentionally practical: by the end of the lab you should have an artifact that can be inspected, tested, and reused in the capstone.

## Concepts you will meet

| Concept | In one line |
|---|---|
| Docker Desktop | Runs n8n and Postgres in a repeatable local stack. |
| Ollama | Runs the chat and embedding models on the learner machine. |
| host.docker.internal | Lets n8n inside Docker call services on the host computer. |
| Environment smoke test | A short repeatable check before any agent lab starts. |

## Before you start

- Complete the setup in Lab 1.1 or confirm Docker, n8n, Ollama, and your browser are ready.
- Keep n8n executions visible while testing. The execution trace is your evidence.
- Do not place API keys in HTML, JavaScript, Markdown examples, screenshots, or exported workflow notes.
- Commit or export a checkpoint before making large workflow changes.

## Step-by-step instructions

1. Install Docker Desktop and confirm `docker --version` and `docker compose version` both work.
2. Install Ollama, then pull `gemma4` for chat and `nomic-embed-text` for embeddings.
3. Start the n8n stack from `lab0/docker-compose.yml` with `docker compose up -d`.
4. Create the first n8n owner account at `http://localhost:5678`.
5. Create an Ollama credential in n8n using `http://host.docker.internal:11434` as the base URL.
6. Run a smoke prompt in Ollama and a smoke credential test in n8n.

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
I am completing Set Up the Local AI Automation Workstation in the course "Automate Video and Voice AI Agents with n8n".
Act as a careful agentic AI workflow reviewer. Review my workflow design against this goal:
A working Docker, n8n, Postgres, Ollama, and browser test environment.

Check for:
- missing trigger, input, output, or credential boundary
- weak system prompt or unclear tool description
- missing evaluation case, refusal case, or human review gate
- any place where a secret could leak to browser code or exported notes

Return a concise list of fixes, then give me one improved test case.
```

## Verify

- [ ] n8n opens at `http://localhost:5678`.
- [ ] `ollama list` shows both required models.
- [ ] The n8n Ollama credential test succeeds.
- [ ] The learner can explain why n8n must not use `localhost:11434` for Ollama.

## Reflection questions

1. What did the agent or workflow do correctly on the first attempt?
2. What evidence proves the output was grounded, safe, or complete?
3. Which failure case was most useful for improving the workflow?
4. What should a human still review before this automation is used with real customers?

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| n8n cannot connect to Ollama | The credential uses localhost from inside Docker. | Use `http://host.docker.internal:11434`. |
| Ollama model not found | The model was not pulled or has a different tag. | Run `ollama pull gemma4` and select the exact model name shown by `ollama list`. |
| Port 5678 is busy | Another n8n container is already running. | Use `docker ps` and stop the older container, or change the compose port. |

## Submission evidence

Submit the following:

- Workflow export or screenshot of the main workflow canvas.
- Screenshot or copy of the successful execution output.
- One normal test case and one edge or unsafe test case.
- A short note explaining what you changed after evaluation.

## Lab deliverable

A checked workstation screenshot plus a short note explaining the local architecture.
