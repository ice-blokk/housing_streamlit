import streamlit as st
import pandas as pd
from util import column_names
from pymongo.mongo_client import MongoClient
from time import sleep

# hide sidebar
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

from mongodb import get_saved_listings, remove_listing, in_listings_feedback, give_feedback, get_user_profiles, check_login, encrypt_password, get_user

# check if authenticated
if "authenticated" not in st.session_state or st.session_state["authenticated"] == False:
    st.switch_page("login.py")

if st.button("Logout"):
    st.session_state["authenticated"] = False
    st.switch_page("login.py")

if st.button("Return to home"):
    st.switch_page("pages/app.py")

if st.button("View Saved Listings"):
    st.switch_page("pages/listings.py")

st.divider()

st.header("Your Profile")

@st.experimental_dialog("Change email")
def confirm_email():
    new_email = st.text_input("Enter your new email:", "")
    if st.button("Submit"):
        get_user_profiles().update_one({'user_email': st.session_state['user_email']}, 
                                       {'$set': {'user_email': new_email}})

        st.session_state['user_email'] = new_email
        st.success("Successfully change email!")
        sleep(1)
        st.rerun()
    if st.button("Cancel"):
        st.rerun()

@st.experimental_dialog("Change password")
def confirm_pw():
    old_pw = st.text_input("Enter your old password here:")

    if check_login(st.session_state['user_email'], old_pw) == True:
        new_pw = st.text_input("Enter your new password here:")

        if st.button("Submit"):
            if new_pw == "":
                st.error("Please enter a new password")
            else:
                get_user_profiles().update_one({'user_email': st.session_state['user_email']}, 
                                               {'$set': {'password': encrypt_password(new_pw)}})
                st.success("Successfully change password!")
                sleep(1)
                st.rerun()

    elif old_pw == "":
        pass
    else:
        st.error("Wrong password!")


    if st.button("Cancel"):
        st.rerun()

user_email = st.text("Email: " + st.session_state['user_email'])
change_email = st.button("Change email")
change_pw = st.button("Change password")

if change_email:
    confirm_email()
if change_pw:
    confirm_pw()

user = get_user(st.session_state['user_email'])

st.write("Voucher Amount: $" + str(user['voucher_amount']))
st.write("Voucher Type: " + user['voucher_type'])
st.write("Number of Beds: " + str(user['number_beds']))
st.write("Preferred Boroughs: " + str(user['preferred_boroughs']))
st.write("Number of Household Children: " + str(user['household_children']))
st.write("Number of Houshold Adults: " + str(user['household_adults']))
st.write("Number of Household Seniors: " + str(user['household_seniors']))
st.write("Age: " + str(user['age']))
st.write("Citizenship: " + str(user['citizenship']))
st.write("Ethnicity: " + str(user['ethnicity']))
st.write("Sexuality: " + str(user['sexuality']))
st.write("Gender: " + str(user['gender']))
st.write("Disability: " + str(user['disability']))
st.write("Credit Score: " + str(user['credit_score']))
st.write("Employment: " + str(user['employment']))

