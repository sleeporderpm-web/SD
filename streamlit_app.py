import streamlit as st
from lib.auth import register, verify

st.set_page_config(
    page_title="Sleep Disorder Analysis MVP",
    page_icon="😴",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if "user_email" not in st.session_state:
    st.session_state["user_email"] = None
if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False

# Try to load landing page HTML
try:
    with open("assets/landing.html", "r", encoding="utf-8") as f:
        landing = f.read()
    from streamlit.components.v1 import html
    html(landing, height=1200, scrolling=True)
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

# Authentication Tabs
st.write("## 🔓 Access Your Account")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.subheader("📝 Register")
    with st.form("register_form", clear_on_submit=True):
        r_email = st.text_input("Email", key="reg_email", placeholder="your.email@example.com")
        r_password = st.text_input("Password", type="password", key="reg_password", placeholder="Secure password")
        r_password_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm", placeholder="Confirm password")
        r_submit = st.form_submit_button("✅ Create Account", use_container_width=True)
        
        if r_submit:
            if not r_email or not r_password:
                st.error("❌ Email and password are required.")
            elif r_password != r_password_confirm:
                st.error("❌ Passwords do not match.")
            elif len(r_password) < 6:
                st.error("❌ Password must be at least 6 characters.")
            else:
                try:
                    ok = register(r_email.strip().lower(), r_password)
                    if ok:
                        st.success("✅ Account created! Please login.")
                    else:
                        st.error("❌ User already exists.")
                except Exception as e:
                    st.error(f"❌ Registration error: {str(e)}")

with col2:
    st.subheader("🔐 Login")
    with st.form("login_form", clear_on_submit=True):
        l_email = st.text_input("Email", key="login_email", placeholder="your.email@example.com")
        l_password = st.text_input("Password", type="password", key="login_password", placeholder="Your password")
        l_submit = st.form_submit_button("🚪 Login", use_container_width=True)
        
        if l_submit:
            if not l_email or not l_password:
                st.error("❌ Email and password are required.")
            else:
                try:
                    if verify(l_email.strip().lower(), l_password):
                        st.session_state["user_email"] = l_email.strip().lower()
                        st.success("✅ Logged in successfully!")
                        st.switch_page("pages/Sleep Analysis Dashboard.py")
                    else:
                        st.error("❌ Invalid credentials.")
                except Exception as e:
                    st.error(f"❌ Login error: {str(e)}")

with col3:
    st.subheader("👨‍⚕️ Admin Access")
    st.write("Hospital administrators can access the action panel.")
    if st.button("🔐 Admin Login", use_container_width=True, type="primary"):
        st.switch_page("pages/Admin Login.py")

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
