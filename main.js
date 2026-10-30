/**
 * potatoGuardProject — Frontend Application Logic
 * Handles file upload, drag-and-drop, webcam capture, sample selection,
 * asynchronous API prediction, interactive visual switching, and report printing.
 */

let selectedFile = null;
let selectedBase64 = null;
let selectedSampleId = null;
let currentDiagnosisData = null;
let activeVisualView = "heatmap";
let webcamStream = null;

// Initialize when DOM loads
document.addEventListener("DOMContentLoaded", () => {
  setupDragAndDrop();
  setupFileInput();
  loadHistoryFromStorage();
  if (window.lucide) {
    lucide.createIcons();
  }
});

// Tab Navigation
function switchTab(tabId) {
  document.querySelectorAll(".tab-content").forEach((el) => {
    el.classList.add("hidden");
    el.classList.remove("block");
  });

  document.querySelectorAll(".nav-tab").forEach((btn) => {
    btn.classList.remove("active", "text-emerald-700", "bg-emerald-50");
    btn.classList.add("text-slate-600");
  });

  const activeTab = document.getElementById(`tab-${tabId}`);
  const activeBtn = document.getElementById(`tab-btn-${tabId}`);

  if (activeTab) {
    activeTab.classList.remove("hidden");
    activeTab.classList.add("block");
  }
  if (activeBtn) {
    activeBtn.classList.add("active", "text-emerald-700", "bg-emerald-50");
    activeBtn.classList.remove("text-slate-600");
  }

  if (window.lucide) {
    lucide.createIcons();
  }
}

function selectSampleAndSwitch(sampleId) {
  switchTab("detector");
  selectSample(sampleId);
}

// Drag & Drop Setup
function setupDragAndDrop() {
  const dropZone = document.getElementById("drop-zone");
  const fileInput = document.getElementById("file-input");

  dropZone.addEventListener("click", () => fileInput.click());

  ["dragenter", "dragover"].forEach((eventName) => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.add("drag-over");
    });
  });

  ["dragleave", "drop"].forEach((eventName) => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.remove("drag-over");
    });
  });

  dropZone.addEventListener("drop", (e) => {
    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      handleImageSelection(files[0]);
    }
  });
}

function setupFileInput() {
  const fileInput = document.getElementById("file-input");
  fileInput.addEventListener("change", (e) => {
    if (e.target.files && e.target.files.length > 0) {
      handleImageSelection(e.target.files[0]);
    }
  });
}

function handleImageSelection(file) {
  if (!file.type.startsWith("image/")) {
    alert("Please select a valid image file (JPEG, PNG, WEBP).");
    return;
  }

  selectedFile = file;
  selectedSampleId = null;
  clearSampleHighlights();

  const reader = new FileReader();
  reader.onload = (e) => {
    selectedBase64 = e.target.result;
    showPreview(e.target.result);
  };
  reader.readAsDataURL(file);
}

function showPreview(dataUrl) {
  const prompt = document.getElementById("drop-prompt");
  const wrapper = document.getElementById("preview-wrapper");
  const previewImg = document.getElementById("preview-img");
  const analyzeBtn = document.getElementById("analyze-btn");

  previewImg.src = dataUrl;
  prompt.classList.add("hidden");
  wrapper.classList.remove("hidden");
  analyzeBtn.disabled = false;
  if (window.lucide) lucide.createIcons();
}

function clearSelectedImage(event) {
  if (event) event.stopPropagation();

  selectedFile = null;
  selectedBase64 = null;
  selectedSampleId = null;

  document.getElementById("file-input").value = "";
  document.getElementById("drop-prompt").classList.remove("hidden");
  document.getElementById("preview-wrapper").classList.add("hidden");
  document.getElementById("preview-img").src = "";
  document.getElementById("analyze-btn").disabled = true;
  clearSampleHighlights();
}

