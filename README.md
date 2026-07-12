# Automate Video and Voice AI Agents with n8n

**WSQ course - Tertiary Infotech Academy Pte Ltd**

This repository contains high-quality adult-training courseware for building AI agents, RAG assistants, voice agents, and AI avatar/video automations with n8n.

The rebuilt courseware follows an **agentic AI loop engineering** standard:

**Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

## Courseware deliverables

- [Learner Guide Markdown](courseware/LG-Automate-Video-and-Voice-AI-Agents-with-n8n.md)
- [Learner Guide DOCX](courseware/LG-Automate-Video-and-Voice-AI-Agents-with-n8n.docx)
- [PowerPoint deck](courseware/Automate-Video-and-Voice-AI-Agents-with-n8n-v3.0.pptx)
- [Lesson Plan](courseware/LP-Automate-Video-and-Voice-AI-Agents-with-n8n.md)

## Topics

- **Topic 01 - Foundations of Agentic AI Loop Engineering:** Set up the local stack and learn the engineering loop used in every lab: define the task, give the agent tools, observe behavior, evaluate outputs, improve the workflow, and add guardrails.
- **Topic 02 - Local AI Agents and RAG with n8n:** Build local agents with Ollama, memory, retrieval, chunking, and document-grounded answers that can be tested and improved.
- **Topic 03 - Customer Experience and Tool-Using Agents:** Turn retrieval into a workplace assistant that can answer customer questions, collect structured data, and call workflow tools.
- **Topic 04 - Voice AI Agents:** Design, connect, test, and improve a voice booking agent using Retell, n8n webhooks, and a browser front end.
- **Topic 05 - AI Video and Avatar Automation:** Generate scripts, avatar videos, text-to-video clips with Veo 3.1, and open-source talking-head video pipelines that run entirely on the learner's own machine.
- **Topic 06 - Publishing, Interactive Avatars, and Capstone Operations:** Publish video outputs, deploy interactive avatars, monitor automations, and assemble a production-ready AI workforce capstone.

## Labs

