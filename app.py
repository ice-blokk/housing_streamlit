import streamlit as st
import pandas as pd
import numpy as np

neighborhood_to_borough = {
    'South Harlem': 'Manhattan',
    'Lower East Side': 'Manhattan',
    'Central Harlem': 'Manhattan',
    'Bedford-Stuyvesant': 'Brooklyn',
    'Bushwick': 'Brooklyn',
    'Little Italy': 'Manhattan',
    'Williamsburg': 'Brooklyn',
    'East Village': 'Manhattan',
    'Kips Bay': 'Manhattan',
    'Sutton Place': 'Manhattan',
    'East Williamsburg': 'Brooklyn',
    "Hell's Kitchen": 'Manhattan',
    'Murray Hill': 'Manhattan',
    'Hamilton Heights': 'Manhattan',
    'Chinatown': 'Manhattan',
    'Crown Heights': 'Brooklyn',
    'East Harlem': 'Manhattan',
    'Yorkville': 'Manhattan',
    'Manhattan Valley': 'Manhattan',
    'Carnegie Hill': 'Manhattan',
    'East Bronx': 'The Bronx',
    'Chelsea': 'Manhattan',
    'Fort Greene': 'Brooklyn',
    'Financial District': 'Manhattan',
    'Lenox Hill': 'Manhattan',
    'Prospect Heights': 'Brooklyn',
    'Downtown Brooklyn': 'Brooklyn',
    'Long Island City': 'Queens',
    'West Village': 'Manhattan',
    'Midtown South': 'Manhattan',
    'Upper West Side': 'Manhattan',
    'Midtown East': 'Manhattan',
    'Bowery': 'Manhattan',
    'Upper East Side': 'Manhattan',
    'Greenpoint': 'Brooklyn',
    'Nolita': 'Manhattan',
    'West Bronx': 'The Bronx',
    'Lincoln Square': 'Manhattan',
    'Flatiron District': 'Manhattan',
    'Greenwich Village': 'Manhattan',
    'Midtown West': 'Manhattan',
    'Tribeca': 'Manhattan',
    'Midwood': 'Brooklyn',
    'Roosevelt Island': 'Manhattan',
    'Sheepshead Bay': 'Brooklyn',
    'Morningside Heights': 'Manhattan',
    'Dumbo': 'Brooklyn',
    'Gramercy Park': 'Manhattan',
    'Rego Park': 'Queens',
    'Windsor Terrace': 'Brooklyn',
    'Mott Haven': 'The Bronx',
    'Astoria': 'Queens',
    'Riverdale': 'The Bronx',
    'Forest Hills': 'Queens',
    'Elmhurst': 'Queens',
    'Battery Park City': 'Manhattan',
    'Cobble Hill': 'Brooklyn',
    'Brooklyn Heights': 'Brooklyn',
    'Queens Village': 'Queens',
    'Prospect Lefferts Gardens': 'Brooklyn',
    'SoHo': 'Manhattan',
    'Flatbush': 'Brooklyn',
    'Jamaica': 'Queens',
    'Spuyten Duyvil': 'The Bronx',
    'Clinton Hill': 'Brooklyn',
    'Kew Gardens': 'Queens',
    'Park Slope': 'Brooklyn',
    'Mount Hope': 'The Bronx',
    'University Heights': 'The Bronx',
    'Washington Heights': 'Manhattan',
    'Jackson Heights': 'Queens',
    'Homecrest': 'Brooklyn',
    'Inwood': 'Manhattan',
    'Carroll Gardens': 'Brooklyn',
    'Flushing': 'Queens',
    None: None
}

st.title('HousingMatch')
st.info("""Hello there! We’re delighted you’re here! 
        Tell us what you’re looking for below, and see a curated list of 
        properties that fit within your Emergency Housing Voucher (EHV) limit.""")
st.info("At this time, we are only serving households with EHV vouchers in New York City.")

