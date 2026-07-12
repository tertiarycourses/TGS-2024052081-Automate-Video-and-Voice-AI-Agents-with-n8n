from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]
COURSEWARE = ROOT / "courseware"
ARCHIVE = COURSEWARE / "archive"

# The WSQ house identity — used on every cover page, footer and filename.
COURSE_TITLE = "Automate Video and Voice AI Agents with n8n"
COURSE_CODE = "TGS-2024052081"
VERSION = "v3.0"
VERSION_DATE = "12 July 2026"
ORG = "Tertiary Infotech Academy Pte Ltd"
UEN = "UEN: 201200696W"
# The deck filename carries the version, and the README links to it. Derive both from one
# place, or the README goes on pointing at a deck that has moved into courseware/archive/.
PPT_STEM = f"{COURSE_TITLE.replace(' ', '-')}-{VERSION}"

# prodoc.py (installed by /wsq-setup) carries the house cover page, the version
# control record, the real Word TOC field and the Page X of Y footer. Reuse it
# rather than hand-rolling a second, subtly-different house style.
SKILLS = ROOT / ".claude" / "skills"
PRODOC = SKILLS / "wsq-slides" / "reference" / "prodoc.py"
ASSETS = SKILLS / "tertiary-learner-guide" / "assets"
ORG_LOGO = ASSETS / "tertiary-infotech-logo.png"
COURSE_LOGO = ASSETS / "n8n-course-logo.png"

VERSION_ROWS = [
    ("v1.0", "8 July 2026", "Initial release.", "Dr Alfred Ang"),
    ("v2.0", "11 July 2026", "Agentic AI loop engineering rewrite; labs 1-6.", "Dr Alfred Ang"),
    ("v3.0", VERSION_DATE,
     "Aligned 100% to the runnable labs: RAG concepts, Retell + ngrok setup, "
     "knowledge base and voice cloning, Vapi FAQ agent, Wav2Lip/MuseTalk/HeyGen "
     "lip-sync comparison, interactive avatars (in-browser and LiveAvatar), and "
     "Gemini Veo 3 video generation.", "Dr Alfred Ang"),
]
LABS_DIR = ROOT / "labs"


@dataclass(frozen=True)
class Lab:
    topic: int
    lab_no: str
    slug: str
    title: str
    minutes: int
    build: str
    concepts: list[tuple[str, str]]
    steps: list[str]
    verify: list[str]
    troubleshooting: list[tuple[str, str, str]]
    deliverable: str
    # Optional: screenshot keys (see SCREENSHOTS) rendered into the LG and the deck.
    shots: tuple[str, ...] = ()


SHOTS_DIR = COURSEWARE / "screenshots"

# Every screenshot used by the courseware. Captured from the running labs, so the
# deck and the Learner Guide show what the learner actually sees on screen.
# key -> (filename in courseware/screenshots, caption)
SCREENSHOTS: dict[str, tuple[str, str]] = {
    "n8n-workflows": ("n8n-workflow-list.png", "The seven course workflows imported into local n8n."),
    "lab1-canvas": ("lab1-ai-agent-ollama.png", "Lab 1 - AI Agent (Ollama): chat trigger, AI Agent and the local Ollama model."),
    "lab2-canvas": ("lab2-rag-flow.png", "Lab 2 - RAG IT Support Chatbot: ingestion, embeddings and the vector store."),
    "lab2-uploader": ("lab2-brochure-uploader.png", "The brochure uploader page: the learner pastes their OWN n8n webhook URL."),
    "lab3-canvas": ("lab3-cx-agent-rag.png", "Lab 3 - CX Agent with RAG: the agent plus its retrieval tool."),
    "lab3-site": ("lab3-website-home.png", "Lab 3 - Cook & Bake Academy site: the customer-facing front end."),
    "lab3-settings": ("lab3-chat-webhook-settings.png", "Lab 3 - the chat widget's gear: each learner points it at their own n8n webhook."),
    "lab4-canvas": ("lab4-retell-web-call.png", "Lab 4 - Retell Web Call Trigger: webhook -> Retell create-web-call -> access token."),
    "lab4-site": ("lab4-website-home.png", "Lab 4 - GG Hair Salon site: the Book by Voice call to action."),
    "lab4-settings": ("lab4-webhook-settings.png", "Lab 4 - Settings: the learner's own n8n webhook URL and Retell agent ID. Nothing is hardcoded."),
    "retell-agent": ("retell-agent.png", "The Retell agent: prompt, Functions (the n8n tool webhooks) and Knowledge Base."),
    "retell-functions": ("retell-functions.png", "Functions -> Custom Function: this is where the Retell -> n8n webhook URL goes."),
    "retell-kb": ("retell-knowledge-base.png", "Knowledge Base -> Add: name it, then Upload Files and select the salon handbook PDF."),
    "retell-kb-attached": ("retell-kb-attached.png", "The handbook attached to the agent. Publish the agent or the live call keeps the old config."),
    "retell-voice-picker": ("retell-voice-picker.png", "Select Voice: cloning lives HERE, in the agent's voice selector - not in the sidebar."),
    "retell-voice-clone": ("retell-voice-clone.png", "Add Voice Clone: name, upload an audio clip under 10 MB, and tick the consent box."),
    "lab6-lipsync-studio": ("lab6-lipsync-studio.png", "Lab 5.1 - Digital Human Studio (http://localhost:8137): face detected, script loaded, and the avatar speaking in the live preview."),
    "lab6-lipsync-engines": ("lab6-lipsync-engines.png", "Lab 5.1 - the controls that matter: Draft with Ollama (gemma4), the voice engine, and the LIP SYNC renderer picker."),
    "lab7-heygen-site": ("lab7-heygen-site.png", "Lab 5.3 - the HeyGen news studio: gemma4's script in the teleprompter and an honest render progress bar."),
    "ngrok-status": ("ngrok-status.png", "http://127.0.0.1:4040 - ngrok's own status page. URL = your public address; Addr = the local n8n it forwards to."),
    "lab4-booking-canvas": ("lab4-booking-tools.png", "Lab 4.7 - the booking tools: check-availability and book-appointment, both wired to Google Calendar."),
    "lab5-vapi-flow": ("lab5-vapi-flow.png", "Lab 4.8 - the Vapi custom-LLM flow: webhook -> AI Agent (Ollama) -> OpenAI-shaped response."),
    "lab5-vapi-site": ("lab5-vapi-site.png", "Lab 4.8 - HomeMart: the FAQ voice agent front end, built on the Vapi Web SDK."),
    "lab5-vapi-settings": ("lab5-vapi-settings.png", "Lab 4.8 - Settings: the learner's own Vapi PUBLIC key and assistant ID. The private key never touches the browser."),
    "lab10-veo-site": ("lab10-veo-site.png", "Lab 5.4 - the Veo studio: one prompt in, gemma4 writes the shot script, Veo 3.1 renders the clip."),
    "lab8-browser-avatar": ("lab8-interactive-avatar.png", "Lab 6.2 - Aria, rendered in the browser: speech in, gemma4 reply, and the mouth drawn live. The latency is printed, not claimed."),
    "lab9-liveavatar": ("lab9-liveavatar-site.png", "Lab 6.3 - the LiveAvatar embed: n8n mints a short-lived session URL, so the API key never reaches the browser."),
}


# Screenshots for labs whose Lab(...) entry does not carry its own `shots` tuple.
LAB_SHOTS: dict[str, tuple[str, ...]] = {
    "1.1": ("n8n-workflows",),
    "2.1": ("lab1-canvas",),
    "2.3": ("lab2-canvas", "lab2-uploader"),
    "3.1": ("lab3-canvas", "lab3-site", "lab3-settings"),
    "4.1": ("retell-agent", "retell-functions"),
    "5.3": ("lab7-heygen-site",),
    "5.4": ("lab10-veo-site",),
    "6.2": ("lab8-browser-avatar",),
    "6.3": ("lab9-liveavatar",),
}


def lab_shots(lab: Lab) -> tuple[str, ...]:
    return lab.shots or LAB_SHOTS.get(lab.lab_no, ())


def shot_path(key: str) -> Path:
    return SHOTS_DIR / SCREENSHOTS[key][0]


def shot_md(key: str, prefix: str) -> str:
    """Markdown image + caption, or an empty string if the file is not captured yet."""
    if key not in SCREENSHOTS or not shot_path(key).exists():
        return ""
    fname, caption = SCREENSHOTS[key]
    return f"![{caption}]({prefix}{fname})\n\n*{caption}*"


TOPICS = [
    (
        "Topic 01 - Foundations of Agentic AI Loop Engineering",
        "Set up the local stack and learn the engineering loop used in every lab: define the task, give the agent tools, observe behavior, evaluate outputs, improve the workflow, and add guardrails.",
    ),
    (
        "Topic 02 - Local AI Agents and RAG with n8n",
        "Build local agents with Ollama, memory, retrieval, chunking, and document-grounded answers that can be tested and improved.",
    ),
    (
        "Topic 03 - Customer Experience and Tool-Using Agents",
        "Turn retrieval into a workplace assistant that can answer customer questions, collect structured data, and call workflow tools.",
    ),
    (
        "Topic 04 - Voice AI Agents",
        "Design, connect, test, and improve a voice booking agent using Retell, n8n webhooks, and a browser front end.",
    ),
    (
        "Topic 05 - AI Video and Avatar Automation",
        "Generate scripts, avatar videos, text-to-video clips with Veo 3.1, and open-source talking-head video pipelines that run entirely on the learner's own machine.",
    ),
    (
        "Topic 06 - Publishing, Interactive Avatars, and Capstone Operations",
        "Publish video outputs, deploy interactive avatars, monitor automations, and assemble a production-ready AI workforce capstone.",
    ),
]


