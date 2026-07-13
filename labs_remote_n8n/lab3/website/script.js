/* =====================================================================
   Cook & Bake Academy — landing page + RAG chatbot widget
   ---------------------------------------------------------------------
   The chatbot calls YOUR n8n RAG webhook (CX Agent with RAG). The URL is
   NOT hardcoded: paste your own production webhook URL into the ⚙ panel
   in the chat header. It is saved in this browser (localStorage), so each
   learner points the same page at their own n8n.
   If no webhook is set (or it is unreachable), the widget falls back to a
   local keyword search over the course data so the demo still works.
   ===================================================================== */

const CONFIG = {
  // Where the learner's webhook URL is remembered in this browser.
  STORAGE_KEY: "cb_n8n_webhook_url",
  // Shown as the input placeholder — an example only, never used as a default.
  URL_EXAMPLE: "https://n8n.tertiarytraining.com/webhook/<your-webhook-id>",
  // n8n usually returns { output: "..." }. Adjust if your workflow differs.
  RESPONSE_KEYS: ["output", "text", "answer", "response", "message"],
};

const getWebhookUrl = () =>
  (localStorage.getItem(CONFIG.STORAGE_KEY) || "").trim() || CONFIG.DEFAULT_URL;
const setWebhookUrl = (url) => localStorage.setItem(CONFIG.STORAGE_KEY, (url || "").trim());

/* ---------------------------------------------------------------------
   Course catalogue (mirrors the 20 brochures in /brochures)
   --------------------------------------------------------------------- */
const COURSES = [
  { code:"BAK-101", title:"Artisan Sourdough Bread Baking", cat:"Bakery", level:"Beginner", weeks:4, fee:680, campus:"Bakehouse", img:"1589367920969-ab8e050bbb04" },
  { code:"BAK-102", title:"French Pastry & Viennoiserie", cat:"Bakery", level:"Intermediate", weeks:8, fee:1480, campus:"Bakehouse", img:"1509440159596-0249088772ff" },
  { code:"BAK-103", title:"Wedding Cake Design & Decoration", cat:"Bakery", level:"Advanced", weeks:6, fee:1280, campus:"Bakehouse", img:"1535141192574-5d4897c12636" },
  { code:"BAK-104", title:"Macaron Masterclass", cat:"Bakery", level:"Intermediate", weeks:2, fee:420, campus:"Bakehouse", img:"1558326567-98ae2405596b" },
  { code:"BAK-105", title:"Chocolate & Confectionery Making", cat:"Bakery", level:"Intermediate", weeks:4, fee:760, campus:"Bakehouse", img:"1511381939415-e44015466834" },
  { code:"BAK-106", title:"Cupcake & Cake Pops Workshop", cat:"Bakery", level:"Beginner", weeks:1, fee:220, campus:"Bakehouse", img:"1486427944299-d1955d23e34d" },
  { code:"BAK-107", title:"Bread Making Fundamentals", cat:"Bakery", level:"Beginner", weeks:3, fee:480, campus:"Bakehouse", img:"1549931319-a545dcf3bc73" },
  { code:"BAK-108", title:"Cookie & Biscuit Baking", cat:"Bakery", level:"Beginner", weeks:1, fee:180, campus:"Bakehouse", img:"1499636136210-6f4ee915583e" },
  { code:"BAK-109", title:"Pie & Tart Specialist", cat:"Bakery", level:"Intermediate", weeks:3, fee:560, campus:"Bakehouse", img:"1535920527002-b35e96722eb9" },
  { code:"BAK-110", title:"Korean & Asian Bakery", cat:"Bakery", level:"Intermediate", weeks:4, fee:720, campus:"Bakehouse", img:"1558961363-fa8fdf82db35" },
  { code:"CUL-201", title:"Italian Cuisine Mastery", cat:"Cooking", level:"Intermediate", weeks:6, fee:1180, campus:"Culinary", img:"1551183053-bf91a1d81141" },
  { code:"CUL-202", title:"Thai Street Food Cooking", cat:"Cooking", level:"Beginner", weeks:3, fee:540, campus:"Culinary", img:"1559314809-0d155014e29e" },
  { code:"CUL-203", title:"Japanese Sushi & Sashimi", cat:"Cooking", level:"Intermediate", weeks:4, fee:980, campus:"Culinary", img:"1579871494447-9811cf80d66c" },
  { code:"CUL-204", title:"French Culinary Foundations", cat:"Cooking", level:"Beginner", weeks:8, fee:1580, campus:"Culinary", img:"1414235077428-338989a2e8c0" },
  { code:"CUL-205", title:"Chinese Wok Cooking", cat:"Cooking", level:"Beginner", weeks:3, fee:520, campus:"Culinary", img:"1525755662778-989d0524087e" },
  { code:"CUL-206", title:"Indian Curry & Spices", cat:"Cooking", level:"Beginner", weeks:3, fee:500, campus:"Culinary", img:"1505253758473-96b7015fcd40" },
  { code:"CUL-207", title:"Healthy Meal Prep & Nutrition", cat:"Cooking", level:"Beginner", weeks:2, fee:360, campus:"Culinary", img:"1490645935967-10de6ba17061" },
  { code:"CUL-208", title:"Vegetarian & Vegan Cuisine", cat:"Cooking", level:"Beginner", weeks:3, fee:540, campus:"Culinary", img:"1512621776951-a57141f2eefd" },
  { code:"CUL-209", title:"Grilling & BBQ Mastery", cat:"Cooking", level:"Intermediate", weeks:2, fee:460, campus:"Culinary", img:"1555939594-58d7cb561ad1" },
  { code:"CUL-210", title:"Knife Skills & Kitchen Essentials", cat:"Cooking", level:"Beginner", weeks:1, fee:160, campus:"Culinary", img:"1556909212-d5b604d0c90d" },
];

