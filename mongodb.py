import streamlit as st

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

cluster_username = st.secrets["mongo"]['cluster_username']
cluster_password = st.secrets["mongo"]['cluster_password']

uri = f'mongodb+srv://{cluster_username}:{cluster_password}@aws-housingmatchnyc.udjucnu.mongodb.net/?retryWrites=true&w=majority&appName=aws-housingmatchnyc'

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return MongoClient(uri, server_api=ServerApi('1'), connect=False)

client = init_connection()
db = client['mydb']
collection = db['mycollection']

def get_collection():
    return collection

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def get_data():
    db = client.mydb
    items = db.mycollection.find()
    items = list(items)  # make hashable for st.cache_data
    return items

def save_listing(row):
    document = {'user_email': st.session_state['user_email']}
    document.update(row.to_dict())
    collection.insert_one(document)
    st.success(f"Listing '{row['Name']}' saved for {st.session_state['user_email']}")