LABS = [
    Lab(
        1,
        "1.1",
        "setup-local-ai-workstation",
        "Set Up the Local AI Automation Workstation",
        60,
        "A working Docker, n8n, Postgres, Ollama, and browser test environment.",
        [
            ("Docker Desktop", "Runs n8n and Postgres in a repeatable local stack."),
            ("Ollama", "Runs the chat and embedding models on the learner machine."),
            ("host.docker.internal", "Lets n8n inside Docker call services on the host computer."),
            ("Environment smoke test", "A short repeatable check before any agent lab starts."),
        ],
        [
            "Install Docker Desktop and confirm `docker --version` and `docker compose version` both work.",
            "Install Ollama, then pull `gemma4` for chat and `nomic-embed-text` for embeddings.",
            "Start the n8n stack from `lab0/docker-compose.yml` with `docker compose up -d`.",
            "Create the first n8n owner account at `http://localhost:5678`.",
            "Create an Ollama credential in n8n using `http://host.docker.internal:11434` as the base URL.",
            "Run a smoke prompt in Ollama and a smoke credential test in n8n.",
        ],
        [
            "n8n opens at `http://localhost:5678`.",
            "`ollama list` shows both required models.",
            "The n8n Ollama credential test succeeds.",
            "The learner can explain why n8n must not use `localhost:11434` for Ollama.",
        ],
        [
            ("n8n cannot connect to Ollama", "The credential uses localhost from inside Docker.", "Use `http://host.docker.internal:11434`."),
            ("Ollama model not found", "The model was not pulled or has a different tag.", "Run `ollama pull gemma4` and select the exact model name shown by `ollama list`."),
            ("Port 5678 is busy", "Another n8n container is already running.", "Use `docker ps` and stop the older container, or change the compose port."),
        ],
        "A checked workstation screenshot plus a short note explaining the local architecture.",
    ),
    Lab(
        1,
        "1.2",
        "agentic-loop-canvas",
        "Map the Agentic AI Loop Before Building",
        45,
        "A one-page agent design canvas for a voice and video automation use case.",
        [
            ("Goal definition", "Names the business outcome before selecting a model or API."),
            ("Tool boundary", "States what the agent may and may not do."),
            ("Evaluation rubric", "Defines what good output means before generation starts."),
            ("Human handoff", "Identifies when the workflow must stop and ask for approval."),
        ],
        [
            "Choose one workplace scenario: customer support, course advisory, booking, training video, or sales follow-up.",
            "Write the agent goal in one measurable sentence.",
            "List inputs, tools, outputs, and forbidden actions.",
            "Create a five-point evaluation rubric covering accuracy, tone, safety, completion, and traceability.",
            "Convert the canvas into an n8n workflow note so the design travels with the automation.",
            "Use an AI assistant to challenge the canvas, then revise weak assumptions.",
        ],
        [
            "The canvas has a clear user, trigger, tool list, output, and stop condition.",
            "The evaluation rubric can be applied by another learner.",
            "At least two risks and two guardrails are documented.",
        ],
        [
            ("The goal is too broad", "It describes a department instead of a task.", "Rewrite it as a single trigger-to-output workflow."),
            ("The agent has unlimited authority", "No tool boundary was defined.", "Add explicit allow and deny lists."),
            ("Rubric is vague", "Words like good or professional are not testable.", "Use observable criteria, examples, and pass or fail thresholds."),
        ],
        "An agentic loop canvas ready to guide the remaining labs.",
    ),
    Lab(
        1,
        "1.3",
        "n8n-workflow-quality-baseline",
        "Create a Workflow Quality Baseline",
        45,
        "A reusable pre-flight checklist and execution log habit for every n8n workflow.",
        [
            ("Execution trace", "The evidence trail used to debug an automation."),
            ("Credential separation", "Secrets live in credentials, never in browser code or exported notes."),
            ("Small test cases", "Inputs designed to reveal one behavior at a time."),
            ("Versioned checkpoints", "Saved workflow exports before risky changes."),
        ],
        [
            "Create a folder named `course-checkpoints` outside the repo for local exported workflows.",
            "In n8n, enable execution saving for successful and failed runs while developing.",
            "Create a workflow note template with purpose, trigger, inputs, expected outputs, and rollback plan.",
            "Run a tiny webhook echo workflow and export it as the first checkpoint.",
            "Record three test cases: normal input, missing input, and malicious or irrelevant input.",
            "Review the execution data and identify which node proves the expected behavior.",
        ],
        [
            "A learner can restore from the exported checkpoint.",
            "The test cases are specific enough to rerun after every edit.",
            "No API keys or secrets appear in notes, browser files, or JSON examples.",
        ],
        [
            ("No execution data appears", "Execution saving is disabled or the workflow did not run.", "Enable saving and trigger the workflow again."),
            ("Export contains secrets", "A credential or API key was placed in a regular field.", "Move it to n8n credentials and rotate the key if it was exposed."),
            ("Tests are hard to repeat", "Inputs were not recorded.", "Save exact sample payloads and expected result text."),
        ],
        "A baseline quality checklist plus a saved echo workflow checkpoint.",
    ),
    Lab(
        2,
        "2.1",
        "first-local-ai-agent",
        "Build Your First Local AI Agent",
        60,
        "A local chat agent using n8n, the AI Agent node, and Ollama.",
        [
            ("AI Agent node", "Coordinates model calls, memory, and tools."),
            ("System message", "Sets the role, boundaries, and style of the assistant."),
            ("Local model", "Keeps experimentation private and low cost."),
            ("Agent evaluation", "Checks whether the response matched the intended role."),
        ],
        [
            "Import `lab1/ai-agent-ollama.json` into n8n.",
            "Select the `Ollama local` credential in the Ollama Chat Model node.",
            "Set the model to `gemma4:latest` or the exact local tag on your machine.",
            "Add a system message that defines a helpful training assistant with concise answers.",
            "Open the chat and ask a simple introduction question.",
            "Run a second prompt asking for something outside the course scope and improve the system message if needed.",
        ],
        [
            "The agent replies without using a cloud LLM.",
            "The execution trace shows the Chat Trigger, AI Agent, and Ollama model nodes.",
            "The learner can point to the system message and explain how it changes behavior.",
        ],
        [
            ("Agent returns empty text", "The model call failed or a tool name is invalid.", "Check the Ollama node output and keep tool names simple."),
            ("Response is too long", "No response style was specified.", "Add a length and format instruction to the system message."),
            ("Model is slow", "The local machine is resource constrained.", "Close other heavy apps or use a smaller model if available."),
        ],
        "A working local AI agent with a documented system message.",
    ),
    Lab(
        2,
        "2.2",
        "memory-and-session-design",
        "Add Memory and Session Design",
        45,
        "A chat agent that remembers context within a learner session and forgets across sessions.",
        [
            ("Conversation memory", "Stores recent turns so follow-up questions make sense."),
            ("Session ID", "Separates one user conversation from another."),
            ("Memory window", "Limits cost and prevents old irrelevant context from dominating."),
            ("Privacy boundary", "Defines what should not be stored."),
        ],
        [
            "Duplicate the Lab 2.1 workflow and rename it with `memory` in the title.",
            "Add a Simple Memory node to the AI Agent memory port.",
            "Set a session key using the chat session or a fixed learner test ID.",
            "Tell the agent your name and role, then ask a follow-up question without repeating them.",
            "Start a second session and confirm the first session details do not leak.",
            "Add a note listing what data is acceptable to remember during training.",
        ],
        [
            "Follow-up questions work inside the same session.",
            "A separate session does not receive the first user's details.",
            "The workflow note describes memory scope and privacy limits.",
        ],
        [
            ("The agent forgets immediately", "Memory is not connected to the AI Agent memory port.", "Reconnect the Simple Memory node and rerun."),
            ("Sessions leak together", "All users share the same session key.", "Use a per-user or per-browser session ID."),
            ("Old messages dominate", "Memory window is too large for the task.", "Reduce the number of retained turns."),
        ],
        "A memory-enabled agent and a privacy note.",
    ),
    Lab(
        2,
        "2.3",
        "rag-pdf-basics",
        "Build a PDF RAG IT Support Agent",
        75,
        "A document-grounded chatbot over the sample IT FAQ PDF.",
        [
            ("RAG", "Retrieves relevant document chunks before generating an answer."),
            ("Embeddings", "Convert text chunks into vectors for similarity search."),
            ("Vector store", "Stores and retrieves document chunks."),
            ("Grounded refusal", "Answers only from available evidence and declines unsupported questions."),
        ],
        [
            "Import `lab2/rag-flow.json` into n8n.",
            "Select the Ollama credential in both chat and embedding nodes.",
            "Open `lab2/index.html` in a browser.",
            "Upload `lab2/it-faq.pdf` through the page and confirm the insert path runs.",
            "Ask three questions that are answered in the PDF.",
            "Ask one unrelated question and tune the system prompt so the agent refuses politely.",
        ],
        [
            "The PDF upload execution inserts chunks into the vector store.",
            "The chat path calls the retrieval tool before answering.",
            "Unsupported questions are refused instead of invented.",
        ],
        [
            ("Answers are invented", "The system prompt does not require document grounding.", "Add an evidence-only answer rule and a refusal phrase."),
            ("Upload succeeds but chat finds nothing", "The vector store was cleared or n8n restarted.", "Upload the PDF again and rerun the chat test."),
            ("Browser cannot call webhook", "Workflow is inactive or URL is wrong.", "Activate the workflow and use the production webhook URL."),
        ],
        "A RAG chatbot that answers from the IT FAQ and refuses unrelated questions.",
    ),
    Lab(
        2,
        "2.4",
        "rag-chunking-evaluation",
        "Improve RAG with Chunking and Evaluation",
        60,
        "A repeatable RAG evaluation sheet with chunking experiments.",
        [
            ("Chunk size", "Controls how much text is retrieved at once."),
            ("Overlap", "Preserves context across chunk boundaries."),
            ("Golden question", "A known test question with an expected evidence-backed answer."),
            ("Regression test", "A test rerun after every prompt or workflow change."),
        ],
        [
            "Create ten golden questions from `it-faq.pdf`, including two unsupported questions.",
            "Record expected answer points and source phrases for each question.",
            "Run the current RAG workflow and score each answer from 0 to 2.",
            "Change chunk size or overlap in the text splitter and re-upload the PDF.",
            "Rerun the same questions and compare score changes.",
            "Choose the best setting and document why it is better.",
        ],
        [
            "The evaluation sheet includes question, expected evidence, actual answer, score, and notes.",
            "At least two chunking configurations were tested.",
            "The final choice is based on scores, not preference.",
        ],
        [
            ("Scores do not change", "The vector store was not refreshed after changing chunking.", "Clear or reinsert the documents before retesting."),
            ("Every answer is too vague", "Chunks are too small or top-k is too low.", "Increase chunk size or retrieve more chunks."),
            ("Answers contain irrelevant sections", "Chunks are too large or overlap is excessive.", "Reduce chunk size and retest."),
        ],
        "A RAG evaluation sheet and selected chunking configuration.",
    ),
    Lab(
        3,
        "3.1",
        "course-cx-rag-agent",
        "Build a Course Advisory CX Agent",
        75,
        "A customer-facing course advisory chatbot over 20 academy brochures.",
        [
            ("Domain grounding", "Restricts answers to approved business documents."),
            ("Customer context", "Keeps tone practical and service oriented."),
            ("Brochure ingestion", "Loads multiple text documents into a vector store."),
            ("Session continuity", "Supports follow-up questions in a website chat."),
        ],
        [
            "Import `lab3/CX Agent with RAG.json`.",
            "Activate the workflow and confirm the brochure upload webhook URL.",
            "Open `lab3/upload-brochures.html` and upload all 20 brochure text files.",
            "Open `lab3/website/index.html` and start a customer chat.",
            "Ask about course fees, duration, campus, and suitable learner profile.",
            "Refine the system prompt so answers are concise, polite, and grounded in brochure facts.",
        ],
        [
            "The website chatbot returns exact details from the brochures.",
            "Follow-up questions work within the same browser session.",
            "The agent refuses to invent discounts, schedules, or policies not in the documents.",
        ],
        [
            ("Tool call fails", "Tool node name contains special characters.", "Rename tool nodes using letters, numbers, and spaces only."),
            ("All courses sound the same", "Retrieval is not specific enough.", "Ask for exact course code or increase retrieval specificity in the prompt."),
            ("CORS or webhook error", "The workflow is inactive or URL is not production webhook.", "Activate and copy the production webhook path."),
        ],
        "A working course advisory chatbot embedded in the sample website.",
    ),
    Lab(
        3,
        "3.2",
        "structured-lead-capture",
        "Add Structured Lead Capture",
        60,
        "A CX agent that extracts name, email, course interest, and urgency into a structured payload.",
        [
            ("Structured output", "Turns conversation into fields another system can use."),
            ("Validation", "Checks required fields before handoff."),
            ("Consent", "Asks permission before storing or sending contact data."),
            ("CRM handoff", "Passes clean data to a downstream node or sheet."),
        ],
        [
            "Duplicate the course advisory workflow.",
            "Add an Edit Fields or Set node after the agent to shape lead fields.",
            "Prompt the agent to ask for missing required fields one at a time.",
            "Add a consent question before collecting email or phone.",
            "Test with a learner who gives incomplete information.",
            "Inspect the final JSON payload and revise field names for clarity.",
        ],
        [
            "The workflow does not hand off a lead until required fields are present.",
            "The agent asks for consent before contact capture.",
            "The resulting payload has stable field names and no extra prose.",
        ],
        [
            ("Lead payload contains paragraphs", "The agent was not instructed to separate conversation from data.", "Use a structured output instruction and post-process with fields."),
            ("Agent asks too many questions", "Required fields are not prioritized.", "Collect only the minimum needed for follow-up."),
            ("Consent is skipped", "It was placed after data capture.", "Move consent before requesting contact details."),
        ],
        "A structured lead capture branch ready for CRM or spreadsheet integration.",
    ),
    Lab(
        3,
        "3.3",
        "tool-calling-booking-request",
        "Create a Tool-Calling Booking Request Agent",
        60,
        "An agent that prepares a booking request and calls a mock booking tool.",
        [
            ("Tool calling", "Lets the agent request an action through a controlled workflow path."),
            ("Argument schema", "Defines exactly what the tool needs."),
            ("Confirmation before action", "Prevents accidental bookings."),
            ("Mock integration", "Tests business logic before connecting a real system."),
        ],
        [
            "Create a mock booking tool branch in n8n with fields for service, date, time, name, and contact.",
            "Connect the tool to the AI Agent.",
            "Write a tool description that clearly states when it should be used.",
            "Require the agent to summarize the booking and ask for confirmation before calling the tool.",
            "Run one complete booking scenario and one cancellation scenario.",
            "Review executions to confirm the tool was called only after confirmation.",
        ],
        [
            "Tool arguments are complete and correctly typed.",
            "The agent does not call the tool before user confirmation.",
            "The mock branch receives one clean payload per confirmed booking.",
        ],
        [
            ("Tool called too early", "The prompt does not require confirmation.", "Add a hard rule: never call the tool until the user says yes."),
            ("Tool receives missing fields", "The schema or prompt does not require all fields.", "List required arguments in the tool description."),
            ("Tool name rejected", "The name contains symbols or punctuation.", "Use a simple name such as `Create Booking Request`."),
        ],
        "A safe mock booking request workflow.",
    ),
    Lab(
        3,
        "3.4",
        "agent-safety-guardrails",
        "Add Safety Guardrails and Escalation",
        60,
        "A guardrailed CX agent with refusal, escalation, and audit notes.",
        [
            ("Policy boundary", "Defines what the agent must not answer or promise."),
            ("Escalation trigger", "Routes sensitive or high-value requests to a human."),
            ("Audit note", "Records why the workflow took a path."),
            ("Prompt injection defense", "Tells the agent to ignore user attempts to override system rules."),
        ],
        [
            "List five prohibited actions for the CX agent, such as guaranteeing admission or inventing subsidies.",
            "Add the prohibited actions to the system message using direct language.",
            "Add escalation wording for complaints, refunds, legal questions, and personal data concerns.",
            "Create test prompts that attempt to override the system instruction.",
            "Run the tests and record whether the agent refused, answered, or escalated.",
            "Revise the prompt until all tests pass.",
        ],
        [
            "Prompt injection attempts do not override the agent role.",
            "Sensitive requests are escalated with useful context.",
            "The audit note explains the reason for refusal or escalation.",
        ],
        [
            ("Agent apologizes but still answers", "The refusal rule is too soft.", "State the prohibited behavior and required alternative response."),
            ("Everything escalates", "Escalation triggers are too broad.", "Separate low-risk FAQ from sensitive cases."),
            ("Audit note is missing", "No branch records the decision.", "Add a Set node that captures decision type and reason."),
        ],
        "A guardrail test set and passing CX workflow.",
    ),
    Lab(
        4,
        "4.1",
        "voice-agent-conversation-design",
        "Design a Voice Agent Conversation",
        60,
        "A voice-agent script with opening, slot filling, repair, and closing paths.",
        [
            ("Voice turn-taking", "Keeps prompts short so callers know when to speak."),
            ("Slot filling", "Collects required booking details naturally."),
            ("Repair strategy", "Handles unclear or missing caller responses."),
            ("Persona", "Defines tone without overloading the voice model."),
        ],
        [
            "Choose the service scenario for the Retell voice agent.",
            "Write a one-sentence persona and three behavior rules.",
            "List required slots: name, service, date, time, and contact method.",
            "Write the opening line, slot questions, repair prompts, confirmation, and closing.",
            "Read the script aloud and remove long sentences.",
            "Create a test call checklist for normal, noisy, and incomplete caller behavior.",
        ],
        [
            "The script can be spoken naturally in under one minute for a simple booking.",
            "Every required slot has a question and a repair prompt.",
            "The agent confirms before creating the booking request.",
        ],
        [
            ("Caller gets interrupted", "Prompts are too long or multi-part.", "Ask one question at a time."),
            ("Agent sounds robotic", "Persona has too many adjectives.", "Use two or three concrete behavior rules."),
            ("Booking details are incomplete", "Slot list and confirmation are not aligned.", "Confirm every required field before handoff."),
        ],
        "A tested voice conversation design script.",
    ),
    Lab(
        4,
        "4.2",
        "retell-web-call-n8n",
        "Connect Retell Web Calls Through n8n",
        75,
        "A browser voice call that mints access through an n8n webhook.",
        [
            ("WebRTC voice call", "Runs the real-time audio session in the browser."),
            ("Server-side token minting", "Keeps the Retell API key away from front-end code."),
            ("Webhook trigger", "Lets the website request a call session securely."),
            ("Credential hygiene", "Stores the API key in n8n or local environment only."),
        ],
        [
            "Import `lab4/retell-web-call-flow.json`.",
            "Create the `Retell API` Header Auth credential (`Authorization` = `Bearer key_...`) on the HTTP Request node.",
            "Put your own `agent_...` ID into the **Create Retell Web Call** node, or send it from the site in the next step. The shipped fallback is the trainer's demo agent.",
            "Activate the workflow and copy the Webhook node's **Production URL** (not the Test URL).",
            "Serve the site: double-click `lab4/website/start.command` (macOS) or `start.bat` (Windows). Or by hand: `cd lab4/website` then `python3 -m http.server 8090` on macOS / `python -m http.server 8090` on Windows. Open `http://localhost:8090`.",
            "Click **⚙ Settings** on the page, paste your webhook URL and your `agent_...` ID, and Save. Nothing is hardcoded: the values live in your browser, so every learner drives the same site from their own n8n.",
            "Start a browser call and complete one short booking conversation.",
            "Inspect the n8n execution to confirm the front end never received the API key.",
        ],
        [
            "The website starts a Retell voice session.",
            "The API key is not present in browser JavaScript.",
            "n8n records a successful token/session creation execution.",
        ],
        [
            ("Call button fails", "The webhook URL in ⚙ Settings is wrong, or the workflow is not active.", "Activate the workflow and paste the production webhook URL into ⚙ Settings."),
            ("401 from Retell", "API key is missing or invalid.", "Update the n8n credential and retest."),
            ("You reach the trainer's agent", "The site sent no agent ID, so the node's fallback was used.", "Put your own `agent_...` ID in ⚙ Settings or in the node."),
            ("Microphone blocked", "Browser permission was denied.", "Allow microphone access and reload the page."),
        ],
        "A secure browser-to-Retell call flow.",
        ("lab4-canvas", "lab4-site", "lab4-settings"),
    ),
    Lab(
        4,
        "4.3",
        "voice-agent-qa-and-analytics",
        "QA the Voice Agent with Call Analytics",
        60,
        "A voice QA scorecard based on transcripts and booking success.",
        [
            ("Transcript review", "Turns a voice call into inspectable text."),
            ("Task success metric", "Measures whether the caller achieved the goal."),
            ("Repair count", "Counts how often the agent had to recover."),
            ("Latency perception", "Checks whether responses feel natural enough."),
        ],
        [
            "Run three calls: easy caller, incomplete caller, and noisy or off-topic caller.",
            "Export or copy the transcript for each call.",
            "Score greeting, slot capture, repair, confirmation, and closing from 0 to 2.",
            "Identify the worst scoring behavior.",
            "Revise the voice instructions or n8n handoff logic.",
            "Repeat the failed call and compare scores.",
        ],
        [
            "At least three call transcripts are reviewed.",
            "The scorecard identifies one concrete improvement.",
            "The revised agent improves or preserves the total score.",
        ],
        [
            ("No transcript available", "The provider setting may not save transcripts.", "Enable transcript or use call notes from the execution data."),
            ("Scores are subjective", "Criteria are not observable.", "Define exact pass conditions for each scoring item."),
            ("Agent overtalks", "It asks multi-part questions.", "Split prompts into one question per turn."),
        ],
        "A voice QA scorecard and one improved voice prompt.",
    ),
    Lab(
        4,
        "4.4",
        "voice-handoff-and-notification",
        "Add Human Handoff and Notifications",
        60,
        "A voice workflow that notifies staff when a booking or escalation is needed.",
        [
            ("Handoff payload", "Summarizes caller intent and captured details."),
            ("Notification channel", "Sends the next action to email, chat, or a sheet."),
            ("Escalation reason", "Explains why the human needs to act."),
            ("SLA thinking", "States how quickly the team should respond."),
        ],
        [
            "Add a handoff branch after the voice call or booking tool branch.",
            "Shape a payload with caller summary, captured slots, urgency, and transcript link if available.",
            "Send the payload to a simple destination such as email, spreadsheet, or local webhook test endpoint.",
            "Create two paths: confirmed booking and escalation.",
            "Test both paths with sample call data.",
            "Add a workflow note stating the response SLA and owner.",
        ],
        [
            "Confirmed bookings create a staff notification.",
            "Escalations include a reason and summary.",
            "The notification does not expose unnecessary personal data.",
        ],
        [
            ("Notification is unreadable", "Raw transcript was sent without summary.", "Add a concise structured summary before sending."),
            ("Every call notifies staff", "Branch conditions are too broad.", "Separate completed self-service calls from handoff cases."),
            ("Sensitive data is overshared", "Payload includes full transcript by default.", "Send only fields required for follow-up."),
        ],
        "A staff handoff branch for bookings and escalations.",
    ),
    Lab(
        4,
        "4.5",
        "voice-agent-knowledge-base",
        "Ground the Voice Agent with a Retell Knowledge Base",
        60,
        "A Retell Knowledge Base that lets the agent answer salon questions from a source document instead of inventing answers.",
        [
            ("Knowledge Base", "A document store the voice agent can retrieve from mid-call."),
            ("Grounding", "Answering from a source document rather than model memory."),
            ("Retrieval vs tools", "The KB answers questions; the n8n webhook tools take actions."),
            ("Refusal behavior", "Saying 'let me pass you to a stylist' beats guessing."),
        ],
        [
            "Open `lab4/knowledge-base/gg-hair-salon-handbook.pdf` and note three facts that appear ONLY in the PDF and nowhere in the agent prompt: the 12-hour cancellation rule, the $30 colour deposit, and the 15-minute late-arrival grace period. These are your test targets. (Edit the content with `build_kb_pdf.py` if you want.)",
            "In the Retell dashboard, open **Knowledge Base** in the left sidebar and click the **+** button.",
            "Name it `GG Hair Salon Handbook`. Under **Documents** click **+ Add** - you get three choices: *Add Web Pages*, *Upload Files*, *Add Text*. Choose **Upload Files** and select the PDF. Click **Save**. (Your first 10 knowledge bases are free.)",
            "Wait until the document shows a green tick and a file size instead of *In progress* - Retell is chunking and embedding it. A two-page PDF takes under a minute.",
            "Open your agent, expand the **Knowledge Base** panel on the right, click **+ Add**, and pick `GG Hair Salon Handbook` from the dropdown. If the dropdown only offers *Add New Knowledge Base*, the document has not finished embedding - wait and reopen it.",
            "Add one line to the agent prompt so it prefers the source over its memory: \"Answer questions about services, prices, stylists and salon policies using the knowledge base only. If the knowledge base does not contain the answer, say you will check with a stylist. Never guess a price or a policy.\"",
            "**Publish** the agent, then use **Run Test** and ask: *What is your cancellation policy?* Nina should state the 12-hour rule and the 50% charge.",
            "Test end to end from the website: open `http://localhost:8090`, click **Book by Voice**, and run the conversation script in the next section.",
            "Prove the grounding did something: detach the knowledge base, ask the same question again, and record the ungrounded answer. Re-attach it. The difference between the two answers is your evidence.",
        ],
        [
            "The knowledge base shows status **Ready** and is attached to the agent.",
            "Nina correctly answers three questions whose answers appear only in the PDF (cancellation policy, colour deposit, parking).",
            "Asked something the PDF does not cover (for example nail extensions), Nina declines to guess and offers to check with a stylist.",
            "Booking still works: grounding did not break the n8n webhook tools.",
        ],
        [
            ("Nina ignores the knowledge base", "The KB was created but never attached to the agent.", "Attach it in the agent settings, then publish the agent."),
            ("Nina still invents prices", "The prompt does not tell it to prefer the source.", "Add the grounding instruction, then publish again."),
            ("Upload stays 'processing'", "The PDF is image-only or corrupt.", "Regenerate it with `build_kb_pdf.py`; the text must be selectable."),
            ("Answers are right but slow", "Retrieval is added to every turn.", "Keep the KB small and focused; one handbook is enough."),
        ],
        "A Retell Knowledge Base attached to the voice agent, plus a transcript showing three grounded answers and one honest refusal.",
        ("retell-kb", "retell-kb-attached"),
    ),
    Lab(
        4,
        "4.6",
        "retell-voice-cloning",
        "Clone Your Own Voice and Give It to the Agent",
        60,
        "A voice clone of the learner's own voice, used as the agent's speaking voice.",
        [
            ("Voice cloning", "Builds a synthetic voice from a short recording of a real person."),
            ("Consent", "You may only clone a voice you own or have written permission to use."),
            ("Reference audio quality", "Clean, quiet, natural speech produces a usable clone."),
            ("Voice vs persona", "The voice is how the agent sounds; the prompt is what it says."),
        ],
        [
            "Record 30-90 seconds of your own speech in a quiet room: read a neutral paragraph at your normal pace, in the language the agent will speak. Do not whisper, shout, or play background music. Your phone's voice recorder is fine.",
            "Save it as a clean audio file (WAV, MP3 or M4A) **under 10 MB** - that is Retell's upload limit for a voice clone. Play it back first: no echo, no keyboard noise, no second voice. The clone copies every flaw it hears.",
            "There is **no Voices page in the sidebar**. Voice cloning lives inside the agent: open your agent and click the **voice selector** in the Agent Details strip (it shows the current voice, e.g. `Cimo`).",
            "In the **Select Voice** dialog, click **+ Add voice clone** at the top left.",
            "In **Add Voice Clone**: type a **Voice Name** (for example `Nina - <your name>`), drag your audio file into **Upload audio clip**, and tick the consent box - *\"I hereby confirm that I have all necessary rights or consents to upload and clone these voice samples...\"*. Retell will not let you save without it. Click **Save**.",
            "Your clone now appears in the voice list. Select it, then click **Save** in the Select Voice dialog.",
            "Click **Publish** on the agent. A voice change does NOT affect a call that is already running, and an unpublished draft keeps the old voice.",
            "Call the site (`http://localhost:8090` -> **Book by Voice**) and run a short booking. Listen to how it says names, prices and dates - clones break on numbers first.",
            "Tune **Speech Settings** (speed, pause before speaking) and re-run the SAME call script so you are comparing like with like.",
            "Write two sentences on where a cloned voice is and is not appropriate for a real business, and what disclosure a caller deserves.",
        ],
        [
            "The cloned voice appears in the Voices list and previews correctly.",
            "The agent speaks the whole call in the cloned voice.",
            "Prices, dates and the caller's name are pronounced correctly, or the prompt was adjusted until they were.",
            "The learner can state the consent and disclosure rules for using a cloned voice with real customers.",
        ],
        [
            ("Cannot find where to clone a voice", "There is no Voices page in the sidebar.", "Open the AGENT, click the voice selector, then '+ Add voice clone' in the Select Voice dialog."),
            ("Clone sounds robotic or muffled", "The reference recording was noisy, echoey, or too short.", "Re-record 60+ seconds of clean, natural speech in a quiet room."),
            ("Save button stays greyed out", "The consent checkbox was not ticked, or the file is over 10 MB.", "Tick the rights/consent box and upload a file under 10 MB."),
            ("Numbers are mispronounced", "The model reads digits literally.", "Ask for spoken forms in the prompt, e.g. 'sixty-five dollars' instead of '$65'."),
            ("Voice change has no effect on the call", "The agent was not published after the voice was changed.", "Publish the agent, then start a NEW call - a live call keeps its old voice."),
        ],
        "A cloned voice used by the working voice agent, plus a short written note on consent and disclosure.",
        ("retell-voice-picker", "retell-voice-clone"),
    ),
    Lab(
        4,
        "4.7",
        "voice-booking-google-calendar",
        "Book the Appointment into Google Calendar",
        75,
        "A voice agent that checks a real calendar and writes a confirmed booking into it.",
        [
            ("Tool call", "The agent asks n8n a question mid-call and waits for the answer."),
            ("Free/busy check", "Reads the calendar before promising a slot."),
            ("Write action", "Creating an event is irreversible - it needs confirmation first."),
            ("Spoken response", "The `speak` field is what the caller hears, so keep it one sentence."),
        ],
        [
            "In n8n, create a **Google Calendar OAuth2** credential (Google Cloud console -> enable the Calendar API -> OAuth client -> paste the redirect URL n8n shows you). The course n8n has Gmail/Drive/Sheets credentials but NOT Calendar - you must add it.",
            "Import `lab4/retell-booking-tools-flow.json`. It has two webhook paths: `check-availability` and `book-appointment`.",
            "Open both Google Calendar nodes and select your new credential. Leave the calendar as `primary` or pick a dedicated test calendar.",
            "Read the **Parse Slot** Code node. It converts the caller's words into a 1-hour slot, rejects Sundays and out-of-hours times, and returns a `speak` sentence when it cannot understand the date or time.",
            "Activate the workflow, then test `check-availability` BEFORE involving any voice - HTTP is far easier to debug than audio. macOS: `curl -X POST <url> -H 'Content-Type: application/json' -d '{\"args\":{\"service\":\"Cut\",\"date\":\"2026-07-16\",\"time\":\"14:00\"}}'`. Windows: PowerShell mangles quotes, so use `curl.exe` and escape the inner quotes with `\\\"`, or simply click **Execute workflow** in n8n and paste the JSON into the webhook's test panel. You should get `available: true` and a `speak` sentence.",
            "Put a real event in your calendar at that time and run the same curl again. It must now answer `available: false`. If it does not, the Calendar node is reading a different calendar.",
            "Start a tunnel (`ngrok http 5678`) - Retell's servers cannot reach localhost.",
            "In the Retell agent, edit the `check_availability` and `book_appointment` Custom Functions to point at `https://<tunnel>/webhook/check-availability` and `https://<tunnel>/webhook/book-appointment`. Give each a parameter schema: `service`, `date` (YYYY-MM-DD), `time` (HH:MM 24h), plus `name` and `phone` for booking.",
            "Add one line to the agent prompt so the model produces machine-readable slots: \"When calling a tool, always convert the caller's words into date as YYYY-MM-DD and time as 24-hour HH:MM. Today's date is <insert>.\" Publish the agent.",
            "Call the site and book Thursday at 2 PM. Watch the n8n executions list - one execution for the availability check, one for the booking - then refresh Google Calendar and see the event.",
            "Try to break it: ask for Sunday, ask for 11 PM, and change your mind after confirming. The agent must never create an event you did not confirm.",
        ],
        [
            "A real event appears in Google Calendar with the service, customer name and phone in it.",
            "The availability check answers truthfully when the slot is already taken.",
            "Sunday and out-of-hours requests are refused politely, without a calendar write.",
            "No event is created before the caller confirms.",
        ],
        [
            ("Nina stalls at 'let me check'", "Retell cannot reach your n8n.", "Start the tunnel and use the https tunnel URL, not localhost, in the Custom Function."),
            ("Event lands at the wrong time", "The date had no timezone, so it was read as UTC.", "Keep the `+08:00` offset built into the Code node."),
            ("Calendar always says free", "The node is reading a different calendar, or timeMin/timeMax are empty.", "Select the same calendar you are looking at and re-run the curl test."),
            ("Double bookings", "The agent booked without checking first.", "Instruct it to call `check_availability` before `book_appointment`."),
            ("Event created before confirmation", "The prompt lets the model act eagerly.", "Require an explicit 'yes' before the booking tool is allowed."),
        ],
        "A voice booking that produces a real, correctly-timed Google Calendar event.",
        ("lab4-booking-canvas",),
    ),
    Lab(
        4,
        "4.8",
        "vapi-faq-voice-agent",
        "Build a FAQ Voice Agent with Vapi",
        75,
        "A second voice agent on a different platform, where n8n is the BRAIN of the call: Vapi speaks, n8n thinks.",
        [
            ("Custom LLM", "Vapi delegates every turn to your own endpoint instead of its built-in model."),
            ("OpenAI-shaped response", "n8n must reply in chat-completion format or the agent goes silent."),
            ("Public vs private key", "A public key can only start calls, so it is safe in the browser."),
            ("Refusal testing", "The question the FAQ cannot answer is the most important test."),
        ],
        [
            "Understand the difference before you build. **Retell (Lab 4.2)**: Retell owns the model; n8n only mints the call token and answers tool calls. **Vapi (this lab)**: Vapi owns the ears and the voice, but every turn of thinking is handed to *your* n8n workflow through its **Custom LLM** setting. n8n is the brain.",
            "Import `lab5/vapi-faq-flow.json`. Read it left to right: **Vapi Webhook** receives an OpenAI-shaped chat request -> **Prepare Prompt** pulls out the caller's latest turn and the transcript -> **FAQ Agent** (Ollama) answers from the HomeMart FAQ in its system message -> **Build OpenAI Response** wraps the answer as a `chat.completion` object -> **Respond to Vapi**.",
            "That last step is the one that breaks silently: Vapi expects a valid OpenAI chat-completion object. Return anything else and the assistant just stops talking mid-call, with no error in the browser.",
            "Select the `Ollama local` credential in the model node, then **Publish/Activate** the workflow and copy the Webhook's **Production URL** (`.../webhook/vapi-faq`).",
            "Test the brain BEFORE any voice - HTTP is far easier to debug than audio: `curl -X POST <url> -H 'Content-Type: application/json' -d '{\"model\":\"gpt-4o\",\"messages\":[{\"role\":\"user\",\"content\":\"How long is the warranty on a Dyson?\"}]}'`. You must get back a `chat.completion` object whose content says **two years** - not one.",
            "Run the refusal test the same way: ask *\"Do you sell nail polish?\"*. The reply must offer a colleague follow-up, NOT invent a product. If it invents one, tighten the grounding rule in the agent's system message and re-run.",
            "Start a tunnel (`ngrok http 5678`) - Vapi's servers cannot reach localhost.",
            "In Vapi, create an assistant named `Ava - HomeMart FAQ`. Set **Model -> Custom LLM** and paste `https://<tunnel>/webhook/vapi-faq` as the URL. Set the **First Message** so Ava speaks first (see `lab5/ava-assistant-prompt.md`). Save, then copy the **assistant ID**.",
            "In **API Keys** you will see a **public** and a **private** key. You need the PUBLIC one - it can only start calls. The private key must never appear in front-end code.",
            "Serve the site: double-click `lab5/website/start.command` (macOS) or `start.bat` (Windows) - or `cd lab5/website` then `python3 -m http.server 8096` (macOS) / `python -m http.server 8096` (Windows). Open `http://localhost:8096`, click **⚙ Settings** and paste your public key and assistant ID. Nothing is hardcoded: the values live in your browser, so every learner drives the same page with their own assistant.",
            "Click **Ask Ava**, allow the microphone, and work through the six-question test set in `ava-assistant-prompt.md` while watching the n8n executions list - one execution per conversational turn. That list IS the agent thinking.",
            "Write three sentences comparing Vapi and Retell: where the model runs, where the secret lives, and which you would choose for a client - and why.",
        ],
        [
            "A curl to the webhook returns a valid `chat.completion` object, and the Dyson answer says two years.",
            "The site starts a Vapi call and the live transcript appears.",
            "Ava answers the *exception* correctly (opened personal-care items cannot be returned).",
            "She REFUSES the nail-polish question instead of inventing a product.",
            "One n8n execution appears per conversational turn, and the private key appears nowhere in the browser.",
        ],
        [
            ("Ava connects then goes silent", "n8n did not return a valid OpenAI chat-completion object.", "Check the Build OpenAI Response node; the reply must have object, choices[0].message.content."),
            ("No n8n execution during the call", "Vapi cannot reach your n8n.", "Start the tunnel and use the https URL in Custom LLM - not localhost."),
            ("Call fails immediately", "The private key was pasted instead of the public key.", "Use the PUBLIC key from Vapi -> API Keys."),
            ("Ava invents a product", "The grounding rule is missing or too soft.", "State the exact refusal sentence in the agent's system message, then re-test."),
            ("Model errors with 401", "The OpenAI credential is expired.", "Use the Ollama local credential - this course runs the model locally."),
        ],
        "A working Vapi FAQ voice agent whose brain is an n8n workflow, proven by a curl test, a live call and one honest refusal.",
        ("lab5-vapi-flow", "lab5-vapi-site", "lab5-vapi-settings"),
    ),
    Lab(
        5,
        "5.1",
        "lipsync-musetalk-vs-heygen",
        "Lip-Sync Face-Off: Wav2Lip vs MuseTalk vs HeyGen",
        75,
        "A side-by-side judgement of a local and a cloud lip-sync engine, using one script written by gemma4.",
        [
            ("Lip sync", "Matching mouth shapes to the phonemes actually being spoken."),
            ("Local vs cloud", "Free and private, against fast and paid - the real trade-off."),
            ("Same-input testing", "Only one variable may change, or the comparison proves nothing."),
            ("Fit for purpose", "The better engine is the one that fits the job, not the one with more features."),
        ],
        [
            "Start the studio. The app lives in `lab6/` - nothing to clone. macOS/Linux: `cd lab6` then `./setup.sh` (add `--musetalk` to also pull the ~3.5 GB weights). Windows: follow the PowerShell block in `lab6/README.md`. Open `http://localhost:8137`.",
            "**MuseTalk needs a GPU** (Apple Silicon or NVIDIA). On a CPU-only machine it is unusable, not merely slow, and the app correctly disables the button rather than offering you a failure. If that is your machine, compare the free **browser preview** against HeyGen instead - the lesson survives.",
            "Get your HeyGen API key: sign in at `https://app.heygen.com` -> click your avatar (top right) -> **Settings** -> the **API** tab -> **Copy** the API token. HeyGen shows it once.",
            "Paste it into `lab6/lipsyncdemo/.env` as `HEYGEN_API_KEY=...` and **restart the app** - the key is only read at startup. The HeyGen renderer stops being greyed out.",
            "Write the script with your LOCAL model, not by hand: `ollama run gemma4 \"Write a 3-sentence TV news bulletin about Singapore's MRT expansion. Spoken style, no headings, no markdown, under 60 words.\"` Keep it short - every second of audio costs render time and HeyGen credits.",
            "Upload a portrait, paste the script, choose a voice, and click **Speak**. Use the instant in-browser preview to check the timing BEFORE you render anything: it is free, immediate, and honest about being geometry rather than a face.",
            "Render the SAME script and the SAME portrait through all three: **⚡ Render Wav2Lip** (local, ~16 s), **✨ Render photoreal** = MuseTalk (local, ~75 s), and **HeyGen** (cloud, ~40 s, costs credits). One variable only - change the script between runs and you have proved nothing.",
            "Watch both back and score each 0-2 on: lip accuracy (do the consonants land?), mouth realism (teeth and shadow, or a smear?), head motion (alive, or a mannequin?), and artefacts (flicker at the jaw, colour mismatch at the crop edge).",
            "Note the structural difference, not just the quality: MuseTalk animates the mouth only - **the head is frozen**. HeyGen also moves the head and blinks. That is not a bug in MuseTalk; it is what the model does.",
            "Write the decision down: which would you ship to a client, and why? A frozen head that is free and keeps the customer's face on your own machine, or a moving head that costs credits and uploads that face to a vendor? There is no single right answer - there is a defensible one.",
        ],
        [
            "The same script and the same portrait were rendered by all three engines.",
            "The learner can state which engine moves the head, which is fastest, and which keeps the photo on their own machine.",
            "A completed scorecard exists, with the four criteria scored for each engine.",
            "A written recommendation names the trade-off (cost and privacy against head motion), not just 'HeyGen looks better'.",
        ],
        [
            ("Render photoreal is greyed out", "MuseTalk needs a GPU and its weights; without them the app reports musetalk:false.", "Run ./setup.sh --musetalk on a GPU machine, or compare the browser preview against HeyGen."),
            ("HeyGen renderer stays greyed out", "The key was added but the app was not restarted.", "The .env is read at startup - restart the app and reload the page."),
            ("HeyGen rejects the avatar", "The v3 API renders only avatars you OWN; stock avatars are refused.", "Upload your own portrait as a photo avatar first."),
            ("The comparison proves nothing", "The script or the portrait changed between the two renders.", "Same script, same photo, same voice. Change ONE thing at a time."),
            ("Everything is slow and expensive", "The script is too long.", "Two or three sentences. Time it in the free browser preview first."),
        ],
        "A side-by-side MuseTalk/HeyGen render of one gemma4 script, a scored comparison, and a written recommendation.",
        ("lab6-lipsync-studio", "lab6-lipsync-engines"),
    ),
    Lab(
        5,
        "5.2",
        "video-script-agent",
        "Build a Video Script Agent",
        60,
        "An n8n workflow that turns a topic into a timed presenter video script.",
        [
            ("Creative brief", "Defines audience, goal, length, tone, and call to action."),
            ("Timed script", "Allocates seconds to scenes and narration."),
            ("Shot list", "Converts words into visual direction."),
            ("Brand constraints", "Keeps voice, claims, and style consistent."),
        ],
        [
            "Create or duplicate a workflow for script generation.",
            "Add fields for target audience, duration, message, tone, and required facts.",
            "Prompt the local model to output scene number, time range, voiceover, on-screen text, and visual direction.",
            "Generate a 60-second script for a course announcement or news update.",
            "Review for unsupported claims and timing overrun.",
            "Revise the prompt so every scene has a visual purpose and every claim has a source.",
        ],
        [
            "The script totals the requested duration.",
            "Every scene has narration and visual direction.",
            "The script avoids unverifiable promises.",
        ],
        [
            ("Script is too long", "The model was not constrained by time per scene.", "Specify words per minute and scene duration."),
            ("Visuals are generic", "The prompt asks only for narration.", "Require camera, subject, motion, and background per scene."),
            ("Claims are risky", "No evidence rule was provided.", "Add a source and approved-claims constraint."),
        ],
        "A timed script and shot list ready for video generation.",
    ),
    Lab(
        5,
        "5.3",
        "heygen-avatar-news-video",
        "Generate an Avatar News Video with HeyGen",
        75,
        "A HeyGen avatar video created from an AI-generated script.",
        [
            ("Avatar video", "Combines script, voice, presenter identity, and scene direction."),
            ("API credential", "Lets n8n call HeyGen without exposing the key in browser code."),
            ("Generation status", "Polls or waits until the video is ready."),
            ("Result handoff", "Stores the generated video URL for review or publishing."),
        ],
        [
            "Import `lab7/heygen-news-avatar-flow.json`.",
            "Create the HeyGen credential or API key variable required by the workflow.",
            "Review the script generation node and video generation node.",
            "Run the workflow with a short news topic.",
            "Wait for the video result and open it for review.",
            "Record quality notes: pronunciation, timing, visual relevance, and brand fit.",
        ],
        [
            "The workflow produces a playable HeyGen video URL or file.",
            "Credentials remain server-side in n8n.",
            "Quality notes identify at least one prompt improvement.",
        ],
        [
            ("Video generation fails", "API key, quota, or payload fields are invalid.", "Check credential status and run a shorter test script."),
            ("Avatar mispronounces names", "No pronunciation guidance was supplied.", "Add phonetic spelling or choose a more suitable voice."),
            ("Video is off-brand", "Prompt lacks style and brand constraints.", "Add tone, audience, and visual rules from the creative brief."),
        ],
        "A generated avatar news video and quality review notes.",
    ),
    Lab(
        5,
        "5.4",
        "veo-gemini-text-to-video",
        "Generate a Cinematic Video with Veo 3.1 and Gemini",
        75,
        "A one-page studio where a single idea becomes a shot script written by gemma4 and an 8-second Veo 3.1 clip with sound.",
        [
            ("Text to video", "Veo 3.1 renders a real video with audio from a written prompt - no camera, no avatar photo."),
            ("Prompt as a shot list", "A local model turns a plain idea into a cinematic prompt: subject, action, camera, lighting, mood."),
            ("Long-running operations", "The render does not finish inside one HTTP call, so the flow starts a job and polls until it is done."),
            ("The key stays in n8n", "The browser receives the video through the flow, never the Gemini API key."),
        ],
        [
            "Import `lab10/veo3-video-flow.json` and publish it.",
            "Create the Gemini API credential in n8n and select it on the Veo nodes.",
            "Start the website with `lab10/website/start.command` (Mac) or `start.bat` (Windows), then open `http://localhost:8098`.",
            "Open the gear and paste the Production webhook URL of the Lab 5.4 flow.",
            "Type a plain idea, for example `a barista making latte art in a quiet morning cafe`, and generate.",
            "Read the script gemma4 produced, then watch the clip Veo returned and note the render time.",
            "Change one element of the prompt - the camera move, or the lighting - and compare the two clips.",
        ],
        [
            "The flow returns a playable MP4 with audio.",
            "The learner can point to the shot script gemma4 wrote and say which words changed the picture.",
            "The learner can explain why the video is proxied through n8n instead of given to the browser as a Google URL.",
        ],
        [
            ("The video never arrives", "Veo renders asynchronously; the flow must poll the operation until `done` is true.", "Open the polling node and confirm it loops on the operation name rather than reading the first response."),
            ("The play button does nothing", "The n8n binary response does not support byte ranges, and the video element needs them to seek.", "Fetch the MP4 into a blob first, then set the blob URL as the source."),
            ("Gemini returns 403", "The API key has no access to the Veo model, or billing is not enabled on the project.", "Check the model name and enable the Generative Language API on the key's project."),
        ],
        "A generated Veo clip, the gemma4 shot script that produced it, and a note on what changed between two prompt versions.",
    ),
    Lab(
        5,
        "5.5",
        "open-source-avatar-pipeline",
        "Build the Free Local Avatar Video Pipeline",
        90,
        "A local avatar video path using Ollama, generated speech, Wav2Lip-style rendering, and ffmpeg.",
        [
            ("Open-source pipeline", "Keeps video generation possible without cloud video credits."),
            ("Render service", "Separates heavy video work from the n8n orchestration flow."),
            ("Audio-video sync", "Aligns speech and face movement."),
            ("Fallback strategy", "Lets a production workflow continue when a paid provider is unavailable."),
        ],
        [
            "Open `lab7-opensource/README.md` and review the service architecture.",
            "Start the local render service using the provided start script for your platform.",
            "Import `lab7-opensource/os-news-avatar-flow.json` into n8n.",
            "Run a short script generation and render test.",
            "Open the website front end and play the generated output.",
            "Compare the local output against the HeyGen output using a quality rubric.",
        ],
        [
            "The local service accepts a render request.",
            "The workflow returns a playable local video file.",
            "The learner can explain quality and cost trade-offs versus HeyGen.",
        ],
        [
            ("Service does not start", "Python dependencies or paths are missing.", "Use the README setup commands and verify Python version."),
            ("Video has no lip sync", "The audio or image input was not passed to the renderer.", "Check the render request payload and service logs."),
            ("ffmpeg error", "ffmpeg is not installed or not on PATH.", "Install ffmpeg and reopen the terminal."),
        ],
        "A free local avatar video and comparison notes.",
    ),
    Lab(
        6,
        "6.1",
        "youtube-publishing-automation",
        "Publish the Avatar Video to YouTube",
        75,
        "An n8n publishing workflow that uploads a generated video with metadata.",
        [
            ("Publishing automation", "Moves from generated asset to distribution channel."),
            ("OAuth credential", "Authorizes YouTube upload without storing passwords."),
            ("Metadata", "Defines title, description, tags, and visibility."),
            ("Review gate", "Prevents unapproved videos from going public."),
        ],
        [
            "Create or import the YouTube upload workflow for Lab 6.",
            "Configure the YouTube OAuth credential in n8n.",
            "Use a generated video file or URL from a previous lab.",
            "Prepare title, description, tags, and visibility as workflow fields.",
            "Add a manual review gate before upload.",
            "Run an unlisted upload test and verify it appears in YouTube Studio.",
        ],
        [
            "The workflow uploads a video as unlisted or private first.",
            "Metadata is populated from workflow fields.",
            "A review gate exists before public publishing.",
        ],
        [
            ("OAuth fails", "Consent screen or redirect URL is not configured.", "Follow n8n credential instructions and retry authorization."),
            ("Video upload rejected", "File URL is inaccessible or format unsupported.", "Download the file locally or provide an MP4 path."),
            ("Wrong visibility", "Default visibility was not set intentionally.", "Use private or unlisted during training."),
        ],
        "An unlisted YouTube upload test with approved metadata.",
    ),
    Lab(
        6,
        "6.2",
        "interactive-browser-avatar",
        "Build an Interactive Avatar That Renders in the Browser",
        75,
        "A talking avatar that listens, thinks and answers with no cloud avatar, no credits and no render wait - and a measured latency to prove it.",
        [
            ("The interactive loop", "Speech to text, then the agent, then text to speech, then the mouth - each stage adds latency the learner can measure."),
            ("Latency engineering", "The reply must arrive in about a second, or the conversation feels dead. Every design choice in this lab serves that."),
            ("Barge-in", "The learner can interrupt the avatar mid-sentence, exactly as they would interrupt a person."),
            ("Drawn mouth vs real pixels", "The mouth here is geometry drawn on a photo - free and instant, but not photoreal. Lab 6.3 is the honest comparison."),
        ],
        [
            "Import `lab8/avatar-chat-flow.json` and publish it.",
            "Start the website with `lab8/website/start.command` (Mac) or `start.bat` (Windows), then open `http://localhost:8100` in Chrome or Edge.",
            "Open the gear and paste the Production webhook URL of the Lab 6.2 flow.",
            "Pick a face, hold the mic, and ask about the academy's courses.",
            "Read the latency line under the stage and note where the time actually goes.",
            "Open the flow and find the three settings that buy that speed: `think: false`, `keep_alive`, and a small `num_predict`.",
            "Interrupt the avatar while it is speaking and confirm it stops and listens.",
        ],
        [
            "The avatar answers out loud in roughly a second, and the page prints the measured time.",
            "Interrupting the avatar cuts it off immediately.",
            "The learner can explain why the flow calls Ollama directly instead of using the AI Agent node, and why a thinking model must be told not to think.",
        ],
        [
            ("The avatar says it did not catch that", "gemma4 is a thinking model: left alone it spends the whole token budget on an internal monologue and returns empty content.", "Set `think: false` in the Ollama request and give `num_predict` enough room for two spoken sentences."),
            ("The first reply takes several seconds", "The 9.6 GB model was not resident and had to be loaded from disk.", "Send a warm-up call when the page loads, and set `keep_alive` so the model stays in memory."),
            ("No microphone", "Speech recognition needs a secure context and a supported browser.", "Serve the page from `http://localhost`, not `file://`, and use Chrome or Edge."),
        ],
        "A working browser avatar, the measured latency, and a note naming the three settings that produced it.",
    ),
    Lab(
        6,
        "6.3",
        "interactive-heygen-liveavatar",
        "Embed an Interactive HeyGen Avatar with LiveAvatar",
        75,
        "The same conversation as Lab 6.2, but with a photoreal streaming avatar - and a clear-eyed comparison of what that costs.",
        [
            ("Streaming avatar", "A real face, streamed from the cloud, that moves its head and holds eye contact."),
            ("The ticket pattern", "n8n exchanges the API key for a short-lived embed URL. The browser gets the ticket, never the key."),
            ("Persona (context)", "One face, several personalities - the context decides what the avatar knows and how it behaves."),
            ("The honest trade-off", "Photoreal costs credits, a network round trip and an account. Drawn geometry costs nothing. Neither is simply better."),
        ],
        [
            "Import `lab9/liveavatar-session-flow.json` and publish it.",
            "Create the LiveAvatar API credential in n8n as a header credential and select it on both HTTP nodes.",
            "Start the website with `lab9/website/start.command` (Mac) or `start.bat` (Windows), then open `http://localhost:8099`.",
            "Open the gear and paste the Production webhook URL of the Lab 6.3 session flow.",
            "Pick a persona from the dropdown - the page lists them by calling the flow, not by hardcoding ids.",
            "Start the session and hold the same conversation you held with Aria in Lab 6.2.",
            "Fill in a two-column scorecard: latency, realism, cost per minute, and setup effort.",
        ],
        [
            "The browser starts a live photoreal avatar session.",
            "The learner can show that the API key is nowhere in the page source - only the short-lived embed URL is.",
            "The scorecard states, in the learner's own words, when to reach for a streaming avatar and when the browser-rendered one is enough.",
        ],
        [
            ("The avatar does not start", "The session flow returned no embed URL - usually a bad key or an avatar id the account cannot use.", "Open the flow's last execution and read the LiveAvatar error message, then check the key and the avatar id."),
            ("The persona dropdown is empty", "The contexts webhook is not published, or the account has no contexts yet.", "Publish the flow and confirm the contexts endpoint returns a list."),
            ("The browser blocks the audio", "Autoplay is blocked until the user interacts with the page.", "Click into the page before starting the session, and allow the microphone."),
        ],
        "A working streaming avatar session plus the two-column scorecard comparing it against the browser-rendered avatar.",
    ),
    Lab(
        6,
        "6.4",
        "workflow-monitoring-and-recovery",
        "Monitor, Debug, and Recover AI Workflows",
        60,
        "A monitoring checklist for failed executions, retries, and provider outages.",
        [
            ("Failure mode", "A predictable way a workflow can break."),
            ("Retry policy", "Defines when to try again and when to stop."),
            ("Fallback provider", "Keeps service running with a lower-quality or local option."),
            ("Runbook", "A short procedure another person can follow during an incident."),
        ],
        [
            "List failure modes for LLM, vector store, Retell, Vapi, HeyGen, LiveAvatar, Veo, and YouTube.",
            "For each failure, define retry, fallback, and human notification behavior.",
            "Add an error branch to one existing workflow.",
            "Simulate a failed API call using a wrong key or test URL, then restore it.",
            "Write a runbook with symptoms, first checks, and recovery steps.",
            "Review the runbook with another learner and close unclear steps.",
        ],
        [
            "At least one workflow has an error branch.",
            "The runbook covers credentials, quota, network, payload, and provider status.",
            "The fallback decision is explicit, not improvised during failure.",
        ],
        [
            ("Errors disappear", "Failed executions are not saved.", "Enable failed execution saving during development."),
            ("Workflow retries forever", "No stop condition exists.", "Limit retries and notify a human after threshold."),
            ("Fallback is unclear", "No provider decision was made.", "Choose the open-source local avatar, the browser-rendered avatar, or manual review as the fallback."),
        ],
        "A monitoring runbook and one tested error branch.",
    ),
    Lab(
        6,
        "6.5",
        "capstone-ai-workforce",
        "Capstone - Build a Human-AI Workforce Automation",
        120,
        "An end-to-end workflow that combines RAG, voice, video, publishing, and monitoring.",
        [
            ("System integration", "Combines multiple agents and tools into one business process."),
            ("Human-in-the-loop", "Places review gates where quality or risk requires judgement."),
            ("Operational handoff", "Documents ownership, monitoring, and improvement process."),
            ("Portfolio evidence", "Packages screenshots, exports, rubrics, and demo outputs."),
        ],
        [
            "Choose a capstone scenario such as course advisory, appointment booking, or training content production.",
            "Draw the workflow from trigger to final output, including human review gates.",
            "Reuse at least three previous lab components.",
            "Add a quality rubric and run three test cases.",
            "Fix the highest-risk failure discovered by testing.",
            "Package the exported workflow, screenshots, video or call output, and a one-page operating guide.",
        ],
        [
            "The capstone completes a realistic business process end to end.",
            "At least three agentic loop components are integrated.",
            "Evidence includes test cases, evaluation results, and improvement notes.",
        ],
        [
            ("Capstone is too broad", "It tries to automate an entire department.", "Reduce it to one trigger, one primary user, and one output."),
            ("No review gate", "The workflow publishes or contacts people automatically.", "Add approval before external publishing or customer communication."),
            ("Demo is fragile", "It depends on many paid services at once.", "Prepare a fallback path and a recorded output."),
        ],
        "A capstone package suitable for trainer assessment and learner portfolio.",
    ),
]


