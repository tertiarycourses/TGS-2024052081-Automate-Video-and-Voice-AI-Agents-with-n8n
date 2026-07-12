# Lab 2.1 - Build Your First Local AI Agent

> Topic 2 - Approximately 60 minutes - Adult workplace lab

## The build so far

This lab is part of a complete agentic AI automation course. Each lab follows the same engineering loop:

**Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

In this lab you build: **A local chat agent using n8n, the AI Agent node, and Ollama.**

## What you will build

A local chat agent using n8n, the AI Agent node, and Ollama. The work is intentionally practical: by the end of the lab you should have an artifact that can be inspected, tested, and reused in the capstone.

## Concepts you will meet

| Concept | In one line |
|---|---|
| AI Agent node | Coordinates model calls, memory, and tools. |
| System message | Sets the role, boundaries, and style of the assistant. |
| Local model | Keeps experimentation private and low cost. |
| Agent evaluation | Checks whether the response matched the intended role. |

## Before you start

- Complete the setup in Lab 1.1 or confirm Docker, n8n, Ollama, and your browser are ready.
- Keep n8n executions visible while testing. The execution trace is your evidence.
- Do not place API keys in HTML, JavaScript, Markdown examples, screenshots, or exported workflow notes.
- Commit or export a checkpoint before making large workflow changes.

## Step-by-step instructions

1. Import `lab1/ai-agent-ollama.json` into n8n.
2. Select the `Ollama local` credential in the Ollama Chat Model node.
3. Set the model to `gemma4:latest` or the exact local tag on your machine.
4. Add a system message that defines a helpful training assistant with concise answers.
5. Open the chat and ask a simple introduction question.
6. Run a second prompt asking for something outside the course scope and improve the system message if needed.

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
I am completing Build Your First Local AI Agent in the course "Automate Video and Voice AI Agents with n8n".
Act as a careful agentic AI workflow reviewer. Review my workflow design against this goal:
A local chat agent using n8n, the AI Agent node, and Ollama.

Check for:
- missing trigger, input, output, or credential boundary
- weak system prompt or unclear tool description
- missing evaluation case, refusal case, or human review gate
- any place where a secret could leak to browser code or exported notes

Return a concise list of fixes, then give me one improved test case.
```

## Verify

- [ ] The agent replies without using a cloud LLM.
- [ ] The execution trace shows the Chat Trigger, AI Agent, and Ollama model nodes.
- [ ] The learner can point to the system message and explain how it changes behavior.

## Reflection questions

1. What did the agent or workflow do correctly on the first attempt?
2. What evidence proves the output was grounded, safe, or complete?
3. Which failure case was most useful for improving the workflow?
4. What should a human still review before this automation is used with real customers?

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| Agent returns empty text | The model call failed or a tool name is invalid. | Check the Ollama node output and keep tool names simple. |
| Response is too long | No response style was specified. | Add a length and format instruction to the system message. |
| Model is slow | The local machine is resource constrained. | Close other heavy apps or use a smaller model if available. |

## Submission evidence

Submit the following:

- Workflow export or screenshot of the main workflow canvas.
- Screenshot or copy of the successful execution output.
- One normal test case and one edge or unsafe test case.
- A short note explaining what you changed after evaluation.

## Lab deliverable

A working local AI agent with a documented system message.
