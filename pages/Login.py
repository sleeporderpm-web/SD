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
from lib.auth import verify

st.set_page_config(
    page_title="Login - Sleep Disorder Analysis",
    page_icon="🔐",
    layout="centered"
)

# Sidebar navigation
with st.sidebar:
    st.write("## 🏥 Service Status")
    service_open = st.checkbox("🟢 Service Open", value=True, key="service_status")
    
    if not service_open:
        st.warning("⛔ Service Currently Closed")
    else:
        st.success("✅ Service Online")
    
    st.divider()
    
    if st.button("⬅️ Back to Home", use_container_width=True):
        st.switch_page("streamlit_app.py")

st.title("🔐 Login")
st.write("Access your account to view and manage sleep analyses.")

if not st.session_state.get("service_status", True):
    st.error("⛔ Service is currently closed. Please try again later.")
else:
    with st.form("login_form", clear_on_submit=True):
        email = st.text_input(
            "Email Address",
            placeholder="your.email@example.com",
            help="Enter your registered email"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Your password",
            help="Enter your account password"
        )
        
        submit = st.form_submit_button("🚪 Login", use_container_width=True, type="primary")
        
        if submit:
            if not email or not password:
                st.error("❌ Email and password are required.")
            else:
                try:
                    if verify(email.strip().lower(), password):
                        st.session_state["user_email"] = email.strip().lower()
                        st.success("✅ Logged in successfully!")
                        st.balloons()
                        st.switch_page("pages/Sleep Analysis Dashboard.py")
                    else:
                        st.error("❌ Invalid email or password.")
                except Exception as e:
                    st.error(f"❌ Login error: {str(e)}")

st.divider()

# Links
col1, col2 = st.columns(2)
with col1:
    if st.button("📝 Don't have an account? Register", use_container_width=True):
        st.switch_page("pages/Register.py")

with col2:
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("streamlit_app.py")
