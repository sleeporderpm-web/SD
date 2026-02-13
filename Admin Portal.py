import streamlit as st
import pandas as pd
from lib.db import list_all_analyses

st.set_page_config(page_title="Admin Portal", page_icon="🛠", layout="wide")

if not st.session_state.get("is_admin"):
    st.error("Unauthorized")
    st.stop()

st.title("Hospital Action Panel")
rows = list_all_analyses(limit=200)
if not rows:
    st.info("No patient analyses.")
    st.stop()

df = pd.DataFrame(rows)
df["URGENT"] = df["severity"].apply(lambda s: "URGENT" if int(s) >= 3 else "")
st.dataframe(df[["created_at", "user_email", "phone", "diagnosis", "severity", "URGENT", "id"]], use_container_width=True)

st.subheader("Quick Actions")
col1, col2 = st.columns(2)
with col1:
    selected_id = st.text_input("Report ID")
    if st.button("VIEW report"):
        if selected_id:
            st.switch_page("pages/Report View.py")
            st.session_state["report_id"] = selected_id
with col2:
    phone = st.text_input("Phone to call")
    if st.button("CALL patient"):
        if phone:
            st.write(f"Call: {phone}")