const CAMPUSES = {
  Bakehouse: "Sweet Heights Bakery Campus, 123 Orchard Road, #04-12, Singapore 238888",
  Culinary:  "Flavour Lab Culinary Campus, 88 Bukit Timah Road, #02-05, Singapore 229841",
};

const imgUrl = (id) => `https://images.unsplash.com/photo-${id}?auto=format&fit=crop&w=700&q=70`;

/* ---------------------------------------------------------------------
   Render course cards + filters
   --------------------------------------------------------------------- */
function renderCourses(filter = "all") {
  const grid = document.getElementById("course-grid");
  const list = COURSES.filter((c) => filter === "all" || c.cat === filter);
  grid.innerHTML = list.map((c) => `
    <article class="card">
      <div class="card__img" style="background-image:url('${imgUrl(c.img)}')">
        <span class="card__tag">${c.cat === "Bakery" ? "🧁 Bakery" : "🍳 Cooking"}</span>
        <span class="card__lvl">${c.level}</span>
      </div>
      <div class="card__body">
        <h3>${c.title}</h3>
        <div class="card__meta">
          <span>🕒 ${c.weeks} week${c.weeks > 1 ? "s" : ""}</span>
          <span>📍 ${c.campus === "Bakehouse" ? "Orchard Rd" : "Bukit Timah"}</span>
        </div>
        <div class="card__foot">
          <span class="card__price">S$${c.fee}</span>
          <button class="card__ask" onclick="window.CookBakeChat.ask('Tell me about the ${c.title.replace(/'/g,"")} course')">Ask &amp; enrol →</button>
        </div>
      </div>
    </article>`).join("");
}

document.getElementById("filters").addEventListener("click", (e) => {
  const btn = e.target.closest(".chip");
  if (!btn) return;
  document.querySelectorAll(".chip").forEach((c) => c.classList.remove("is-active"));
  btn.classList.add("is-active");
  renderCourses(btn.dataset.filter);
});
renderCourses();

/* =====================================================================
   Chatbot widget
   ===================================================================== */
