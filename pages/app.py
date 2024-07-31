import streamlit as st
import pandas as pd
import numpy as np

from util import neighborhood_selection

from streamlit_feedback import streamlit_feedback
from trubrics.integrations.streamlit import FeedbackCollector
from trubrics_beta import Trubrics

# makes page wider
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# hide sidebar

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

from mongodb import get_data, save_listing

# get data from mongodb
items = get_data()

trubrics = Trubrics(api_key="tru-SNMkticg50rWw-aYYAF4tyvBsIpiv0Nw44GJzEcmJQ4")

st.title('HousingMatch')
st.info("""Hello there! We’re delighted you’re here! 
        Tell us what you’re looking for below, and see a curated list of 
        properties that fit within your housing voucher limit...""")
st.info("""These listings do not guarantee housing.  
        We want to know whether the listings will lead to housing and 
        ask for your help in rating the listings.""")

if st.button("See profile"):
    st.switch_page("pages/profile.py")

st.header('Criteria')
col1, col2, col3, col4 = st.columns(4)
with col1:
    borough = st.multiselect(
        "Borough",
        ['Manhattan', 'Brooklyn', 'Queens', 'Bronx']
    )
with col2:
    neighborhood = st.multiselect(
        "Neighborhood",
        neighborhood_selection
    )
with col3:
    beds = st.multiselect(
    "# Beds",
    ["Studio", '1', "2", "3"])
with col4:
    baths = st.multiselect(
    "# Baths",
    [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])

df = pd.read_csv('transparentcity_citysnap_listings_with_probability.csv')

if st.button('Submit'):

    df = df.sort_values(by='Probability', ascending=False)

    df = df[df.Borough.isin(list(borough))]
    df = df[df['# Beds'].isin(list(beds))]
    df = df[df['# Baths'].isin(list(baths))]

    for bor in borough:
        for bed in beds:
            filtered_df = df[df['Borough'] == bor]
            filtered_df = df[df['# Beds'] == bed]

            if len(list(neighborhood)) != 0:
                filtered_df = df[df['Neighborhood'].isin(list(neighborhood))]
            
            result = filtered_df

            result = result.drop(columns=['Image URL', 'Latitude', 'Longitude'])
            result = result[result['Name'].notna()]
            result = result.head(20)
            
            col1, col2, col3, col4, col5, col6, col7 = st.columns([3, 2, 1, 2, 2, 5, 4])
            with col1:
                st.subheader("Name")
            with col2:
                st.subheader("Borough")
            with col3:
                st.subheader("Beds")
            with col4:
                st.subheader("Baths")
            with col5:
                st.subheader("Rating")
            with col6:
                st.subheader("URL")
            with col7:
                st.subheader("Save listing")

            for i, row in result.iterrows():
                col1, col2, col3, col4, col5, col6, col7 = st.columns([3, 2, 1, 2, 2, 5, 4])
                with col1:
                    st.write(row['Name'])
                with col2:
                    st.write(row['Borough'])
                with col3:
                    st.write(row['# Beds'])
                with col4:
                    st.write(row['# Baths'])
                with col5:
                    if row['Probability'] > .66:
                        st.write(":green[Highly Likely]")
                    elif row['Probability'] < .66 and row['Probability'] > .33:
                        st.write(":orange[Somewhat Likely]")
                    else:
                        st.write(":blue[Less Likely]")
                with col6:
                    st.write(row['URL'])
                with col7:
                    button_name = str(row.name) + "_savelisting"
                    if st.button("Save listing", key=button_name, on_click=save_listing, args=(row,)):
                        save_listing(row)

                st.divider()
