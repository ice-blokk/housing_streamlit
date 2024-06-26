import streamlit as st
import pandas as pd
import numpy as np

st.title('HousingMatch')
st.info("""Hello there! We’re delighted you’re here! 
        Tell us what you’re looking for below, and see a curated list of 
        properties that fit within your Emergency Housing Voucher (EHV) limit.""")
st.info("At this time, we are only serving households with EHV vouchers in New York City.")

st.header('Criteria')
col1, col2, col3= st.columns(3)
with col1:
    # st.text('Sepal characteristics')
    # sepal_l = st.slider('Sepal lenght (cm)', 1.0, 8.0, 0.5)
    # sepal_w = st.slider('Sepal width (cm)', 2.0, 4.4, 0.5)
    # borough = st.text_input("Borough", '')
    borough = st.multiselect(
        "Borough/Neighborhood",
        ['Manhattan', 'Brooklyn', 'Upper West Side']
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
    [1, 2, 3, 4])

if st.button('Submit'):
    df = pd.read_csv('ActiveListingsAsOfJun24_with_probability.csv')

    df = df.sort_values(by='Probability', ascending=False)

    df = df.drop(columns=['Months Free', 'Owner Paid', 'Rent Stabilized',
                          'Postal Code','Payment Standard (PS)', 'Ratio', 'Parent Neighborhood',	
                          'Neighborhood3', 'Property Manager', 'Number of Floors', 'Number of Units',	
                          'Year Built',	'Active', 'Amenities', 'Unnamed: 22', 'Unnamed: 23',	
                          'Unnamed: 24', 'Unnamed: 25', 'Unnamed: 26', 'Unnamed: 27',	
                          'Unnamed: 28', 'Unnamed: 29', 'Unnamed: 30', 'Unnamed: 31',	
                          'Unnamed: 32', 'Unnamed: 33', 'Unnamed: 34'])

    df = df[df.Neighborhood.isin(list(borough))]
    df = df[df['# Beds'].isin(list(beds))]
    df = df[df['# Baths'].isin(list(baths))]

    for bor in borough:
        filtered_df = df[df['Neighborhood'] == bor]
        
        result = filtered_df

        # TODO: add URLS to ActiveListingsAsOfJun24_with_probability.csv
        # # Make the URLs in the 'URL' column clickable
        # def make_clickable(val):
        #     return f'<a href="{val}" target="_blank">{val}</a>'
        # result['URL'] = result['URL'].apply(make_clickable)

        result = result.to_html(index=False, escape=False) # convert df to html and remove index

        st.markdown(f"<h3>Listings for {bor}:</h3>", unsafe_allow_html=True)
        st.markdown(result, unsafe_allow_html=True)


# st.markdown('---')
# st.text_input("""Do you want to receive personalized listings everyday and make a difference? 
#               We’re looking for your help to rate listings so that we can serve you better.  Sign up!""",'')

# st.button("Submit Email")