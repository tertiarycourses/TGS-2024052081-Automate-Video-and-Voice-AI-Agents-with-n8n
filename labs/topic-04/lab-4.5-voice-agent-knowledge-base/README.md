# Lab 4.5 - Ground the Voice Agent with a Retell Knowledge Base

> Topic 4 - Approximately 60 minutes - Adult workplace lab

## The build so far

This lab is part of a complete agentic AI automation course. Each lab follows the same engineering loop:

**Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

In this lab you build: **A Retell Knowledge Base that lets the agent answer salon questions from a source document instead of inventing answers.**

## What you will build

A Retell Knowledge Base that lets the agent answer salon questions from a source document instead of inventing answers. The work is intentionally practical: by the end of the lab you should have an artifact that can be inspected, tested, and reused in the capstone.

## Concepts you will meet

| Concept | In one line |
|---|---|
| Knowledge Base | A document store the voice agent can retrieve from mid-call. |
| Grounding | Answering from a source document rather than model memory. |
| Retrieval vs tools | The KB answers questions; the n8n webhook tools take actions. |
| Refusal behavior | Saying 'let me pass you to a stylist' beats guessing. |

## Before you start

- Complete the setup in Lab 1.1 or confirm Docker, n8n, Ollama, and your browser are ready.
- Keep n8n executions visible while testing. The execution trace is your evidence.
- Do not place API keys in HTML, JavaScript, Markdown examples, screenshots, or exported workflow notes.
- Commit or export a checkpoint before making large workflow changes.

## Step-by-step instructions

1. Open `lab4/knowledge-base/gg-hair-salon-handbook.pdf` and note three facts that appear ONLY in the PDF and nowhere in the agent prompt: the 12-hour cancellation rule, the $30 colour deposit, and the 15-minute late-arrival grace period. These are your test targets. (Edit the content with `build_kb_pdf.py` if you want.)
2. In the Retell dashboard, open **Knowledge Base** in the left sidebar and click the **+** button.
3. Name it `GG Hair Salon Handbook`. Under **Documents** click **+ Add** - you get three choices: *Add Web Pages*, *Upload Files*, *Add Text*. Choose **Upload Files** and select the PDF. Click **Save**. (Your first 10 knowledge bases are free.)
4. Wait until the document shows a green tick and a file size instead of *In progress* - Retell is chunking and embedding it. A two-page PDF takes under a minute.
5. Open your agent, expand the **Knowledge Base** panel on the right, click **+ Add**, and pick `GG Hair Salon Handbook` from the dropdown. If the dropdown only offers *Add New Knowledge Base*, the document has not finished embedding - wait and reopen it.
6. Add one line to the agent prompt so it prefers the source over its memory: "Answer questions about services, prices, stylists and salon policies using the knowledge base only. If the knowledge base does not contain the answer, say you will check with a stylist. Never guess a price or a policy."
7. **Publish** the agent, then use **Run Test** and ask: *What is your cancellation policy?* Nina should state the 12-hour rule and the 50% charge.
8. Test end to end from the website: open `http://localhost:8090`, click **Book by Voice**, and run the conversation script in the next section.
9. Prove the grounding did something: detach the knowledge base, ask the same question again, and record the ungrounded answer. Re-attach it. The difference between the two answers is your evidence.

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
I am completing Ground the Voice Agent with a Retell Knowledge Base in the course "Automate Video and Voice AI Agents with n8n".
Act as a careful agentic AI workflow reviewer. Review my workflow design against this goal:
A Retell Knowledge Base that lets the agent answer salon questions from a source document instead of inventing answers.

Check for:
- missing trigger, input, output, or credential boundary
- weak system prompt or unclear tool description
- missing evaluation case, refusal case, or human review gate
- any place where a secret could leak to browser code or exported notes

Return a concise list of fixes, then give me one improved test case.
```

## Verify

- [ ] The knowledge base shows status **Ready** and is attached to the agent.
- [ ] Nina correctly answers three questions whose answers appear only in the PDF (cancellation policy, colour deposit, parking).
- [ ] Asked something the PDF does not cover (for example nail extensions), Nina declines to guess and offers to check with a stylist.
- [ ] Booking still works: grounding did not break the n8n webhook tools.

## Reflection questions

1. What did the agent or workflow do correctly on the first attempt?
2. What evidence proves the output was grounded, safe, or complete?
3. Which failure case was most useful for improving the workflow?
4. What should a human still review before this automation is used with real customers?

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| Nina ignores the knowledge base | The KB was created but never attached to the agent. | Attach it in the agent settings, then publish the agent. |
| Nina still invents prices | The prompt does not tell it to prefer the source. | Add the grounding instruction, then publish again. |
| Upload stays 'processing' | The PDF is image-only or corrupt. | Regenerate it with `build_kb_pdf.py`; the text must be selectable. |
| Answers are right but slow | Retrieval is added to every turn. | Keep the KB small and focused; one handbook is enough. |

## Submission evidence

Submit the following:

- Workflow export or screenshot of the main workflow canvas.
- Screenshot or copy of the successful execution output.
- One normal test case and one edge or unsafe test case.
- A short note explaining what you changed after evaluation.

## Lab deliverable

A Retell Knowledge Base attached to the voice agent, plus a transcript showing three grounded answers and one honest refusal.
