<<<<<<< HEAD:util.py
=======
import streamlit as st
import pandas as pd
import numpy as np

from streamlit_feedback import streamlit_feedback
from trubrics.integrations.streamlit import FeedbackCollector
from trubrics_beta import Trubrics

# makes page wider
st.set_page_config(layout="wide")

trubrics = Trubrics(api_key=st.secrets["TRUBRICS_API_KEY"])

>>>>>>> e1f3e2b4ca2bc529134605ec862a2bd4eab2b8dc:app.py
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

neighborhood_selection = ['South Harlem', 'Lower East Side', 'Central Harlem', 'Bedford-Stuyvesant',
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

column_names = ['_id', 
                'user_email',
                'Name', 
                'Street Address', 
                'Locality', 'Borough', 
                'Postal Code', 
                'Country', 
                'Rent', 
                'Payment Standard (PS)', 
                'Ratio', 'Price Currency', 
                'Description', 
                'Property Type',
                '# Beds',
                '# Baths',
                'Square Footage', 
                'URL', 
                'Probability'
                ]

# Make the URLs in the 'URL' column clickable
# def make_clickable(val):
#     return f'<a href="{val}" target="_blank">{val}</a>'
# result['URL'] = result['URL'].apply(make_clickable)

# def clicked():
#     print("clicked")

# result['Feedback'] = '<button type="button">&#128077</button> <button type="button">&#128077</button>'

        #result = result.to_html(index=False, escape=False) # convert df to html and remove index
        #edited_df = st.experimental_data_editor(result)


        # st.markdown(f"<h3>Listings for {bor}:</h3>", unsafe_allow_html=True)
        # st.markdown(result, unsafe_allow_html=True)

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