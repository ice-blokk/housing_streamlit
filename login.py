from st_pages import hide_pages
from time import sleep
import streamlit as st

login, create, guest = st.tabs(["Login to existing account", "Create a new account", "Continue as guest"])

def log_in(user_email = "testemail", user_pw = "testpw"):
    st.session_state["authenticated"] = True
    st.session_state["user_email"] = user_email
    hide_pages([])
    st.success("Logged in!")
    sleep(0.5)
    st.switch_page("pages/app.py")


def log_out():
    st.session_state["authenticated"] = False
    st.success("Logged out!")
    sleep(0.5)

with login:
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", key="login_pw")
    if st.button("Login"):
        log_in(email, password)

with create:
    email = st.text_input("Email", key="create_email")
    password = st.text_input("Password", key="create_pw")
    if st.button("Create account"):
        log_in(email, password)

with guest:
    if st.button("Continue as guest"):
        log_in()



if not st.session_state.get("authenticated", False):
    hide_pages(["app", "profile"])