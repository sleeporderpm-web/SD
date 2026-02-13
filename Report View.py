import streamlit as st
from lib.db import get_analysis_by_id
from lib.pdf import build_report

st.set_page_config(page_title="Report View", page_icon="🧾", layout="centered")

analysis_id = None
params = st.experimental_get_query_params()
if "id" in params:
    analysis_id = params["id"][0]
if not analysis_id:
    analysis_id = st.session_state.get("report_id")

if not analysis_id:
    st.error("No report ID provided.")
    st.stop()

row = get_analysis_by_id(analysis_id)
if not row:
    st.error("Report not found.")
    st.stop()

st.title("Medical Report")
st.write(f"Report ID: {analysis_id}")
for k, v in row.items():
    st.write(f"{k}: {v}")

pdf_bytes = build_report(row)
st.download_button("Print / Download Medical Report (PDF)", data=pdf_bytes, file_name=f"report_{analysis_id}.pdf", mime="application/pdf")
