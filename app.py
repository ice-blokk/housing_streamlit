import streamlit as st
import pandas as pd
import numpy as np

st.title('HousingMatch')
st.markdown('Match housing voucher holders with listings')

st.header('Criteria')
col1, col2, col3= st.columns(3)
with col1:
    # st.text('Sepal characteristics')
    # sepal_l = st.slider('Sepal lenght (cm)', 1.0, 8.0, 0.5)
    # sepal_w = st.slider('Sepal width (cm)', 2.0, 4.4, 0.5)
    # borough = st.text_input("Borough", '')
    borough = st.multiselect(
        "Borough/Neighborhood",
        ['Manhattan', 'Brooklyn']
    )
with col2:
    # st.text('Pepal characteristics')
    # petal_l = st.slider('Petal lenght (cm)', 1.0, 7.0, 0.5)
    # petal_w = st.slider('Petal width (cm)', 0.1, 2.5, 0.5)
    # beds = st.text_input("# Beds (Studio, 1, 2, 3)", '')
    beds = st.multiselect(
    "# Beds",
    ["Studio", '1', "2", "3"])
with col3:
    baths = st.multiselect(
    "# Baths",
    ["1", "2", "3", "4+"])

# for bed in beds:
#     if beds[bed] != 'Studio':
#         beds[bed] = beds[:1]

# if borough != '' and beds != '':
#     if beds == 'Studio':
#         st.write("Looking for ", beds, ' apartments in ', borough)
#     else:
#         st.write("Looking for ", beds, ' bed apartments in ', borough)

if st.button('Submit'):
    df = pd.read_csv('user_citysnap_listings_with_probability.csv')

    df = df.sort_values(by='Probability', ascending=False)
    # df = df.drop(columns=['Probability'])
    #df = df[df['Neighborhood'].str.contains(borough, case=False)]
    #df = df[df['# Beds'].str.contains(beds, case=False)]

    df = df.drop(columns=['Postal Code','Payment Standard (PS)', 'Ratio', 'Property Type', 'Probability'])
    df = df[df.Neighborhood.isin(list(borough))]
    df = df[df['# Beds'].isin(list(beds))]

    # df = df.to_string(index=False) # drop index

    result = df.head(30)
    #result = result.to_string(index=False) # drop index

    st.write(result)