// 1-Click Sample Leaf Selection
function selectSample(sampleId) {
  selectedSampleId = sampleId;
  selectedFile = null;
  selectedBase64 = null;

  clearSampleHighlights();
  try {
    if (typeof event !== "undefined" && event && event.currentTarget) {
      event.currentTarget.classList.add("active");
    }
  } catch (err) {}

  const sampleMap = {
    early_blight: "/static/samples/early_blight_sample.jpg",
    late_blight: "/static/samples/late_blight_sample.jpg",
    healthy: "/static/samples/healthy_sample.jpg",
  };

  if (sampleMap[sampleId]) {
    showPreview(sampleMap[sampleId]);
    runAnalysis();
  }
}

function clearSampleHighlights() {
  document.querySelectorAll(".sample-card").forEach((card) => {
    card.classList.remove("active");
  });
}

// Live Camera Modal
async function openWebcamModal() {
  const modal = document.getElementById("webcam-modal");
  const video = document.getElementById("webcam-video");
  modal.classList.remove("hidden");

  try {
    webcamStream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "environment", width: { ideal: 1280 } },
    });
    video.srcObject = webcamStream;
  } catch (err) {
    alert("Camera access denied or unavailable: " + err.message);
    closeWebcamModal();
  }
}

function closeWebcamModal() {
  const modal = document.getElementById("webcam-modal");
  modal.classList.add("hidden");

  if (webcamStream) {
    webcamStream.getTracks().forEach((track) => track.stop());
    webcamStream = null;
  }
}

function captureWebcamFrame() {
  const video = document.getElementById("webcam-video");
  const canvas = document.getElementById("webcam-canvas");
  canvas.width = video.videoWidth || 640;
  canvas.height = video.videoHeight || 480;

  const ctx = canvas.getContext("2d");
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

  const dataUrl = canvas.toDataURL("image/jpeg", 0.92);
  selectedBase64 = dataUrl;
  selectedFile = null;
  selectedSampleId = null;

  closeWebcamModal();
  showPreview(dataUrl);
}

