import sys
import os

# Fix import path for lib module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
from lib.db import list_all_analyses

st.set_page_config(page_title="Admin Portal", page_icon="🛠", layout="wide")

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
        st.session_state["is_admin"] = False
        st.switch_page("streamlit_app.py")

if not st.session_state.get("is_admin"):
    st.error("❌ Unauthorized Access")
    st.stop()

if not st.session_state.get("service_status", True):
    st.error("⛔ Service is temporarily closed. Please try again later.")
    st.stop()

st.title("🛠 Hospital Action Panel")
st.write("View all patient analyses and take quick actions.")

# Logout button
if st.button("Logout", key="admin_logout"):
    st.session_state["is_admin"] = False
    st.session_state["user_email"] = None
    st.switch_page("streamlit_app.py")

st.divider()

# Fetch all analyses
rows = list_all_analyses(limit=200)
if not rows:
    st.info("📋 No patient analyses yet.")
    st.stop()

# Create DataFrame with analysis data
df = pd.DataFrame(rows)
df["URGENCY"] = df["severity"].apply(
    lambda s: "🔴 URGENT" if int(s) >= 3 else "🟡 MODERATE" if int(s) == 2 else "🟢 NORMAL"
)

# Display main table
st.subheader("All Sleep Disorder Reports")
display_cols = ["created_at", "user_email", "phone", "age", "diagnosis", "severity", "URGENCY", "id"]
st.dataframe(
    df[display_cols],
    use_container_width=True,
    hide_index=True
)

st.divider()

# Quick Actions
st.subheader("⚡ Quick Actions")
col1, col2 = st.columns(2)

with col1:
    st.write("**View Detailed Report**")
    selected_id = st.text_input("Enter Report ID:", placeholder="UUID or ID")
    if st.button("📄 VIEW report", use_container_width=True):
        if selected_id:
            st.session_state["report_id"] = selected_id
            st.switch_page("pages/Report View.py")
        else:
            st.warning("Please enter a Report ID")

with col2:
    st.write("**Contact Patient**")
    phone = st.text_input("Phone Number:", placeholder="Patient phone")
    if st.button("☎️ CALL patient", use_container_width=True):
        if phone:
            st.success(f"✅ Dial: {phone}")
        else:
            st.warning("Please enter a phone number")

st.divider()
st.caption("📊 Hospital Action Panel - Use filters above to search for specific patients.")
