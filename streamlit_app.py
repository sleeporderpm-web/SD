import sys
from pathlib import Path

# Add repo root to sys.path (for imports to work)
_file = Path(__file__).resolve()
_repo_root = _file.parent  # We're already at repo root
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

import streamlit as st

st.set_page_config(
    page_title="Sleep Disorder Analysis MVP",
    page_icon="😴",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "user_email" not in st.session_state:
    st.session_state["user_email"] = None
if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False

# Sidebar - Service Status
with st.sidebar:
    st.write("## 🏥 Service Status")
    
    col1, col2 = st.columns(2)
    with col1:
        service_open = st.checkbox("🟢 Service Open", value=True, key="service_status")
    
    if not service_open:
        st.warning("⛔ Service Currently Closed for Maintenance")
    else:
        st.success("✅ Service Online")
    
    st.divider()
    
    if st.session_state.get("user_email"):
        st.write(f"👤 **Logged in as:**\n{st.session_state['user_email']}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 Dashboard", use_container_width=True):
                st.switch_page("pages/Sleep Analysis Dashboard.py")
        with col2:
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state["user_email"] = None
                st.session_state["is_admin"] = False
                st.rerun()
    else:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 Register", use_container_width=True):
                st.switch_page("pages/Register.py")
        with col2:
            if st.button("🔐 Login", use_container_width=True):
                st.switch_page("pages/Login.py")
        
        if st.button("👨‍⚕️ Admin Login", use_container_width=True, type="primary"):
            st.switch_page("pages/Admin Login.py")
    
    st.divider()
    st.write("### 📊 Data Management")
    if st.button("📊 View Data Tracker", use_container_width=True):
        st.switch_page("pages/Data Tracker.py")

# Landing Page
try:
    with open("assets/landing.html", "r", encoding="utf-8") as f:
        landing = f.read()
    from streamlit.components.v1 import html
    html(landing, height=600, scrolling=True)
except FileNotFoundError:
    # Fallback content if HTML file not found
    st.title("😴 Sleep Disorder Classification")
    st.header("An Ensemble Learning Approach for Improved Sleep Disorder Prediction")
    st.write("""
    Our platform utilizes a **Multi-Model Ensemble** technique combining:
    - **Artificial Neural Networks (ANN)** - Pattern recognition for sleep cycle irregularities
    - **Random Forest** - Handling high-dimensional physiological data
    - **Support Vector Machines (SVM)** - Accurate classification of sleep disorders
    """)

st.divider()

# Information sections
st.write("## 📚 How It Works")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    ### 👥 Step 1: Register
    Create your account with email and password.
    """)

with col2:
    st.info("""
    ### 📊 Step 2: Analyze
    Enter your sleep metrics and health data.
    """)

with col3:
    st.info("""
    ### 🔬 Step 3: Predict
    Get ML-powered sleep disorder classification.
    """)

st.write("---")

# Features section
st.write("## ✨ Features")
col1, col2 = st.columns(2)

with col1:
    st.success("✅ Secure user authentication")
    st.success("✅ Real-time sleep disorder prediction")
    st.success("✅ Analysis history tracking")

with col2:
    st.success("✅ Detailed medical reports")
    st.success("✅ PDF download capability")
    st.success("✅ Hospital admin dashboard")

st.write("---")
st.caption(
    "💡 This MVP uses an Ensemble Learning approach for improved sleep disorder prediction. "
    "Results are for informational purposes only. Always consult healthcare professionals."
)