| Lab | Title | Time | Folder |
|---|---:|---:|---|
| 1.1 | Set Up the Local AI Automation Workstation | 60 min | [`labs/topic-01/lab-1.1-setup-local-ai-workstation/`](labs/topic-01/lab-1.1-setup-local-ai-workstation/) |
| 1.2 | Map the Agentic AI Loop Before Building | 45 min | [`labs/topic-01/lab-1.2-agentic-loop-canvas/`](labs/topic-01/lab-1.2-agentic-loop-canvas/) |
| 1.3 | Create a Workflow Quality Baseline | 45 min | [`labs/topic-01/lab-1.3-n8n-workflow-quality-baseline/`](labs/topic-01/lab-1.3-n8n-workflow-quality-baseline/) |
| 2.1 | Build Your First Local AI Agent | 60 min | [`labs/topic-02/lab-2.1-first-local-ai-agent/`](labs/topic-02/lab-2.1-first-local-ai-agent/) |
| 2.2 | Add Memory and Session Design | 45 min | [`labs/topic-02/lab-2.2-memory-and-session-design/`](labs/topic-02/lab-2.2-memory-and-session-design/) |
| 2.3 | Build a PDF RAG IT Support Agent | 75 min | [`labs/topic-02/lab-2.3-rag-pdf-basics/`](labs/topic-02/lab-2.3-rag-pdf-basics/) |
| 2.4 | Improve RAG with Chunking and Evaluation | 60 min | [`labs/topic-02/lab-2.4-rag-chunking-evaluation/`](labs/topic-02/lab-2.4-rag-chunking-evaluation/) |
| 3.1 | Build a Course Advisory CX Agent | 75 min | [`labs/topic-03/lab-3.1-course-cx-rag-agent/`](labs/topic-03/lab-3.1-course-cx-rag-agent/) |
| 3.2 | Add Structured Lead Capture | 60 min | [`labs/topic-03/lab-3.2-structured-lead-capture/`](labs/topic-03/lab-3.2-structured-lead-capture/) |
| 3.3 | Create a Tool-Calling Booking Request Agent | 60 min | [`labs/topic-03/lab-3.3-tool-calling-booking-request/`](labs/topic-03/lab-3.3-tool-calling-booking-request/) |
| 3.4 | Add Safety Guardrails and Escalation | 60 min | [`labs/topic-03/lab-3.4-agent-safety-guardrails/`](labs/topic-03/lab-3.4-agent-safety-guardrails/) |
| 4.1 | Design a Voice Agent Conversation | 60 min | [`labs/topic-04/lab-4.1-voice-agent-conversation-design/`](labs/topic-04/lab-4.1-voice-agent-conversation-design/) |
| 4.2 | Connect Retell Web Calls Through n8n | 75 min | [`labs/topic-04/lab-4.2-retell-web-call-n8n/`](labs/topic-04/lab-4.2-retell-web-call-n8n/) |
| 4.3 | QA the Voice Agent with Call Analytics | 60 min | [`labs/topic-04/lab-4.3-voice-agent-qa-and-analytics/`](labs/topic-04/lab-4.3-voice-agent-qa-and-analytics/) |
| 4.4 | Add Human Handoff and Notifications | 60 min | [`labs/topic-04/lab-4.4-voice-handoff-and-notification/`](labs/topic-04/lab-4.4-voice-handoff-and-notification/) |
| 4.5 | Ground the Voice Agent with a Retell Knowledge Base | 60 min | [`labs/topic-04/lab-4.5-voice-agent-knowledge-base/`](labs/topic-04/lab-4.5-voice-agent-knowledge-base/) |
| 4.6 | Clone Your Own Voice and Give It to the Agent | 60 min | [`labs/topic-04/lab-4.6-retell-voice-cloning/`](labs/topic-04/lab-4.6-retell-voice-cloning/) |
| 4.7 | Book the Appointment into Google Calendar | 75 min | [`labs/topic-04/lab-4.7-voice-booking-google-calendar/`](labs/topic-04/lab-4.7-voice-booking-google-calendar/) |
| 4.8 | Build a FAQ Voice Agent with Vapi | 75 min | [`labs/topic-04/lab-4.8-vapi-faq-voice-agent/`](labs/topic-04/lab-4.8-vapi-faq-voice-agent/) |
| 5.1 | Lip-Sync Face-Off: Wav2Lip vs MuseTalk vs HeyGen | 75 min | [`labs/topic-05/lab-5.1-lipsync-musetalk-vs-heygen/`](labs/topic-05/lab-5.1-lipsync-musetalk-vs-heygen/) |
| 5.2 | Build a Video Script Agent | 60 min | [`labs/topic-05/lab-5.2-video-script-agent/`](labs/topic-05/lab-5.2-video-script-agent/) |
| 5.3 | Generate an Avatar News Video with HeyGen | 75 min | [`labs/topic-05/lab-5.3-heygen-avatar-news-video/`](labs/topic-05/lab-5.3-heygen-avatar-news-video/) |
| 5.4 | Generate a Cinematic Video with Veo 3.1 and Gemini | 75 min | [`labs/topic-05/lab-5.4-veo-gemini-text-to-video/`](labs/topic-05/lab-5.4-veo-gemini-text-to-video/) |
| 5.5 | Build the Free Local Avatar Video Pipeline | 90 min | [`labs/topic-05/lab-5.5-open-source-avatar-pipeline/`](labs/topic-05/lab-5.5-open-source-avatar-pipeline/) |
| 6.1 | Publish the Avatar Video to YouTube | 75 min | [`labs/topic-06/lab-6.1-youtube-publishing-automation/`](labs/topic-06/lab-6.1-youtube-publishing-automation/) |
| 6.2 | Build an Interactive Avatar That Renders in the Browser | 75 min | [`labs/topic-06/lab-6.2-interactive-browser-avatar/`](labs/topic-06/lab-6.2-interactive-browser-avatar/) |
| 6.3 | Embed an Interactive HeyGen Avatar with LiveAvatar | 75 min | [`labs/topic-06/lab-6.3-interactive-heygen-liveavatar/`](labs/topic-06/lab-6.3-interactive-heygen-liveavatar/) |
| 6.4 | Monitor, Debug, and Recover AI Workflows | 60 min | [`labs/topic-06/lab-6.4-workflow-monitoring-and-recovery/`](labs/topic-06/lab-6.4-workflow-monitoring-and-recovery/) |
| 6.5 | Capstone - Build a Human-AI Workforce Automation | 120 min | [`labs/topic-06/lab-6.5-capstone-ai-workforce/`](labs/topic-06/lab-6.5-capstone-ai-workforce/) |

## Existing runnable assets

The original runnable n8n workflows and websites remain in `lab0/` to `lab10/` and `lab7-opensource/`. The new `labs/` folder provides the adult-training lab instructions and quality standard around those assets.

## Quick start

```bash
cd lab0
docker compose up -d
ollama pull gemma4
ollama pull nomic-embed-text
```

Then open n8n at `http://localhost:5678` and create an Ollama credential with:

```text
http://host.docker.internal:11434
```

## Security rule

API keys belong in n8n credentials or local environment files. They must not be placed in browser JavaScript, Markdown examples, screenshots, workflow notes, or committed JSON.
