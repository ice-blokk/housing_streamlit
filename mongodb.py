import streamlit as st

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

cluster_username = st.secrets["mongo"]['cluster_username']
cluster_password = st.secrets["mongo"]['cluster_password']

uri = f'mongodb+srv://{cluster_username}:{cluster_password}@aws-housingmatchnyc.udjucnu.mongodb.net/?retryWrites=true&w=majority&appName=aws-housingmatchnyc&ssl=true&ssl_cert_reqs=CERT_NONE'

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return MongoClient(uri, server_api=ServerApi('1'), connect=False)

client = init_connection()
db = client['mydb']
collection = db['mycollection']

def get_saved_listings():
    return db['mycollection']

def get_user_profiles():
    return db['test_profiles']

def get_listings_feedback():
    return db['test_listings_feedback']

def get_ebbie_feedback():
    return db['ebbie_feedback']

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
    if check_in_listing(row) == False:
        st.error(f"Listing '{row['Name']}' is already saved for {st.session_state['user_email']}")
        return False
    document = {'user_email': st.session_state['user_email']}
    document.update(row.to_dict())
    get_saved_listings().insert_one(document)
    st.success(f"Listing '{row['Name']}' saved for {st.session_state['user_email']}")

def check_in_listing(row):
    result = get_saved_listings().find_one({'user_email': st.session_state['user_email'], 'Name': row['Name']})
    if result is None:
        return True
    return False

def remove_listing(row):
    get_saved_listings().delete_one({'user_email': st.session_state['user_email'], 'Name': row['Name']})
    st.success(f"Listing '{row['Name']}' removed for {st.session_state['user_email']}")

def give_feedback(row, applied, why_applied, approved, extra_info):
    document = {'user_email': st.session_state['user_email']}
    document.update(row.to_dict())
    document.update({"applied": applied, "why_applied": why_applied, "approved": approved, "extra_info": extra_info})

    document.pop('_id', None)

    filter_query = {'user_email': st.session_state['user_email'], 'Name': row['Name']}
    update_operation = {
        "$set": document
    }

    get_listings_feedback().update_one(filter_query, update_operation, upsert=True)
    st.success(f"Saved feedback for {row['Name']}")
    
def in_listings_feedback(row):
    result = get_listings_feedback().find_one({'user_email': st.session_state['user_email'], 'Name': row['Name']})
    if result is None:
        return False
    return result

def create_user(user_email, password, details):
    entry = {'user_email': user_email, 'password': bcrypt.generate_password_hash(password)}
    entry.update(details)

    get_user_profiles().insert_one(entry)

def check_login(user_email, password):
    pw = get_user_profiles().find_one({'user_email': user_email})
    if pw == {}:
        return False
    return bcrypt.check_password_hash(pw["password"], password)

def get_user(user_email):
    result = get_user_profiles().find_one({'user_email': user_email})
    return result

def encrypt_password(password):
    return bcrypt.generate_password_hash(password)

def give_ebbie_feedback(row, responsive, led_to_housing):
    document = row.to_dict()
    
    if responsive != None:
        document.update({"responsive": responsive})
    
    if led_to_housing != None:
        document.update({"led_to_housing": led_to_housing})

    get_ebbie_feedback().insert_one(document)
    st.success(f"Saved feedback for {row['Name']}")