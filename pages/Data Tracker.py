import streamlit as st
import json
from pathlib import Path
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Data Tracker", page_icon="📊", layout="wide")

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

st.title("📊 Data Tracker & Management")
st.write("Track and manage all stored data: registrations, analyses, and reports")

st.divider()

# Data storage location info
col1, col2 = st.columns(2)

with col1:
    st.info("""
    ### 📁 Storage Location
    
    **Local Development:**
    - Path: `.data/` folder
    - Users: `.data/users.json`
    - Analyses: `.data/analyses.json`
    
    **Files auto-created** when you register users and submit analyses
    """)

with col2:
    st.warning("""
    ### 🔐 Data Format
    
    **Users File:**
    - Email addresses (hashed)
    - PBKDF2-SHA256 hashed passwords
    - Format: JSON
    
    **Analyses File:**
    - Sleep disorder predictions
    - Patient health metrics
    - Diagnosis results
    """)

st.divider()

# Tab 1: View All Users/Registrations
tab1, tab2, tab3, tab4 = st.tabs(["👥 Registrations", "📋 Analyses", "📄 Reports", "🗄️ Raw Data"])

with tab1:
    st.subheader("Registered Users")
    
    data_dir = Path(__file__).parent.parent / ".data"
    users_file = data_dir / "users.json"
    
    if users_file.exists():
        with open(users_file, "r") as f:
            users_data = json.load(f)
        
        users = users_data.get("users", {})
        
        if users:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Users", len(users))
            
            st.subheader("User List")
            user_list = []
            for email in users.keys():
                user_list.append({
                    "Email": email,
                    "Status": "✅ Active",
                    "Password Hash": users[email][:30] + "..."
                })
            
            df = pd.DataFrame(user_list)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No users registered yet. Go to Register page to create an account.")
    else:
        st.warning("No users data file found yet.")

with tab2:
    st.subheader("Sleep Disorder Analyses")
    
    analyses_file = data_dir / "analyses.json"
    
    if analyses_file.exists():
        with open(analyses_file, "r") as f:
            analyses_data = json.load(f)
        
        analyses = analyses_data.get("analyses", [])
        
        if analyses:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Analyses", len(analyses))
            with col2:
                diagnoses = [a.get("diagnosis") for a in analyses]
                normal_count = diagnoses.count("Normal")
                st.metric("Normal Cases", normal_count)
            with col3:
                risk_count = len([d for d in diagnoses if "Risk" in str(d)])
                st.metric("Risk Cases", risk_count)
            
            st.subheader("Analysis Details")
            
            # Create display dataframe
            display_data = []
            for analysis in analyses:
                display_data.append({
                    "Date": analysis.get("created_at", "N/A"),
                    "Patient Email": analysis.get("user_email", "N/A"),
                    "Phone": analysis.get("phone", "N/A"),
                    "Age": analysis.get("age", "N/A"),
                    "Sleep Duration (hrs)": analysis.get("sleep_duration", "N/A"),
                    "BP (mmHg)": analysis.get("blood_pressure", "N/A"),
                    "Heart Rate": analysis.get("heart_rate", "N/A"),
                    "Diagnosis": analysis.get("diagnosis", "N/A"),
                    "Severity": analysis.get("severity", "N/A"),
                    "Report ID": analysis.get("id", "N/A")[:8] + "..."
                })
            
            df = pd.DataFrame(display_data)
            st.dataframe(df, use_container_width=True)
            
            # Filter and search
            st.subheader("Filter & Search")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                search_email = st.text_input("Search by Email", placeholder="test@gmail.com")
            with col2:
                filter_diagnosis = st.selectbox("Filter by Diagnosis", 
                    ["All"] + list(set([a.get("diagnosis") for a in analyses])))
            with col3:
                filter_severity = st.selectbox("Filter by Severity", 
                    ["All", "0 - Normal", "1 - Low", "2 - Moderate", "3 - High"])
            
            # Apply filters
            filtered = analyses
            if search_email:
                filtered = [a for a in filtered if search_email.lower() in a.get("user_email", "").lower()]
            if filter_diagnosis != "All":
                filtered = [a for a in filtered if a.get("diagnosis") == filter_diagnosis]
            if filter_severity != "All":
                severity_map = {"0 - Normal": 0, "1 - Low": 1, "2 - Moderate": 2, "3 - High": 3}
                severity_val = severity_map.get(filter_severity)
                filtered = [a for a in filtered if a.get("severity") == severity_val]
            
            if filtered:
                st.success(f"Found {len(filtered)} matching analyses")
                filtered_df = pd.DataFrame(filtered)
                st.dataframe(filtered_df, use_container_width=True)
        else:
            st.info("No analyses recorded yet. Go to Sleep Analysis Dashboard to submit data.")
    else:
        st.warning("No analyses data file found yet.")

