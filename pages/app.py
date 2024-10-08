import streamlit as st
import pandas as pd
import numpy as np

from util import neighborhood_selection, navbar_style_1, navbar_style_2

from streamlit_navigation_bar import st_navbar

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

from mongodb import get_data, save_listing, get_user

# get data from mongodb
items = get_data()

# # navigation bar
# navbar = st_navbar(["Home", "Profile", "Saved Listings"], styles=navbar_style_1)
# st.write(navbar)

# nav_functions = {
#     "Home": st.switch_page("pages/app.py"),
#     "Profile": st.switch_page("pages/profile.py"),
#     "Saved Listings": st.switch_page("pages/listings.py")
# }

# go_to = nav_functions.get(navbar)
# if go_to:
#     go_to()

# check if authenticated
if "authenticated" not in st.session_state or st.session_state["authenticated"] == False:
    st.switch_page("login.py")

# app
st.title('HousingMatch')
st.info("""Hello there! We’re delighted you’re here! 
        Tell us what you’re looking for below, and see a curated list of 
        properties that fit within your housing voucher limit.""")
st.info("""These listings do not guarantee housing.  
        We want to know whether the listings will lead to housing and 
        ask for your help in rating the listings.""")

if st.button("Logout"):
    st.session_state["authenticated"] = False
    st.switch_page("login.py")

if st.button("View Profile"):
    st.switch_page("pages/profile.py")

if st.button("View Saved Listings"):
    st.switch_page("pages/listings.py")

user = get_user(st.session_state['user_email'])

st.header('Criteria')
col1, col2, col3, col4 = st.columns(4)
with col1:
    default_borough = None

    # if array is not empty
    if user['preferred_boroughs']:
        default_borough = user['preferred_boroughs']

    borough = st.multiselect(
        "Borough",
        ['Manhattan', 'Brooklyn', 'Queens', 'Bronx'],
        default=default_borough
    )

with col2:
    neighborhood = st.multiselect(
        "Neighborhood",
        neighborhood_selection
    )
with col3:
    default_beds = user['number_beds']
    if default_beds == 0:
        default_beds = 'Studio'
    default_beds = str(default_beds)

    beds = st.multiselect(
        "# Beds",
        ["Studio", '1', "2", "3"],
        default=default_beds
    )

with col4:
    baths = st.multiselect(
    "# Baths",
    [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])

df = None

# only shuffle df once per session
if 'df' not in st.session_state:
    df = pd.read_csv('transparentcity_citysnap_listings_with_probability.csv')
    df = df.sample(frac=1).reset_index(drop=True)

    st.session_state['df'] = df
else:
    df = st.session_state['df']

if st.button('Click to see the listings'):

    # df = df.sort_values(by='Probability', ascending=False)
    df = st.session_state['df']
    df = df[df.Borough.isin(list(borough))]
    df = df[df['# Beds'].isin(list(beds))]

    if baths:
        df = df[df['# Baths'].isin(list(baths))]

    if len(list(neighborhood)) != 0:
        df = df[df['Neighborhood'].isin(list(neighborhood))]

    for bor in borough:
        filtered_df = df[df['Borough'] == bor]
        
        result = filtered_df

        result = result.drop(columns=['Image URL', 'Latitude', 'Longitude'])
        result = result[result['Name'].notna()]
        result = result.head(20)
        
        col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 1, 2, 5, 4])
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
            st.subheader("Save listing")

        if result.empty:
            st.error("Sorry! We don't have any listings with that criteria.")

        for i, row in result.iterrows():
            col1, col2, col3, col4, col5, col6= st.columns([3, 2, 1, 2, 5, 4])
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
                if st.button("Save listing", key=button_name, on_click=save_listing, args=(row,)):
                    save_listing(row)

            st.divider()