def rag_concepts_section() -> str:
    """Topic 02 prose: what RAG, tokenization and embeddings actually are."""
    return normalize_md(dedent(
        """
        ### The concepts behind RAG

        Read this before Lab 2.3. The labs will work if you only click the nodes, but you cannot *debug* a RAG agent - or explain to a manager why it answered wrongly - without these four ideas.

        #### What RAG is, and the problem it solves

        A language model only knows what was in its training data. It has never seen your IT FAQ, your course brochures, or your salon's cancellation policy. Ask it anyway and it will not say "I don't know" - it will produce fluent, confident, invented text. That failure has a name: **hallucination**.

        **Retrieval-Augmented Generation (RAG)** fixes this by changing the question you ask the model. Instead of:

        > "What is the refund policy?"

        the workflow silently asks:

        > "Here are three passages from the company handbook. Using ONLY these passages, answer: what is the refund policy? If the passages do not contain the answer, say you do not know."

        The model stops being a source of facts and becomes a *reader* of facts you supply. That is the whole idea. Everything else - embeddings, vector stores, chunking - exists only to answer one narrow question: **which passages should we paste in front of the question?**

        A RAG system therefore has two phases:

        | Phase | When it runs | What happens |
        |---|---|---|
        | **Indexing** (write) | Once, when a document is uploaded | Split the document into chunks -> embed each chunk -> store the vectors |
        | **Retrieval** (read) | On every question | Embed the question -> find the nearest chunks -> paste them into the prompt -> generate |

        In your n8n workflow these are the two paths you can literally see on the canvas: the upload path that ends at the vector store, and the chat path that reads from it.

        #### Tokenization - how text becomes numbers

        Models do not read characters or words. They read **tokens**: the sub-word units the model's vocabulary is built from. A tokenizer splits text deterministically:

        ```text
        "The salon is closed on Sundays."
          -> ["The", " salon", " is", " closed", " on", " Sund", "ays", "."]
             8 tokens
        ```

        Useful rules of thumb for English: **1 token is roughly 4 characters, or about 0.75 of a word** - so 1,000 tokens is roughly 750 words, or about 1.5 pages. Rare words, names, code and non-English text split into more tokens than you would expect (`Sundays` above became two).

        Tokens matter for three practical reasons:

        1. **Context windows are measured in tokens.** Everything you paste in - the system prompt, the retrieved chunks, the conversation memory, the question - competes for the same budget. Retrieve too many chunks and you push out the instructions.
        2. **Cost and latency are measured in tokens.** Doubling the retrieved text roughly doubles the prompt cost of every single call.
        3. **Chunk size is measured in tokens** (or characters, as an approximation of them). This is the number you will actually tune in Lab 2.4.

        #### Embeddings - meaning as coordinates

        An **embedding** is a list of numbers (a **vector**) that represents the *meaning* of a piece of text. An embedding model reads the text and outputs a fixed-length vector - in this course, `nomic-embed-text` running in Ollama, which outputs **768 numbers** for any input, whether it is three words or three paragraphs:

        ```text
        "How do I reset my password?"  ->  [0.021, -0.118, 0.334, ... ]   768 numbers
        ```

        The magic property is that **texts with similar meaning land close together in that 768-dimensional space, even when they share no words at all.** "How do I reset my password?" sits near "I forgot my login credentials" and far from "What are your opening hours?" - which is exactly what keyword search cannot do.

        Closeness is measured with **cosine similarity**: the cosine of the angle between two vectors, from `1.0` (identical direction/meaning) through `0.0` (unrelated) to `-1.0` (opposite). Retrieval is then embarrassingly simple:

        1. Embed the user's question with the **same** model used for the documents.
        2. Compare that vector against every stored chunk vector.
        3. Return the **top-k** most similar chunks (k is typically 3 to 5).

        Two consequences follow directly, and both cause real bugs:

        - **You must embed questions and documents with the same model.** Vectors from different models are not comparable - the numbers mean different things. Switch the embedding model and you must re-index every document.
        - **A vector store is not a database you can query with SQL.** It answers only one kind of question: "what is near this vector?"

        #### Chunking - why documents are cut up

        You cannot embed a 40-page PDF as one vector. A single vector would average away all the detail, and the retrieved passage would be far too big to paste into a prompt. So the document is **split into chunks** (say 800 characters each) with a small **overlap** (say 100 characters) carried between neighbours so a sentence cut in half still appears whole in one of them.

        Chunk size is a genuine trade-off, and it is the main thing you will tune:

        | Chunks too small | Chunks too large |
        |---|---|
        | Retrieved passage lacks context; the model sees half an answer | Retrieved passage contains the answer plus three irrelevant sections |
        | High precision, low recall | High recall, low precision |
        | Model says "the document does not say" when it does | Model gets distracted and cites the wrong part; tokens are wasted |

        There is no universally correct value. That is exactly why Lab 2.4 makes you measure it with golden questions instead of guessing.

        #### Putting it together

        ```text
        INDEXING   PDF -> split into chunks -> embed each chunk -> store 768-dim vectors
                                                (nomic-embed-text)      (Supabase / Qdrant / Pinecone)

        RETRIEVAL  question -> embed question -> cosine-similarity search -> top-k chunks
                                                                              |
                                                 "Using ONLY this context: <chunks>  Q: <question>"
                                                                              |
                                                                        gemma (Ollama) -> grounded answer
        ```

        **The habit to build:** when a RAG agent answers badly, do not immediately rewrite the prompt. First look at *what was retrieved*. Open the n8n execution and read the chunks that came back from the vector store. If the right chunk was never retrieved, no prompt in the world will save the answer - the bug is in chunking, embedding, or top-k, not in the wording.
        """
    ))


