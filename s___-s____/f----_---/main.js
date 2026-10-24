<script src="js/main.js"></script>



/* ========================================
   SignSpeak - Main JavaScript
   ======================================== */

document.addEventListener("DOMContentLoaded", () => {
  // ---------- ELEMENTS ----------
  const pages = document.querySelectorAll(".page");
  const userText = document.getElementById("userText");
  const result = document.getElementById("result");
  const inputPanel = document.getElementById("inputPanel");

  const textModeBtn = document.getElementById("textMode");
  const signModeBtn = document.getElementById("signMode");
  const swapModeBtn = document.getElementById("swapMode");
  const translateBtn = document.getElementById("translateBtn");

  const historyList = document.getElementById("historyList");
  const signList = document.getElementById("signList");
  const searchSign = document.getElementById("searchSign");

  let currentMode = "text";
  let translations = [];
  let cameraStream = null;

  // ---------- NAVIGATION ----------
  document.querySelectorAll("[data-page]").forEach(link => {
    link.addEventListener("click", event => {
      event.preventDefault();

      const targetPage = link.dataset.page;

      pages.forEach(page => {
        page.classList.toggle("active", page.id === targetPage);
      });

      document.querySelectorAll("[data-page]").forEach(navLink => {
        navLink.classList.toggle("active", navLink === link);
      });

      history.replaceState(null, "", "#" + targetPage);
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  });

  // Open the requested page when a URL hash is provided.
  function openPageFromHash() {
    const pageId = location.hash.slice(1);
    const target = document.getElementById(pageId);

    if (target && target.classList.contains("page")) {
      pages.forEach(page => {
        page.classList.toggle("active", page === target);
      });
    }
  }

  openPageFromHash();
  window.addEventListener("hashchange", openPageFromHash);

  // ---------- TRANSLATION MODES ----------
  function setMode(mode) {
    currentMode = mode;

    textModeBtn?.classList.toggle("active", mode === "text");
    signModeBtn?.classList.toggle("active", mode === "sign");

    if (inputPanel) {
      inputPanel.style.display = mode === "text" ? "block" : "none";
    }

    const outputTitle = document.getElementById("outputTitle");

    if (outputTitle) {
      outputTitle.textContent =
        mode === "text" ? "SIGN TRANSLATION" : "TEXT OUTPUT";
    }

    if (translateBtn) {
      translateBtn.textContent =
        mode === "text" ? "✧ Translate" : "📹 Start Camera";
    }

    if (result) {
      result.textContent =
        mode === "text"
          ? "Translation will appear here"
          : "Start the camera to begin sign detection.";
    }
  }

  textModeBtn?.addEventListener("click", () => setMode("text"));
  signModeBtn?.addEventListener("click", () => setMode("sign"));

  swapModeBtn?.addEventListener("click", () => {
    setMode(currentMode === "text" ? "sign" : "text");
  });

  // ---------- TEXT TRANSLATION ----------
  function translateText() {
    const text = userText?.value.trim();

    if (!text) {
      if (result) result.textContent = "Please enter some text first.";
      userText?.focus();
      return;
    }

    if (currentMode === "sign") {
      startCamera();
      return;
    }

    /*
      This is a demonstration preview.
      Real sign-language translation requires a
      connected translation API or trained model.
    */
    if (result) {
      result.replaceChildren();

      const preview = document.createElement("div");
      preview.textContent =
        "🤟\n" + text +
        "\n\nDemo preview — connect a sign-language model for real sign output.";

      result.appendChild(preview);
    }

    saveTranslation(text, "Text to Sign");
    speakText(text);
  }

  translateBtn?.addEventListener("click", translateText);

  // Quick phrase buttons.
  document.querySelectorAll(".quick button").forEach(button => {
    button.addEventListener("click", () => {
      if (userText) userText.value = button.textContent.trim();

      setMode("text");
      translateText();
    });
  });

  // ---------- VOICE OUTPUT ----------
  function speakText(text) {
    if (!("speechSynthesis" in window)) {
      console.warn("Speech output is not supported in this browser.");
      return;
    }

    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "en-US";
    utterance.rate = 0.9;

    window.speechSynthesis.speak(utterance);
  }

  // ---------- TRANSLATION HISTORY ----------
  function saveTranslation(text, direction) {
    const entry = {
      text,
      direction,
      date: new Date().toLocaleString()
    };

    translations.unshift(entry);
    renderHistory();
  }

  function renderHistory() {
    if (!historyList) return;

    historyList.replaceChildren();

    if (translations.length === 0) {
      historyList.textContent =
        "No translations yet. Start translating to see your history.";
      return;
    }

    translations.forEach(entry => {
      const card = document.createElement("article");
      card.className = "glass";
      card.style.marginBottom = "12px";

      const title = document.createElement("h3");
      title.textContent = entry.text;

      const direction = document.createElement("p");
      direction.textContent = entry.direction;

      const date = document.createElement("small");
      date.textContent = entry.date;

      card.append(title, direction, date);
      historyList.appendChild(card);
    });
  }

  // ---------- SIGN DICTIONARY ----------
  const signs = [
    ["👋", "Hello", "Greetings"],
    ["👋", "Goodbye", "Greetings"],
    ["🙏", "Thank You", "Greetings"],
    ["🤲", "Please", "Greetings"],
    ["😔", "Sorry", "Greetings"],
    ... "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("").map(letter => [
      "✋", letter, "Alphabet"
    ]),
    ...Array.from({ length: 10 }, (_, i) => [
      "☝️", String(i + 1), "Numbers"
    ]),
    ["🤟", "I Love You", "Phrases"],
    ["🤝", "How Are You", "Phrases"],
    ["👋", "Nice to Meet You", "Phrases"],
    ["🆘", "Help", "Phrases"],
    ["✅", "Yes", "Phrases"],
    ["🚫", "No", "Phrases"],
    ["💧", "Water", "Common"],
    ["🍽️", "Eat", "Common"],
    ["🏠", "Home", "Common"],
    ["🙂", "Happy", "Emotions"],
    ["😢", "Sad", "Emotions"],
    ["😠", "Angry", "Emotions"],
    ["❓", "What", "Common"],
    ["📍", "Where", "Common"],
    ["☀️", "Day", "Common"],
    ["🌙", "Night", "Common"]
  ];

  function renderSigns(query = "") {
    if (!signList) return;

    signList.replaceChildren();

    const filtered = signs.filter(([, word, category]) =>
      `${word} ${category}`.toLowerCase().includes(query.toLowerCase())
    );

    if (filtered.length === 0) {
      signList.textContent = "No matching signs found.";
      return;
    }

    filtered.forEach(([emoji, word, category]) => {
      const card = document.createElement("article");
      card.className = "glass sign";

      const icon = document.createElement("span");
      icon.textContent = emoji;

      const title = document.createElement("strong");
      title.textContent = word;

      const label = document.createElement("p");
      label.className = "muted";
      label.textContent = category;

      card.append(icon, title, label);

      card.addEventListener("click", () => {
        if (userText) userText.value = word;

        setMode("text");

        pages.forEach(page => {
          page.classList.toggle("active", page.id === "translate");
        });

        window.location.hash = "translate";
        window.scrollTo({ top: 0, behavior: "smooth" });
      });

      signList.appendChild(card);
    });
  }

  searchSign?.addEventListener("input", event => {
    renderSigns(event.target.value);
  });

  renderSigns();

  // ---------- LEARNING PROGRESS ----------
  function updateProgress() {
    const topics = [...document.querySelectorAll(".topic")];
    const completed = topics.filter(topic => topic.checked).length;

    const percentage = topics.length
      ? Math.round((completed / topics.length) * 100)
      : 0;

    const progressText = document.getElementById("progress");
    const progressBar = document.getElementById("progressBar");

    if (progressText) progressText.textContent = percentage + "%";
    if (progressBar) progressBar.value = percentage;
  }

  document.querySelectorAll(".topic").forEach(topic => {
    topic.addEventListener("change", updateProgress);
  });

  // ---------- CAMERA ACCESS ----------
  async function startCamera() {
    if (!navigator.mediaDevices?.getUserMedia) {
      if (result) {
        result.textContent =
          "Camera access is unavailable. Use HTTPS or localhost in a supported browser.";
      }
      return;
    }

    try {
      if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
      }

      cameraStream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: false
      });

      if (result) {
        result.replaceChildren();

        const video = document.createElement("video");
        video.autoplay = true;
        video.playsInline = true;
        video.muted = true;
        video.style.width = "100%";
        video.style.borderRadius = "12px";
        video.srcObject = cameraStream;

        const message = document.createElement("p");
        message.textContent =
          "Camera active. A trained sign-recognition model is needed to identify signs.";

        result.append(video, message);
      }
    } catch (error) {
      console.error("Camera error:", error);

      if (result) {
        result.textContent =
          "Unable to access the camera. Check browser permissions and try again.";
      }
    }
  }

  // ---------- EMERGENCY SOS DEMO ----------
  const sosButton = document.getElementById("sosBtn");

  sosButton?.addEventListener("click", () => {
    const type = document.getElementById("emergencyType")?.value || "General";
    const message = document.getElementById("sosMessage")?.value.trim() || "None";
    const output = document.getElementById("sosResult");

    if (output) {
      output.textContent =
        `SOS demo preview — Type: ${type}. Message: ${message}. ` +
        "No emergency alert was sent. Contact local emergency services directly if needed.";
    }
  });

  // ---------- INITIALIZE ----------
  setMode("text");
  renderHistory();
  updateProgress();

  // Release the camera when leaving the page.
  window.addEventListener("pagehide", () => {
    if (cameraStream) {
      cameraStream.getTracks().forEach(track => track.stop());
    }
  });
});



