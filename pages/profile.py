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

if st.button("Return to home"):
    st.switch_page("pages/app.py")


user_tab, listings_tab = st.tabs(['User Details', 'Saved Listings'])

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

with user_tab:
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

with listings_tab:
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
            st.write(row['# Baths'])
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