// Execute ML Diagnostic Inference
async function runAnalysis() {
  const analyzeBtn = document.getElementById("analyze-btn");
  const btnText = document.getElementById("analyze-btn-text");
  const spinner = document.getElementById("analyze-spinner");

  // Show Loading state
  analyzeBtn.disabled = true;
  btnText.classList.add("hidden");
  spinner.classList.remove("hidden");

  try {
    const formData = new FormData();
    if (selectedFile) {
      formData.append("file", selectedFile);
    }
    if (selectedBase64) {
      formData.append("image_base64", selectedBase64);
    }
    if (selectedSampleId) {
      formData.append("sample_id", selectedSampleId);
    }

    // Safety fallback: if no input flagged yet, check preview src
    if (!selectedFile && !selectedBase64 && !selectedSampleId) {
      const previewImg = document.getElementById("preview-img");
      if (previewImg && previewImg.src && previewImg.src.startsWith("data:")) {
        formData.append("image_base64", previewImg.src);
      } else {
        alert("Please upload an image or choose a sample first.");
        return;
      }
    }

    const res = await fetch("/api/predict", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    if (!res.ok || !data.success) {
      throw new Error(data.detail || "Prediction failed");
    }

    currentDiagnosisData = data.data;
    renderDiagnosisResults(data.data);
    addToHistory(data.data);

    // Smooth scroll to results on mobile devices
    if (window.innerWidth < 1024) {
      document.getElementById("results-panel").scrollIntoView({ behavior: "smooth" });
    }
  } catch (err) {
    alert("Diagnostic error: " + err.message);
  } finally {
    analyzeBtn.disabled = false;
    btnText.classList.remove("hidden");
    spinner.classList.add("hidden");
  }
}

// Render Results to UI
function renderDiagnosisResults(result) {
  document.getElementById("results-placeholder").classList.add("hidden");
  const panel = document.getElementById("results-panel");
  panel.classList.remove("hidden");

  // Primary Diagnosis
  document.getElementById("diag-display-name").textContent = result.display_name;
  document.getElementById("diag-scientific-name").textContent = `${result.scientific_name} • ${result.pathogen_type}`;

  // Risk Badge
  const riskBadge = document.getElementById("diag-risk-badge");
  const riskText = document.getElementById("diag-risk-text");
  riskBadge.className = `inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold border mb-2 ${result.badge_color}`;
  riskText.textContent = `${result.risk_level} Risk`;

  // Confidence & SVG Circle
  document.getElementById("diag-conf-value").textContent = `${result.confidence_pct}%`;
  const confOffset = 100 - result.confidence_pct;
  const circleProgress = document.getElementById("conf-circle-progress");
  circleProgress.setAttribute("stroke-dashoffset", confOffset);

  // Mini metrics
  document.getElementById("diag-severity-grade").textContent = result.severity.grade;
  document.getElementById("diag-affected-pct").textContent = `${result.severity.affected_pct}%`;
  document.getElementById("diag-pathogen-type").textContent = result.pathogen_type;

  // Multi-class probability distribution bars
  const probContainer = document.getElementById("prob-bars-container");
  probContainer.innerHTML = "";
  result.probabilities.forEach((p) => {
    const isTop = p.class === result.class_id;
    const barHtml = `
      <div>
        <div class="flex justify-between text-xs font-medium mb-1">
          <span class="${isTop ? 'font-bold text-slate-800' : 'text-slate-600'}">${p.name}</span>
          <span class="${isTop ? 'font-bold text-emerald-600' : 'text-slate-500'}">${p.prob}%</span>
        </div>
        <div class="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
          <div class="h-2.5 rounded-full transition-all duration-700 ${isTop ? 'bg-emerald-600' : 'bg-slate-300'}" style="width: ${p.prob}%"></div>
        </div>
      </div>
    `;
    probContainer.insertAdjacentHTML("beforeend", barHtml);
  });

  // Setup Visual Studio images
  activeVisualView = "heatmap";
  switchVisualView("heatmap");

  // Populate Clinical Symptoms
  const symptomsList = document.getElementById("diag-symptoms-list");
  symptomsList.innerHTML = "";
  result.symptoms.forEach((s) => {
    symptomsList.insertAdjacentHTML(
      "beforeend",
      `<li class="flex items-start space-x-2"><i data-lucide="check" class="w-4 h-4 text-emerald-600 shrink-0 mt-0.5"></i><span>${s}</span></li>`
    );
  });

  // Populate Chemical Treatments
  const chemList = document.getElementById("diag-chemicals-list");
  chemList.innerHTML = "";
  result.chemical_treatments.forEach((chem) => {
    chemList.insertAdjacentHTML(
      "beforeend",
      `
      <div class="bg-slate-50 border border-slate-200/80 rounded-xl p-3.5 space-y-1">
        <div class="text-xs font-bold text-slate-900">${chem.name}</div>
        <div class="text-[11px] text-emerald-700 font-semibold">${chem.type}</div>
        <div class="text-[11px] text-slate-600 mt-1"><strong>Dosage:</strong> ${chem.dosage}</div>
        <div class="text-[11px] text-slate-500"><strong>Schedule:</strong> ${chem.application}</div>
      </div>
    `
    );
  });

  // Populate Organic Controls
  const organicList = document.getElementById("diag-organic-list");
  organicList.innerHTML = "";
  result.organic_controls.forEach((org) => {
    organicList.insertAdjacentHTML(
      "beforeend",
      `<li class="flex items-start space-x-2"><i data-lucide="sprout" class="w-4 h-4 text-emerald-600 shrink-0 mt-0.5"></i><span>${org}</span></li>`
    );
  });

  // Populate Preventive Cultural Practices
  const prevList = document.getElementById("diag-prevent-list");
  prevList.innerHTML = "";
  result.preventive_practices.forEach((prev) => {
    prevList.insertAdjacentHTML(
      "beforeend",
      `<li class="flex items-start space-x-2"><i data-lucide="shield-check" class="w-4 h-4 text-emerald-600 shrink-0 mt-0.5"></i><span>${prev}</span></li>`
    );
  });

  // Environmental triggers
  document.getElementById("diag-env-triggers").textContent = result.environmental_triggers;

  if (window.lucide) {
    lucide.createIcons();
  }
}

// Visual Inspection Studio View Toggles
function switchVisualView(view) {
  if (!currentDiagnosisData) return;
  activeVisualView = view;

  // Toggle button styles
  const btnOriginal = document.getElementById("vis-tab-original");
  const btnHeatmap = document.getElementById("vis-tab-heatmap");
  const btnOverlay = document.getElementById("vis-tab-overlay");
  const displayImg = document.getElementById("vis-display-img");
  const badge = document.getElementById("vis-badge");
  const caption = document.getElementById("vis-caption");

  [btnOriginal, btnHeatmap, btnOverlay].forEach((btn) => {
    btn.className = "vis-btn px-3 py-1.5 rounded-lg text-slate-700 hover:text-slate-900 transition";
  });

  const previewSrc = document.getElementById("preview-img").src;

  if (view === "original") {
    btnOriginal.className = "vis-btn px-3 py-1.5 rounded-lg bg-white shadow-sm text-emerald-700 font-bold transition";
    displayImg.src = previewSrc;
    badge.textContent = "Original Leaf Image";
    caption.textContent = "High-definition camera capture showing natural leaf color and morphology.";
  } else if (view === "heatmap") {
    btnHeatmap.className = "vis-btn px-3 py-1.5 rounded-lg bg-white shadow-sm text-emerald-700 font-bold transition";
    displayImg.src = currentDiagnosisData.visualizations.heatmap;
    badge.textContent = "AI Saliency Anomaly Heatmap";
    caption.textContent = "Grad-CAM saliency colormap: warm red/yellow tones pinpoint active necrotic infection clusters.";
  } else if (view === "overlay") {
    btnOverlay.className = "vis-btn px-3 py-1.5 rounded-lg bg-white shadow-sm text-emerald-700 font-bold transition";
    displayImg.src = currentDiagnosisData.visualizations.overlay;
    badge.textContent = "Lesion Segmentation Mask";
    caption.textContent = "Pixel-level boundary mask segmenting diseased pathology margins from healthy leaf tissue.";
  }
}

// Session Scan History Management
function addToHistory(result) {
  let history = JSON.parse(sessionStorage.getItem("leaf_history") || "[]");
  const previewSrc = document.getElementById("preview-img").src;

  const item = {
    id: Date.now(),
    name: result.display_name,
    class_id: result.class_id,
    conf: result.confidence_pct,
    severity: result.severity.grade,
    thumbnail: previewSrc,
    time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
  };

  history.unshift(item);
  if (history.length > 5) history.pop();
  sessionStorage.setItem("leaf_history", JSON.stringify(history));
  renderHistory(history);
}

function loadHistoryFromStorage() {
  const history = JSON.parse(sessionStorage.getItem("leaf_history") || "[]");
  renderHistory(history);
}

function renderHistory(history) {
  const container = document.getElementById("history-container");
  const list = document.getElementById("history-list");

  if (!history || history.length === 0) {
    container.classList.add("hidden");
    return;
  }

  container.classList.remove("hidden");
  list.innerHTML = "";

  history.forEach((h) => {
    const isHealthy = h.class_id === "Potato___healthy";
    const badgeColor = isHealthy ? "text-emerald-700 bg-emerald-50" : "text-amber-700 bg-amber-50";

    const itemHtml = `
      <div class="flex items-center justify-between p-2 rounded-xl bg-slate-50 border border-slate-100 text-xs hover:bg-slate-100/60 transition">
        <div class="flex items-center space-x-2.5 truncate">
          <img src="${h.thumbnail}" class="w-8 h-8 rounded-lg object-cover border border-slate-200 shrink-0">
          <div class="truncate">
            <div class="font-bold text-slate-800 truncate">${h.name}</div>
            <div class="text-[10px] text-slate-400">${h.time} &bull; ${h.conf}% Conf</div>
          </div>
        </div>
        <span class="px-2 py-0.5 rounded-full text-[10px] font-bold ${badgeColor} shrink-0">
          ${h.conf}%
        </span>
      </div>
    `;
    list.insertAdjacentHTML("beforeend", itemHtml);
  });
}

function clearHistory() {
  sessionStorage.removeItem("leaf_history");
  renderHistory([]);
}

