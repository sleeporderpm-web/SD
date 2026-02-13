import streamlit as st
from streamlit.components.v1 import html
from lib.auth import register, verify

st.set_page_config(page_title="Sleep Disorder MVP", page_icon="😴", layout="centered")

if "user_email" not in st.session_state:
    st.session_state["user_email"] = None
if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False

try:
    with open("assets/landing.html", "r", encoding="utf-8") as f:
        landing = f.read()
    html(landing, height=800, scrolling=False)
except Exception:
    st.title("Sleep Disorder Analysis")
    st.write("Register or login to access the Sleep Analysis Dashboard.")

tab1, tab2 = st.tabs(["Register", "Login"])
with tab1:
    r_email = st.text_input("Email")
    r_password = st.text_input("Password", type="password")
    if st.button("Register"):
        if r_email and r_password:
            ok = register(r_email, r_password)
            if ok:
                st.success("Registered. Please login.")
            else:
                st.error("User already exists.")
        else:
            st.error("Provide email and password.")

with tab2:
    l_email = st.text_input("Email", key="login_email")
    l_password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        if l_email and l_password and verify(l_email, l_password):
            st.session_state["user_email"] = l_email.strip().lower()
            st.success("Logged in. Redirecting to dashboard...")
            st.switch_page("pages/Sleep Analysis Dashboard.py")
        else:
            st.error("Invalid credentials.")

st.divider()
st.write("Admin?")
if st.button("Go to Admin Login"):
    st.switch_page("pages/Admin Login.py")