const CookBakeChat = (() => {
  const panel  = document.getElementById("chat");
  const fab    = document.getElementById("chat-fab");
  const body   = document.getElementById("chat-body");
  const form   = document.getElementById("chat-form");
  const input  = document.getElementById("chat-text");
  const suggest= document.getElementById("chat-suggest");
  const settings = document.getElementById("chat-settings");
  const urlInput = document.getElementById("chat-webhook-url");
  const urlState = document.getElementById("chat-webhook-state");
  let greeted = false;

  /* ---- Webhook setting (⚙ in the chat header) ------------------------ */
  urlInput.placeholder = CONFIG.URL_EXAMPLE;

  function renderWebhookState() {
    const url = getWebhookUrl();
    urlInput.value = url;
    urlState.textContent = url
      ? "✅ Connected to your n8n webhook."
      : "⚠️ No webhook set — answers come from the offline demo data, not your RAG agent.";
    urlState.className = url ? "chat__hint chat__hint--ok" : "chat__hint chat__hint--warn";
  }

  function openSettings() {
    settings.style.display = "block";
    renderWebhookState();
    setTimeout(() => urlInput.focus(), 50);
  }
  function toggleSettings() {
    settings.style.display === "block" ? (settings.style.display = "none") : openSettings();
  }
  function saveWebhook() {
    setWebhookUrl(urlInput.value);
    renderWebhookState();
    addMsg("bot", getWebhookUrl()
      ? "Webhook saved. Ask me something and I'll route it through **your** n8n RAG agent."
      : "Webhook cleared. I'll answer from the local demo data until you add one.");
    settings.style.display = "none";
  }

  function open() {
    panel.classList.add("is-open");
    panel.setAttribute("aria-hidden", "false");
    fab.style.display = "none";
    if (!greeted) { greet(); greeted = true; }
    setTimeout(() => input.focus(), 250);
  }
  function close() {
    panel.classList.remove("is-open");
    panel.setAttribute("aria-hidden", "true");
    fab.style.display = "grid";
  }
  function toggle() { panel.classList.contains("is-open") ? close() : open(); }

  function greet() {
    addMsg("bot",
      "👋 Hi! I'm the **Cook & Bake Academy** course assistant.\n\n" +
      "Ask me anything about our cooking & bakery courses — duration, course fees, locations, schedules or what you'll learn!");
    if (!getWebhookUrl()) {
      addMsg("bot",
        "⚙️ **Setup needed:** I'm not connected to an n8n agent yet, so I'm answering from local demo data.\n\n" +
        "Click the ⚙ icon above and paste the **production webhook URL** of your *CX Agent with RAG* workflow.");
      openSettings();
    }
  }

  function addMsg(who, text) {
    const el = document.createElement("div");
    el.className = `msg msg--${who}`;
    el.innerHTML = formatText(text);
    body.appendChild(el);
    body.scrollTop = body.scrollHeight;
    return el;
  }

  function formatText(t) {
    return t
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
      .replace(/\n/g, "<br>");
  }

  function showTyping() {
    const el = document.createElement("div");
    el.className = "msg msg--bot";
    el.innerHTML = '<span class="typing"><span></span><span></span><span></span></span>';
    body.appendChild(el);
    body.scrollTop = body.scrollHeight;
    return el;
  }

  async function send(text) {
    text = (text || "").trim();
    if (!text) return;
    addMsg("user", text);
    input.value = "";
    suggest.style.display = "none";
    const typing = showTyping();

    let reply;
    try {
      reply = getWebhookUrl()
        ? await callWebhook(text)
        : localAnswer(text);
    } catch (err) {
      console.warn("Webhook failed, using local fallback:", err);
      reply = localAnswer(text) +
        "\n\n_(Your n8n webhook could not be reached, so this answer came from local demo data. " +
        "Check the ⚙ URL and that the workflow is Active.)_";
    }
    typing.remove();
    addMsg("bot", reply);
  }

  async function callWebhook(text) {
    const res = await fetch(getWebhookUrl(), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chatInput: text, message: text, sessionId: getSession() }),
    });
    if (!res.ok) throw new Error("HTTP " + res.status);
    const data = await res.json();
    for (const k of CONFIG.RESPONSE_KEYS) {
      if (data && typeof data[k] === "string") return data[k];
    }
    return typeof data === "string" ? data : JSON.stringify(data);
  }

  function getSession() {
    let s = sessionStorage.getItem("cb_session");
    if (!s) { s = "web-" + Math.random().toString(36).slice(2); sessionStorage.setItem("cb_session", s); }
    return s;
  }

  /* ---- Local RAG-style fallback (keyword search over course data) ---- */
  function localAnswer(q) {
    const t = q.toLowerCase();

    // location intent
    if (/(where|location|located|address|campus|venue)/.test(t)) {
      return "We have **two campuses** in Singapore:\n\n" +
        "🧁 **Bakehouse Campus** (bakery courses)\n" + CAMPUSES.Bakehouse + "\n\n" +
        "🍳 **Culinary Campus** (cooking courses)\n" + CAMPUSES.Culinary;
    }

    // beginner / list intent
    if (/(beginner|new|start|no experience|list|what courses|which courses)/.test(t) && !matchCourse(t)) {
      const cooking = COURSES.filter(c => c.cat === "Cooking" && c.level === "Beginner");
      const bakery  = COURSES.filter(c => c.cat === "Bakery"  && c.level === "Beginner");
      const fmt = a => a.map(c => `• ${c.title} (${c.weeks}wk, S$${c.fee})`).join("\n");
      return "Great choice for beginners! Here are some popular starter courses:\n\n" +
        "**Bakery**\n" + fmt(bakery) + "\n\n**Cooking**\n" + fmt(cooking) +
        "\n\nAsk me about any one for full details. 🙂";
    }

    const c = matchCourse(t);
    if (c) {
      const wants = {
        fee: /(fee|cost|price|how much|expensive|charge)/.test(t),
        dur: /(duration|how long|weeks|length|time)/.test(t),
        loc: /(where|location|located|address|campus|venue)/.test(t),
      };
      const addr = CAMPUSES[c.campus];
      if (wants.fee && !wants.dur && !wants.loc)
        return `The **${c.title}** course (${c.code}) costs **S$${c.fee}**, inclusive of ingredients, apron and recipe booklet. 10% early-bird discount applies 4 weeks before intake.`;
      if (wants.dur && !wants.fee && !wants.loc)
        return `The **${c.title}** course runs for **${c.weeks} week${c.weeks>1?"s":""}** (${c.level} level).`;
      if (wants.loc && !wants.fee && !wants.dur)
        return `The **${c.title}** course is held at our ${c.campus} Campus:\n${addr}`;
      // full summary
      return `**${c.title}** (${c.code})\n\n` +
        `• 📂 Category: ${c.cat}\n` +
        `• 🎯 Level: ${c.level}\n` +
        `• 🕒 Duration: ${c.weeks} week${c.weeks>1?"s":""}\n` +
        `• 💰 Fee: S$${c.fee} (incl. ingredients & materials)\n` +
        `• 📍 Location: ${addr}\n\n` +
        `Would you like to know about intakes or how to enrol?`;
    }

    // fee comparison without specific course
    if (/(fee|cost|price|how much)/.test(t)) {
      const min = Math.min(...COURSES.map(c=>c.fee));
      const max = Math.max(...COURSES.map(c=>c.fee));
      return `Our course fees range from **S$${min}** (short workshops) to **S$${max}** (full diploma programmes). Tell me which course you're interested in and I'll give you the exact fee. 🙂`;
    }

    return "I can help with our cooking & bakery courses — durations, fees, locations and what you'll learn. " +
      "Try asking e.g. *\"How much is the sourdough course?\"* or *\"How long is the sushi course?\"* 🍞🍳";
  }

  function matchCourse(t) {
    const KEY = {
      sourdough:"BAK-101", "french pastry":"BAK-102", viennoiserie:"BAK-102",
      wedding:"BAK-103", macaron:"BAK-104", chocolate:"BAK-105", confection:"BAK-105",
      cupcake:"BAK-106", "cake pop":"BAK-106", "bread making":"BAK-107", "bread fundamental":"BAK-107",
      cookie:"BAK-108", biscuit:"BAK-108", pie:"BAK-109", tart:"BAK-109",
      korean:"BAK-110", "asian bakery":"BAK-110",
      italian:"CUL-201", pasta:"CUL-201", thai:"CUL-202", sushi:"CUL-203", sashimi:"CUL-203", japanese:"CUL-203",
      "french culinary":"CUL-204", "french cooking":"CUL-204", chinese:"CUL-205", wok:"CUL-205",
      indian:"CUL-206", curry:"CUL-206", healthy:"CUL-207", "meal prep":"CUL-207", nutrition:"CUL-207",
      vegan:"CUL-208", vegetarian:"CUL-208", grill:"CUL-209", bbq:"CUL-209", barbecue:"CUL-209",
      knife:"CUL-210", "kitchen essential":"CUL-210",
    };
    for (const k in KEY) if (t.includes(k)) return COURSES.find(c => c.code === KEY[k]);
    // try title words
    return COURSES.find(c => t.includes(c.title.toLowerCase()));
  }

  // wire events
  form.addEventListener("submit", (e) => { e.preventDefault(); send(input.value); });
  suggest.addEventListener("click", (e) => {
    const b = e.target.closest("button");
    if (b) { open(); send(b.textContent); }
  });

  renderWebhookState();

  return {
    open, close, toggle,
    toggleSettings, saveWebhook,
    ask: (q) => { open(); setTimeout(() => send(q), 300); },
  };
})();

window.CookBakeChat = CookBakeChat;