st.header('Criteria')
col1, col2, col3, col4 = st.columns(4)
with col1:
    # st.text('Sepal characteristics')
    # sepal_l = st.slider('Sepal lenght (cm)', 1.0, 8.0, 0.5)
    # sepal_w = st.slider('Sepal width (cm)', 2.0, 4.4, 0.5)
    # borough = st.text_input("Borough", '')
    borough = st.multiselect(
        "Borough",
        ['Manhattan', 'Brooklyn', 'Queens', 'Bronx']
    )
with col2:
    neighborhood = st.multiselect(
        "Neighborhood",
        ['South Harlem', 'Lower East Side', 'Central Harlem', 'Bedford-Stuyvesant',
        'Bushwick', 'Little Italy', 'Williamsburg', 'East Village', 'Kips Bay',
        'Sutton Place', 'East Williamsburg', "Hell's Kitchen", 'Murray Hill',
        'Hamilton Heights', 'Chinatown', 'Crown Heights', 'East Harlem', 'Yorkville',
        'Manhattan Valley', 'Carnegie Hill', 'East Bronx', 'Chelsea', 'Fort Greene',
        'Financial District', 'Lenox Hill', 'Prospect Heights', 'Downtown Brooklyn',
        'Long Island City', 'West Village', 'Midtown South', 'Upper West Side',
        'Midtown East', 'Bowery', 'Upper East Side', 'Greenpoint', 'Nolita',
        'West Bronx', 'Lincoln Square', 'Flatiron District', 'Greenwich Village',
        'Midtown West', 'Tribeca', 'Midwood', 'Roosevelt Island', 'Sheepshead Bay',
        'Morningside Heights', 'Dumbo', 'Gramercy Park', 'Rego Park',
        'Windsor Terrace', 'Mott Haven', 'Astoria', 'Riverdale', 'Forest Hills',
        'Elmhurst', 'Battery Park City', 'Cobble Hill', 'Brooklyn Heights',
        'Queens Village', 'Prospect Lefferts Gardens', 'SoHo', 'Flatbush', 'Jamaica',
        'Spuyten Duyvil', 'Clinton Hill', 'Kew Gardens', 'Park Slope', 'Mount Hope',
        'University Heights', 'Washington Heights', 'Jackson Heights', 'Homecrest',
        'Inwood', 'Carroll Gardens', 'Flushing']
    )
with col3:
    # st.text('Pepal characteristics')
    # petal_l = st.slider('Petal lenght (cm)', 1.0, 7.0, 0.5)
    # petal_w = st.slider('Petal width (cm)', 0.1, 2.5, 0.5)
    # beds = st.text_input("# Beds (Studio, 1, 2, 3)", '')
    beds = st.multiselect(
    "# Beds",
    ["Studio", '1', "2", "3"])
with col4:
    baths = st.multiselect(
    "# Baths",
    [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])

if st.button('Submit'):
    df = pd.read_csv('June_24_2024_Listings.csv')

    df = df.sort_values(by='Probability', ascending=False)

    df = df.drop(columns=['Months Free', 'Owner Paid', 'Rent Stabilized',
                          'Postal Code','Payment Standard (PS)', 'Ratio', 'Parent Neighborhood',	
                          'Neighborhood3', 'Property Manager', 'Number of Floors', 'Number of Units',	
                          'Year Built',	'Active', 'Amenities', 'Unnamed: 22', 'Unnamed: 23',	
                          'Unnamed: 24', 'Unnamed: 25', 'Unnamed: 26', 'Unnamed: 27',	
                          'Unnamed: 28', 'Unnamed: 29', 'Unnamed: 30', 'Unnamed: 31',	
                          'Unnamed: 32', 'Unnamed: 33', 'Unnamed: 34'])

    df = df[df.Borough.isin(list(borough))]
    df = df[df['# Beds'].isin(list(beds))]
    df = df[df['# Baths'].isin(list(baths))]

    for bor in borough:
        filtered_df = df[df['Borough'] == bor]

        if len(list(neighborhood)) != 0:

            filtered_df = df[df['Neighborhood'].isin(list(neighborhood))]
        
        result = filtered_df

        # TODO: add URLS to June_24_2024_Listings.csv
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
