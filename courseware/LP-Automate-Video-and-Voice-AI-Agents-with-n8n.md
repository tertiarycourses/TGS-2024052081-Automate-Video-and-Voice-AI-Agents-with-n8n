# Lesson Plan - Automate Video and Voice AI Agents with n8n

## Course profile

| | |
|---|---|
| Provider | Tertiary Infotech Academy Pte Ltd |
| Course code | TGS-2024052081 |
| WSQ skill | Artificial Intelligence Application (AER-TEM-4026-1.1) |
| Version | v4.0 (14 July 2026) |
| Mode | Instructor-led adult training, hands-on labs |
| Duration | 2 training days, 8 instructional hours each |
| Practical ratio | At least 70 percent hands-on lab time |
| Trainer | Dr Alfred Ang |

## Trainer strategy

Demonstrate each concept with one small working example, then move quickly into learner practice. For every lab, ask learners to show the **evidence** - the n8n execution trace, the generated media, the call transcript, the scorecard. Do not accept a screenshot of a finished screen as proof that the workflow is correct: a fluent output and a correct workflow are not the same thing, and telling them apart is the skill this course teaches.

## Topic map

Each topic delivers one WSQ learning outcome of Artificial Intelligence Application (AER-TEM-4026-1.1). The Written Assessment (SAQ) tests K1-K6; the Case Study tests A1-A6.

| Session | Topic | Focus | WSQ outcome | Labs |
|---|---|---|---|---|
| 1 | Topic 01 - Chatbot | Agents, retrieval and grounded answers: your first n8n AI agent, a RAG chatbot that admits what it does not know, and a customer-facing course advisor on a real website. Labs 0-3. | LO1 (K1, K6, A3, A5) | Lab 0, Lab 1, Lab 2, Lab 3 |
| 2 | Topic 02 - Voice Agent | Two vendors, two architectures: ElevenLabs runs the model and calls your n8n tools; with Vapi your n8n workflow IS the model. The contrast is the lesson. Labs 4-5. | LO2 (K2, K3, A1, A4) | Lab 4, Lab 5 |
| 3 | Topic 03 - Video Agent | Lip-sync, avatars and text-to-video: from a script, to a mouth that moves, to a face that talks back, to video from nothing but a sentence. Labs 6-10. | LO3 (K4, K5, A2, A6) | Lab 6, Lab 7, Lab 7-os, Lab 8, Lab 9, Lab 10 |

## Daily schedule

Total taught content: 12 hours 00 minutes across 12 labs.

### Day 1

| Time | Duration | Topic / Activity | Deck | Evidence produced |
|---|---|---|---|---|
| 9:30am - 10:15am | 45 min | Lab 0 - Set Up n8n Locally | Slide 23 | A running local stack: screenshots of docker compose ps, ollama list and the passing credential test. |
| 10:15am - 11:00am | 45 min | Lab 1 - Your First AI Agent | Slide 29 | A working local agent plus a one-line note on how the system prompt changed its behaviour. |
| 11:00am - 12:00pm | 60 min | Lab 2 - RAG IT Support Chatbot | Slide 35 | A RAG chatbot answering from the IT FAQ, plus one provoked refusal captured in the execution trace. |
| 12:00pm - 1:00pm | 60 min | Lab 3 - CX Agent with RAG (Cook & Bake Academy) | Slide 42 | A working course-advisory chatbot on the site, with one grounded answer and one honest refusal in the trace. |
| 1:00pm - 2:00pm | 60 min | **LUNCH** | - | - |
| 2:00pm - 4:00pm | 120 min | Lab 4 - Voice Booking Agent with ElevenLabs (GG Hair Salon) | Slide 55 | A real calendar booking made by voice: the calendar event, the call transcript, and the n8n tool execution. |
| 4:00pm - 5:30pm | 90 min | Lab 5 - Grounded FAQ Voice Agent with Vapi (MediRefill) | Slide 62 | A live Vapi call transcript showing grounded answers, a hard medical refusal, and the emergency escalation. |
| 5:30pm - 6:30pm | 60 min | Concept delivery, review and evidence check - the trainer teaches the concept, workflow and quality slides for the day's labs, then learners show their executions, transcripts and scorecards | - | Trainer sign-off on the day's evidence |

