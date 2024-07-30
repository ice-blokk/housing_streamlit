import streamlit as st
import pandas as pd
from mongodb import get_collection, remove_listing
from util import column_names
from pymongo.mongo_client import MongoClient

user_tab, listings_tab = st.tabs(['User Details', 'Saved Listings'])

@st.experimental_dialog("Change email")
def confirm():
    new_email = st.text_input("Enter your new email:", "")
    if st.button("Submit"):
        st.session_state['user_email'] = new_email
        st.rerun()
    if st.button("Cancel"):
        st.rerun()

with user_tab:
    user_email = st.text("Email: " + st.session_state['user_email'])
    change_email = st.button("Change email")
    change_pw = st.button("Change password")

    if change_email:
        confirm()

with listings_tab:
    st.header("Your saved listings")
    listings = get_collection().find({"user_email": st.session_state['user_email']})
    listings = list(listings)
    
    df = pd.DataFrame(listings, columns=column_names)

    col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 5, 4])
    with col1:
        st.subheader("Name")
    with col2:
        st.subheader("Borough")
    with col3:
        st.subheader("Rating")
    with col4:
        st.subheader("URL")
    with col5:
        st.subheader("Remove Listing")

    for i, row in df.iterrows():
        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 5, 4])
        with col1:
            st.write(row['Name'])
        with col2:
            st.write(row['Borough'])
        with col3:
            if row['Probability'] > .66:
                st.write("Highly Likely")
            elif row['Probability'] < .66 and row['Probability'] > .33:
                st.write("Somewhat Likely")
            else:
                st.write("Less Likely")
        with col4:
            st.write(row['URL'])
        with col5:
            button_name = str(row.name) + "_savelisting"
            if st.button("Remove Listing", key=button_name, on_click=remove_listing, args=(row,)):
                continue
        st.divider()



