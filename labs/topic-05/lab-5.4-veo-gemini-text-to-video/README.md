# Lab 5.4 - Generate a Cinematic Video with Veo 3.1 and Gemini

> Topic 5 - Approximately 75 minutes - Adult workplace lab

## The build so far

This lab is part of a complete agentic AI automation course. Each lab follows the same engineering loop:

**Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

In this lab you build: **A one-page studio where a single idea becomes a shot script written by gemma4 and an 8-second Veo 3.1 clip with sound.**

## What you will build

A one-page studio where a single idea becomes a shot script written by gemma4 and an 8-second Veo 3.1 clip with sound. The work is intentionally practical: by the end of the lab you should have an artifact that can be inspected, tested, and reused in the capstone.

## Concepts you will meet

| Concept | In one line |
|---|---|
| Text to video | Veo 3.1 renders a real video with audio from a written prompt - no camera, no avatar photo. |
| Prompt as a shot list | A local model turns a plain idea into a cinematic prompt: subject, action, camera, lighting, mood. |
| Long-running operations | The render does not finish inside one HTTP call, so the flow starts a job and polls until it is done. |
| The key stays in n8n | The browser receives the video through the flow, never the Gemini API key. |

## Before you start

- Complete the setup in Lab 1.1 or confirm Docker, n8n, Ollama, and your browser are ready.
- Keep n8n executions visible while testing. The execution trace is your evidence.
- Do not place API keys in HTML, JavaScript, Markdown examples, screenshots, or exported workflow notes.
- Commit or export a checkpoint before making large workflow changes.

## Step-by-step instructions

1. Import `lab10/veo3-video-flow.json` and publish it.
2. Create the Gemini API credential in n8n and select it on the Veo nodes.
3. Start the website with `lab10/website/start.command` (Mac) or `start.bat` (Windows), then open `http://localhost:8098`.
4. Open the gear and paste the Production webhook URL of the Lab 5.4 flow.
5. Type a plain idea, for example `a barista making latte art in a quiet morning cafe`, and generate.
6. Read the script gemma4 produced, then watch the clip Veo returned and note the render time.
7. Change one element of the prompt - the camera move, or the lighting - and compare the two clips.

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
I am completing Generate a Cinematic Video with Veo 3.1 and Gemini in the course "Automate Video and Voice AI Agents with n8n".
Act as a careful agentic AI workflow reviewer. Review my workflow design against this goal:
A one-page studio where a single idea becomes a shot script written by gemma4 and an 8-second Veo 3.1 clip with sound.

Check for:
- missing trigger, input, output, or credential boundary
- weak system prompt or unclear tool description
- missing evaluation case, refusal case, or human review gate
- any place where a secret could leak to browser code or exported notes

Return a concise list of fixes, then give me one improved test case.
```

## Verify

- [ ] The flow returns a playable MP4 with audio.
- [ ] The learner can point to the shot script gemma4 wrote and say which words changed the picture.
- [ ] The learner can explain why the video is proxied through n8n instead of given to the browser as a Google URL.

## Reflection questions

1. What did the agent or workflow do correctly on the first attempt?
2. What evidence proves the output was grounded, safe, or complete?
3. Which failure case was most useful for improving the workflow?
4. What should a human still review before this automation is used with real customers?

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| The video never arrives | Veo renders asynchronously; the flow must poll the operation until `done` is true. | Open the polling node and confirm it loops on the operation name rather than reading the first response. |
| The play button does nothing | The n8n binary response does not support byte ranges, and the video element needs them to seek. | Fetch the MP4 into a blob first, then set the blob URL as the source. |
| Gemini returns 403 | The API key has no access to the Veo model, or billing is not enabled on the project. | Check the model name and enable the Generative Language API on the key's project. |

## Submission evidence

Submit the following:

- Workflow export or screenshot of the main workflow canvas.
- Screenshot or copy of the successful execution output.
- One normal test case and one edge or unsafe test case.
- A short note explaining what you changed after evaluation.

## Lab deliverable

A generated Veo clip, the gemma4 shot script that produced it, and a note on what changed between two prompt versions.
