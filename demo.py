import streamlit as st
import pandas as pd
import numpy as np

from util import neighborhood_selection

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

st.session_state['authenicated'] = True

st.title('HousingMatch')
st.info("""Hello there! We’re delighted you’re here! 
        Tell us what you’re looking for below, and see a curated list of 
        properties that fit within your housing voucher limit...""")

st.header('Criteria')
col1, col2, col3, col4 = st.columns(4)
with col1:
    default_borough = None

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
    default_beds = 0
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

    df = df.sort_values(by='Probability', ascending=False)
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
            st.subheader("Likelihood")
        with col6:
            st.subheader("URL")
        with col7:
            st.subheader("Save listing")

        if result.empty:
            st.error("Sorry! We don't have any listings with that criteria.")

        for i, row in result.iterrows():
            col1, col2, col3, col4, col5, col6, col7= st.columns([3, 2, 1, 2, 2, 5, 4])
            with col1:
                st.write(row['Name'])
            with col2:
                st.write(row['Borough'])
            with col3:
                st.write(row['# Beds'])
            with col4:
                st.write(str(int(row['# Baths'])))
            with col5:
                prob = row['Probability']
                if prob < .33:
                    st.write(":red[Less Likely]")
                elif prob > .33 and prob < .66:
                    st.write(":orange[Somewhat Likely]")
                else:
                    st.write(":green[Most Likely]")
                
                # st.write(prob)
            with col6:
                st.write(row['URL'])
            with col7:
                button_name = str(row.name) + "_savelisting"
                if st.button("Save listing", key=button_name):
                    continue

            st.divider()
