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
from lib.auth import register

st.set_page_config(
    page_title="Register - Sleep Disorder Analysis",
    page_icon="📝",
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

st.title("📝 Create Account")
st.write("Register a new account to get started with sleep disorder analysis.")

st.info("💡 **Development Mode**: Data is stored locally. For production, configure Supabase credentials.")

if not st.session_state.get("service_status", True):
    st.error("⛔ Service is currently closed. Please try again later.")
else:
    with st.form("register_form", clear_on_submit=True):
        email = st.text_input(
            "Email Address",
            placeholder="your.email@example.com",
            help="Use a valid email address"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="At least 6 characters",
            help="Must be at least 6 characters long"
        )
        
        password_confirm = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter your password",
            help="Passwords must match"
        )
        
        submit = st.form_submit_button("✅ Create Account", use_container_width=True)
        
        if submit:
            # Validation
            if not email or not password:
                st.error("❌ Email and password are required.")
            elif password != password_confirm:
                st.error("❌ Passwords do not match.")
            elif len(password) < 6:
                st.error("❌ Password must be at least 6 characters.")
            elif "@" not in email:
                st.error("❌ Please enter a valid email address.")
            else:
                try:
                    ok = register(email.strip().lower(), password)
                    if ok:
                        st.success("✅ Account created successfully!")
                        st.info("🔐 Please go to Login page to access your account.")
                    else:
                        st.error("❌ Email already registered. Please login or use a different email.")
                except Exception as e:
                    st.error(f"❌ Registration error: {str(e)}")

st.divider()

# Links
col1, col2 = st.columns(2)
with col1:
    if st.button("🔐 Already have an account? Login", use_container_width=True):
        st.switch_page("pages/Login.py")

with col2:
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("streamlit_app.py")
