import os
import streamlit as st

st.set_page_config(page_title="Admin Login", page_icon="🔐", layout="centered")

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

if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False

if not st.session_state.get("service_status", True):
    st.error("⛔ Service is temporarily closed. Please try again later.")
    st.stop()

st.title("🔐 Admin Login")
st.write("Enter the admin password to access the Hospital Action Panel.")

pwd = st.text_input("Admin Password", type="password", placeholder="Enter admin password")

admin_pwd = None
try:
    admin_pwd = st.secrets.get("ADMIN_PASSWORD")
except Exception:
    pass
admin_pwd = admin_pwd or os.environ.get("ADMIN_PASSWORD") or "admin123"

if st.button("Login as Admin", use_container_width=True):
    if pwd == admin_pwd:
        st.session_state["is_admin"] = True
        st.success("✅ Authenticated. Redirecting to Admin Portal...")
        st.switch_page("pages/Admin Portal.py")
    else:
        st.error("❌ Invalid admin password.")
