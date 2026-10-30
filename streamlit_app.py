"""
potatoGuardProject — Streamlit Interactive Web Application
Potato Leaf Disease Detection and Classification Using Machine Learning.
"""

import os
import io
import streamlit as st
from PIL import Image
from ml.classifier import predict_leaf_disease, load_image
from ml.disease_info import DISEASE_CLASSES, DISEASE_DETAILS

st.set_page_config(
    page_title="potatoGuardProject — Potato Leaf Disease Detection",
    page_icon="🥔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #064e3b 0%, #047857 50%, #0f766e 100%);
        padding: 24px 32px;
        border-radius: 16px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(6, 78, 59, 0.3);
    }
    .main-header h1 {
        color: white !important;
        font-weight: 800;
        margin: 0;
        font-size: 2.2rem;
    }
    .metric-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }
    .stProgress > div > div > div > div {
        background-color: #059669;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <div style="font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: #a7f3d0; margin-bottom: 4px;">
        Plant Pathology Computer Vision &bull; Precision Agriculture
    </div>
    <h1>🥔 potatoGuardProject — Leaf Disease Classifier</h1>
    <p style="margin-top: 8px; margin-bottom: 0; color: #ecfdf5; font-size: 15px;">
        Instant Machine Learning detection for <strong>Early Blight</strong>, <strong>Late Blight</strong>, and <strong>Healthy</strong> potato foliage.
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.header("🔬 Input Source")
input_option = st.sidebar.radio(
    "Choose input method:",
    ("1-Click Quick Samples", "Upload Image File", "Use Live Camera")
)

sample_map = {
    "Early Blight (Alternaria solani)": "static/samples/early_blight_sample.jpg",
    "Late Blight (Phytophthora infestans)": "static/samples/late_blight_sample.jpg",
    "Healthy Potato Leaf": "static/samples/healthy_sample.jpg"
}

leaf_image = None

if input_option == "1-Click Quick Samples":
    sample_choice = st.sidebar.selectbox("Select botanical sample:", list(sample_map.keys()))
    sample_path = sample_map[sample_choice]
    if os.path.exists(sample_path):
        leaf_image = Image.open(sample_path)
elif input_option == "Upload Image File":
    uploaded_file = st.sidebar.file_uploader("Upload leaf photo (JPG, PNG, WEBP)", type=["jpg", "jpeg", "png", "webp"])
    if uploaded_file is not None:
        leaf_image = Image.open(uploaded_file)
elif input_option == "Use Live Camera":
    camera_img = st.sidebar.camera_input("Take photo of potato leaf")
    if camera_img is not None:
        leaf_image = Image.open(camera_img)

st.sidebar.markdown("---")
st.sidebar.info("""
**Presented by:**
- **Sarthak Patidar** (BTET24O1116)
- **Sarvesh Patidar** (BTET24O1117)

**Classes Supported:**
- 🍂 **Potato Early Blight** (*Alternaria solani*)
- 🥀 **Potato Late Blight** (*Phytophthora infestans*)
- 🌿 **Healthy Foliage** (*Solanum tuberosum*)
""")

# Main Area
if leaf_image is not None:
    col1, col2 = st.columns([5, 7], gap="large")

    with col1:
        st.subheader("📷 Selected Leaf Image")
        st.image(leaf_image, use_container_width=True)
        analyze_trigger = st.button("🔍 Run Machine Learning Diagnosis", type="primary", use_container_width=True)

    with col2:
        if analyze_trigger or input_option == "1-Click Quick Samples":
            with st.spinner("Analyzing leaf color, texture, and necrotic morphology..."):
                result = predict_leaf_disease(leaf_image)

            # Diagnosis Display
            st.subheader("🩺 Diagnostic Findings")
            
            # Risk Banner
            risk_color = result["risk_color"]
            st.markdown(f"""
            <div style="background-color: {risk_color}15; border-left: 6px solid {risk_color}; padding: 16px; border-radius: 8px; margin-bottom: 16px;">
                <span style="font-size: 12px; font-weight: 800; text-transform: uppercase; color: {risk_color};">{result['risk_level']} RISK</span>
                <h2 style="margin: 4px 0; color: #1e293b; font-size: 24px; font-weight: 800;">{result['display_name']}</h2>
                <span style="font-style: italic; color: #64748b; font-size: 14px;">{result['scientific_name']} &bull; {result['pathogen_type']}</span>
            </div>
            """, unsafe_allow_html=True)

            # Metrics
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric(label="Model Confidence", value=f"{result['confidence_pct']}%")
            with m2:
                st.metric(label="Severity Grade", value=result['severity']['grade'])
            with m3:
                st.metric(label="Affected Leaf Area", value=f"{result['severity']['affected_pct']}%")

            # Probability Breakdown
            st.markdown("#### Multi-Class Softmax Probabilities")
            for prob in result['probabilities']:
                st.write(f"**{prob['name']}**: {prob['prob']}%")
                st.progress(prob['prob'] / 100.0)

            # Visual Inspection Studio
            st.markdown("---")
            st.subheader("🔬 Visual Inspection & AI Saliency Heatmap")
            vcol1, vcol2 = st.columns(2)
            with vcol1:
                st.caption("AI Saliency Anomaly Heatmap")
                st.image(result['visualizations']['heatmap'], use_container_width=True)
            with vcol2:
                st.caption("Lesion Boundary Segmentation Mask")
                st.image(result['visualizations']['overlay'], use_container_width=True)

            # Treatment Tabs
            st.markdown("---")
            st.subheader("📋 Agronomic Action & Treatment Plan")
            tab_sym, tab_chem, tab_org, tab_prev = st.tabs([
                "🔍 Symptoms", "💊 Chemical Fungicides", "🌿 Organic Controls", "🛡️ Prevention & GAP"
            ])

            with tab_sym:
                for s in result['symptoms']:
                    st.markdown(f"- {s}")

            with tab_chem:
                for chem in result['chemical_treatments']:
                    st.markdown(f"**{chem['name']}** (*{chem['type']}*)")
                    st.caption(f"Dosage: {chem['dosage']} | Schedule: {chem['application']}")

            with tab_org:
                for org in result['organic_controls']:
                    st.markdown(f"- {org}")

            with tab_prev:
                for p in result['preventive_practices']:
                    st.markdown(f"- {p}")

            st.warning(f"**Environmental Weather Advisory:** {result['environmental_triggers']}")
else:
    st.info("👈 Please select a quick sample leaf or upload an image from the sidebar to begin.")

