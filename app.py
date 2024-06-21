import streamlit as st
import pandas as pd
import numpy as np

st.title('Housing Match')
st.markdown('Match housing voucher holders with listings')

st.header('Criteria')
col1, col2 = st.columns(2)
with col1:
    # st.text('Sepal characteristics')
    # sepal_l = st.slider('Sepal lenght (cm)', 1.0, 8.0, 0.5)
    # sepal_w = st.slider('Sepal width (cm)', 2.0, 4.4, 0.5)
    borough = st.text_input("Borough", '')
with col2:
    # st.text('Pepal characteristics')
    # petal_l = st.slider('Petal lenght (cm)', 1.0, 7.0, 0.5)
    # petal_w = st.slider('Petal width (cm)', 0.1, 2.5, 0.5)
    beds = st.text_input("# Beds (Studio, 1, 2, 3)", '')

if borough != '' and beds != '':
    if beds.lower == 'studio':
        st.write("Looking for ", beds, ' apartments in ', borough)
    else:
        st.write("Looking for ", beds, ' bed apartments in ', borough)

if st.button('Submit'):
    df = pd.read_csv('user_citysnap_listings_with_probability.csv')

    df = df.sort_values(by='Probability', ascending=False)
    df = df[df['Neighborhood'].str.contains(borough, case=False)]
    df = df[df['# Beds'].str.contains(beds, case=False)]

    result = df.head()

    st.write(result)