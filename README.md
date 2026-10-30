# 🥔 potatoGuardProject — Potato Leaf Disease Detection and Classification

> **Presented by:**
> - **Sarthak Patidar** (BTET24O1116)
> - **Sarvesh Patidar** (BTET24O1117)

An intelligent, full-stack Machine Learning web application for automatic detection and classification of Potato Leaf Diseases from digital images.

Designed for farmers, agronomists, agricultural researchers, and plant pathologists to identify foliar diseases instantly, assess damage severity, and apply targeted agronomic remedies.

---

## 🌟 Key Features

- **Multi-Class Pathology Detection**:
  - 🍂 **Early Blight** (*Alternaria solani*) — Concentric target rings, chlorosis halos.
  - 🥀 **Late Blight** (*Phytophthora infestans*) — Water-soaked lesions, purplish dark necrosis.
  - 🌿 **Healthy Foliage** (*Solanum tuberosum*) — Vibrant chlorophyll distribution.
- **Computer Vision Feature Engine**:
  - Excess Green Index ($ExG = 2G - R - B$) and Normalized Difference Vegetation indices.
  - Gray-Level Co-occurrence Matrix (GLCM) spatial contrast, dissimilarity, energy, and homogeneity.
  - Concentric ring circularity & target spot detection algorithms.
  - Water-soaked lesion diffusion analysis.
- **Visual Inspection Studio**:
  - **AI Saliency Anomaly Heatmap**: Grad-CAM style thermal map highlighting infection hotspots.
  - **Lesion Segmentation Boundary Mask**: Segments necrotic spots from healthy green tissue.
- **Severity & Impact Grading**:
  - Automatically calculates affected leaf area percentage.
  - Classifies severity: Mild (Stage 1), Moderate (Stage 2), Severe (Stage 3), or Optimal Health.
- **Agronomic Action Plan**:
  - Approved chemical fungicides, precise dosages, and spray intervals.
  - Biological & organic remedies (*Bacillus subtilis*, *Trichoderma*, Copper formulations).
  - Good Agricultural Practices (GAP) and weather trigger advisories.
- **Multiple Input Channels**:
  - Drag-and-drop image upload (JPG, PNG, WEBP).
  - Live webcam capture directly inside the browser.
  - 1-Click test samples for instant demonstration.
- **Export & History**:
  - Session scan history log.
  - One-click printable diagnostic certificate / agronomic report.
- **Dual Web Interfaces**:
  - Modern Single-Page Application (HTML5 + Tailwind CSS + FastAPI).
  - Streamlit dashboard (`streamlit_app.py`).

---

## 🚀 Quick Start

### 1. Requirements

Ensure Python 3.10+ is installed:
```bash
pip install -r requirements.txt
```

### 2. Launch FastAPI Web Application (Recommended)

```bash
# Using the launch script:
./run.sh

# Or directly with uvicorn:
python3 -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Open your browser at: **`http://localhost:8000`**

### 3. Launch Streamlit Application (Alternative)

```bash
streamlit run streamlit_app.py
```

Open your browser at: **`http://localhost:8501`**

---

## 📡 REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the web dashboard |
| `POST` | `/api/predict` | Accepts image file, base64, or `sample_id` and returns complete diagnosis JSON |
| `GET` | `/api/samples` | Lists available 1-click test sample images |
| `GET` | `/api/disease-info` | Returns complete clinical encyclopedia |
| `GET` | `/api/health` | Health check endpoint |

### Example API Request (cURL):
```bash
curl -X POST http://localhost:8000/api/predict \
  -F "file=@static/samples/early_blight_sample.jpg"
```

---

## 📁 Project Structure

```
PDDUML/
├── app.py                 # FastAPI server (APIs & Web UI)
├── streamlit_app.py       # Streamlit alternative interface
├── ml/
│   ├── __init__.py
│   ├── classifier.py      # Vision pipeline, GLCM, logits, heatmap generator
│   ├── disease_info.py    # Pathology database, symptoms, and treatments
│   └── samples_gen.py     # Generator for realistic botanical sample leaves
├── static/
│   ├── css/
│   │   └── style.css      # Custom styling, print formats, animations
│   ├── js/
│   │   └── main.js        # Dynamic frontend logic & API calls
│   └── samples/           # Botanical sample leaf images
├── templates/
│   └── index.html         # Modern responsive dashboard
├── requirements.txt       # Dependencies
├── run.sh                 # Quick launch script
└── README.md              # Documentation
```

