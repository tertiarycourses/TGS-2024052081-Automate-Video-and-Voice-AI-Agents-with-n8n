# Lab 4.7 - Book the Appointment into Google Calendar

> Topic 4 - Approximately 75 minutes - Adult workplace lab

## The build so far

This lab is part of a complete agentic AI automation course. Each lab follows the same engineering loop:

**Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

In this lab you build: **A voice agent that checks a real calendar and writes a confirmed booking into it.**

## What you will build

A voice agent that checks a real calendar and writes a confirmed booking into it. The work is intentionally practical: by the end of the lab you should have an artifact that can be inspected, tested, and reused in the capstone.

## Concepts you will meet

| Concept | In one line |
|---|---|
| Tool call | The agent asks n8n a question mid-call and waits for the answer. |
| Free/busy check | Reads the calendar before promising a slot. |
| Write action | Creating an event is irreversible - it needs confirmation first. |
| Spoken response | The `speak` field is what the caller hears, so keep it one sentence. |

## Before you start

- Complete the setup in Lab 1.1 or confirm Docker, n8n, Ollama, and your browser are ready.
- Keep n8n executions visible while testing. The execution trace is your evidence.
- Do not place API keys in HTML, JavaScript, Markdown examples, screenshots, or exported workflow notes.
- Commit or export a checkpoint before making large workflow changes.

## Step-by-step instructions

1. In n8n, create a **Google Calendar OAuth2** credential (Google Cloud console -> enable the Calendar API -> OAuth client -> paste the redirect URL n8n shows you). The course n8n has Gmail/Drive/Sheets credentials but NOT Calendar - you must add it.
2. Import `lab4/retell-booking-tools-flow.json`. It has two webhook paths: `check-availability` and `book-appointment`.
3. Open both Google Calendar nodes and select your new credential. Leave the calendar as `primary` or pick a dedicated test calendar.
4. Read the **Parse Slot** Code node. It converts the caller's words into a 1-hour slot, rejects Sundays and out-of-hours times, and returns a `speak` sentence when it cannot understand the date or time.
5. Activate the workflow, then test `check-availability` BEFORE involving any voice - HTTP is far easier to debug than audio. macOS: `curl -X POST <url> -H 'Content-Type: application/json' -d '{"args":{"service":"Cut","date":"2026-07-16","time":"14:00"}}'`. Windows: PowerShell mangles quotes, so use `curl.exe` and escape the inner quotes with `\"`, or simply click **Execute workflow** in n8n and paste the JSON into the webhook's test panel. You should get `available: true` and a `speak` sentence.
6. Put a real event in your calendar at that time and run the same curl again. It must now answer `available: false`. If it does not, the Calendar node is reading a different calendar.
7. Start a tunnel (`ngrok http 5678`) - Retell's servers cannot reach localhost.
8. In the Retell agent, edit the `check_availability` and `book_appointment` Custom Functions to point at `https://<tunnel>/webhook/check-availability` and `https://<tunnel>/webhook/book-appointment`. Give each a parameter schema: `service`, `date` (YYYY-MM-DD), `time` (HH:MM 24h), plus `name` and `phone` for booking.
9. Add one line to the agent prompt so the model produces machine-readable slots: "When calling a tool, always convert the caller's words into date as YYYY-MM-DD and time as 24-hour HH:MM. Today's date is <insert>." Publish the agent.
10. Call the site and book Thursday at 2 PM. Watch the n8n executions list - one execution for the availability check, one for the booking - then refresh Google Calendar and see the event.
11. Try to break it: ask for Sunday, ask for 11 PM, and change your mind after confirming. The agent must never create an event you did not confirm.

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
I am completing Book the Appointment into Google Calendar in the course "Automate Video and Voice AI Agents with n8n".
Act as a careful agentic AI workflow reviewer. Review my workflow design against this goal:
A voice agent that checks a real calendar and writes a confirmed booking into it.

Check for:
- missing trigger, input, output, or credential boundary
- weak system prompt or unclear tool description
- missing evaluation case, refusal case, or human review gate
- any place where a secret could leak to browser code or exported notes

Return a concise list of fixes, then give me one improved test case.
```

## Verify

- [ ] A real event appears in Google Calendar with the service, customer name and phone in it.
- [ ] The availability check answers truthfully when the slot is already taken.
- [ ] Sunday and out-of-hours requests are refused politely, without a calendar write.
- [ ] No event is created before the caller confirms.

## Reflection questions

1. What did the agent or workflow do correctly on the first attempt?
2. What evidence proves the output was grounded, safe, or complete?
3. Which failure case was most useful for improving the workflow?
4. What should a human still review before this automation is used with real customers?

## Common errors

| Error | Likely cause | Fix |
|---|---|---|
| Nina stalls at 'let me check' | Retell cannot reach your n8n. | Start the tunnel and use the https tunnel URL, not localhost, in the Custom Function. |
| Event lands at the wrong time | The date had no timezone, so it was read as UTC. | Keep the `+08:00` offset built into the Code node. |
| Calendar always says free | The node is reading a different calendar, or timeMin/timeMax are empty. | Select the same calendar you are looking at and re-run the curl test. |
| Double bookings | The agent booked without checking first. | Instruct it to call `check_availability` before `book_appointment`. |
| Event created before confirmation | The prompt lets the model act eagerly. | Require an explicit 'yes' before the booking tool is allowed. |

## Submission evidence

Submit the following:

- Workflow export or screenshot of the main workflow canvas.
- Screenshot or copy of the successful execution output.
- One normal test case and one edge or unsafe test case.
- A short note explaining what you changed after evaluation.

## Lab deliverable

A voice booking that produces a real, correctly-timed Google Calendar event.
