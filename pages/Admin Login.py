import os
import streamlit as st

st.set_page_config(page_title="Admin Login", page_icon="🔐", layout="centered")

if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False

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
