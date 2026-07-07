// Lab 7 — embed a HeyGen Interactive Avatar by its share/embed URL.
// (The advanced n8n + LiveAvatar-SDK route is described in the Learner Guide.)

function loadAvatar() {
  const url = document.getElementById("shareUrl").value.trim();
  if (!url) {
    alert("Paste your HeyGen Interactive Avatar share URL first.");
    return;
  }
  const frame = document.getElementById("avatarFrame");
  frame.innerHTML =
    '<iframe allow="microphone; camera; autoplay; clipboard-write; encrypted-media" ' +
    'allowfullscreen src="' + url.replace(/"/g, "&quot;") + '"></iframe>';
  // remember it for next time
  try { localStorage.setItem("heygen_ia_url", url); } catch (e) {}
}

// restore a previously entered URL
window.addEventListener("DOMContentLoaded", () => {
  try {
    const saved = localStorage.getItem("heygen_ia_url");
    if (saved) document.getElementById("shareUrl").value = saved;
  } catch (e) {}
});

window.loadAvatar = loadAvatar;
