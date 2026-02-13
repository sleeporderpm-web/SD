import sys
from pathlib import Path

# Find and add repo root to path
current_path = Path(__file__).resolve()
while current_path != current_path.parent:
    if (current_path / "lib").exists() and (current_path / "streamlit_app.py").exists():
        sys.path.insert(0, str(current_path))
        break
    current_path = current_path.parent

import streamlit as st
from lib.db import get_analysis_by_id
from lib.pdf import build_report

st.set_page_config(page_title="Report View", page_icon="🧾", layout="centered")

# Sidebar - Service Status
with st.sidebar:
    st.write("## 🏥 Service Status")
    service_open = st.checkbox("🟢 Service Open", value=True, key="service_status")
    
    if not service_open:
        st.warning("⛔ Service Currently Closed")
    else:
        st.success("✅ Service Online")
    
    st.divider()
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("streamlit_app.py")

if not st.session_state.get("service_status", True):
    st.error("⛔ Service is temporarily closed. Please try again later.")
    st.stop()

# Get report ID from query params or session state
analysis_id = None
try:
    params = st.query_params
    if "id" in params:
        analysis_id = params["id"]
except:
    pass

if not analysis_id:
    analysis_id = st.session_state.get("report_id")

if not analysis_id:
    st.error("❌ No report ID provided.")
    if st.button("🏠 Go Back"):
        st.switch_page("streamlit_app.py")
    st.stop()

# Fetch the report
try:
    row = get_analysis_by_id(analysis_id)
except Exception as e:
    st.error(f"❌ Error fetching report: {str(e)}")
    if st.button("🏠 Go Back"):
        st.switch_page("streamlit_app.py")
    st.stop()

if not row:
    st.error("❌ Report not found.")
    if st.button("🏠 Go Back"):
        st.switch_page("streamlit_app.py")
    st.stop()

# Display report details
st.title("🧾 Medical Report")
st.write(f"**Report ID:** `{analysis_id}`")

st.divider()

# Patient Information Section
st.subheader("👤 Patient Information")
col1, col2 = st.columns(2)
with col1:
    st.write(f"**Email:** {row.get('user_email', 'N/A')}")
    st.write(f"**Phone:** {row.get('phone', 'N/A')}")
    st.write(f"**Age:** {row.get('age', 'N/A')}")
    st.write(f"**Gender:** {row.get('gender', 'N/A')}")
with col2:
    st.write(f"**Occupation:** {row.get('occupation', 'N/A')}")
    st.write(f"**BMI Category:** {row.get('bmi_category', 'N/A')}")
    st.write(f"**Analysis Date:** {row.get('created_at', 'N/A')}")

st.divider()

# Vital Signs Section
st.subheader("❤️ Vital Signs")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Blood Pressure", f"{row.get('blood_pressure', 'N/A')} mmHg")
with col2:
    st.metric("Heart Rate", f"{row.get('heart_rate', 'N/A')} bpm")
with col3:
    st.metric("Sleep Duration", f"{row.get('sleep_duration', 'N/A')} hrs")

col4, col5, col6 = st.columns(3)
with col4:
    st.metric("Stress Level", f"{row.get('stress', 'N/A')}/10")
with col5:
    st.metric("Snoring Frequency", f"{row.get('snoring_frequency', 'N/A')}/week")
with col6:
    st.metric("Working Hours", f"{row.get('working_hours', 'N/A')} hrs/day")

st.divider()

# Diagnosis Section
st.subheader("🔬 Diagnosis Result")
diagnosis = row.get("diagnosis", "Pending")
severity = int(row.get("severity", 1))

if severity == 3:
    st.error(f"🔴 **HIGH RISK**\n\n{diagnosis}")
elif severity == 2:
    st.warning(f"🟡 **MODERATE RISK**\n\n{diagnosis}")
else:
    st.success(f"🟢 **NORMAL / LOW RISK**\n\n{diagnosis}")

st.divider()

# ML Prediction Summary Section
st.subheader("📊 Machine Learning Analysis Summary")

severity_labels = {
    0: "🟢 GREEN - No Risk",
    1: "🟡 YELLOW - Low Risk / Needs Review",
    2: "🟠 ORANGE - Moderate Risk",
    3: "🔴 RED - High Risk / Urgent"
}

col1, col2 = st.columns([2, 1])
with col1:
    st.write(f"**Risk Level:** {severity_labels.get(severity, 'Unknown')}")
with col2:
    st.write(f"**Severity Score:** {severity}/3")

# Display ML classification details based on severity
if severity == 0:
    st.info(
        "**Normal Sleep Pattern Detected**\n\n"
        "- All vital signs within healthy ranges\n"
        "- No indicators of sleep-related disorders\n"
        "- Recommendation: Continue current sleep habits and regular monitoring"
    )
elif severity == 1:
    st.info(
        "**Mild Abnormalities Detected**\n\n"
        "- Some vital signs show minor deviations\n"
        "- Further monitoring recommended\n"
        "- Recommendation: Consider lifestyle adjustments for better sleep quality"
    )
elif severity == 2:
    st.warning(
        "**Moderate Sleep Disorder Risk Identified**\n\n"
        "- Multiple vital sign abnormalities detected\n"
        "- Sleep deprivation or irregular patterns observed\n"
        "- Recommendation: Medical consultation with sleep specialist recommended"
    )
elif severity == 3:
    st.error(
        "**High-Risk Sleep Disorder Detected**\n\n"
        "- Critical vital sign abnormalities present\n"
        "- Urgent medical intervention may be needed\n"
        "- Recommendation: Immediate healthcare professional consultation required"
    )

st.divider()

# Medical Disclaimer
st.info(
    "⚠️ **MEDICAL DISCLAIMER**\n\n"
    "This report is for informational purposes only and does not constitute medical advice. "
    "The analysis is based on machine learning models trained on sleep study data. "
    "Please consult a qualified healthcare professional for proper diagnosis and treatment."
)

st.divider()

# PDF Download Section
st.subheader("📥 Download Report")
try:
    pdf_bytes = build_report(row)
    st.download_button(
        label="📄 Download as PDF",
        data=pdf_bytes,
        file_name=f"sleep_report_{analysis_id}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
except Exception as e:
    st.error(f"❌ Error generating PDF: {str(e)}")

st.divider()

# Navigation
if st.button("🏠 Back to Home"):
    st.switch_page("streamlit_app.py")
