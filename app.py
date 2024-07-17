import streamlit as st
import pandas as pd
import numpy as np

from streamlit_feedback import streamlit_feedback
from trubrics.integrations.streamlit import FeedbackCollector
from trubrics_beta import Trubrics

# makes page wider
st.set_page_config(layout="wide")

trubrics = Trubrics(api_key=st.secrets["TRUBRICS_API_KEY"])

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
        properties that fit within your housing voucher limit.""")
# st.info("At this time, we are only serving households with EHV vouchers in New York City.")

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
    beds = st.multiselect(
    "# Beds",
    ["Studio", '1', "2", "3"])
with col4:
    baths = st.multiselect(
    "# Baths",
    [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])

if st.button('Submit'):
    trubrics.track(
        user_id = 'test',
        event = 'Feedback',
        properties = {
            "User email": "test@email.com",
            "User name": "name"
        }
    )
    df = pd.read_csv('transparentcity_citysnap_listings_with_probability.csv')

    df = df.sort_values(by='Probability', ascending=False)

    df = df[df.Borough.isin(list(borough))]
    df = df[df['# Beds'].isin(list(beds))]
    df = df[df['# Baths'].isin(list(baths))]

    for bor in borough:
        filtered_df = df[df['Borough'] == bor]

        if len(list(neighborhood)) != 0:

            filtered_df = df[df['Neighborhood'].isin(list(neighborhood))]
        
        result = filtered_df

        result = result.drop(columns=['Image URL', 'Latitude', 'Longitude'])

        # Make the URLs in the 'URL' column clickable
        # def make_clickable(val):
        #     return f'<a href="{val}" target="_blank">{val}</a>'
        # result['URL'] = result['URL'].apply(make_clickable)

        # def clicked():
        #     print("clicked")

        # result['Feedback'] = '<button type="button">&#128077</button> <button type="button">&#128077</button>'

        def handle_click(name):
            st.write(f'Button clicked for {name}')
        
        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 5, 4])
        with col1:
            st.write("Name")
        with col2:
            st.write("Borough")
        with col3:
            st.write("Probability")
        with col4:
            st.write("URL")
        with col5:
            st.write("Feedback")

        for i, row in result.iterrows():
            col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 5, 4])
            with col1:
                st.write(row['Name'])
            with col2:
                st.write(row['Borough'])
            with col3:
                st.write(round(row['Probability'], 2))
            with col4:
                st.write(row['URL'])
            with col5:
                # feedback = streamlit_feedback(
                #     feedback_type="thumbs",
                #     key=row.name
                # )
                # if feedback:
                #     print(feedback)

                if st.button(":thumbsup:", key=str(row.name) + "_up"):
                    trubrics.track(
                        user_id = 'test',
                        event = 'Feedback',
                        properties = {
                            "User email": "test@email.com",
                            "User name": "up",
                        }
                    )
                if st.button(":thumbsdown:", key=str(row.name) + "_down"):
                    trubrics.track(
                        user_id = 'test',
                        event = 'Feedback',
                        properties = {
                            "User email": "test@email.com",
                            "User name": "down"
                        }
                    )
            st.divider()

        #result = result.to_html(index=False, escape=False) # convert df to html and remove index
        #edited_df = st.experimental_data_editor(result)


        st.markdown(f"<h3>Listings for {bor}:</h3>", unsafe_allow_html=True)
        st.markdown(result, unsafe_allow_html=True)

    # feedback = collector.st_feedback(
    #     feedback_type="thumbs",
    #     path="thumbs_feedback.json"
    # )

    # # print out the feedback object as a dictionary in your app
    # feedback.dict() if feedback else None


# st.markdown('---')
# st.text_input("""Do you want to receive personalized listings everyday and make a difference? 
#               We’re looking for your help to rate listings so that we can serve you better.  Sign up!""",'')

# st.button("Submit Email")
