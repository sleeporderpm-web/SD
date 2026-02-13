import streamlit as st
import pandas as pd
from lib.ml import classify
from lib.db import save_analysis, list_user_analyses
from streamlit.components.v1 import html

st.set_page_config(page_title="Sleep Analysis Dashboard", page_icon="📊", layout="centered")

user = st.session_state.get("user_email")
if not user:
    st.error("Please login from Home page.")
    st.page_link("streamlit_app.py", label="Go to Home", icon="🏠")
    st.stop()

css = """
body { background:#050a14; color:white; font-family:Arial; }
.container { max-width:1100px; margin:40px auto; }
.header { display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #333; padding-bottom:20px; }
.logout { color:#ff4d4d; text-decoration:none; border:1px solid #ff4d4d; padding:6px 16px; border-radius:5px; font-weight:bold; }
.grid { display:grid; grid-template-columns:1.2fr 1fr; gap:30px; margin-top:30px; }
.card { background:#0b1120; padding:25px; border-radius:10px; border:1px solid #333; }
.card h3 { color:#f39c12; margin-bottom:20px; }
"""
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
st.markdown('<div class="container"><div class="header"><h2>Sleep Analysis Dashboard</h2></div></div>', unsafe_allow_html=True)

with st.form("sleep_form"):
    phone = st.text_input("Phone number")
    age = st.number_input("Age", min_value=0, max_value=120, value=30)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    occupation = st.text_input("Occupation")
    stress = st.slider("Stress level", 0, 10, 5)
    blood_pressure = st.number_input("Blood pressure (systolic mmHg)", min_value=70, max_value=220, value=120)
    heart_rate = st.number_input("Heart rate (bpm)", min_value=40, max_value=200, value=72)
    sleep_duration = st.number_input("Sleep duration (hours)", min_value=0.0, max_value=24.0, value=7.0, step=0.5)
    bmi_category = st.selectbox("BMI category", ["Underweight", "Normal", "Overweight", "Obese"])
    snoring_frequency = st.number_input("Snoring frequency (per week)", min_value=0, max_value=21, value=1)
    working_hours = st.number_input("Working hours (per day)", min_value=0, max_value=24, value=8)
    submit = st.form_submit_button("Generate Prediction")

if submit:
    inputs = {
        "phone": phone,
        "age": int(age),
        "gender": gender,
        "occupation": occupation,
        "stress": int(stress),
        "blood_pressure": float(blood_pressure),
        "heart_rate": int(heart_rate),
        "sleep_duration": float(sleep_duration),
        "bmi_category": bmi_category,
        "snoring_frequency": int(snoring_frequency),
        "working_hours": int(working_hours),
    }
    diagnosis, severity = classify(inputs)
    st.metric("Diagnosis", diagnosis)
    row = {
        "user_email": user,
        "phone": phone,
        "age": int(age),
        "gender": gender,
        "occupation": occupation,
        "stress": int(stress),
        "blood_pressure": float(blood_pressure),
        "heart_rate": int(heart_rate),
        "sleep_duration": float(sleep_duration),
        "bmi_category": bmi_category,
        "snoring_frequency": int(snoring_frequency),
        "working_hours": int(working_hours),
        "diagnosis": diagnosis,
        "severity": int(severity),
    }
    saved = save_analysis(row)
    st.success("Prediction saved.")
    st.session_state["last_saved_id"] = saved.get("id")

st.markdown('<div class="card"><h3>Analysis History</h3></div>', unsafe_allow_html=True)
rows = list_user_analyses(user, limit=30)
if rows:
    df = pd.DataFrame(rows)
    df = df[["created_at", "diagnosis", "phone", "severity", "id"]]
    st.dataframe(df, use_container_width=True)
    if "last_saved_id" in st.session_state and st.session_state["last_saved_id"]:
        st.page_link("pages/Report View.py", label="View last report", icon="🧾", args={"id": st.session_state["last_saved_id"]})
else:
    st.info("No past records.")
