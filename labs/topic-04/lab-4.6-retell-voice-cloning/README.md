# Lab 4.6 - Clone Your Own Voice and Give It to the Agent

> Topic 4 - Approximately 60 minutes - Adult workplace lab

## The build so far

This lab is part of a complete agentic AI automation course. Each lab follows the same engineering loop:

**Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

In this lab you build: **A voice clone of the learner's own voice, used as the agent's speaking voice.**

## What you will build

A voice clone of the learner's own voice, used as the agent's speaking voice. The work is intentionally practical: by the end of the lab you should have an artifact that can be inspected, tested, and reused in the capstone.

## Concepts you will meet

| Concept | In one line |
|---|---|
| Voice cloning | Builds a synthetic voice from a short recording of a real person. |
| Consent | You may only clone a voice you own or have written permission to use. |
| Reference audio quality | Clean, quiet, natural speech produces a usable clone. |
| Voice vs persona | The voice is how the agent sounds; the prompt is what it says. |

## Before you start

- Complete the setup in Lab 1.1 or confirm Docker, n8n, Ollama, and your browser are ready.
- Keep n8n executions visible while testing. The execution trace is your evidence.
- Do not place API keys in HTML, JavaScript, Markdown examples, screenshots, or exported workflow notes.
- Commit or export a checkpoint before making large workflow changes.

## Step-by-step instructions

1. Record 30-90 seconds of your own speech in a quiet room: read a neutral paragraph at your normal pace, in the language the agent will speak. Do not whisper, shout, or play background music. Your phone's voice recorder is fine.
2. Save it as a clean audio file (WAV, MP3 or M4A) **under 10 MB** - that is Retell's upload limit for a voice clone. Play it back first: no echo, no keyboard noise, no second voice. The clone copies every flaw it hears.
3. There is **no Voices page in the sidebar**. Voice cloning lives inside the agent: open your agent and click the **voice selector** in the Agent Details strip (it shows the current voice, e.g. `Cimo`).
4. In the **Select Voice** dialog, click **+ Add voice clone** at the top left.
5. In **Add Voice Clone**: type a **Voice Name** (for example `Nina - <your name>`), drag your audio file into **Upload audio clip**, and tick the consent box - *"I hereby confirm that I have all necessary rights or consents to upload and clone these voice samples..."*. Retell will not let you save without it. Click **Save**.
6. Your clone now appears in the voice list. Select it, then click **Save** in the Select Voice dialog.
7. Click **Publish** on the agent. A voice change does NOT affect a call that is already running, and an unpublished draft keeps the old voice.
8. Call the site (`http://localhost:8090` -> **Book by Voice**) and run a short booking. Listen to how it says names, prices and dates - clones break on numbers first.
9. Tune **Speech Settings** (speed, pause before speaking) and re-run the SAME call script so you are comparing like with like.
10. Write two sentences on where a cloned voice is and is not appropriate for a real business, and what disclosure a caller deserves.

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
I am completing Clone Your Own Voice and Give It to the Agent in the course "Automate Video and Voice AI Agents with n8n".
Act as a careful agentic AI workflow reviewer. Review my workflow design against this goal:
A voice clone of the learner's own voice, used as the agent's speaking voice.

Check for:
- missing trigger, input, output, or credential boundary
- weak system prompt or unclear tool description
- missing evaluation case, refusal case, or human review gate
- any place where a secret could leak to browser code or exported notes

Return a concise list of fixes, then give me one improved test case.
```

## Verify

- [ ] The cloned voice appears in the Voices list and previews correctly.
- [ ] The agent speaks the whole call in the cloned voice.
- [ ] Prices, dates and the caller's name are pronounced correctly, or the prompt was adjusted until they were.
- [ ] The learner can state the consent and disclosure rules for using a cloned voice with real customers.

## Reflection questions

1. What did the agent or workflow do correctly on the first attempt?
2. What evidence proves the output was grounded, safe, or complete?
3. Which failure case was most useful for improving the workflow?
4. What should a human still review before this automation is used with real customers?

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| Cannot find where to clone a voice | There is no Voices page in the sidebar. | Open the AGENT, click the voice selector, then '+ Add voice clone' in the Select Voice dialog. |
| Clone sounds robotic or muffled | The reference recording was noisy, echoey, or too short. | Re-record 60+ seconds of clean, natural speech in a quiet room. |
| Save button stays greyed out | The consent checkbox was not ticked, or the file is over 10 MB. | Tick the rights/consent box and upload a file under 10 MB. |
| Numbers are mispronounced | The model reads digits literally. | Ask for spoken forms in the prompt, e.g. 'sixty-five dollars' instead of '$65'. |
| Voice change has no effect on the call | The agent was not published after the voice was changed. | Publish the agent, then start a NEW call - a live call keeps its old voice. |

## Submission evidence

Submit the following:

- Workflow export or screenshot of the main workflow canvas.
- Screenshot or copy of the successful execution output.
- One normal test case and one edge or unsafe test case.
- A short note explaining what you changed after evaluation.

## Lab deliverable

A cloned voice used by the working voice agent, plus a short written note on consent and disclosure.
