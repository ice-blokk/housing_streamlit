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

if st.button("View Profile"):
    st.switch_page("pages/profile.py")

st.header("Your saved listings")
listings = get_saved_listings().find({"user_email": st.session_state['user_email']})
listings = list(listings)

df = pd.DataFrame(listings, columns=column_names)

col1, col2, col3, col4, col5, col6, col7 = st.columns([3, 2, 2, 2, 5, 4, 4])
with col1:
    st.subheader("Name")
with col2:
    st.subheader("Borough")
with col3:
    st.subheader("Beds")
with col4:
    st.subheader("Baths")
with col5:
    st.subheader("URL")
with col6:
    st.subheader("Remove Listing")
with col7:
    st.subheader("Feedback")

for i, row in df.iterrows():
    col1, col2, col3, col4, col5, col6, col7 = st.columns([3, 2, 2, 2, 5, 4, 4])
    with col1:
        st.write(row['Name'])
    with col2:
        st.write(row['Borough'])
    with col3:
        st.write(row['# Beds'])
    with col4:
        st.write(str(int(row['# Baths'])))
    with col5:
        st.write(row['URL'])
    with col6:
        button_name = str(row.name) + "_savelisting"
        if st.button("Remove Listing", key=button_name, on_click=remove_listing, args=(row,)):
            continue
    with col7:
        popover_name = str(row.name) + "_feedback"
        with st.popover("Feedback"):
            st.markdown(f"Give feedback for property: {row['Name']}")
            
            feedback = in_listings_feedback(row)
            applied_response = None
            why_applied_response = ""
            approved_response = None
            extra_info_response = ""
            if feedback != False:
                st.info("Feedback has already been given. You can update your feedback below by clicking 'Submit feedback'")
                
                if feedback['applied'] == "Yes":
                    applied_response = 0
                elif feedback['applied'] == "No":
                    applied_response = 1

                why_applied_response = feedback['why_applied']

                if feedback['approved'] == "Yes":
                    approved_response = 0
                elif feedback['approved'] == "No":
                    approved_response = 1

                extra_info_response = feedback['extra_info']

            applied = st.radio("Did you apply to the listing?", ['Yes', 'No'], index=applied_response, key=str(row.name) + "_apply")
            why_applied = st.text_input("Why/why not?", why_applied_response, key=str(row.name) + "_why_apply")

            approved = None

            if applied == "Yes":
                approved = st.radio("Has your application been approved?", ["Yes", "No"], index=approved_response, key=str(row.name) + "_approved")

            extra_info = st.text_input("Please provide any extra information here (optional)", extra_info_response, key=str(row.name) + "_extra")

            submit = st.button("Submit feedback", key=str(row.name) + "_submit_feedback")

            if submit:
                give_feedback(row, applied, why_applied, approved, extra_info)

    st.divider()



