import streamlit as st
import pandas as pd
import numpy as np

st.title('HousingMatch')
st.markdown('Match housing voucher holders with listings')

st.header('Criteria')
col1, col2 = st.columns(2)
with col1:
    # st.text('Sepal characteristics')
    # sepal_l = st.slider('Sepal lenght (cm)', 1.0, 8.0, 0.5)
    # sepal_w = st.slider('Sepal width (cm)', 2.0, 4.4, 0.5)
    # borough = st.text_input("Borough", '')
    borough = st.radio(
        "Borough/Neighborhood",
        ['Manhattan', 'Brooklyn', 'Dumbo', 'Clinton Hill']
    )
with col2:
    # st.text('Pepal characteristics')
    # petal_l = st.slider('Petal lenght (cm)', 1.0, 7.0, 0.5)
    # petal_w = st.slider('Petal width (cm)', 0.1, 2.5, 0.5)
    # beds = st.text_input("# Beds (Studio, 1, 2, 3)", '')
    beds = st.radio(
    "# Beds",
    ["Studio", '1 bed', "2 beds", "3 beds"])

if beds != 'Studio':
    beds = beds[:1]

if borough != '' and beds != '':
    if beds == 'Studio':
        st.write("Looking for ", beds, ' apartments in ', borough)
    else:
        st.write("Looking for ", beds, ' bed apartments in ', borough)

if st.button('Submit'):
    df = pd.read_csv('user_citysnap_listings_with_probability.csv')

    df = df.sort_values(by='Probability', ascending=False)
    # df = df.drop(columns=['Probability'])
    df = df[df['Neighborhood'].str.contains(borough, case=False)]
    df = df[df['# Beds'].str.contains(beds, case=False)]

    result = df.head()

    st.write(result)