def ngrok_section(prefix: str) -> str:
    """Topic 04 prose: expose local n8n to the internet so a voice platform can call it."""
    return normalize_md(dedent(
        f"""
        ### Exposing n8n with ngrok - and why you must

        Labs 4.7 and 4.8 are the first time something **outside your machine** needs to call **into** n8n. Up to now every request came from your own browser, so `http://localhost:5678` worked. It will not work now.

        When Nina says *"let me check that for you"*, the request is made by **Retell's servers**, sitting in a datacenter. To them, `localhost` means *their own machine*, not yours. The request never leaves their building. The caller hears the agent stall in silence, and nothing at all appears in your n8n executions list. Same for Vapi's Custom LLM in Lab 4.8.

        A tunnel fixes this. It gives your local n8n a temporary public address, and forwards anything sent there to port 5678 on your laptop.

        | Who is calling n8n | Example | Needs a tunnel? |
        |---|---|---|
        | Your own browser | Labs 1-3, the Book by Voice button, `curl` | **No.** `localhost` is correct. |
        | Retell's servers | `check_availability`, `book_appointment` | **Yes.** |
        | Vapi's servers | the Custom LLM endpoint | **Yes.** |

        **Step-by-step (macOS and Windows)**

        1. Install ngrok:

            | macOS (Terminal) | Windows (PowerShell) |
            |---|---|
            | `brew install ngrok` | `winget install ngrok.ngrok` |

            On Windows, **close and reopen PowerShell** afterwards, or `ngrok` will not be found. (If winget is unavailable, download the ZIP from `https://ngrok.com/download`, unzip it, and run `.\\ngrok.exe` from the folder you unzipped it into.)

        2. Create a free account at `https://dashboard.ngrok.com/signup`, then copy your **authtoken** from *Getting Started -> Your Authtoken*. ngrok refuses to tunnel without one.
        3. Register the token once - it is saved to your ngrok config file, so you never repeat this. The command is the same on both platforms:

            ```bash
            ngrok config add-authtoken <YOUR_TOKEN>
            ```
        4. Start the tunnel, and **leave this window open** for the whole session. Closing it kills the tunnel:

            ```bash
            ngrok http 5678
            ```
        5. Read your public URL from the `Forwarding` line ngrok prints in that terminal:

            ```text
            Forwarding   https://3af5-175-156-143-249.ngrok-free.app -> http://localhost:5678
                         └────────── your public base URL ──────────┘
            ```

        6. Open ngrok's own dashboard in your browser - **bookmark this link, you will use it all day**:

            ```text
            http://127.0.0.1:4040
            ```

            It runs on your own machine (that is why the address is `127.0.0.1`, not an ngrok domain) and it has two tabs:

            - **Status** - your public URL. Look for **Tunnels -> command_line**: `URL` is the public address to paste into Retell or Vapi, and `Addr` confirms it forwards to `http://localhost:5678`. If you lose the URL, get it here - do not restart ngrok, or the URL will change.
            - **Inspect** - every request Retell or Vapi sends you, with its headers and body, as it arrives. This is the single most useful debugging tool in this topic: when the agent stalls mid-call, this page tells you instantly whether the request even reached your machine.

            An empty **Inspect** tab during a call means the request never arrived: the URL in Retell/Vapi is wrong, the tunnel is down, or the agent was not re-published after you changed it.

        {shot_md("ngrok-status", prefix)}

        **How to build the URL you paste into Retell or Vapi**

        You are gluing two halves together. n8n supplies the path; ngrok supplies the address.

        ```text
        https://3af5-175-156-143-249.ngrok-free.app  /webhook/  check-availability
        └────────── from ngrok ──────────────────┘             └── from the n8n Webhook node ──┘
        ```

        The rule: **open the Webhook node, take its Production URL, and replace `http://localhost:5678` with your ngrok address.** Everything after `/webhook/` stays exactly as n8n shows it.

        | n8n webhook node | Path | What you paste into Retell / Vapi |
        |---|---|---|
        | Webhook - check_availability | `check-availability` | `https://<your-ngrok>/webhook/check-availability` |
        | Webhook - book_appointment | `book-appointment` | `https://<your-ngrok>/webhook/book-appointment` |
        | Vapi Webhook (Lab 4.8) | `vapi-faq` | `https://<your-ngrok>/webhook/vapi-faq` |

        **Prove the tunnel works before you touch the voice platform**

        ```bash
        curl -X POST https://<your-ngrok>/webhook/vapi-faq \\
          -H 'Content-Type: application/json' \\
          -d '{{"model":"gpt-4o","messages":[{{"role":"user","content":"How long is the warranty on a Dyson?"}}]}}'
        ```

        A real answer means the tunnel, the webhook and the agent are all healthy. If this fails, fix it here - debugging over HTTP is far easier than debugging over audio.

        **Four things that will bite you**

        | Trap | What you see | Fix |
        |---|---|---|
        | The free URL changes every restart | Calls worked this morning, fail after lunch | Re-copy the new URL into Retell/Vapi and **publish the agent again**. Start ngrok once per day and leave it running. |
        | You used the **Test** URL | Works once during your demo, never again | Use the **Production** URL - `/webhook/`, never `/webhook-test/`. |
        | The workflow is not published | 404 "not registered" | Publish/activate the workflow, then retest. |
        | You set `WEBHOOK_URL` on the n8n container | Every lab now shows learners a public URL that goes stale | Do NOT change the Docker config. `localhost` must keep working for Labs 1-3. Paste the tunnel URL only where it is needed. |

        Closing the ngrok window kills the tunnel and the public URL is gone for good - the next start hands you a different one.
        """
    ))


def video_pipeline_section() -> str:
    """Topic 05 prose: the avatar-video pipeline, and the three lip-sync engines."""
    return normalize_md(dedent(
        """
        ### How the avatar video pipeline works

        Every video lab in this topic is the same three-step pipeline. Only the *renderer* changes - and choosing the renderer is the engineering decision the topic is really about.

        ```text
        YOU                    n8n                          RENDERER            BACK TO YOU
        ---------------------------------------------------------------------------------------
        type a TOPIC  --POST-->  Webhook
        (raw facts)                |
                                   v
                          Write Script (Ollama)        gemma4 turns facts into
                          + gemma4 chat model          SPOKEN COPY (~55-70 words)
                                   |
                                   v
                          send script + portrait --->  HeyGen / Wav2Lip / MuseTalk
                                   |                   renders the talking video
                                   v
                          Respond  ---------------------------------------->  video plays
                                                                              in the page
        ```

        **The two texts are not the same text, and this is the point people miss.** You type a *topic* - "Belgium beats USA 4-1 to reach the quarter-finals". That is a fact, not something an anchor can read aloud. gemma4 turns it into *broadcast copy* - "Welcome back to Global Sports News! Massive upsets continue...". The renderer speaks **every character** it is given: feed it your raw topic and the avatar reads out a comma-spliced list of facts. The system message is what makes the difference - it forbids stage directions, markdown and camera notes, because the avatar would dutifully read them out loud.

        **Synchronous or polled?** Two shapes appear in this topic, and they change the front end:

        | Lab | Shape | Why |
        |---|---|---|
        | Lab 5.3 (HeyGen) | n8n returns a `video_id` at once; the **page polls** `heygen-status` | Cloud renders take 1-3 minutes. Holding an HTTP request open that long is fragile. |
        | Lab 5.5 (local) | n8n returns the finished `video_url` in **one** response | A local render takes ~16 s, so the caller can simply wait. |

        Both pages show a progress bar. Note what it does NOT do: HeyGen reports only *processing* or *completed* - there is **no percentage to read**. So the bar is an honest elapsed-time estimate that eases toward 95% and stops there, reaching 100% only when the renderer actually reports done. A bar that sits at 100% while still spinning is a lie, and learners notice.

        ### The three lip-sync engines

        All three animate a still portrait to speech. They are not interchangeable, and Lab 5.1 makes you prove it on the same photo and the same script.

        | | Wav2Lip | MuseTalk | HeyGen |
        |---|---|---|---|
        | Where it runs | your machine | your machine | the cloud |
        | Cost | free | free | **credits** |
        | Privacy | photo never leaves | photo never leaves | photo + audio uploaded |
        | Speed (measured) | **~16 s** for a 7-second clip | ~75 s (Apple M4) | ~40 s to 3 min |
        | Mouth | 96x96 model, upscaled - **soft at 1080p** | real inpainted pixels: teeth, lips, shadow | photoreal |
        | Head / blinks | **no** - the head is frozen | **no** - the head is frozen | **yes** |
        | Needs | ffmpeg + the checkpoint | a GPU (Apple MPS / NVIDIA) + 3.5 GB weights | an API key and credits |
        | Fails when | - | no GPU | no credits, no network |

        The honest summary: **Wav2Lip is the fastest, MuseTalk looks the best, and only HeyGen moves the head.** Wav2Lip's mouth is generated at 96x96 pixels and then scaled up into a 1080p frame - the *timing* is excellent (it is still the sync benchmark others are measured against), but the mouth itself is soft, and the larger your output, the more you notice. MuseTalk inpaints real mouth pixels in latent space, which is exactly why it costs about seven times the compute.

        **The workplace question is not "which is best".** It is: would you upload a customer's face to a vendor in order to gain a moving head? Would you accept a soft mouth to keep a 16-second turnaround in a classroom? There is no single right answer - there is a defensible one, and writing it down is the deliverable.
        """
    ))


def retell_setup_section(prefix: str) -> str:
    """Topic 04 prose: how to set up Retell, and where each of the two webhooks goes."""
    return normalize_md(dedent(
        f"""
        ### Setting up Retell AI - and where each webhook goes

        Do this once, before Lab 4.2. Most of the pain in this topic comes from confusing the **two different webhooks** that point in **opposite directions**. Get the direction clear and the rest is form filling.

        | Webhook | Direction | Where the URL is written | Must it be public? |
        |---|---|---|---|
        | **Web-call trigger** (`/webhook/retell-web-call`) | Browser -> n8n -> Retell API | In the **website**: click **⚙ Settings** on the page and paste your own URL. Nothing is hardcoded. | No. `http://localhost:5678` is fine - your own browser calls it. |
        | **Agent tools** (`check_availability`, `book_appointment`) | Retell cloud -> n8n | In **Retell**, in each Custom Function's URL field | **Yes.** Retell's servers cannot reach your `localhost`. This needs a tunnel. |

        **Part A - Create the Retell account and API key**

        1. Sign up at `https://retellai.com`. The free trial credit is enough for this topic; a web call costs roughly $0.10 per minute, so keep test calls short.
        2. Go to **API Keys** and create a key (`key_...`). Copy it now - Retell shows it once.
        3. In n8n, create a **Header Auth** credential named exactly `Retell API`: **Name** `Authorization`, **Value** `Bearer key_...`. The key lives in n8n and never reaches the browser. That is the whole point of this architecture.

        **Part B - Create the agent (Nina)**

        4. **Agents -> Create an Agent -> single-prompt agent.** Name it `GG Hair Salon - Nina`, pick a voice and an LLM.
        5. Paste the persona, salon info, services and prices, and the behavior rules you wrote in Lab 4.1. Keep the rules short: one or two sentences per reply, one question at a time, confirm before booking, offer a stylist follow-up when unsure.
        6. Set the **Welcome Message** so Nina speaks first: *"Thanks for calling GG Hair Salon, this is Nina. How can I help you today?"* If you leave this blank the caller hears silence and assumes the call is broken.
        7. Click **Publish**. An unpublished agent will not answer a web call.
        8. Copy the **agent ID**. It is the `⧉ ID` button in the *Agent Details* strip at the top of the agent page (it is also the last part of the browser URL, after `/agents/`). It looks like `agent_7323e166b991e5d0067a1adaf8`.

        {shot_md("retell-agent", prefix)}

        **Part C - Point n8n and the website at YOUR agent**

        9. Open the `Lab 4 - Retell Web Call Trigger` workflow. Copy the **Webhook** node's **Production URL** (not the Test URL).
        10. In the **Create Retell Web Call** node, the body reads `agent_id` from the request with a fallback - and that fallback is the **trainer's** demo agent. Replace it with your own ID, or send yours from the website in the next step, or you will be calling the trainer's agent.
        11. Confirm the node uses the `Retell API` credential, then **Activate** the workflow.
        12. Open the site (`http://localhost:8090`), click **⚙ Settings**, paste the **Production URL** and your **`agent_...` ID**, and Save. The values are stored in your browser only, so every learner drives the same site from their own n8n and their own agent.

        **Part D - The agent's tool webhooks (this is the part that needs a tunnel)**

        The functions in your agent - `check_availability` and `book_appointment` - are called by **Retell's servers**, not by your browser. Retell cannot see `http://localhost:5678`, so a localhost URL here fails silently mid-call: Nina says she is checking availability and then stalls.

        13. Expose n8n publicly with a tunnel, and keep it running for the whole lab:

            ```bash
            ngrok http 5678                              # copy the https://….ngrok-free.app URL
            cloudflared tunnel --url http://localhost:5678
            ```

            Free ngrok URLs change on every restart, so if calls break after lunch, re-copy the URL and re-publish the agent.
        14. Build the n8n workflow that answers the tool call: a **Webhook** node (POST, path `check-availability`, and a second for `book-appointment`), your availability or Google Calendar logic, then a **Respond to Webhook** node returning a small JSON result. Nina speaks the response, so keep it short - `{{ "available": true, "slots": ["2 PM", "4 PM"] }}` is plenty. Activate it and use the **Production** URL.
        15. In Retell, open the agent and find the **Functions** panel. Click **+ Add -> Custom Function**. *This is where the webhook goes in Retell:*
            - **Name:** `check_availability` - the name the LLM uses to decide when to call it.
            - **Description:** "Check whether a service slot is free on a given date and time." The LLM picks the tool from this sentence, so write it for the model, not for a human.
            - **URL:** your tunnel URL plus the path - `https://<your-tunnel>/webhook/check-availability`
            - **Parameters:** a JSON schema with the slots you collect - `service`, `date`, `time`, plus `name` and `phone` for booking.
        16. Repeat for `book_appointment` at `https://<your-tunnel>/webhook/book-appointment`. Keep `end_call` enabled so Nina can hang up cleanly.
        17. **Publish the agent again.** Function changes do not affect a live call until you publish.
        18. Test the wiring before you test by voice: use **Run Test** and ask for a Thursday 2 PM slot. Watch the n8n executions list - a new execution must appear *during* the call. No execution means Retell could not reach your URL: check the tunnel, the `/webhook/` (not `/webhook-test/`) path, and that the workflow is Active.

        {shot_md("retell-functions", prefix)}

        **How to tell which webhook is broken**

        | Symptom | The broken webhook |
        |---|---|
        | The call never starts | Browser -> n8n. Wrong URL in ⚙ Settings, workflow inactive, or CORS. |
        | Nina greets you, then stalls while "checking availability" | Retell -> n8n. Tunnel is down, or the function URL is a localhost URL. |
        | The call connects but Nina is silent from the start | Not a webhook at all - empty Welcome Message, or the agent is unpublished. |
        """
    ))


def voice_conversation_section() -> str:
    """Topic 04 prose: the turn-by-turn call the learner runs with the voice agent."""
    return normalize_md(dedent(
        """
        ### The voice conversation, turn by turn

        Use this script for your first end-to-end call after Lab 4.5. Click **Book by Voice** on `http://localhost:8090`, allow the microphone, and wait for Nina to speak first. Say one line at a time and let her finish - interrupting is the most common cause of a broken slot capture.

        The **What to listen for** column is what you are grading. If a turn fails, note it and keep going; you will fix it in the QA pass (Lab 4.3).

        | # | You say | Nina should | What to listen for |
        |---|---|---|---|
        | 1 | *(say nothing - just listen)* | Greet and offer help: "Thanks for calling GG Hair Salon, this is Nina. How can I help you today?" | She opens the call. Silence here means the token was minted but the audio session never started. |
        | 2 | "Hi Nina, I'd like to book a haircut." | Ask a single question - which service, or which day. | **One** question, not three. A multi-part question is a Lab 4.1 script defect. |
        | 3 | "How much is a women's cut?" | Answer **$65**, a 1-hour slot. | The price comes from the handbook. A vague or wrong price means the KB is not attached. |
        | 4 | "And what's your cancellation policy?" | State the **12-hour** rule and the **50%** charge for a late cancellation or no-show. | This fact exists only in the PDF. This is the grounding proof. |
        | 5 | "Do I need to pay a deposit for colour?" | Say **$30**, applied to the final bill. | Second grounded fact. She should not hedge. |
        | 6 | "Do you do nail extensions?" | Decline to guess and offer to check with a stylist. | The honest refusal. If she invents a nail price, the grounding instruction is missing. |
        | 7 | "Okay, book me the women's cut." | Start slot filling: ask for the day and time. | She moves from answering to acting - the KB answers questions, the tools take actions. |
        | 8 | "Thursday at 2 PM." | Check availability through the n8n tool webhook and respond. | Watch the n8n executions list: a new execution must appear **during** the call. |
        | 9 | "It's Alex, and my number is 9123 4567." | Read the details back for confirmation. | Every slot repeated: name, service, date, time, contact. |
        | 10 | "Yes, that's correct." | Confirm the booking and close the call. | The booking is created only **after** you confirm - never before. |

        **Two more calls you must run** - they are what the Lab 4.3 QA scorecard is built from:

        - **The incomplete caller.** At turn 8 say only *"sometime Thursday"*. Nina must ask a repair question for the time. An agent that silently invents 9:00 AM has failed.
        - **The changed-mind caller.** At turn 10 say *"actually, make it Friday instead"*. She must update the slot and re-confirm, not book Thursday anyway.

        Save all three transcripts from **Call History** in the Retell dashboard. They are the evidence for Lab 4.3 and for the capstone.
        """
    ))


def lab_dir(lab: Lab) -> Path:
    return LABS_DIR / f"topic-{lab.topic:02d}" / f"lab-{lab.lab_no}-{lab.slug}"


def md_table(rows: list[tuple[str, str]]) -> str:
    body = "\n".join(f"| {a} | {b} |" for a, b in rows)
    return f"| Concept | In one line |\n|---|---|\n{body}"


def normalize_md(text: str) -> str:
    cleaned = []
    for line in text.splitlines():
        while line.startswith("    "):
            line = line[4:]
        cleaned.append(line.rstrip())
    return "\n".join(cleaned).strip() + "\n"


def lab_readme(lab: Lab) -> str:
    concepts = md_table(lab.concepts)
    steps = "\n".join(f"{i}. {step}" for i, step in enumerate(lab.steps, 1))
    verify = "\n".join(f"- [ ] {item}" for item in lab.verify)
    trouble = "\n".join(f"| {a} | {b} | {c} |" for a, b, c in lab.troubleshooting)
    agent_prompt = dedent(
        f"""
        I am completing {lab.title} in the course "Automate Video and Voice AI Agents with n8n".
        Act as a careful agentic AI workflow reviewer. Review my workflow design against this goal:
        {lab.build}

        Check for:
        - missing trigger, input, output, or credential boundary
        - weak system prompt or unclear tool description
        - missing evaluation case, refusal case, or human review gate
        - any place where a secret could leak to browser code or exported notes

        Return a concise list of fixes, then give me one improved test case.
        """
    ).strip()
    return normalize_md(dedent(
        f"""
        # Lab {lab.lab_no} - {lab.title}

        > Topic {lab.topic} - Approximately {lab.minutes} minutes - Adult workplace lab

        ## The build so far

        This lab is part of a complete agentic AI automation course. Each lab follows the same engineering loop:

        **Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

        In this lab you build: **{lab.build}**

        ## What you will build

        {lab.build} The work is intentionally practical: by the end of the lab you should have an artifact that can be inspected, tested, and reused in the capstone.

        ## Concepts you will meet

        {concepts}

        ## Before you start

        - Complete the setup in Lab 1.1 or confirm Docker, n8n, Ollama, and your browser are ready.
        - Keep n8n executions visible while testing. The execution trace is your evidence.
        - Do not place API keys in HTML, JavaScript, Markdown examples, screenshots, or exported workflow notes.
        - Commit or export a checkpoint before making large workflow changes.

        ## Step-by-step instructions

        {steps}

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
        {agent_prompt}
        ```

        ## Verify

        {verify}

        ## Reflection questions

        1. What did the agent or workflow do correctly on the first attempt?
        2. What evidence proves the output was grounded, safe, or complete?
        3. Which failure case was most useful for improving the workflow?
        4. What should a human still review before this automation is used with real customers?

        ## Common errors

        | Error | Likely cause | Fix |
        |---|---|---|
        {trouble}

        ## Submission evidence

        Submit the following:

        - Workflow export or screenshot of the main workflow canvas.
        - Screenshot or copy of the successful execution output.
        - One normal test case and one edge or unsafe test case.
        - A short note explaining what you changed after evaluation.

        ## Lab deliverable

        {lab.deliverable}
        """
    ))


