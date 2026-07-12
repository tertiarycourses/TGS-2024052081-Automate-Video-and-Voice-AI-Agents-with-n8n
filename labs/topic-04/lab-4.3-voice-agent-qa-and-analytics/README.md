# Lab 4.3 - QA the Voice Agent with Call Analytics

> Topic 4 - Approximately 60 minutes - Adult workplace lab

## The build so far

This lab is part of a complete agentic AI automation course. Each lab follows the same engineering loop:

**Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

In this lab you build: **A voice QA scorecard based on transcripts and booking success.**

## What you will build

A voice QA scorecard based on transcripts and booking success. The work is intentionally practical: by the end of the lab you should have an artifact that can be inspected, tested, and reused in the capstone.

## Concepts you will meet

| Concept | In one line |
|---|---|
| Transcript review | Turns a voice call into inspectable text. |
| Task success metric | Measures whether the caller achieved the goal. |
| Repair count | Counts how often the agent had to recover. |
| Latency perception | Checks whether responses feel natural enough. |

## Before you start

- Complete the setup in Lab 1.1 or confirm Docker, n8n, Ollama, and your browser are ready.
- Keep n8n executions visible while testing. The execution trace is your evidence.
- Do not place API keys in HTML, JavaScript, Markdown examples, screenshots, or exported workflow notes.
- Commit or export a checkpoint before making large workflow changes.

## Step-by-step instructions

1. Run three calls: easy caller, incomplete caller, and noisy or off-topic caller.
2. Export or copy the transcript for each call.
3. Score greeting, slot capture, repair, confirmation, and closing from 0 to 2.
4. Identify the worst scoring behavior.
5. Revise the voice instructions or n8n handoff logic.
6. Repeat the failed call and compare scores.

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
I am completing QA the Voice Agent with Call Analytics in the course "Automate Video and Voice AI Agents with n8n".
Act as a careful agentic AI workflow reviewer. Review my workflow design against this goal:
A voice QA scorecard based on transcripts and booking success.

Check for:
- missing trigger, input, output, or credential boundary
- weak system prompt or unclear tool description
- missing evaluation case, refusal case, or human review gate
- any place where a secret could leak to browser code or exported notes

Return a concise list of fixes, then give me one improved test case.
```

## Verify

- [ ] At least three call transcripts are reviewed.
- [ ] The scorecard identifies one concrete improvement.
- [ ] The revised agent improves or preserves the total score.

## Reflection questions

1. What did the agent or workflow do correctly on the first attempt?
2. What evidence proves the output was grounded, safe, or complete?
3. Which failure case was most useful for improving the workflow?
4. What should a human still review before this automation is used with real customers?

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| No transcript available | The provider setting may not save transcripts. | Enable transcript or use call notes from the execution data. |
| Scores are subjective | Criteria are not observable. | Define exact pass conditions for each scoring item. |
| Agent overtalks | It asks multi-part questions. | Split prompts into one question per turn. |

## Submission evidence

Submit the following:

- Workflow export or screenshot of the main workflow canvas.
- Screenshot or copy of the successful execution output.
- One normal test case and one edge or unsafe test case.
- A short note explaining what you changed after evaluation.

## Lab deliverable

A voice QA scorecard and one improved voice prompt.
