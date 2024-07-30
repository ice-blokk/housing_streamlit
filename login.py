from st_pages import hide_pages
from time import sleep
import streamlit as st

login, create, guest = st.tabs(["Login to existing account", "Create a new account", "Continue as guest"])

import requests

def get_external_ip():
    response = requests.get("https://api64.ipify.org?format=json")
    if response.status_code == 200:
        data = response.json()
        return data.get("ip")
    else:
        return "Unknown"

external_ip = get_external_ip()
st.write("External IP:", external_ip)

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
    email = st.text_input("Email :red[(required)]", key="create_email")
    password = st.text_input("Password :red[(required)]", key="create_pw")

    voucher_amount = st.text_input("Enter voucher amount ($) :red[(required)]")
    type_of_voucher = st.radio("Select voucher type :red[(required)]", ['Section 8 NYCHA', 'Section 8 EHV', 'Section 8 HPD', 'CityFHEPS', 'FHEPS'])

    # if type_of_voucher == "Other":
    #     type_of_voucher = st.text_input("Enter other voucher type")

    number_beds = st.number_input("Select number of beds the voucher is for (zero beds denotes studio) :red[(required)]", value=0, min_value=0, max_value=10, step=1)

    preferred_borough = st.multiselect("Select your preferred borough :red[(required)]",
        ['Manhattan', 'Brooklyn', 'Queens', 'Bronx'])

    if st.button("Create account"):
        log_in(email, password)

with guest:
    if st.button("Continue as guest"):
        log_in()



if not st.session_state.get("authenticated", False):
    hide_pages(["app", "profile"])