def learner_guide(img_prefix: str = "courseware/screenshots/") -> str:
    """img_prefix makes the image links resolve from wherever the guide is written."""
    toc = [
        "# Learner Guide - Automate Video and Voice AI Agents with n8n",
        "",
        f"**Course code:** {COURSE_CODE}  |  **Conducted by:** {ORG}  |  "
        f"**Version:** {VERSION}  |  **Date:** {VERSION_DATE}",
        "",
        "## Contents",
        "",
        "- Introduction",
        "- Course learning outcomes",
        "- How this course uses agentic AI loop engineering",
        "- Environment setup",
        "- Topic and lab guides",
        "- How you are assessed",
        "- Capstone assessment guidance",
        "- Troubleshooting and glossary",
        "",
    ]
    intro = dedent(
        """
        ## Introduction

        This Learner Guide supports the adult training course **Automate Video and Voice AI Agents with n8n**. The course teaches learners how to design, build, test, and improve practical AI automations using n8n, Ollama, RAG, Retell, Vapi, HeyGen, LiveAvatar, Google Veo 3.1, open-source lip-sync rendering, and publishing workflows.

        The emphasis is not "click nodes until it works". The emphasis is engineering judgement. Learners will practise the agentic AI loop:

        **Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

        Every lab produces evidence: workflow exports, screenshots, test cases, quality rubrics, generated videos, call transcripts, or monitoring runbooks. This makes the course suitable for adult learners who need workplace-ready habits, not just tool demonstrations.

        ## Course learning outcomes

        By the end of the course, learners will be able to:

        - LO1: Set up a local AI automation workstation using Docker, n8n, Postgres, Ollama, and browser-based test pages.
        - LO2: Apply agentic AI loop engineering to define goals, tools, evaluation criteria, guardrails, and human review gates.
        - LO3: Build local AI agents with n8n and Ollama, including memory, tool calling, and execution-based debugging.
        - LO4: Build document-grounded RAG agents using embeddings, vector stores, chunking, retrieval tests, and grounded refusal behavior.
        - LO5: Build customer-facing and staff-facing AI assistants that collect structured data and prepare safe workflow handoffs.
        - LO6: Build voice AI agents using Retell, secure n8n webhooks, browser call front ends, transcript review, and QA scorecards.
        - LO7: Build AI video workflows using script agents, HeyGen, Google Veo 3.1 text-to-video, open-source local avatar rendering, and interactive avatars.
        - LO8: Publish and operate AI outputs using review gates, YouTube upload automation, monitoring, fallback plans, and capstone documentation.

        ## How this course uses agentic AI loop engineering

        Agentic AI loop engineering is the repeatable practice of designing and improving an AI workflow through evidence. A model response is not trusted because it sounds fluent. A workflow is not accepted because it ran once. Each automation must define the job, expose the right tools, capture the execution trace, evaluate against test cases, improve the weakest behavior, add guardrails, and document how to operate it.

        ### The seven-part loop

        1. **Define** - Name the user, trigger, input, output, success criteria, and non-goals.
        2. **Build** - Create the smallest useful workflow before adding features.
        3. **Observe** - Inspect n8n executions, model prompts, retrieved documents, API responses, and generated media.
        4. **Evaluate** - Use normal, edge, unsafe, and unsupported inputs. Score the result.
        5. **Improve** - Change one prompt, node, chunking parameter, or guardrail at a time.
        6. **Guardrail** - Protect secrets, personal data, external publishing, bookings, refunds, and unsupported claims.
        7. **Document** - Record setup, test evidence, decisions, fallback, and owner.

        ### Adult learning approach

        The labs use workplace examples: course advisory, IT support, appointment booking, training videos, customer follow-up, and publishing. Learners are expected to compare alternatives, explain trade-offs, and build evidence. Trainers should ask learners to show execution traces and quality rubrics, not only final screens.

        ## Environment setup

        ### Required tools

        Every lab runs on **macOS and on Windows**. The tools are identical; only the way you install them and the way you type a command differ. Where this guide shows a command, it gives both.

        | Tool | What it is for |
        |---|---|
        | Docker Desktop | Runs n8n and Postgres |
        | Ollama | The local chat and embedding models - no cloud, no cost |
        | A modern browser | The lab websites; must allow microphone access for the voice labs |
        | Python 3 | Serving the lab websites over `http://localhost` |
        | ffmpeg | Local video rendering and verification (Topic 05) |
        | ngrok | Only from Lab 4.7 onward, when a cloud platform must call into your n8n |
        | Paid accounts (optional) | Retell, Vapi, HeyGen, LiveAvatar, Google Gemini (Veo 3.1), YouTube |

        ### Installing the tools

        **The package manager (do this first - everything else is one line after it)**

        | | macOS | Windows |
        |---|---|---|
        | Manager | **Homebrew** - paste the install line from `https://brew.sh` into Terminal | **winget** - already built into Windows 10/11. Nothing to install. |
        | Terminal | **Terminal** (Applications -> Utilities) | **PowerShell** - press Start, type `powershell`, and open it |

        **The tools**

        | Tool | macOS | Windows |
        |---|---|---|
        | Docker Desktop | `brew install --cask docker`, then launch Docker from Applications | `winget install Docker.DockerDesktop`, then launch Docker Desktop |
        | Ollama | `brew install ollama` then `ollama serve` | `winget install Ollama.Ollama` (it runs in the system tray) |
        | Python 3 | Already installed. Check: `python3 --version` | `winget install Python.Python.3.12` - **tick "Add python.exe to PATH"** if you use the installer instead |
        | ffmpeg | `brew install ffmpeg` | `winget install Gyan.FFmpeg` |
        | ngrok | `brew install ngrok` | `winget install ngrok.ngrok` |

        On Windows, **close and reopen PowerShell after installing** - a new program is not on your PATH until you do. If a command is "not recognized", that is almost always the reason.

        Docker Desktop on Windows needs **WSL 2**. The installer usually enables it, but if Docker refuses to start, run `wsl --install` in PowerShell **as Administrator**, reboot, and start Docker again.

        ### Core setup steps

        Both platforms, from the repository folder:

        ```bash
        cd lab0
        docker compose up -d
        ollama pull gemma4
        ollama pull nomic-embed-text
        ```

        Then open n8n at `http://localhost:5678` and create your owner account.

        In n8n, create an **Ollama** credential with this base URL:

        ```text
        http://host.docker.internal:11434
        ```

        This matters because n8n runs inside Docker. From the container's point of view, `localhost` is the container itself, not the machine running Ollama. `host.docker.internal` is how a container says "my host". It works the same on macOS and Windows.

        ### The four command differences you will actually hit

        This is the whole list. Everything else in the course is identical on both platforms.

        | Task | macOS (Terminal) | Windows (PowerShell) |
        |---|---|---|
        | Serve a lab website | `cd lab4/website`<br>`python3 -m http.server 8090` | `cd lab4\\website`<br>`python -m http.server 8090` |
        | One-click launcher | double-click `start.command` | double-click `start.bat` |
        | Path separator | `lab4/website` (forward slash) | `lab4\\website` (backslash) |
        | A `curl` with a JSON body | single quotes work:<br>`curl -X POST url -H 'Content-Type: application/json' -d '{{"a":1}}'` | PowerShell mangles quotes. Use `curl.exe` and escape:<br>`curl.exe -X POST url -H "Content-Type: application/json" -d '{{\\"a\\":1}}'`<br>Or simply use the n8n UI's own test panel instead. |

        Note the Python one: on macOS the command is **`python3`**; on Windows it is **`python`**. Typing `python3` on Windows opens the Microsoft Store, which is confusing and does nothing useful.

        ### Course evidence folder

        Create a local folder outside the repository for personal evidence:

        ```text
        course-evidence/
          lab-01/
          lab-02/
          screenshots/
          workflow-exports/
          rubrics/
          videos/
        ```

        Do not store API keys in this folder.
        """
    ).strip()

    lab_sections = []
    for idx, (topic_title, topic_desc) in enumerate(TOPICS, 1):
        lab_sections.append(f"\n\n## {topic_title}\n\n{topic_desc}\n")
        topic_labs = [lab for lab in LABS if lab.topic == idx]
        lab_sections.append("\n### Key concepts\n\n")
        lab_sections.append(
            "\n".join(
                f"- **{lab.title}:** {lab.build}" for lab in topic_labs
            )
        )
        lab_sections.append("\n\n")
        # Topic 02 needs RAG/tokenization/embeddings defined before the RAG labs.
        if idx == 2:
            lab_sections.append("\n" + rag_concepts_section() + "\n")
        # Topic 04 needs the Retell account/webhook setup before its labs make sense,
        # and the tunnel section before any lab where a cloud platform calls into n8n.
        if idx == 4:
            lab_sections.append("\n" + retell_setup_section(img_prefix) + "\n")
            lab_sections.append("\n" + ngrok_section(img_prefix) + "\n")
        # Topic 05 needs the pipeline shape and the engine trade-off up front.
        if idx == 5:
            lab_sections.append("\n" + video_pipeline_section() + "\n")
        for lab in topic_labs:
            lab_sections.append("\n\n")
            lab_sections.append(
                dedent(
                    f"""

                    ### Lab {lab.lab_no} - {lab.title}

                    **Time:** {lab.minutes} minutes

                    **Goal:** {lab.build}

                    **Why this matters:** This lab trains a practical part of the agentic AI loop. The important habit is to inspect evidence, not to assume that a fluent model output is correct.

                    **Concepts**

                    {md_table(lab.concepts)}

                    **Step-by-step**

                    {chr(10).join(f"{i}. {step}" for i, step in enumerate(lab.steps, 1))}

                    **Checkpoint**

                    {chr(10).join(f"- {item}" for item in lab.verify)}

                    **Trainer facilitation notes**

                    - Ask learners to show the exact execution or output that proves completion.
                    - Ask one learner to run an edge case while another observes the trace.
                    - Ask learners what they changed after evaluation and why.
                    - Do not accept a screenshot alone if the lab requires a workflow export, scorecard, transcript, or generated media.

                    **Common errors**

                    | Error | Likely cause | Fix |
                    |---|---|---|
                    {chr(10).join(f"| {a} | {b} | {c} |" for a, b, c in lab.troubleshooting)}

                    **Deliverable:** {lab.deliverable}
                    """
                ).strip()
            )
            shots = "\n\n".join(
                md for md in (shot_md(key, img_prefix) for key in lab_shots(lab)) if md
            )
            if shots:
                lab_sections.append("\n\n" + shots)
            # The turn-by-turn call belongs right after the knowledge-base lab.
            if lab.lab_no == "4.5":
                lab_sections.append("\n\n" + voice_conversation_section())

    appendices = dedent(
        """

        ## How you are assessed

        The deck tells you the appeal route is in this guide. Here it is, along with everything
        else you are entitled to know before you sit the papers.

        | | Written Assessment (SAQ) | Case Study (CS) |
        |---|---|---|
        | What it tests | Knowledge - the concepts behind the labs | Application - judgement on a workplace scenario |
        | Length | 6 open-ended questions | 6 scenario tasks |
        | Time | 60 minutes | 60 minutes |
        | Conditions | Open book, individually attempted | Open book, individually attempted |

        Both papers are sat on the final day, after an assessment briefing. There are no multiple
        choice questions. Nothing is assessed that the slides and the labs did not teach.

        **Marking.** Each criterion is graded **Competent (C)** or **Not Yet Competent (NYC)**. You
        are competent when every criterion on the paper is met.

        **If you are Not Yet Competent.** You are re-assessed **once**, on the failed instrument
        only. The trainer records the gap, you close it, and you sit that paper again. A
        re-assessment is a normal part of competency-based training - it is not a failure of the
        course.

        **Submission.** Complete your answers on the document provided and upload them to the LMS
        at https://lms-tms.tertiaryinfotech.com/.

        **Appeals.** If you believe an assessment decision is wrong, tell the trainer on the day and
        ask for the appeal form. State what you were marked NYC on and why you disagree. The
        assessment is reviewed by a second assessor, and you are told the outcome in writing. Raising
        an appeal never counts against you.

        ## Capstone assessment guidance

        The capstone must combine at least three lab components. A strong capstone includes:

        - A one-page workflow design canvas.
        - An n8n workflow export.
        - Test cases covering normal, edge, and unsafe input.
        - A quality rubric with scores and improvement notes.
        - A human review gate before external publishing or customer-impacting action.
        - A fallback plan if a paid provider is unavailable.
        - Screenshots, transcript, generated video, or other output evidence.

        ### Suggested capstone scenarios

        - Course advisory assistant that answers from brochures, captures leads, and notifies staff.
        - Voice booking assistant that confirms appointment details and escalates exceptions.
        - Training video factory that turns approved learning points into avatar videos or Veo 3.1 clips.
        - Customer support workflow that uses RAG, structured handoff, and monitoring.

        ### Assessment rubric

        | Criterion | Meets standard |
        |---|---|
        | Problem definition | Clear user, trigger, output, success criteria, and non-goals. |
        | Workflow correctness | Nodes are connected logically and executions prove the expected path. |
        | AI quality | Prompts, retrieval, and generated outputs are tested against a rubric. |
        | Guardrails | Secrets, personal data, unsupported claims, and publishing actions are controlled. |
        | Human review | High-risk decisions have approval or escalation. |
        | Documentation | Another operator can run, test, and recover the workflow. |

        ## Troubleshooting

        | Symptom | First check | Typical fix |
        |---|---|---|
        | n8n cannot reach Ollama | Ollama credential base URL | Use `http://host.docker.internal:11434`. |
        | Agent produces empty answer | Tool name, model output, execution trace | Rename tools simply and inspect model node output. |
        | RAG answer is invented | Prompt and retrieval trace | Add evidence-only instruction and refusal rule. |
        | Website cannot call n8n | Workflow active state and webhook URL | Activate workflow and use production webhook URL. |
        | Voice call fails | API key, microphone permission, session response | Fix credential and browser permission. |
        | Video generation fails | API quota, payload length, credential | Run a short test and inspect provider response. |
        | The generated video does not match the idea | The gemma4 shot script | Tighten the subject, camera and lighting wording, then regenerate. |

        ## Glossary

        - **Agent:** A workflow component that uses a model plus context, memory, or tools to complete a task.
        - **Agentic AI loop:** The engineering cycle used to design, test, improve, and operate AI workflows.
        - **Embedding:** A numeric representation of text used for similarity search.
        - **Grounding:** Requiring answers to come from approved sources or retrieved documents.
        - **Guardrail:** A rule, branch, approval, or technical boundary that reduces unsafe behavior.
        - **Human-in-the-loop:** A workflow design where a person reviews or approves high-risk actions.
        - **RAG:** Retrieval-Augmented Generation, where the model retrieves relevant information before answering.
        - **Tool call:** A controlled action the agent can request, such as creating a booking or searching a vector store.
        - **Vector store:** A database or memory store that retrieves text chunks by semantic similarity.
        - **Webhook:** A URL that starts a workflow when another app or browser sends an HTTP request.
        """
    ).strip()
    return normalize_md("\n".join(toc) + "\n" + intro + "".join(lab_sections) + "\n\n" + appendices)


DAYS = 5
ASSESSMENT_BLOCK = [
    ("Assessment briefing - instruments, timing, and what evidence is graded", 15),
    ("**Written Assessment (SAQ)** - 6 open-ended knowledge questions (K1-K6)", 60),
    ("**Case Study (CS)** - 6 scenario tasks drawn from the labs (A1-A6)", 60),
]
ASSESSMENT_MINUTES = sum(m for _, m in ASSESSMENT_BLOCK)


def _day_plan():
    """Spread the labs across the five training days, each of exactly 8 instructional hours.

    9:30-6:30 with a 1-hour lunch = 8 hours taught. Tea breaks are counted inside the
    sessions, not on top of them, or the day silently becomes nine hours.

    Filling each day to the brim in order is what produced the old Day 5: one 120-minute
    capstone followed by a six-hour "review" block, with the assessment nowhere on the
    timetable. So we level the load instead - each day takes its fair share of what is
    left - and the final day reserves the assessment first, then takes labs.
    """
    day_minutes = 8 * 60
    total = sum(lab.minutes for lab in LABS)
    last_cap = day_minutes - ASSESSMENT_MINUTES     # the final day owes 2h15 to the papers

    # Each of the first four days carries at least `target`, which is whichever is larger:
    # an even share of the labs, or the share that leaves the final day no more lab time
    # than it can hold alongside the assessment. Aim only for the even share and the labs
    # the early days decline pile up on Day 5 - which is how it ended at 11:30pm.
    target = max(total / DAYS, (total - last_cap) / (DAYS - 1))

    days, current, used = [], [], 0
    for lab in LABS:
        on_last_day = len(days) == DAYS - 1
        full = used >= target or used + lab.minutes > day_minutes
        if current and full and not on_last_day:
            days.append(current)
            current, used = [], 0
        current.append(lab)
        used += lab.minutes
    if current:
        days.append(current)

    final = sum(lab.minutes for lab in days[-1])
    assert final <= last_cap, f"Day {len(days)} has {final} min of labs but only {last_cap} free"
    return days


def lesson_plan(slide_map: dict[str, int] | None = None) -> str:
    slide_map = slide_map or {}
    days = _day_plan()

    def hhmm(total: int) -> str:
        """Wall-clock time, `total` being minutes since midnight."""
        h, m = divmod(total, 60)
        ampm = "am" if h < 12 else "pm"
        h12 = h if h <= 12 else h - 12
        return f"{h12}:{m:02d}{ampm}"

    day_sections = []
    for d, labs in enumerate(days, 1):
        is_last = d == len(days)

        # Build the day as an ordered list of (title, minutes, deck ref, evidence), then
        # walk a real wall clock over it. The old version derived the clock from a taught-
        # minutes counter and bolted +60 on once it passed 1:00pm, which stretched whichever
        # activity happened to straddle noon into a two-hour block and printed the LUNCH row
        # out of sequence beside it.
        items = []
        for lab in labs:
            slide = slide_map.get(lab.lab_no)
            items.append((
                f"Lab {lab.lab_no} - {lab.title}", lab.minutes,
                f"Slide {slide}" if slide else "-", lab.deliverable,
            ))

        taught = sum(l.minutes for l in labs) + (ASSESSMENT_MINUTES if is_last else 0)
        # Every training day totals EXACTLY 8 instructional hours. What the labs do not fill
        # is concept delivery and evidence review - the deck's concept, workflow and quality
        # slides are taught time too, and calling that "review" understated it.
        slack = 8 * 60 - taught
        if slack > 0:
            items.append((
                "Concept delivery, review and evidence check - the trainer teaches the "
                "concept, workflow and quality slides for the day's labs, then learners "
                "show their executions, transcripts and scorecards",
                slack, "-", "Trainer sign-off on the day's evidence",
            ))
            taught += slack

        if is_last:
            for title, mins in ASSESSMENT_BLOCK:
                items.append((title, mins, "-", "Completed answer script submitted on the LMS"))

        # Lunch is a fixed hour, taken at the activity boundary nearest 1:00pm. It never
        # splits an activity, so the clock in this table is the clock in the room.
        bounds, run = [], 0
        for _, mins, _, _ in items:
            run += mins
            bounds.append(run)
        target = 210                                  # 210 min after 9:30am = 1:00pm
        lunch_after = min(range(len(bounds)), key=lambda i: abs(bounds[i] - target))

        rows, t = [], 9 * 60 + 30                     # the day starts at 9:30am
        for i, (title, mins, ref, evidence) in enumerate(items):
            rows.append(f"| {hhmm(t)} - {hhmm(t + mins)} | {mins} min | {title} | {ref} | {evidence} |")
            t += mins
            if i == lunch_after:
                rows.append(f"| {hhmm(t)} - {hhmm(t + 60)} | 60 min | **LUNCH** | - | - |")
                t += 60

        day_sections.append(
            f"### Day {d}\n\n"
            "| Time | Duration | Topic / Activity | Deck | Evidence produced |\n"
            "|---|---|---|---|---|\n"
            + "\n".join(rows)
            + f"\n\n**Day {d} instructional time: {taught // 60}h {taught % 60:02d}m** "
            f"(9:30am-{hhmm(t)}, less a 1-hour lunch; tea breaks are taken inside the sessions).\n"
        )

    topic_rows = []
    for idx, (topic, desc) in enumerate(TOPICS, 1):
        labs = ", ".join(f"Lab {lab.lab_no}" for lab in LABS if lab.topic == idx)
        topic_rows.append(f"| {idx} | {topic} | {desc} | {labs} |")

    total_min = sum(l.minutes for l in LABS)

    return normalize_md(dedent(
        f"""
        # Lesson Plan - {COURSE_TITLE}

        ## Course profile

        | | |
        |---|---|
        | Provider | {ORG} |
        | Course code | {COURSE_CODE} |
        | Version | {VERSION} ({VERSION_DATE}) |
        | Mode | Instructor-led adult training, hands-on labs |
        | Duration | {len(days)} training days, 8 instructional hours each |
        | Practical ratio | At least 70 percent hands-on lab time |
        | Trainer | Dr Alfred Ang |

        ## Trainer strategy

        Demonstrate each concept with one small working example, then move quickly into learner practice. For every lab, ask learners to show the **evidence** - the n8n execution trace, the generated media, the call transcript, the scorecard. Do not accept a screenshot of a finished screen as proof that the workflow is correct: a fluent output and a correct workflow are not the same thing, and telling them apart is the skill this course teaches.

        ## Topic map

        | Session | Topic | Focus | Labs |
        |---|---|---|---|
        {chr(10).join(topic_rows)}

        ## Daily schedule

        Total taught content: {total_min // 60} hours {total_min % 60:02d} minutes across {len(LABS)} labs.

        {chr(10).join(day_sections)}

        ## Assessment

        | Instrument | Duration | What it tests | When |
        |---|---|---|---|
        | Briefing for Assessment | 15 min | The learner knows the instruments, the criteria and the appeal route | Before the assessment, on the final day |
        | Written Assessment (WA) - Short Answer | 60 min | KNOWLEDGE: the concepts behind the labs | Final day, after the briefing |
        | Case Study (CS) | 60 min | APPLICATION: judgement on a workplace scenario built from the labs | Final day, after the WA |

        Both instruments are **open book**, individually attempted, and marked **Competent / Not Yet Competent**. A learner assessed NYC is re-assessed once, on the failed instrument only.

        ## Evidence the trainer collects

        - Workflow exports and n8n execution traces for each lab.
        - The RAG evaluation sheet (Lab 2.4) with two chunking configurations scored.
        - Voice call transcripts and the QA scorecard (Lab 4.3).
        - The lip-sync comparison scorecard: Wav2Lip vs MuseTalk vs HeyGen on one script (Lab 5.1).
        - Generated media: the avatar news video, the Veo clip, the interactive avatar session.
        - The capstone workflow export and its one-page operating guide.
        """
    ))


def readme() -> str:
    lab_rows = "\n".join(
        f"| {lab.lab_no} | {lab.title} | {lab.minutes} min | [`labs/topic-{lab.topic:02d}/lab-{lab.lab_no}-{lab.slug}/`](labs/topic-{lab.topic:02d}/lab-{lab.lab_no}-{lab.slug}/) |"
        for lab in LABS
    )
    topic_rows = "\n".join(f"- **{title}:** {desc}" for title, desc in TOPICS)
    return normalize_md(dedent(
        f"""
        # Automate Video and Voice AI Agents with n8n

        **WSQ course - Tertiary Infotech Academy Pte Ltd**

        This repository contains high-quality adult-training courseware for building AI agents, RAG assistants, voice agents, and AI avatar/video automations with n8n.

        The rebuilt courseware follows an **agentic AI loop engineering** standard:

        **Define -> Build -> Observe -> Evaluate -> Improve -> Guardrail -> Document**

        ## Courseware deliverables

        - [Learner Guide Markdown](courseware/LG-Automate-Video-and-Voice-AI-Agents-with-n8n.md)
        - [Learner Guide DOCX](courseware/LG-Automate-Video-and-Voice-AI-Agents-with-n8n.docx)
        - [PowerPoint deck](courseware/{PPT_STEM}.pptx)
        - [Lesson Plan](courseware/LP-Automate-Video-and-Voice-AI-Agents-with-n8n.md)

        ## Topics

        {topic_rows}

        ## Labs

        | Lab | Title | Time | Folder |
        |---|---:|---:|---|
        {lab_rows}

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
        """
    ))


IMG_RE = re.compile(r"^!\[(?P<alt>[^\]]*)\]\((?P<src>[^)]+)\)\s*$")


def plain(text: str) -> str:
    """Strip Markdown emphasis/code marks. Slides render text literally, so a step
    written as **Publish** must not appear on the slide as asterisks."""
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"(?<!\w)\*(.+?)\*(?!\w)", r"\1", text)
    return text.replace("**", "").replace("`", "")