**Day 1 instructional time: 8h 00m** (9:30am-6:30pm, less a 1-hour lunch; tea breaks are taken inside the sessions).

### Day 2

| Time | Duration | Topic / Activity | Deck | Evidence produced |
|---|---|---|---|---|
| 9:30am - 10:30am | 60 min | Lab 6 - Lip-Sync Face-Off: MuseTalk vs HeyGen | Slide 73 | Two rendered clips of one script, a scored comparison, and a one-line recommendation per engine. |
| 10:30am - 11:15am | 45 min | Lab 7 - Avatar News Video with HeyGen (GG News Studio) | Slide 80 | A generated avatar news video plus quality-review notes on the script and the render. |
| 11:15am - 12:00pm | 45 min | Lab 7-os - Open-Source News Avatar - Free and Local | Slide 86 | A locally rendered news video and a written HeyGen-versus-local comparison. |
| 12:00pm - 12:45pm | 45 min | Lab 8 - Interactive Avatar Brain (Aria, In-Browser) | Slide 92 | A conversation with Aria plus the latency-panel screenshot proving ~2 s replies. |
| 12:45pm - 1:45pm | 60 min | **LUNCH** | - | - |
| 1:45pm - 2:30pm | 45 min | Lab 9 - Interactive Avatar Session (Nova, HeyGen LiveAvatar) | Slide 98 | A working Nova session plus the two-column scorecard comparing her against the browser-rendered avatar. |
| 2:30pm - 3:30pm | 60 min | Lab 10 - AI Video Generation with Gemini Veo 3 (Veo Studio) | Slide 104 | A rendered Veo clip, the shot prompt that produced it, and a note on what changed between two prompt versions. |
| 3:30pm - 4:15pm | 45 min | Concept delivery, review and evidence check - the trainer teaches the concept, workflow and quality slides for the day's labs, then learners show their executions, transcripts and scorecards | - | Trainer sign-off on the day's evidence |
| 4:15pm - 4:30pm | 15 min | Assessment briefing - instruments, timing, and what evidence is graded | - | Completed answer script submitted on the LMS |
| 4:30pm - 5:30pm | 60 min | **Written Assessment (SAQ)** - 6 open-ended knowledge questions (K1-K6) | - | Completed answer script submitted on the LMS |
| 5:30pm - 6:30pm | 60 min | **Case Study (CS)** - 6 scenario tasks drawn from the labs (A1-A6) | - | Completed answer script submitted on the LMS |

**Day 2 instructional time: 8h 00m** (9:30am-6:30pm, less a 1-hour lunch; tea breaks are taken inside the sessions).


## Assessment

| Instrument | Duration | What it tests | When |
|---|---|---|---|
| Briefing for Assessment | 15 min | The learner knows the instruments, the criteria and the appeal route | Before the assessment, on the final day |
| Written Assessment (WA) - Short Answer | 60 min | KNOWLEDGE: the concepts behind the labs | Final day, after the briefing |
| Case Study (CS) | 60 min | APPLICATION: judgement on a workplace scenario built from the labs | Final day, after the WA |

Both instruments are **open book**, individually attempted, and marked **Competent / Not Yet Competent**. A learner assessed NYC is re-assessed once, on the failed instrument only.

## Evidence the trainer collects

- Workflow exports and n8n execution traces for each lab.
- The provoked failures: the RAG refusal (Lab 2), the course that does not exist (Lab 3), Ava's medical refusals (Lab 5).
- The Google Calendar booking created by voice, with its call transcript (Lab 4).
- The lip-sync comparison scorecard: MuseTalk vs HeyGen on one script (Lab 6).
- Generated media: the news avatar videos (Labs 7 and 7-os), the Aria latency screenshot (Lab 8), the Nova session scorecard (Lab 9), the Veo clip and its shot prompt (Lab 10).
