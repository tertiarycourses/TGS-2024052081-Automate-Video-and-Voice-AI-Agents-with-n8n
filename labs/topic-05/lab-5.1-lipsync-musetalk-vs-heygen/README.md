# Lab 5.1 - Lip-Sync Face-Off: Wav2Lip vs MuseTalk vs HeyGen

> Topic 5 - Approximately 75 minutes - Adult workplace lab

## The build so far

This lab is part of a complete agentic AI automation course. Each lab follows the same engineering loop:

**Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

In this lab you build: **A side-by-side judgement of a local and a cloud lip-sync engine, using one script written by gemma4.**

## What you will build

A side-by-side judgement of a local and a cloud lip-sync engine, using one script written by gemma4. The work is intentionally practical: by the end of the lab you should have an artifact that can be inspected, tested, and reused in the capstone.

## Concepts you will meet

| Concept | In one line |
|---|---|
| Lip sync | Matching mouth shapes to the phonemes actually being spoken. |
| Local vs cloud | Free and private, against fast and paid - the real trade-off. |
| Same-input testing | Only one variable may change, or the comparison proves nothing. |
| Fit for purpose | The better engine is the one that fits the job, not the one with more features. |

## Before you start

- Complete the setup in Lab 1.1 or confirm Docker, n8n, Ollama, and your browser are ready.
- Keep n8n executions visible while testing. The execution trace is your evidence.
- Do not place API keys in HTML, JavaScript, Markdown examples, screenshots, or exported workflow notes.
- Commit or export a checkpoint before making large workflow changes.

## Step-by-step instructions

1. Start the studio. The app lives in `lab6/` - nothing to clone. macOS/Linux: `cd lab6` then `./setup.sh` (add `--musetalk` to also pull the ~3.5 GB weights). Windows: follow the PowerShell block in `lab6/README.md`. Open `http://localhost:8137`.
2. **MuseTalk needs a GPU** (Apple Silicon or NVIDIA). On a CPU-only machine it is unusable, not merely slow, and the app correctly disables the button rather than offering you a failure. If that is your machine, compare the free **browser preview** against HeyGen instead - the lesson survives.
3. Get your HeyGen API key: sign in at `https://app.heygen.com` -> click your avatar (top right) -> **Settings** -> the **API** tab -> **Copy** the API token. HeyGen shows it once.
4. Paste it into `lab6/lipsyncdemo/.env` as `HEYGEN_API_KEY=...` and **restart the app** - the key is only read at startup. The HeyGen renderer stops being greyed out.
5. Write the script with your LOCAL model, not by hand: `ollama run gemma4 "Write a 3-sentence TV news bulletin about Singapore's MRT expansion. Spoken style, no headings, no markdown, under 60 words."` Keep it short - every second of audio costs render time and HeyGen credits.
6. Upload a portrait, paste the script, choose a voice, and click **Speak**. Use the instant in-browser preview to check the timing BEFORE you render anything: it is free, immediate, and honest about being geometry rather than a face.
7. Render the SAME script and the SAME portrait through all three: **⚡ Render Wav2Lip** (local, ~16 s), **✨ Render photoreal** = MuseTalk (local, ~75 s), and **HeyGen** (cloud, ~40 s, costs credits). One variable only - change the script between runs and you have proved nothing.
8. Watch both back and score each 0-2 on: lip accuracy (do the consonants land?), mouth realism (teeth and shadow, or a smear?), head motion (alive, or a mannequin?), and artefacts (flicker at the jaw, colour mismatch at the crop edge).
9. Note the structural difference, not just the quality: MuseTalk animates the mouth only - **the head is frozen**. HeyGen also moves the head and blinks. That is not a bug in MuseTalk; it is what the model does.
10. Write the decision down: which would you ship to a client, and why? A frozen head that is free and keeps the customer's face on your own machine, or a moving head that costs credits and uploads that face to a vendor? There is no single right answer - there is a defensible one.

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
I am completing Lip-Sync Face-Off: Wav2Lip vs MuseTalk vs HeyGen in the course "Automate Video and Voice AI Agents with n8n".
Act as a careful agentic AI workflow reviewer. Review my workflow design against this goal:
A side-by-side judgement of a local and a cloud lip-sync engine, using one script written by gemma4.

Check for:
- missing trigger, input, output, or credential boundary
- weak system prompt or unclear tool description
- missing evaluation case, refusal case, or human review gate
- any place where a secret could leak to browser code or exported notes

Return a concise list of fixes, then give me one improved test case.
```

## Verify

- [ ] The same script and the same portrait were rendered by all three engines.
- [ ] The learner can state which engine moves the head, which is fastest, and which keeps the photo on their own machine.
- [ ] A completed scorecard exists, with the four criteria scored for each engine.
- [ ] A written recommendation names the trade-off (cost and privacy against head motion), not just 'HeyGen looks better'.

## Reflection questions

1. What did the agent or workflow do correctly on the first attempt?
2. What evidence proves the output was grounded, safe, or complete?
3. Which failure case was most useful for improving the workflow?
4. What should a human still review before this automation is used with real customers?

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| Render photoreal is greyed out | MuseTalk needs a GPU and its weights; without them the app reports musetalk:false. | Run ./setup.sh --musetalk on a GPU machine, or compare the browser preview against HeyGen. |
| HeyGen renderer stays greyed out | The key was added but the app was not restarted. | The .env is read at startup - restart the app and reload the page. |
| HeyGen rejects the avatar | The v3 API renders only avatars you OWN; stock avatars are refused. | Upload your own portrait as a photo avatar first. |
| The comparison proves nothing | The script or the portrait changed between the two renders. | Same script, same photo, same voice. Change ONE thing at a time. |
| Everything is slow and expensive | The script is too long. | Two or three sentences. Time it in the free browser preview first. |

## Submission evidence

Submit the following:

- Workflow export or screenshot of the main workflow canvas.
- Screenshot or copy of the successful execution output.
- One normal test case and one edge or unsafe test case.
- A short note explaining what you changed after evaluation.

## Lab deliverable

A side-by-side MuseTalk/HeyGen render of one gemma4 script, a scored comparison, and a written recommendation.