def _prodoc():
    """Load prodoc.py (the WSQ house document helpers) by path."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("prodoc", PRODOC)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _toc_field(doc, entries):
    """A real Word TOC field whose CACHED RESULT is the actual table of contents.

    Word recomputes the field when the document opens. LibreOffice - which is what turns
    these into the PDFs learners are given - does not: it renders whatever result the field
    already carries. With prodoc's placeholder cached in there, every shipped PDF printed
    "Right-click and choose Update Field..." where its contents page should be.

    So we cache a computed result. A field may span paragraphs: begin/instrText/separate,
    then the entry paragraphs, then end. Word still replaces all of it on update, so the
    DOCX stays a live TOC while the PDF finally shows one.
    """
    from docx.shared import Pt, Inches
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    from docx.enum.text import WD_TAB_ALIGNMENT, WD_TAB_LEADER

    head = doc.add_paragraph()
    r = head.add_run("TABLE OF CONTENTS")
    r.bold = True
    r.font.size = Pt(12)

    def fld(p, kind_):
        e = OxmlElement("w:fldChar")
        e.set(qn("w:fldCharType"), kind_)
        run = p.add_run()
        run._r.append(e)

    p0 = doc.add_paragraph()
    fld(p0, "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = 'TOC \\o "1-3" \\h \\z \\u'
    p0.add_run()._r.append(instr)
    fld(p0, "separate")

    for level, text, page in entries:
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.left_indent = Inches(0.25 * (level - 1))
        pf.space_after = Pt(2)
        pf.tab_stops.add_tab_stop(Inches(6.3), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        run = p.add_run(f"{text}\t{page}")
        run.font.size = Pt(10 if level > 1 else 11)
        run.bold = level == 1

    pend = doc.add_paragraph()
    fld(pend, "end")


def write_docx(md: str, path: Path, kind: str = "Learner Guide", toc_entries=None) -> None:
    """Render a Markdown document as a WSQ house DOCX: cover page, Document Version
    Control Record, a real Word TOC field, Arial 11pt body and a Page X of Y footer."""
    try:
        from docx import Document
        from docx.shared import Inches, Pt
        from docx.enum.text import WD_BREAK
    except Exception as exc:  # pragma: no cover
        print(f"python-docx unavailable, skipped DOCX: {exc}")
        return

    pd = _prodoc()
    doc = Document()
    doc.styles["Normal"].font.name = "Arial"
    doc.styles["Normal"].font.size = Pt(11)
    pd.style_headings(doc)

    pd.add_cover_page(
        doc, kind, COURSE_TITLE, VERSION,
        org_logo=str(ORG_LOGO) if ORG_LOGO.exists() else None,
        course_logo=str(COURSE_LOGO) if COURSE_LOGO.exists() else None,
        course_code=COURSE_CODE,
    )
    # add_version_control already ends with a page break; a second one here left a blank
    # page sitting between the version record and the contents page.
    pd.add_version_control(doc, VERSION_ROWS)
    if toc_entries:
        _toc_field(doc, toc_entries)
        doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    else:
        pd.add_toc(doc)          # first pass: no page numbers yet; it breaks the page itself

    # The cover already carries the title block, so drop the markdown's own H1/meta.
    lines = md.splitlines()
    body = []
    seen_h1 = False
    for line in lines:
        if line.startswith("# ") and not seen_h1:
            seen_h1 = True
            continue
        if not body and (line.startswith("**Course code:**") or not line.strip()):
            continue
        body.append(line)

    in_table = False
    for line in body:
        img = IMG_RE.match(line)
        if img:
            src = (ROOT / img.group("src")).resolve()
            if src.exists():
                doc.add_picture(str(src), width=Inches(6.1))
                cap = doc.add_paragraph(img.group("alt"))
                cap.runs[0].italic = True
                cap.runs[0].font.size = Pt(9)
            continue

        if line.startswith("|"):
            # Markdown tables become real Word tables, not pipe soup.
            cells = [c.strip() for c in line.strip("|").split("|")]
            if set("".join(cells)) <= set("-: "):
                continue  # the |---|---| separator row
            if not in_table:
                tbl = doc.add_table(rows=0, cols=len(cells))
                tbl.style = "Light Grid Accent 1"
                in_table = True
            row = tbl.add_row().cells
            for i, c in enumerate(cells[: len(row)]):
                row[i].text = plain(c)
            continue
        in_table = False

        if line.startswith("#### "):
            doc.add_heading(plain(line[5:]), 3)
        elif line.startswith("### "):
            doc.add_heading(plain(line[4:]), 2)
        elif line.startswith("## "):
            doc.add_heading(plain(line[3:]), 1)
        elif line.startswith("- "):
            doc.add_paragraph(plain(line[2:]), style="List Bullet")
        elif line and line[0].isdigit() and ". " in line[:4]:
            # Word's "List Number" style shares ONE counter across the whole document, so
            # the steps ran on and on: Lab 1.2 opened at step 14, Lab 4.7 at 149. The
            # Markdown already numbers each lab from 1, so print ITS number as text and let
            # the two documents say the same thing.
            num, text = line.split(". ", 1)
            p = doc.add_paragraph(f"{num}. {plain(text)}")
            p.paragraph_format.left_indent = Inches(0.25)
        elif line.strip() == "":
            doc.add_paragraph("")
        else:
            doc.add_paragraph(plain(line))

    pd.add_page_numbers(doc, left_text=f"{COURSE_CODE} - {COURSE_TITLE}")
    pd.enable_update_fields(doc)
    doc.save(path)


SLIDE_MAP: dict[str, int] = {}   # lab_no -> the slide the lab starts on


def write_pptx(path: Path) -> dict[str, int]:
    from pptx import Presentation
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor

    BLUE = "1F6FEB"
    TEAL = "10B981"
    INK = "161B26"
    GREY = "5B6372"
    VIOLET = "7C3AED"
    PALE = "F5F8FC"
    LINE = "DCE5F0"
    AMBER = "F59E0B"
    RED = "E25555"
    WHITE = "FFFFFF"

    def rgb(value: str):
        return RGBColor.from_string(value)

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    def text_box(slide, text, x, y, w, h, size=18, color=INK, bold=False,
                 align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.TOP, margin=0.04):
        shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        shape.text_frame.clear()
        shape.text_frame.word_wrap = True
        shape.text_frame.margin_left = Inches(margin)
        shape.text_frame.margin_right = Inches(margin)
        shape.text_frame.margin_top = Inches(margin)
        shape.text_frame.margin_bottom = Inches(margin)
        shape.text_frame.vertical_anchor = valign
        p = shape.text_frame.paragraphs[0]
        p.text = str(text)
        p.alignment = align
        p.font.name = "Arial"
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.color.rgb = rgb(color)
        return shape

    def shape_box(slide, x, y, w, h, fill=PALE, radius=True, line=LINE, line_width=1):
        kind = MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE
        shape = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
        shape.fill.solid()
        shape.fill.fore_color.rgb = rgb(fill)
        shape.line.color.rgb = rgb(line)
        shape.line.width = Pt(line_width)
        return shape

    def circle(slide, label, x, y, d, fill=BLUE, color=WHITE, size=16):
        shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
        shape.fill.solid()
        shape.fill.fore_color.rgb = rgb(fill)
        shape.line.fill.background()
        text_box(slide, label, x, y, d, d, size, color, True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
        return shape

    def add_footer(slide, slide_no):
        shape_box(slide, 0.55, 7.03, 12.23, 0.015, LINE, False, LINE, 0)
        text_box(slide, "TGS-2024052081 - Automate Video and Voice AI Agents with n8n", 0.6, 7.09, 5.7, 0.22, 8, GREY)
        text_box(slide, "Copyright 2026 Tertiary Infotech Academy Pte Ltd", 4.65, 7.09, 4.1, 0.22, 8, GREY, False, PP_ALIGN.CENTER)
        text_box(slide, f"{slide_no:03d}", 12.15, 7.09, 0.55, 0.22, 8, GREY, True, PP_ALIGN.RIGHT)

    def base(title, kicker="COURSEWARE"):
        s = prs.slides.add_slide(blank)
        s.background.fill.solid()
        s.background.fill.fore_color.rgb = rgb(WHITE)
        # The kicker gets the full slide width. At 3.0" a long one ("LAB 6.2 - BUILD AN
        # INTERACTIVE AVATAR THAT RENDERS IN THE BROWSER") wrapped onto three lines and
        # printed straight through the title underneath it.
        text_box(s, kicker.upper(), 0.62, 0.33, 12.0, 0.28, 11, BLUE, True)
        text_box(s, title, 0.62, 0.68, 12.0, 0.62, 28, INK, True)
        return s

    def card(slide, x, y, w, h, label, body, accent=BLUE, badge=None):
        shape_box(slide, x, y, w, h, WHITE, True, LINE, 1)
        shape_box(slide, x, y, 0.08, h, accent, False, accent, 0)
        if badge:
            circle(slide, badge, x + 0.26, y + 0.24, 0.48, accent, WHITE, 12)
            tx = x + 0.88
            tw = w - 1.12
        else:
            tx = x + 0.3
            tw = w - 0.55
        compact = h < 1.3
        text_box(slide, label, tx, y + (0.15 if compact else 0.22), tw, 0.34, 16 if compact else 17, INK, True)
        body_x = tx if compact and badge else x + 0.3
        body_w = tw if compact and badge else w - 0.55
        text_box(slide, body, body_x, y + (0.55 if compact else 0.72), body_w,
                 h - (0.62 if compact else 0.9), 11 if compact else 14, GREY)

    def topic_slide(index, title, description):
        s = base(title, f"TOPIC {index:02d}")
        text_box(s, f"{index:02d}", 9.9, 0.95, 2.5, 1.65, 74, "E7EFFA", True, PP_ALIGN.RIGHT)
        shape_box(s, 0.65, 1.65, 7.75, 2.0, PALE, True, PALE, 0)
        text_box(s, description, 1.0, 2.03, 6.95, 1.2, 20, INK, False, PP_ALIGN.LEFT, MSO_ANCHOR.MIDDLE)
        # Seven steps have to fit LEFT of the LEARNING ARC card (which starts at x=9.15).
        # At the old 1.76" pitch, steps 6 and 7 - Guardrail and Document - ran underneath
        # it, so the loop this whole course is built on silently showed only five steps.
        labels = ["Define", "Build", "Observe", "Evaluate", "Improve", "Guardrail", "Document"]
        pitch = 1.17
        for i, label in enumerate(labels):
            x = 0.72 + i * pitch
            circle(s, str(i + 1), x, 4.38, 0.48, BLUE if i < 4 else TEAL, WHITE, 12)
            text_box(s, label, x - 0.31, 5.0, 1.10, 0.32, 11, INK, True, PP_ALIGN.CENTER)
            if i < len(labels) - 1:
                shape_box(s, x + 0.53, 4.59, pitch - 0.55, 0.045, LINE, False, LINE, 0)
        text_box(s, "Every lab produces visible evidence for trainer review.", 0.72, 5.72, 7.5, 0.5, 17, TEAL, True)
        shape_box(s, 9.15, 3.18, 3.1, 2.7, WHITE, True, LINE, 1)
        text_box(s, "LEARNING ARC", 9.5, 3.52, 2.4, 0.28, 11, VIOLET, True)
        text_box(s, "Concept", 9.5, 4.05, 2.3, 0.3, 18, INK, True)
        text_box(s, "Practice", 9.5, 4.52, 2.3, 0.3, 18, INK, True)
        text_box(s, "Evidence", 9.5, 4.99, 2.3, 0.3, 18, INK, True)
        text_box(s, "Reflection", 9.5, 5.46, 2.3, 0.3, 18, INK, True)

    def lab_target(lab):
        s = base(f"Lab {lab.lab_no}: {lab.title}", "BUILD TARGET")
        shape_box(s, 0.65, 1.55, 8.05, 3.55, PALE, True, PALE, 0)
        circle(s, lab.lab_no, 1.0, 1.92, 1.18, BLUE, WHITE, 21)
        text_box(s, "YOU WILL BUILD", 2.55, 1.88, 2.4, 0.3, 11, BLUE, True)
        # The box is middle-anchored, so text longer than it fits grows in BOTH directions
        # and prints over the two labels that bracket it. Size the type to the sentence:
        # roughly 30 characters fit on a 5.55" line at 24pt, and four lines fill the box.
        build_pt = 24 if len(lab.build) <= 95 else 20 if len(lab.build) <= 130 else 17
        text_box(s, lab.build, 2.55, 2.24, 5.55, 1.44, build_pt, INK, True, valign=MSO_ANCHOR.MIDDLE)
        text_box(s, "DELIVERABLE", 2.55, 3.8, 2.1, 0.28, 11, TEAL, True)
        text_box(s, lab.deliverable, 2.55, 4.18, 5.55, 0.62, 15, GREY)
        card(s, 9.08, 1.55, 3.6, 1.05, "TIMEBOX", f"{lab.minutes} minutes", AMBER, "T")
        card(s, 9.08, 2.85, 3.6, 1.05, "MODE", "Demo, guided build, independent test", VIOLET, "M")
        card(s, 9.08, 4.15, 3.6, 1.05, "EVIDENCE", "Execution trace plus learner artifact", TEAL, "E")
        text_box(s, "Success is demonstrated, not assumed.", 0.72, 5.72, 8.0, 0.5, 20, VIOLET, True)

    def concept_slide(lab):
        s = base(f"Lab {lab.lab_no}: Four Ideas That Make It Work", "CONCEPT MAP")
        colors = [BLUE, TEAL, VIOLET, AMBER]
        positions = [(0.68, 1.52), (6.78, 1.52), (0.68, 4.02), (6.78, 4.02)]
        for i, ((name, desc), (x, y)) in enumerate(zip(lab.concepts, positions)):
            card(s, x, y, 5.85, 2.08, plain(name), plain(desc), colors[i], str(i + 1))
        text_box(s, "Connect the four ideas before touching the workflow canvas.", 0.75, 6.35, 8.8, 0.38, 16, GREY)

    def step_slide(lab):
        """Build-sequence slides. Steps are PAGINATED (six per slide) so a long lab
        never silently loses steps, and the font shrinks to fit the longest step."""
        per_slide = 6
        pages = [lab.steps[i:i + per_slide] for i in range(0, len(lab.steps), per_slide)] or [[]]

        for page_no, page in enumerate(pages, 1):
            suffix = "" if len(pages) == 1 else f" ({page_no}/{len(pages)})"
            s = base(f"Lab {lab.lab_no}: Build Sequence{suffix}", "WORKFLOW PLAN")

            # One font size for the whole page, driven by its longest step, so the
            # boxes stay a uniform grid instead of each one sizing itself.
            longest = max((len(plain(step)) for step in page), default=0)
            if longest <= 105:
                size = 14
            elif longest <= 150:
                size = 12
            elif longest <= 210:
                size = 11
            elif longest <= 280:
                size = 10
            else:
                size = 9

            for i, step in enumerate(page):
                col = i % 2
                row = i // 2
                x = 0.72 + col * 6.25
                y = 1.45 + row * 1.78
                n = (page_no - 1) * per_slide + i + 1
                circle(s, str(n), x, y + 0.15, 0.58, BLUE if col == 0 else TEAL, WHITE, 14)
                shape_box(s, x + 0.82, y, 5.13, 1.5, WHITE, True, LINE, 1)
                text_box(s, plain(step), x + 1.05, y + 0.1, 4.68, 1.3, size, INK, False,
                         valign=MSO_ANCHOR.MIDDLE)

            text_box(s, "Build one observable behavior at a time.", 0.75, 6.62, 6.5, 0.3, 15, VIOLET, True)

    def verify_slide(lab):
        s = base(f"Lab {lab.lab_no}: Prove, Evaluate, Improve", "QUALITY GATE")
        shape_box(s, 0.68, 1.48, 7.65, 4.92, PALE, True, PALE, 0)
        checks = lab.verify + ["Run one edge case and record the change made after evaluation."]
        checks = checks[:6]
        # Spacing and font follow the row count so a 6-check lab still fits the panel.
        gap = 0.91 if len(checks) <= 5 else 0.78
        size = 15 if max((len(plain(c)) for c in checks), default=0) <= 95 else 13
        for i, item in enumerate(checks):
            y = 1.82 + i * gap
            circle(s, "OK", 1.02, y, 0.5, TEAL, WHITE, 10)
            text_box(s, plain(item), 1.78, y - 0.02, 5.95, gap - 0.06, size, INK, valign=MSO_ANCHOR.MIDDLE)
        shape_box(s, 8.72, 1.48, 3.95, 4.92, WHITE, True, LINE, 1)
        text_box(s, "EVIDENCE STACK", 9.08, 1.84, 3.2, 0.3, 11, BLUE, True)
        evidence = [("01", "Input", "Exact test payload"), ("02", "Trace", "Node execution path"), ("03", "Output", "Generated result"), ("04", "Decision", "Rubric and revision")]
        for i, (num, label, note) in enumerate(evidence):
            y = 2.38 + i * 0.87
            circle(s, num, 9.08, y, 0.45, VIOLET, WHITE, 10)
            text_box(s, label, 9.72, y - 0.02, 1.0, 0.25, 14, INK, True)
            text_box(s, note, 10.72, y - 0.02, 1.48, 0.45, 12, GREY)
        text_box(s, "PASS", 9.08, 5.92, 1.0, 0.28, 12, TEAL, True)
        shape_box(s, 10.12, 5.97, 2.12, 0.12, TEAL, False, TEAL, 0)

    def fixes_slide(lab):
        """Troubleshooting table, PAGINATED three rows per slide so a lab with five
        known failure modes does not quietly show only the first three."""
        rows = lab.troubleshooting
        pages = [rows[i:i + 3] for i in range(0, len(rows), 3)] or [[]]
        headers = [("SYMPTOM", RED), ("LIKELY CAUSE", AMBER), ("TARGETED FIX", TEAL)]
        xs = [0.68, 4.72, 8.76]

        for page_no, page in enumerate(pages, 1):
            suffix = "" if len(pages) == 1 else f" ({page_no}/{len(pages)})"
            s = base(f"Lab {lab.lab_no}: Diagnose Before Rebuilding{suffix}", "TROUBLESHOOTING")
            for (label, color), x in zip(headers, xs):
                shape_box(s, x, 1.47, 3.78, 0.48, color, True, color, 0)
                text_box(s, label, x, 1.54, 3.78, 0.25, 11, WHITE, True, PP_ALIGN.CENTER)

            longest = max((len(plain(v)) for row in page for v in row), default=0)
            size = 14 if longest <= 60 else (12 if longest <= 95 else 11)

            for row_i, (err, cause, fix) in enumerate(page):
                y = 2.18 + row_i * 1.43
                colors = ["FFF4F4", "FFF8E8", "ECFDF5"]
                for col, value in enumerate([err, cause, fix]):
                    shape_box(s, xs[col], y, 3.78, 1.12, colors[col], True, colors[col], 0)
                    text_box(s, plain(value), xs[col] + 0.18, y + 0.1, 3.42, 0.92, size, INK,
                             col == 0, valign=MSO_ANCHOR.MIDDLE)
            text_box(s, "Change one variable, rerun the same test, compare the trace.", 0.75, 6.55, 9.5, 0.3, 16, VIOLET, True)

    s = prs.slides.add_slide(blank)
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = rgb(WHITE)
    # The cover carries the house identity as LOGOS, the way the LP and LG covers do -
    # a text-only cover is not the WSQ cover page.
    if ORG_LOGO.exists():
        s.shapes.add_picture(str(ORG_LOGO), Inches(0.72), Inches(0.42), height=Inches(0.52))
    if COURSE_LOGO.exists():
        # Beside the org logo, NOT top-right: the accent panel is added after this and
        # would paint straight over it (in pptx, later shapes win).
        s.shapes.add_picture(str(COURSE_LOGO), Inches(1.62), Inches(0.44), height=Inches(0.48))
    text_box(s, "TERTIARY INFOTECH ACADEMY", 0.72, 1.02, 4.5, 0.32, 12, BLUE, True)
    text_box(s, "Automate Video and Voice\nAI Agents with n8n", 0.72, 1.62, 7.35, 1.9, 38, INK, True, valign=MSO_ANCHOR.MIDDLE)
    text_box(s, "Agentic AI loop engineering for adult workplace training", 0.78, 3.72, 6.75, 0.72, 20, GREY)
    text_box(s, f"{COURSE_CODE}  |  {VERSION}  ·  {VERSION_DATE}  |  {UEN}",
             0.78, 5.55, 7.4, 0.38, 12, GREY, True)
    shape_box(s, 8.33, 0.62, 4.32, 5.95, PALE, True, PALE, 0)
    nodes = [(9.0, 1.2, "VOICE", BLUE), (10.7, 2.12, "n8n", VIOLET), (8.88, 3.25, "AI", TEAL), (10.78, 4.3, "VIDEO", AMBER), (9.02, 5.36, "REVIEW", RED)]
    for i, (x, y, label, color) in enumerate(nodes):
        if i < len(nodes) - 1:
            nx, ny, _, _ = nodes[i + 1]
            line = s.shapes.add_connector(1, Inches(x + 0.62), Inches(y + 0.62), Inches(nx + 0.62), Inches(ny + 0.62))
            line.line.color.rgb = rgb(LINE)
            line.line.width = Pt(3)
        circle(s, label, x, y, 1.22, color, WHITE, 13)


    # ── WSQ admin block ──────────────────────────────────────────────────────
    def traqom_slide(where: str) -> None:
        s = base("Digital Attendance - TRAQOM", "ADMIN")
        text_box(s, f"Please take attendance {where} of the session.", 0.75, 1.45, 11.9, 0.4, 19, GREY)
        for i, (n, label, note, color) in enumerate([
            ("1", "Open TRAQOM", "Scan the QR code shown by the trainer", BLUE),
            ("2", "Verify identity", "SingPass / NRIC as prompted", TEAL),
            ("3", "Confirm", "Attendance is recorded against TGS-2024052081", VIOLET),
        ]):
            y = 2.3 + i * 1.25
            circle(s, n, 1.0, y, 0.62, color, WHITE, 15)
            text_box(s, label, 1.95, y + 0.02, 3.2, 0.35, 18, INK, True)
            text_box(s, note, 5.3, y + 0.02, 7.0, 0.5, 15, GREY)
        shape_box(s, 0.72, 6.15, 11.9, 0.85, PALE, True, PALE, 0)
        text_box(s, "Attendance is a funding requirement. No attendance record, no course fee funding.",
                 1.05, 6.3, 11.3, 0.55, 15, RED, True, valign=MSO_ANCHOR.MIDDLE)

    traqom_slide("at the START")

    # Two trainer profiles, on two SEPARATE pages — the house checklist asks for a general
    # trainer template card AND the named trainer, each as its own visual profile page.
    def trainer_slide(kicker, title, badge, badge_color, name, creds, lines, footer, footer_color):
        s = base(title, kicker)
        shape_box(s, 3.55, 1.5, 6.3, 5.05, PALE if badge == "T" else WHITE, True, LINE, 1)
        circle(s, badge, 6.05, 1.95, 1.7, badge_color, WHITE, 40 if len(badge) == 1 else 30)
        text_box(s, name, 3.75, 3.9, 5.9, 0.45, 24, INK, True, PP_ALIGN.CENTER)
        text_box(s, creds, 3.75, 4.42, 5.9, 0.35, 15, GREY, False, PP_ALIGN.CENTER)
        text_box(s, lines, 3.95, 4.95, 5.5, 1.45, 15, GREY, False, PP_ALIGN.CENTER)
        text_box(s, footer, 3.75, 6.15, 5.9, 0.3, 12, footer_color, True, PP_ALIGN.CENTER)

    trainer_slide(
        "YOUR TRAINER", "About the Trainer", "?", BLUE,
        "<< Trainer Name >>", "<< Qualification >>  ·  << Years of experience >>",
        "<< Industry practice >>\n<< Teaching experience >>\n<< Specialisation >>",
        "General trainer template", BLUE,
    )
    trainer_slide(
        "YOUR TRAINER", "About the Trainer", "AA", VIOLET,
        "Dr Alfred Ang", "PhD  ·  ACTA / ACLP certified adult educator",
        "Founder, Tertiary Infotech Academy\nAI automation, voice and video agents\n"
        "n8n, RAG, LLM systems in production",
        "Your trainer today", VIOLET,
    )

    # Ground rules
    s = base("Ground Rules", "HOUSEKEEPING")
    rules = [
        ("Be on time", "Sessions start at 9:30am sharp", BLUE),
        ("Phones on silent", "Take calls outside the room", TEAL),
        ("Ask as you go", "A question now saves an hour later", VIOLET),
        ("Work the labs", "70% of this course is hands-on", AMBER),
        ("Respect the room", "One conversation at a time", RED),
    ]
    for i, (label, note, color) in enumerate(rules):
        y = 1.6 + i * 1.05
        circle(s, str(i + 1), 0.85, y, 0.58, color, WHITE, 14)
        text_box(s, label, 1.75, y - 0.02, 3.2, 0.35, 18, INK, True)
        text_box(s, note, 5.1, y - 0.02, 7.4, 0.45, 15, GREY)

    # Learning outcomes
    s = base("Learning Outcomes", "WHAT YOU WILL BE ABLE TO DO")
    los = [
        "Set up a local AI automation workstation (Docker, n8n, Ollama).",
        "Build local AI agents and document-grounded RAG with evaluation.",
        "Build customer-facing agents that collect data and call tools safely.",
        "Build voice AI agents with Retell and Vapi, grounded and QA-scored.",
        "Build AI video: lip-sync engines, avatar news video, Veo 3 generation.",
        "Publish, monitor and operate AI outputs with human review gates.",
    ]
    for i, lo in enumerate(los):
        y = 1.55 + i * 0.88
        circle(s, f"LO{i + 1}", 0.85, y, 0.62, [BLUE, TEAL, VIOLET, AMBER, RED, BLUE][i], WHITE, 12)
        text_box(s, lo, 1.85, y - 0.02, 10.6, 0.6, 16, INK, False, valign=MSO_ANCHOR.MIDDLE)

    # Lesson plan slide
    s = base("Lesson Plan", "HOW THE DAYS RUN")
    text_box(s, "9:30am - 6:30pm  ·  1-hour lunch  ·  tea breaks inside the sessions  ·  8 instructional hours a day",
             0.75, 1.42, 11.9, 0.35, 16, GREY)
    for i, (topic, desc) in enumerate(TOPICS):
        y = 1.95 + i * 0.82
        labs = ", ".join(f"Lab {l.lab_no}" for l in LABS if l.topic == i + 1)
        color = [BLUE, TEAL, VIOLET, AMBER, RED, BLUE][i % 6]
        circle(s, str(i + 1), 0.85, y, 0.55, color, WHITE, 13)
        text_box(s, topic.split(" - ", 1)[-1], 1.75, y - 0.02, 6.6, 0.45, 15, INK, True, valign=MSO_ANCHOR.MIDDLE)
        text_box(s, labs, 8.5, y - 0.02, 4.1, 0.45, 13, GREY, False, valign=MSO_ANCHOR.MIDDLE)

    # Download course material — a visual, not a bare link
    s = base("Download Your Course Material", "BEFORE WE START")
    text_box(s, "Everything - slides, Learner Guide, lab files - is on the LMS.", 0.75, 1.42, 11.9, 0.35, 17, GREY)
    steps = [
        ("1", "Go to", "lms-tms.tertiaryinfotech.com", BLUE),
        ("2", "Sign in", "Use the email you registered with", TEAL),
        ("3", "Open the course", "Automate Video and Voice AI Agents with n8n", VIOLET),
        ("4", "Download", "Learner Slides (PDF), Learner Guide (PDF), lab files", AMBER),
    ]
    for i, (n, label, note, color) in enumerate(steps):
        y = 2.0 + i * 1.15
        circle(s, n, 0.9, y, 0.6, color, WHITE, 15)
        text_box(s, label, 1.8, y, 2.6, 0.35, 17, INK, True)
        text_box(s, note, 4.5, y, 8.0, 0.5, 15, GREY)
    shape_box(s, 0.72, 6.3, 11.9, 0.72, PALE, True, PALE, 0)
    text_box(s, "lms-tms.tertiaryinfotech.com", 1.05, 6.4, 11.3, 0.5, 18, BLUE, True, valign=MSO_ANCHOR.MIDDLE)

    s = base("What You Will Be Able to Build", "COURSE OUTCOMES")
    outcomes = [
        ("LOCAL AI", "n8n agents powered by Ollama", BLUE),
        ("RAG", "Evidence-grounded workplace answers", TEAL),
        ("VOICE", "Secure browser-to-agent handoffs", VIOLET),
        ("VIDEO", "Avatar and cinematic automation", AMBER),
        ("OPERATIONS", "Tests, guardrails, review and recovery", RED),
    ]
    for i, (label, body, color) in enumerate(outcomes):
        x = 0.7 + (i % 3) * 4.15
        y = 1.55 + (i // 3) * 2.32
        w = 3.86 if i < 3 else 5.95
        if i >= 3:
            x = 0.7 + (i - 3) * 6.18
        card(s, x, y, w, 1.82, label, body, color, str(i + 1))
    text_box(s, "The course ends with an integrated, reviewable AI workforce capstone.", 0.75, 6.35, 10.8, 0.35, 16, GREY)

    # ---- Setup: the same stack on both operating systems ----
    s = base("Set Up Your Machine - macOS or Windows", "ENVIRONMENT")
    text_box(s, "Every lab runs on both. The tools are identical; only the install command and a little typing differ.", 0.75, 1.4, 11.9, 0.35, 17, GREY)

    shape_box(s, 0.72, 1.95, 5.9, 0.55, INK, True, INK, 0)
    text_box(s, "macOS  -  Terminal  +  Homebrew (brew.sh)", 0.72, 2.07, 5.9, 0.32, 14, WHITE, True, PP_ALIGN.CENTER)
    shape_box(s, 6.95, 1.95, 5.68, 0.55, BLUE, True, BLUE, 0)
    text_box(s, "Windows  -  PowerShell  +  winget (built in)", 6.95, 2.07, 5.68, 0.32, 14, WHITE, True, PP_ALIGN.CENTER)

    tools = [
        ("Docker Desktop", "brew install --cask docker", "winget install Docker.DockerDesktop"),
        ("Ollama", "brew install ollama", "winget install Ollama.Ollama"),
        ("Python 3", "already installed (python3)", "winget install Python.Python.3.12"),
        ("ffmpeg", "brew install ffmpeg", "winget install Gyan.FFmpeg"),
        ("ngrok  (from Lab 4.7)", "brew install ngrok", "winget install ngrok.ngrok"),
    ]
    for i, (tool, mac, win) in enumerate(tools):
        y = 2.68 + i * 0.62
        fill = PALE if i % 2 == 0 else WHITE
        shape_box(s, 0.72, y, 11.9, 0.55, fill, False, LINE, 1)
        text_box(s, tool, 0.92, y + 0.05, 2.6, 0.45, 13, INK, True, valign=MSO_ANCHOR.MIDDLE)
        text_box(s, mac, 3.6, y + 0.05, 4.3, 0.45, 12, GREY, False, valign=MSO_ANCHOR.MIDDLE)
        text_box(s, win, 8.0, y + 0.05, 4.5, 0.45, 12, BLUE, False, valign=MSO_ANCHOR.MIDDLE)

    shape_box(s, 0.72, 5.9, 11.9, 1.0, PALE, True, PALE, 0)
    text_box(s, "WINDOWS GOTCHAS", 1.0, 6.0, 3.0, 0.28, 12, RED, True)
    text_box(s, "Reopen PowerShell after installing, or the command is 'not recognized'  ·  Docker needs WSL 2 (wsl --install)  ·  The command is python, NOT python3", 1.0, 6.3, 11.4, 0.5, 14, INK, True)

    s = base("The Agentic AI Loop", "ENGINEERING METHOD")
    loop = [
        ("1", "DEFINE", "Outcome + risk"), ("2", "BUILD", "Smallest proof"),
        ("3", "OBSERVE", "Trace behavior"), ("4", "EVALUATE", "Test rubric"),
        ("5", "IMPROVE", "One variable"), ("6", "GUARDRAIL", "Control action"),
        ("7", "DOCUMENT", "Make repeatable"),
    ]
    for i, (num, label, note) in enumerate(loop):
        x = 0.58 + i * 1.8
        color = BLUE if i < 3 else (VIOLET if i < 5 else TEAL)
        circle(s, num, x + 0.38, 2.02, 0.85, color, WHITE, 18)
        text_box(s, label, x, 3.13, 1.62, 0.3, 13, INK, True, PP_ALIGN.CENTER)
        text_box(s, note, x, 3.55, 1.62, 0.62, 12, GREY, False, PP_ALIGN.CENTER)
        if i < 6:
            shape_box(s, x + 1.32, 2.41, 0.5, 0.07, LINE, False, LINE, 0)
    shape_box(s, 1.02, 4.75, 11.28, 1.13, PALE, True, PALE, 0)
    text_box(s, "Learner habit", 1.35, 5.08, 1.55, 0.3, 13, VIOLET, True)
    text_box(s, "Show the input, trace, output, evaluation decision, and the next revision.", 3.05, 4.98, 8.75, 0.48, 20, INK, True, valign=MSO_ANCHOR.MIDDLE)

    def screenshot_slide(key: str, kicker: str) -> None:
        """One full-bleed screenshot slide, shown INSIDE the lab it belongs to."""
        if key not in SCREENSHOTS:
            return
        fname, caption = SCREENSHOTS[key]
        img = SHOTS_DIR / fname
        if not img.exists():
            print(f"  (skipped slide, screenshot not captured: {fname})")
            return

        # The title is the caption's opening clause. Split on ": " and NOT on a bare colon -
        # "http://localhost:8137" chopped one title to "Lab 5.1 - Digital Human Studio (http".
        # And a caption with no colon at all became a whole sentence, which wrapped down into
        # the screenshot below it. The image is pinned, so the title must stay one line.
        title = caption.split(": ", 1)[0].strip()
        if len(title) > 62:
            title = title.split(". ", 1)[0].strip().rstrip(".")
        if len(title) > 62:
            # Cut at a WORD boundary. A blind character slice left slide 98 reading
            # "...the Book by Voice call to acti".
            title = title[:62].rsplit(" ", 1)[0].rstrip(" ,-")
        s = base(title, kicker)

        # Fit the image inside the content area without distorting it.
        max_w, max_h = 11.6, 4.55
        try:
            from PIL import Image  # type: ignore

            with Image.open(img) as im:
                iw, ih = im.size
            ratio = min(max_w / iw, max_h / ih) if iw and ih else 0
            w, h = (iw * ratio, ih * ratio) if ratio else (max_w, max_h)
        except Exception:
            w, h = max_w, max_h * 0.9

        left = (13.333 - w) / 2
        top = 1.45 + (max_h - h) / 2
        shape_box(s, left - 0.06, top - 0.06, w + 0.12, h + 0.12, PALE, True, LINE, 1)
        s.shapes.add_picture(str(img), Inches(left), Inches(top), Inches(w), Inches(h))
        text_box(s, caption, 0.78, 6.35, 11.8, 0.5, 15, GREY, False, PP_ALIGN.CENTER)

    def arrow(slide, x, y, color=LINE):
        """Small horizontal connector between pipeline boxes."""
        shape_box(slide, x, y, 0.42, 0.06, color, False, color, 0)
        text_box(slide, ">", x + 0.1, y - 0.19, 0.3, 0.3, 15, color, True, PP_ALIGN.CENTER)

    def rag_concept_slides() -> None:
        # ---- 1. Why RAG: the hallucination problem, as a before/after ----
        s = base("Why RAG? The Model Has Never Seen Your Documents", "RAG - THE PROBLEM")
        shape_box(s, 0.7, 1.5, 5.85, 4.05, PALE, True, LINE, 1)
        shape_box(s, 0.7, 1.5, 5.85, 0.52, RED, True, RED, 0)
        text_box(s, "WITHOUT RAG", 0.7, 1.62, 5.85, 0.3, 13, WHITE, True, PP_ALIGN.CENTER)
        text_box(s, "“What is the refund policy?”", 1.05, 2.25, 5.15, 0.4, 17, INK, True)
        text_box(s, "The model was never trained on your handbook.\nIt does not say “I don't know”.", 1.05, 2.8, 5.15, 0.8, 15, GREY)
        shape_box(s, 1.05, 3.75, 5.15, 1.45, WHITE, True, RED, 1)
        text_box(s, "“Refunds are accepted within 30 days…”", 1.25, 3.95, 4.75, 0.5, 15, INK, True)
        text_box(s, "Fluent. Confident. Invented.\nThis failure is called HALLUCINATION.", 1.25, 4.48, 4.75, 0.6, 14, RED, True)

        shape_box(s, 6.85, 1.5, 5.78, 4.05, PALE, True, LINE, 1)
        shape_box(s, 6.85, 1.5, 5.78, 0.52, TEAL, True, TEAL, 0)
        text_box(s, "WITH RAG", 6.85, 1.62, 5.78, 0.3, 13, WHITE, True, PP_ALIGN.CENTER)
        text_box(s, "The workflow silently rewrites the question:", 7.2, 2.25, 5.1, 0.35, 15, GREY)
        shape_box(s, 7.2, 2.68, 5.08, 1.72, WHITE, True, TEAL, 1)
        text_box(s, "“Using ONLY these passages from the handbook:\n\n  <retrieved chunk 1>\n  <retrieved chunk 2>\n\nanswer: what is the refund policy?\nIf they do not contain the answer, say you do not know.”", 7.4, 2.78, 4.7, 1.55, 12, INK)
        text_box(s, "The model stops being a SOURCE of facts\nand becomes a READER of facts you supply.", 7.2, 4.55, 5.08, 0.7, 15, TEAL, True)

        # ---- 2. The two phases, as a pipeline diagram ----
        s = base("RAG Has Two Phases", "RAG - ARCHITECTURE")
        text_box(s, "Everything below exists to answer ONE question: which passages do we paste in front of the user's question?", 0.75, 1.42, 11.9, 0.4, 16, VIOLET, True)

        shape_box(s, 0.75, 2.05, 11.85, 1.85, PALE, True, LINE, 1)
        circle(s, "1", 1.1, 2.25, 0.5, BLUE, WHITE, 13)
        text_box(s, "INDEXING", 1.75, 2.28, 1.7, 0.3, 14, BLUE, True)
        text_box(s, "runs ONCE, when a document is uploaded", 3.3, 2.31, 4.2, 0.28, 12, GREY)
        idx_steps = [("PDF", 1.15), ("Split into\nchunks", 3.15), ("Embed each\nchunk", 5.6), ("768-dim\nvectors", 8.05), ("Vector\nstore", 10.5)]
        for i, (label, x) in enumerate(idx_steps):
            shape_box(s, x, 2.95, 1.75, 0.72, WHITE, True, BLUE, 1)
            text_box(s, label, x, 3.02, 1.75, 0.6, 12, INK, True, PP_ALIGN.CENTER)
            if i < len(idx_steps) - 1:
                arrow(s, x + 1.87, 3.31, BLUE)

        shape_box(s, 0.75, 4.15, 11.85, 2.15, PALE, True, LINE, 1)
        circle(s, "2", 1.1, 4.35, 0.5, TEAL, WHITE, 13)
        text_box(s, "RETRIEVAL", 1.75, 4.38, 1.9, 0.3, 14, TEAL, True)
        text_box(s, "runs on EVERY question", 3.5, 4.41, 3.6, 0.28, 12, GREY)
        ret_steps = [("Question", 1.15), ("Embed the\nquestion", 3.15), ("Cosine\nsimilarity", 5.6), ("Top-k\nchunks", 8.05), ("Grounded\nanswer", 10.5)]
        for i, (label, x) in enumerate(ret_steps):
            shape_box(s, x, 5.05, 1.75, 0.72, WHITE, True, TEAL, 1)
            text_box(s, label, x, 5.12, 1.75, 0.6, 12, INK, True, PP_ALIGN.CENTER)
            if i < len(ret_steps) - 1:
                arrow(s, x + 1.87, 5.41, TEAL)
        text_box(s, "On the n8n canvas these are the two visible paths: the upload path ending at the vector store, and the chat path reading from it.", 1.15, 5.9, 11.1, 0.3, 13, GREY)

        # ---- 3. Tokenization ----
        s = base("Tokenization: How Text Becomes Numbers", "RAG - TOKENS")
        text_box(s, "Models do not read words. They read TOKENS - the sub-word units in the model's vocabulary.", 0.75, 1.42, 11.9, 0.35, 16, GREY)
        text_box(s, "“The salon is closed on Sundays.”", 0.78, 1.95, 6.0, 0.42, 19, INK, True)
        tokens = ["The", " salon", " is", " closed", " on", " Sund", "ays", "."]
        x = 0.78
        for i, tok in enumerate(tokens):
            w = max(0.72, 0.30 + 0.145 * len(tok))
            color = AMBER if tok in (" Sund", "ays") else BLUE
            shape_box(s, x, 2.55, w, 0.62, WHITE, True, color, 1)
            text_box(s, tok.strip(), x, 2.64, w, 0.4, 14, color, True, PP_ALIGN.CENTER)
            x += w + 0.14
        text_box(s, "8 tokens  ·  note that “Sundays” split into TWO", 0.78, 3.3, 7.5, 0.3, 13, AMBER, True)

        shape_box(s, 0.75, 3.9, 11.85, 0.75, PALE, True, PALE, 0)
        text_box(s, "RULE OF THUMB (English):   1 token ≈ 4 characters ≈ 0.75 of a word   →   1,000 tokens ≈ 750 words ≈ 1.5 pages", 1.1, 3.95, 11.2, 0.65, 15, VIOLET, True, PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

        why = [
            ("CONTEXT WINDOW", "System prompt, retrieved chunks, memory and the question all compete for the SAME token budget.", BLUE),
            ("COST + LATENCY", "Double the retrieved text and you roughly double the prompt cost of every call.", AMBER),
            ("CHUNK SIZE", "Chunks are measured in tokens. This is the number you tune in Lab 2.4.", TEAL),
        ]
        for i, (label, note, color) in enumerate(why):
            x = 0.75 + i * 4.05
            shape_box(s, x, 4.95, 3.75, 1.5, WHITE, True, color, 1)
            shape_box(s, x, 4.95, 3.75, 0.42, color, True, color, 0)
            text_box(s, label, x, 5.03, 3.75, 0.28, 12, WHITE, True, PP_ALIGN.CENTER)
            text_box(s, note, x + 0.18, 5.5, 3.4, 0.85, 13, GREY)

        # ---- 4. Embeddings ----
        s = base("Embeddings: Meaning as Coordinates", "RAG - EMBEDDINGS")
        text_box(s, "An embedding turns ANY text into a fixed-length vector. Here: nomic-embed-text (Ollama) → 768 numbers.", 0.75, 1.4, 11.9, 0.32, 15, GREY)
        shape_box(s, 0.75, 1.95, 5.4, 0.72, WHITE, True, BLUE, 1)
        text_box(s, "“How do I reset my password?”", 0.95, 2.06, 5.0, 0.45, 15, INK, True, valign=MSO_ANCHOR.MIDDLE)
        arrow(s, 6.3, 2.28, BLUE)
        shape_box(s, 7.0, 1.95, 5.6, 0.72, PALE, True, BLUE, 1)
        text_box(s, "[ 0.021, -0.118, 0.334, … ]   768 numbers", 7.2, 2.06, 5.2, 0.45, 14, BLUE, True, valign=MSO_ANCHOR.MIDDLE)

        text_box(s, "Texts with similar MEANING land close together - even with zero words in common.", 0.75, 2.85, 11.9, 0.32, 16, VIOLET, True)
        pairs = [
            ("“reset my password”  vs  “I forgot my login credentials”", "0.89", "NEAR - no shared words, same meaning", TEAL),
            ("“reset my password”  vs  “what are your opening hours?”", "0.11", "FAR - unrelated", RED),
        ]
        for i, (pair, score, note, color) in enumerate(pairs):
            y = 3.35 + i * 0.92
            shape_box(s, 0.75, y, 8.3, 0.72, WHITE, True, LINE, 1)
            text_box(s, pair, 0.95, y + 0.1, 8.0, 0.5, 14, INK, False, valign=MSO_ANCHOR.MIDDLE)
            shape_box(s, 9.25, y, 1.3, 0.72, color, True, color, 0)
            text_box(s, score, 9.25, y + 0.16, 1.3, 0.4, 17, WHITE, True, PP_ALIGN.CENTER)
            text_box(s, note, 10.75, y + 0.1, 2.0, 0.55, 11, color, True, valign=MSO_ANCHOR.MIDDLE)
        text_box(s, "Cosine similarity:  1.0 = same direction/meaning   ·   0.0 = unrelated   ·   -1.0 = opposite. Retrieval returns the top-k nearest chunks (k is usually 3-5).", 0.75, 5.2, 11.9, 0.32, 13, GREY)

        shape_box(s, 0.75, 5.68, 11.85, 0.8, PALE, True, PALE, 0)
        text_box(s, "TWO RULES THAT CAUSE REAL BUGS:   Questions and documents MUST use the same embedding model · A vector store answers only “what is near this vector?” - not SQL", 1.05, 5.8, 11.3, 0.6, 14, RED, True, valign=MSO_ANCHOR.MIDDLE)

        # ---- 5. Chunking trade-off ----
        s = base("Chunking: The Trade-off You Must Measure", "RAG - CHUNKING")
        text_box(s, "You cannot embed a 40-page PDF as one vector - the detail would be averaged away. So documents are split into chunks (e.g. 800 characters) with an overlap (e.g. 100) so a sentence cut in half still appears whole somewhere.", 0.75, 1.42, 11.9, 0.6, 15, GREY)

        cols = [
            ("CHUNKS TOO SMALL", RED, [
                "Retrieved passage lacks context",
                "The model sees half an answer",
                "High precision, low recall",
                "“The document does not say” - when it does",
            ]),
            ("CHUNKS TOO LARGE", AMBER, [
                "Answer arrives with 3 irrelevant sections",
                "The model gets distracted, cites the wrong part",
                "High recall, low precision",
                "Tokens - and money - are wasted",
            ]),
        ]
        for i, (label, color, items) in enumerate(cols):
            x = 0.75 + i * 6.1
            shape_box(s, x, 2.2, 5.75, 2.9, PALE, True, LINE, 1)
            shape_box(s, x, 2.2, 5.75, 0.5, color, True, color, 0)
            text_box(s, label, x, 2.31, 5.75, 0.3, 13, WHITE, True, PP_ALIGN.CENTER)
            for j, item in enumerate(items):
                circle(s, "•", x + 0.35, 2.92 + j * 0.52, 0.26, color, WHITE, 10)
                text_box(s, item, x + 0.78, 2.9 + j * 0.52, 4.8, 0.42, 13, INK, False, valign=MSO_ANCHOR.MIDDLE)

        shape_box(s, 0.75, 5.3, 11.85, 1.15, PALE, True, PALE, 0)
        text_box(s, "There is no universally correct value.", 1.1, 5.45, 4.2, 0.3, 15, VIOLET, True)
        text_box(s, "That is why Lab 2.4 MEASURES it with golden questions instead of guessing. And when an answer is wrong: read the RETRIEVED CHUNKS first - if the right chunk never came back, no prompt rewrite will save it.", 1.1, 5.75, 11.2, 0.6, 14, INK, True)

    def ngrok_slides() -> None:
        # ---- Why a tunnel is needed at all ----
        s = base("Why localhost Stops Working", "TUNNEL - THE PROBLEM")
        text_box(s, "In Labs 4.7 and 4.8 something OUTSIDE your machine calls INTO n8n for the first time.", 0.75, 1.42, 11.9, 0.35, 17, GREY)

        shape_box(s, 0.72, 2.0, 5.9, 2.5, PALE, True, LINE, 1)
        shape_box(s, 0.72, 2.0, 5.9, 0.5, TEAL, True, TEAL, 0)
        text_box(s, "WORKS - your own browser", 0.72, 2.11, 5.9, 0.3, 13, WHITE, True, PP_ALIGN.CENTER)
        text_box(s, "Labs 1-3  ·  Book by Voice  ·  curl", 1.05, 2.72, 5.3, 0.35, 15, INK, True)
        text_box(s, "Your browser and n8n are on the SAME machine,\nso http://localhost:5678 resolves correctly.", 1.05, 3.15, 5.3, 0.9, 14, GREY)
        text_box(s, "No tunnel needed. Do not change this.", 1.05, 4.02, 5.3, 0.3, 14, TEAL, True)

        shape_box(s, 6.95, 2.0, 5.68, 2.5, PALE, True, LINE, 1)
        shape_box(s, 6.95, 2.0, 5.68, 0.5, RED, True, RED, 0)
        text_box(s, "FAILS - Retell / Vapi servers", 6.95, 2.11, 5.68, 0.3, 13, WHITE, True, PP_ALIGN.CENTER)
        text_box(s, "check_availability · book_appointment · Custom LLM", 7.28, 2.7, 5.1, 0.32, 12, INK, True)
        text_box(s, "To a datacenter in another country, “localhost”\nmeans ITS OWN machine. The request never\nleaves their building.", 7.28, 3.1, 5.1, 0.95, 14, GREY)
        text_box(s, "Tunnel required.", 7.28, 4.05, 5.1, 0.3, 14, RED, True)

        shape_box(s, 0.72, 4.8, 11.9, 1.5, PALE, True, PALE, 0)
        text_box(s, "THE SYMPTOM YOU WILL ACTUALLY SEE", 1.05, 4.95, 6.0, 0.3, 12, VIOLET, True)
        text_box(s, "Nina says “let me check that for you” … then silence. Nothing appears in the n8n executions list, because the\nrequest never arrived. That is not a prompt bug. It is a networking bug.", 1.05, 5.32, 11.2, 0.85, 15, INK, True)

        # ---- The five commands ----
        s = base("Expose n8n With ngrok", "TUNNEL - SETUP")
        steps = [
            ("1", "Install", "brew install ngrok\n(Windows: ngrok.com/download)", BLUE),
            ("2", "Authtoken", "Free signup, then:\nngrok config add-authtoken <TOKEN>", TEAL),
            ("3", "Start it", "ngrok http 5678\nLeave this window OPEN all session", VIOLET),
            ("4", "Read the URL", "Forwarding  https://<id>.ngrok-free.app\n-> http://localhost:5678", AMBER),
            ("5", "Inspect", "http://127.0.0.1:4040   <- bookmark this\nStatus tab = your public URL.  Inspect tab = every request as it arrives.", RED),
        ]
        for i, (num, label, body_text, color) in enumerate(steps):
            y = 1.5 + i * 1.06
            circle(s, num, 0.78, y + 0.1, 0.56, color, WHITE, 14)
            shape_box(s, 1.6, y, 11.0, 0.92, WHITE, True, LINE, 1)
            text_box(s, label, 1.85, y + 0.08, 2.0, 0.35, 15, INK, True)
            text_box(s, body_text, 4.0, y + 0.06, 8.4, 0.8, 13, GREY)
        text_box(s, "Prove it with curl BEFORE touching the voice platform - HTTP is far easier to debug than audio.", 0.78, 6.88, 11.8, 0.3, 14, VIOLET, True)

        # ---- Building the URL ----
        s = base("Building the URL You Paste Into Retell", "TUNNEL - THE URL")
        text_box(s, "You are gluing two halves together: ngrok supplies the address, the n8n Webhook node supplies the path.", 0.75, 1.42, 11.9, 0.35, 16, GREY)

        shape_box(s, 0.75, 2.0, 6.4, 0.85, PALE, True, BLUE, 1)
        text_box(s, "https://3af5-…ngrok-free.app", 0.95, 2.18, 6.0, 0.45, 16, BLUE, True, valign=MSO_ANCHOR.MIDDLE)
        text_box(s, "from ngrok", 0.95, 2.88, 6.0, 0.28, 12, GREY)
        shape_box(s, 7.45, 2.0, 5.2, 0.85, PALE, True, TEAL, 1)
        text_box(s, "/webhook/check-availability", 7.65, 2.18, 4.8, 0.45, 16, TEAL, True, valign=MSO_ANCHOR.MIDDLE)
        text_box(s, "from the n8n Webhook node", 7.65, 2.88, 4.8, 0.28, 12, GREY)

        shape_box(s, 0.75, 3.4, 11.85, 0.72, PALE, True, PALE, 0)
        text_box(s, "THE RULE:  take the node's PRODUCTION URL and swap http://localhost:5678 for your ngrok address.", 1.05, 3.5, 11.3, 0.52, 16, VIOLET, True, valign=MSO_ANCHOR.MIDDLE)

        traps = [
            ("The free URL changes on every restart", "Re-paste it and PUBLISH the agent again", AMBER),
            ("Test URL instead of Production URL", "Use /webhook/ - never /webhook-test/", RED),
            ("Workflow not published", "404 'not registered' - publish, then retest", BLUE),
            ("Setting WEBHOOK_URL on the container", "Do NOT. It breaks localhost for Labs 1-3", VIOLET),
        ]
        for i, (trap, fix, color) in enumerate(traps):
            y = 4.4 + i * 0.72
            circle(s, "!", 0.85, y, 0.42, color, WHITE, 12)
            text_box(s, trap, 1.5, y - 0.02, 5.4, 0.45, 14, INK, True, valign=MSO_ANCHOR.MIDDLE)
            text_box(s, fix, 7.1, y - 0.02, 5.5, 0.45, 14, GREY, False, valign=MSO_ANCHOR.MIDDLE)

    def video_slides() -> None:
        # ---- The pipeline, as a flow diagram ----
        s = base("How the Avatar Video Pipeline Works", "VIDEO - PIPELINE")
        text_box(s, "Every video lab is this same pipeline. Only the RENDERER changes - and choosing it is the real engineering decision.", 0.75, 1.4, 11.9, 0.35, 16, GREY)

        stages = [
            ("YOU", "type a TOPIC\n(raw facts)", BLUE),
            ("n8n", "Webhook receives it", TEAL),
            ("gemma4", "turns facts into\nSPOKEN COPY", VIOLET),
            ("RENDERER", "HeyGen / Wav2Lip /\nMuseTalk", AMBER),
            ("PAGE", "the video plays", RED),
        ]
        for i, (label, note, color) in enumerate(stages):
            x = 0.72 + i * 2.5
            shape_box(s, x, 2.05, 2.15, 1.5, WHITE, True, color, 1)
            shape_box(s, x, 2.05, 2.15, 0.45, color, True, color, 0)
            text_box(s, label, x, 2.14, 2.15, 0.3, 13, WHITE, True, PP_ALIGN.CENTER)
            text_box(s, note, x + 0.12, 2.62, 1.9, 0.85, 12, INK, False, PP_ALIGN.CENTER)
            if i < len(stages) - 1:
                arrow(s, x + 2.2, 2.78, LINE)

        shape_box(s, 0.72, 3.85, 11.9, 1.35, PALE, True, PALE, 0)
        text_box(s, "THE TWO TEXTS ARE NOT THE SAME TEXT", 1.05, 3.98, 6.0, 0.3, 12, RED, True)
        text_box(s, "You type a TOPIC: “Belgium beats USA 4-1.”   ->   gemma4 writes the SCRIPT: “Welcome back to Global Sports News!…”\nThe renderer speaks EVERY character - feed it raw facts and the avatar reads out a list.", 1.05, 4.32, 11.3, 0.78, 13, INK, True)

        shape_box(s, 0.72, 5.45, 5.85, 1.35, WHITE, True, LINE, 1)
        text_box(s, "Lab 5.3 - HeyGen (cloud)", 0.95, 5.55, 5.4, 0.3, 13, AMBER, True)
        text_box(s, "n8n returns a video_id at once; the PAGE POLLS for status.\nA 1-3 minute HTTP request is fragile.", 0.95, 5.88, 5.4, 0.75, 13, GREY)
        shape_box(s, 6.75, 5.45, 5.87, 1.35, WHITE, True, LINE, 1)
        text_box(s, "Lab 5.5 - local render", 6.98, 5.55, 5.4, 0.3, 13, TEAL, True)
        text_box(s, "n8n returns the finished video_url in ONE response.\n~16 s, so the caller can simply wait.", 6.98, 5.88, 5.4, 0.75, 13, GREY)

        # ---- Three engines, side by side ----
        s = base("Three Lip-Sync Engines, One Photo", "VIDEO - THE TRADE-OFF")
        text_box(s, "Lab 5.1 renders the SAME script and the SAME portrait through all three. Change one variable only.", 0.75, 1.4, 11.9, 0.35, 16, GREY)

        cols = [
            ("WAV2LIP", TEAL, [
                ("Where", "your machine"),
                ("Cost", "free"),
                ("Speed", "~16 s   FASTEST"),
                ("Mouth", "96x96 - soft at 1080p"),
                ("Head", "frozen"),
                ("Needs", "ffmpeg + checkpoint"),
            ]),
            ("MUSETALK", VIOLET, [
                ("Where", "your machine"),
                ("Cost", "free"),
                ("Speed", "~75 s  (7x slower)"),
                ("Mouth", "real pixels  BEST"),
                ("Head", "frozen"),
                ("Needs", "GPU + 3.5 GB weights"),
            ]),
            ("HEYGEN", AMBER, [
                ("Where", "the cloud"),
                ("Cost", "CREDITS"),
                ("Speed", "~40 s - 3 min"),
                ("Mouth", "photoreal"),
                ("Head", "MOVES + blinks"),
                ("Needs", "API key + credits"),
            ]),
        ]
        for i, (name, color, rows) in enumerate(cols):
            x = 0.72 + i * 4.05
            shape_box(s, x, 1.95, 3.8, 4.15, PALE, True, LINE, 1)
            shape_box(s, x, 1.95, 3.8, 0.5, color, True, color, 0)
            text_box(s, name, x, 2.06, 3.8, 0.3, 14, WHITE, True, PP_ALIGN.CENTER)
            for j, (k, v) in enumerate(rows):
                y = 2.6 + j * 0.56
                text_box(s, k, x + 0.2, y, 1.15, 0.3, 11, GREY, False)
                text_box(s, v, x + 1.35, y, 2.35, 0.35, 12, INK, True)

        shape_box(s, 0.72, 6.22, 11.9, 0.82, PALE, True, PALE, 0)
        text_box(s, "Wav2Lip is FASTEST · MuseTalk looks BEST · only HeyGen MOVES THE HEAD", 1.05, 6.3, 11.3, 0.3, 14, VIOLET, True)
        text_box(s, "The question is not “which is best” - it is whether you would upload a customer's face to a vendor to gain a moving head.", 1.05, 6.63, 11.3, 0.3, 13, INK, False)

    for idx, (topic_title, topic_desc) in enumerate(TOPICS, 1):
        topic_slide(idx, topic_title, topic_desc)
        if idx == 2:
            rag_concept_slides()
        if idx == 4:
            ngrok_slides()
        if idx == 5:
            video_slides()
        for lab in [l for l in LABS if l.topic == idx]:
            # Record the slide number BEFORE the lab's first slide is added, so the
            # Lesson Plan cites the deck as it actually is. Any reorder of the deck
            # updates the LP automatically — they cannot drift apart.
            SLIDE_MAP[lab.lab_no] = len(prs.slides._sldIdLst) + 1
            lab_target(lab)
            concept_slide(lab)
            step_slide(lab)
            # The screenshots belong WITH the lab, not in a gallery at the end of
            # the deck - a trainer walking through Lab 4 must see the canvas here.
            for key in lab_shots(lab):
                screenshot_slide(key, f"LAB {lab.lab_no} - {lab.title.upper()}")
            verify_slide(lab)
            fixes_slide(lab)

    s = base("Capstone: Assemble the AI Workforce", "INTEGRATION")
    components = [("TRIGGER", "Customer or operator request", BLUE), ("AGENT", "Reason over approved context", VIOLET), ("TOOLS", "Voice, video, retrieval and data", TEAL), ("REVIEW", "Human approval before impact", AMBER), ("OUTPUT", "Publish, notify and archive", RED)]
    for i, (label, note, color) in enumerate(components):
        x = 0.62 + i * 2.52
        circle(s, str(i + 1), x + 0.69, 1.76, 0.78, color, WHITE, 16)
        shape_box(s, x, 2.82, 2.18, 2.0, WHITE, True, LINE, 1)
        text_box(s, label, x + 0.18, 3.14, 1.82, 0.3, 15, INK, True, PP_ALIGN.CENTER)
        text_box(s, note, x + 0.18, 3.62, 1.82, 0.74, 13, GREY, False, PP_ALIGN.CENTER)
        if i < 4:
            text_box(s, ">", x + 2.18, 3.42, 0.34, 0.35, 19, LINE, True, PP_ALIGN.CENTER)
    text_box(s, "Required evidence: workflow export, screenshots, generated output, tests, rubric, operating guide.", 0.78, 5.55, 11.8, 0.55, 17, VIOLET, True, PP_ALIGN.CENTER)

    s = base("Assessment Rubric", "EVIDENCE STANDARD")
    rubric = [
        ("Problem definition", "User, trigger, output and non-goals", BLUE),
        ("Workflow correctness", "Expected paths proven by execution", TEAL),
        ("AI quality", "Prompts, retrieval and media evaluated", VIOLET),
        ("Guardrails", "Secrets, claims and publishing controlled", AMBER),
        ("Documentation", "Another operator can run and recover", RED),
    ]
    for i, (label, note, color) in enumerate(rubric):
        y = 1.5 + i * 1.0
        circle(s, str(i + 1), 0.78, y, 0.54, color, WHITE, 13)
        text_box(s, label, 1.58, y - 0.02, 2.35, 0.32, 16, INK, True)
        text_box(s, note, 4.0, y - 0.02, 4.95, 0.38, 14, GREY)
        shape_box(s, 9.28, y + 0.06, 2.8, 0.18, PALE, True, PALE, 0)
        shape_box(s, 9.28, y + 0.06, 0.56 * (i + 1), 0.18, color, True, color, 0)
    text_box(s, "Score the evidence, explain one improvement, then rerun the test.", 1.58, 6.45, 10.2, 0.32, 16, VIOLET, True)

    # ── closing block ────────────────────────────────────────────────────────────
    # Practice Exam -> Briefing -> Assessment -> Assessment Flow -> TRAQOM -> Thank You.
    # The practice exam is something you sit BEFORE the day, so it cannot sit between the
    # assessment flow and the closing attendance - that is also the order the house
    # standard fixes for the closing block.
    s = base("Practice Exam", "PREPARE BEFORE THE DAY")
    text_box(s, "A practice exam for this course is available online. Sit it before the assessment day.",
             0.75, 1.45, 11.9, 0.4, 18, GREY)
    shape_box(s, 0.75, 2.1, 11.85, 2.5, PALE, True, LINE, 1)
    text_box(s, "exams.tertiaryinfotech.com", 0.95, 2.6, 11.4, 0.7, 30, BLUE, True, PP_ALIGN.CENTER)
    text_box(s, f"Search for: {COURSE_TITLE}  ({COURSE_CODE})",
             0.95, 3.4, 11.4, 0.5, 17, GREY, False, PP_ALIGN.CENTER)
    for i, (n, label, note, color) in enumerate([
        ("1", "Sit the practice exam", "Same style of questions as the WA", BLUE),
        ("2", "Review what you missed", "Every gap points at a lab you should re-run", TEAL),
        ("3", "Re-run that lab", "Evidence beats revision - go and make the thing work", VIOLET),
    ]):
        y = 4.85 + i * 0.72
        circle(s, n, 0.9, y, 0.5, color, WHITE, 12)
        text_box(s, label, 1.65, y - 0.02, 3.6, 0.4, 15, INK, True, valign=MSO_ANCHOR.MIDDLE)
        text_box(s, note, 5.3, y - 0.02, 7.3, 0.4, 14, GREY, False, valign=MSO_ANCHOR.MIDDLE)

    s = base("Briefing for Assessment", "BEFORE YOU ARE ASSESSED")
    text_box(s, "Read this before the papers are handed out. You are entitled to know exactly how you will be judged.",
             0.75, 1.42, 11.9, 0.4, 17, GREY)
    briefing = [
        ("What you sit", "A Written Assessment (short answer) and a Case Study.", BLUE),
        ("How long", "60 minutes each. Open book. Individually attempted.", TEAL),
        ("How it is marked", "Competent / Not Yet Competent against the assessment criteria.", VIOLET),
        ("If you are NYC", "You are re-assessed once, on the failed instrument only.", AMBER),
        ("Appeals", "Tell the trainer on the day; the appeal route is in your Learner Guide.", RED),
    ]
    for i, (label, note, color) in enumerate(briefing):
        y = 2.05 + i * 0.95
        circle(s, str(i + 1), 0.85, y, 0.58, color, WHITE, 14)
        text_box(s, label, 1.75, y - 0.02, 3.1, 0.4, 17, INK, True, valign=MSO_ANCHOR.MIDDLE)
        text_box(s, note, 5.0, y - 0.02, 7.6, 0.5, 15, GREY, False, valign=MSO_ANCHOR.MIDDLE)

    s = base("Assessment", "HOW YOU ARE ASSESSED")
    for i, (name, dur, tests, color) in enumerate([
        ("Written Assessment (WA)", "60 min", "KNOWLEDGE - the concepts behind the labs: RAG, grounding, webhooks, lip-sync engines, guardrails.", BLUE),
        ("Case Study (CS)", "60 min", "APPLICATION - judgement on a workplace scenario built from the labs you ran.", VIOLET),
    ]):
        x = 0.75 + i * 6.1
        shape_box(s, x, 1.6, 5.85, 4.2, PALE, True, LINE, 1)
        shape_box(s, x, 1.6, 5.85, 0.6, color, True, color, 0)
        text_box(s, name, x, 1.73, 5.85, 0.35, 16, WHITE, True, PP_ALIGN.CENTER)
        circle(s, dur, x + 2.35, 2.4, 1.15, color, WHITE, 15)
        text_box(s, tests, x + 0.35, 3.9, 5.15, 1.6, 15, INK, False, PP_ALIGN.CENTER)
    shape_box(s, 0.75, 6.05, 11.85, 0.95, PALE, True, PALE, 0)
    text_box(s, "Open book · individually attempted · marked Competent / Not Yet Competent · one re-assessment on the failed instrument",
             1.05, 6.2, 11.3, 0.6, 15, VIOLET, True, PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    s = base("Assessment Flow", "FROM PAPER TO SIGN-OFF")
    # The full path, not just the papers: attendance is taken for the assessment session,
    # the scripts are submitted on the LMS, and the day ends on the Assessment Summary
    # Record. Leave those out and the diagram describes an exam, not a WSQ assessment.
    flow = [
        ("BRIEFING", "criteria explained", BLUE),
        ("ATTENDANCE", "TRAQOM, digital", TEAL),
        ("WA (SAQ)", "60 min · knowledge", BLUE),
        ("CASE STUDY", "60 min · application", VIOLET),
        ("SUBMIT", "upload on the LMS", TEAL),
        ("MARKING", "C / NYC per criterion", AMBER),
        ("SIGN-OFF", "Assessment Summary Record", RED),
    ]
    for i, (label, note, color) in enumerate(flow):
        x = 0.62 + i * 1.82
        shape_box(s, x, 2.3, 1.62, 1.75, WHITE, True, color, 1)
        shape_box(s, x, 2.3, 1.62, 0.44, color, True, color, 0)
        text_box(s, label, x, 2.37, 1.62, 0.3, 10, WHITE, True, PP_ALIGN.CENTER)
        text_box(s, note, x + 0.08, 2.88, 1.46, 1.0, 10, INK, False, PP_ALIGN.CENTER)
        if i < len(flow) - 1:
            arrow(s, x + 1.66, 3.14, LINE)
    shape_box(s, 0.62, 4.5, 12.0, 1.5, PALE, True, PALE, 0)
    text_box(s, "NOT YET COMPETENT?", 0.95, 4.65, 4.0, 0.3, 12, RED, True)
    text_box(s, "You are re-assessed ONCE, on the failed instrument only. The trainer records the gap, you close it, and you sit that paper again.\nA re-assessment is a normal part of competency-based training - it is not a failure of the course.",
             0.95, 5.0, 11.4, 0.85, 15, INK, True)

    traqom_slide("at the END")

    s = base("Thank You", "COURSE CLOSE")
    shape_box(s, 0.75, 1.6, 11.82, 3.5, PALE, True, PALE, 0)
    text_box(s, "A polished output is only the beginning.", 1.2, 2.05, 10.9, 0.55, 27, INK, True, PP_ALIGN.CENTER)
    text_box(s, "Professional agentic systems are observable, testable, guarded, recoverable, and documented.", 1.5, 2.95, 10.3, 0.88, 21, GREY, False, PP_ALIGN.CENTER)
    for i, (label, color) in enumerate([("TRACE", BLUE), ("TEST", VIOLET), ("REVIEW", TEAL), ("RECOVER", AMBER), ("DOCUMENT", RED)]):
        x = 1.25 + i * 2.18
        shape_box(s, x, 4.42, 1.82, 0.52, color, True, color, 0)
        text_box(s, label, x, 4.52, 1.82, 0.24, 11, WHITE, True, PP_ALIGN.CENTER)
    text_box(s, "www.tertiarycourses.com.sg", 4.4, 5.82, 4.5, 0.38, 16, BLUE, True, PP_ALIGN.CENTER)

    # Add footers last so later content cannot mask them in PowerPoint or LibreOffice.
    for slide_no, slide in enumerate(prs.slides, 1):
        add_footer(slide, slide_no)

    prs.save(path)
    return SLIDE_MAP


def toc_entries_from_pdf(md: str, pdf: Path):
    """(level, heading, page) for every heading, with the page it ACTUALLY landed on.

    Read out of the rendered PDF rather than guessed, so the contents page agrees with the
    document a learner is holding. Returns [] if the PDF or PyMuPDF is unavailable - the
    caller then keeps the plain field, which Word will still populate on open.
    """
    try:
        import fitz
    except Exception:
        return []
    if not pdf.exists():
        return []

    heads = []
    for line in md.splitlines():
        for hashes, level in (("### ", 3), ("## ", 2), ("# ", 1)):
            if line.startswith(hashes):
                text = plain(line[len(hashes):]).strip()
                if text:
                    heads.append((level, text))
                break

    doc = fitz.open(pdf)
    pages = [p.get_text() for p in doc]
    doc.close()

    # Skip the contents pages themselves. Once the TOC carries a real result, every heading
    # ALSO appears on the TOC page - so a naive forward scan finds "Course profile" on the
    # contents page and reports page 4 for the whole document. It even converges there: the
    # wrong answer reproduces itself on the next pass.
    body_start = 0
    for i, text in enumerate(pages):
        if "TABLE OF CONTENTS" in text.upper():
            body_start = i + 1
            while body_start < len(pages) and "......" in pages[body_start]:
                body_start += 1
            break

    entries, start = [], body_start
    for level, text in heads:
        # Headings are unique and in order, so scan forward only: a lab title that repeats
        # in a cross-reference must not drag the entry back to an earlier page.
        needle = text.lower()
        for i in range(start, len(pages)):
            if needle in " ".join(pages[i].lower().split()):
                entries.append((level, text, i + 1))
                start = i
                break
    return entries


def to_pdf(path: Path, quiet: bool = False) -> None:
    """LibreOffice renders the PDF. A missing PDF is a QA failure, so say so loudly."""
    import subprocess

    try:
        subprocess.run(
            ["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(path.parent), str(path)],
            check=True, capture_output=True, timeout=300,
        )
        pdf = path.with_suffix(".pdf")
        if quiet:
            return
        print(f"  PDF: {pdf.name} ({pdf.stat().st_size // 1024} KB)" if pdf.exists()
              else f"  PDF FAILED for {path.name}")
    except Exception as exc:
        print(f"  PDF skipped for {path.name}: {exc}")


def archive_old(keep: set[str]) -> None:
    """One live version in courseware/, everything superseded in courseware/archive/."""
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    moved = 0
    for f in COURSEWARE.iterdir():
        if f.is_dir() or f.name in keep or f.name.startswith("~$"):
            continue
        if f.suffix.lower() in {".pptx", ".docx", ".pdf", ".md"}:
            f.rename(ARCHIVE / f.name)
            moved += 1
    if moved:
        print(f"  archived {moved} superseded file(s) -> courseware/archive/")


def main() -> None:
    COURSEWARE.mkdir(exist_ok=True)
    LABS_DIR.mkdir(exist_ok=True)
    live = set()
    for lab in LABS:
        path = lab_dir(lab)
        path.mkdir(parents=True, exist_ok=True)
        (path / "README.md").write_text(lab_readme(lab), encoding="utf-8")
        live.add(path.resolve())

    # Prune labs that no longer exist. Renaming or renumbering a lab used to LEAVE the old
    # folder behind, so labs/ accumulated ghosts - a Replicate lab and two HyperFrames labs
    # were still sitting there, and the Drive push would have published all of them.
    import shutil
    for topic in LABS_DIR.iterdir():
        if not topic.is_dir():
            continue
        for folder in topic.iterdir():
            if folder.is_dir() and folder.resolve() not in live:
                print(f"  pruned stale lab: {topic.name}/{folder.name}")
                shutil.rmtree(folder)

    ppt = COURSEWARE / f"{PPT_STEM}.pptx"
    lg_docx = COURSEWARE / f"LG-{COURSE_TITLE.replace(' ', '-')}.docx"
    lp_docx = COURSEWARE / f"LP-{COURSE_TITLE.replace(' ', '-')}.docx"
    lg_md = COURSEWARE / f"LG-{COURSE_TITLE.replace(' ', '-')}.md"
    lp_md = COURSEWARE / f"LP-{COURSE_TITLE.replace(' ', '-')}.md"

    # The deck goes FIRST: it reports the slide number each lab starts on, and the
    # Lesson Plan must cite the deck as it actually is.
    slide_map = write_pptx(ppt)
    print(f"PPTX: {ppt.name}")

    lg_root = learner_guide("courseware/screenshots/")
    lg_courseware = learner_guide("screenshots/")
    (ROOT / "LEARNER_GUIDE.md").write_text(lg_root, encoding="utf-8")
    lg_md.write_text(lg_courseware, encoding="utf-8")

    lp = lesson_plan(slide_map)
    lp_md.write_text(lp, encoding="utf-8")
    (ROOT / "README.md").write_text(readme(), encoding="utf-8")

    # The contents page cannot know its own page numbers until the document has been laid
    # out - and writing it CHANGES that layout, because a 60-entry TOC is itself pages long.
    # So render, read the real page of every heading, rewrite, and repeat until the numbers
    # stop moving. Two passes are not enough: they leave the TOC pointing one page short.
    for md, docx_path, kind in ((lg_root, lg_docx, "Learner Guide"), (lp, lp_docx, "LESSON PLAN")):
        entries = None
        for attempt in range(4):
            write_docx(md, docx_path, kind=kind, toc_entries=entries)
            to_pdf(docx_path, quiet=True)
            fresh = toc_entries_from_pdf(md, docx_path.with_suffix(".pdf"))
            if fresh == entries:
                break
            entries = fresh
        write_docx(md, docx_path, kind=kind, toc_entries=entries)
        print(f"DOCX: {docx_path.name}  (TOC: {len(entries or [])} entries, settled in {attempt + 1})")

    for f in (ppt, lg_docx, lp_docx):
        to_pdf(f)

    archive_old(keep={
        ppt.name, lg_docx.name, lp_docx.name, lg_md.name, lp_md.name,
        ppt.with_suffix(".pdf").name, lg_docx.with_suffix(".pdf").name, lp_docx.with_suffix(".pdf").name,
    })

    missing = [f for _, (f, _c) in SCREENSHOTS.items() if not (SHOTS_DIR / f).exists()]
    if missing:
        print(f"\nScreenshots still to capture ({len(missing)}): {', '.join(sorted(missing))}")


if __name__ == "__main__":
    main()