with tab3:
    st.subheader("Generated Reports")
    
    if analyses_file.exists():
        with open(analyses_file, "r") as f:
            analyses_data = json.load(f)
        
        analyses = analyses_data.get("analyses", [])
        
        if analyses:
            st.info("Each analysis automatically generates a reportable record with the following data:")
            
            report_list = []
            for i, analysis in enumerate(analyses, 1):
                report_list.append({
                    "Report #": i,
                    "Report ID": analysis.get("id"),
                    "Patient": analysis.get("user_email"),
                    "Date": analysis.get("created_at"),
                    "Diagnosis": analysis.get("diagnosis"),
                    "Severity": analysis.get("severity"),
                    "Status": "✅ Ready for Download"
                })
            
            df = pd.DataFrame(report_list)
            st.dataframe(df, use_container_width=True)
            
            st.subheader("Download Report")
            selected_idx = st.selectbox("Select a report to download", 
                range(len(analyses)), 
                format_func=lambda i: f"{i+1}. {analyses[i].get('user_email')} - {analyses[i].get('diagnosis')}")
            
            if selected_idx is not None:
                report = analyses[selected_idx]
                st.json(report, expanded=False)
                st.info(f"Report ID: {report.get('id')}")
                st.info("To download as PDF: Go to Sleep Analysis Dashboard → View Report")
        else:
            st.info("No reports yet. Submit analyses first.")

with tab4:
    st.subheader("Raw Data View")
    
    st.write("**View raw JSON data:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📖 Show Users (JSON)"):
            if users_file.exists():
                with open(users_file, "r") as f:
                    users_data = json.load(f)
                st.json(users_data)
            else:
                st.warning("No users file found")
    
    with col2:
        if st.button("📖 Show Analyses (JSON)"):
            if analyses_file.exists():
                with open(analyses_file, "r") as f:
                    analyses_data = json.load(f)
                st.json(analyses_data)
            else:
                st.warning("No analyses file found")

st.divider()

# Admin section
st.subheader("🛠️ Admin Actions")

col1, col2 = st.columns(2)

with col1:
    if st.button("🗑️ Clear All Test Data", help="Delete all local data files"):
        if st.session_state.get("confirm_delete", False):
            try:
                if users_file.exists():
                    users_file.unlink()
                if analyses_file.exists():
                    analyses_file.unlink()
                st.success("✅ All data cleared!")
                st.session_state["confirm_delete"] = False
            except Exception as e:
                st.error(f"Error deleting files: {e}")
        else:
            st.warning("Click again to confirm deletion")
            st.session_state["confirm_delete"] = True

with col2:
    if st.button("📥 Export All Data as JSON"):
        if users_file.exists() or analyses_file.exists():
            export_data = {}
            if users_file.exists():
                with open(users_file, "r") as f:
                    export_data["users"] = json.load(f)
            if analyses_file.exists():
                with open(analyses_file, "r") as f:
                    export_data["analyses"] = json.load(f)
            
            st.download_button(
                label="Download Data (JSON)",
                data=json.dumps(export_data, indent=2),
                file_name=f"sd_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        else:
            st.warning("No data to export")

st.divider()
st.caption("💾 Data is stored locally in `.data/` folder for development. For production, configure Supabase.")
