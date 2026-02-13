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
import pandas as pd
from lib.ml import classify
from lib.db import save_analysis, list_user_analyses

st.set_page_config(page_title="Sleep Analysis Dashboard", page_icon="📊", layout="wide")

# Sidebar - Service Status
with st.sidebar:
    st.write("## 🏥 Service Status")
    service_open = st.checkbox("🟢 Service Open", value=True, key="service_status")
    
    if not service_open:
        st.warning("⛔ Service Currently Closed for Maintenance")
    else:
        st.success("✅ Service Online")
    
    st.divider()
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("streamlit_app.py")

# Check if user is logged in
user = st.session_state.get("user_email")
if not user:
    st.error("❌ Please login from Home page.")
    st.page_link("streamlit_app.py", label="🏠 Go to Home", icon="🏠")
    st.stop()

if not st.session_state.get("service_status", True):
    st.error("⛔ Service is temporarily closed. Please try again later.")
    st.stop()

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("📊 Sleep Analysis Dashboard")
    st.write(f"Welcome, **{user}**")
with col2:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state["user_email"] = None
        st.session_state["is_admin"] = False
        st.switch_page("streamlit_app.py")

st.divider()

# Tabs for form and history
tab1, tab2 = st.tabs(["📝 New Analysis", "📋 History"])

with tab1:
    st.subheader("Enter Your Sleep Analysis Details")
    
    with st.form("sleep_form"):
        # Patient Information
        col1, col2 = st.columns(2)
        with col1:
            phone = st.text_input("📱 Phone Number", placeholder="10-digit phone number")
            age = st.number_input("👤 Age", min_value=1, max_value=120, value=30)
            gender = st.selectbox("⚥ Gender", ["Male", "Female", "Other"])
            occupation = st.text_input("💼 Occupation", placeholder="e.g., Engineer, Doctor")
        
        with col2:
            stress = st.slider("😰 Stress Level", 0, 10, 5, help="1=Low, 10=High")
            blood_pressure = st.number_input("❤️ Blood Pressure (Systolic mmHg)", min_value=70, max_value=220, value=120)
            heart_rate = st.number_input("💓 Heart Rate (bpm)", min_value=40, max_value=200, value=72)
            sleep_duration = st.number_input("😴 Sleep Duration (hours)", min_value=0.0, max_value=24.0, value=7.0, step=0.5)
        
        # Lifestyle factors
        col3, col4 = st.columns(2)
        with col3:
            bmi_category = st.selectbox("⚖️ BMI Category", ["Underweight", "Normal", "Overweight", "Obese"])
            snoring_frequency = st.number_input("🔊 Snoring Frequency (per week)", min_value=0, max_value=21, value=1)
        
        with col4:
            working_hours = st.number_input("⏰ Working Hours (per day)", min_value=0, max_value=24, value=8)
        
        submit = st.form_submit_button("🔍 Generate Prediction", use_container_width=True)

    if submit:
        # Validate required fields
        if not phone:
            st.error("❌ Phone number is required")
        else:
            # Prepare data for classification
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
            
            # Get ML prediction
            diagnosis, severity = classify(inputs)
            
            # Prepare record for database
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
            
            # Save to database
            try:
                saved = save_analysis(row)
                st.success("✅ Prediction saved successfully!")
                
                # Display diagnosis result
                st.subheader("📋 Your Diagnosis Result")
                if severity == 3:
                    st.error(f"🔴 {diagnosis}")
                elif severity == 2:
                    st.warning(f"🟡 {diagnosis}")
                else:
                    st.success(f"🟢 {diagnosis}")
                
                # Store ID for report viewing
                st.session_state["last_saved_id"] = saved.get("id")
                
                # Provide report viewing option
                if st.session_state.get("last_saved_id"):
                    if st.button("📄 View Full Report", use_container_width=True):
                        st.switch_page("pages/Report View.py")
            except Exception as e:
                st.error(f"❌ Error saving prediction: {str(e)}")

with tab2:
    st.subheader("📋 Your Analysis History")
    
    rows = list_user_analyses(user, limit=50)
    if rows:
        df = pd.DataFrame(rows)
        df = df[["created_at", "age", "diagnosis", "phone", "severity", "id"]].sort_values("created_at", ascending=False)
        
        # Display dataframe with styling
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
        
        # Option to view any report
        st.subheader("View Any Report")
        report_id = st.text_input("Enter Report ID:", placeholder="Select from table above")
        if st.button("📄 View Report", use_container_width=True):
            if report_id:
                st.session_state["report_id"] = report_id
                st.switch_page("pages/Report View.py")
            else:
                st.warning("Please enter a Report ID")
    else:
        st.info("📭 No analysis records yet. Create your first analysis above!")

st.divider()
st.caption("💡 This analysis uses an Ensemble Learning approach combining ANN, Random Forest, and SVM for accurate predictions.")
