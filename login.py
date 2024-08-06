from st_pages import hide_pages
from time import sleep
import streamlit as st

# hide sidebar
st.set_page_config(initial_sidebar_state="collapsed")

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

from mongodb import create_user, check_login

login, create = st.tabs(["Login to existing account", "Create a new account"])

def log_in(user_email = "guest"):
    st.session_state["authenticated"] = True
    st.session_state["user_email"] = user_email
    hide_pages([])
    st.success("Logged in!")
    sleep(0.5)
    st.switch_page("pages/app.py")


def log_out():
    st.session_state["authenticated"] = False
    st.success("Logged out!")
    sleep(0.5)

with login:
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", key="login_pw", type="password")
    if st.button("Login"):
        if check_login(email, password):
            log_in(email)
        else:
            st.error("Login failed! Make sure to check that your email and password are correct, and that you have created an account.")

with create:

    user_details = {"user_email": "", "password": "", "voucher_amount": None,
                "voucher_type": None, "number_beds": None, "preferred_boroughs": None,
                "household_children": 0, "household_adults": 1,
                "household_seniors": 0, "citizenship": None, "ethnicity": None,
                "sexuality": None, "gender": None, "disability": None,
                "credit_score": None, "employment": None, "age": 0}

    st.info("Please fill out all required information below, then click 'Create account'")

    user_details['user_email'] = st.text_input("Email :red[(required)]", key="create_email")
    
    password = st.text_input("Password :red[(required)]", key="create_pw", type="password")
    confirm_password = st.text_input("Confirm password :red[(required)]", type="password")
    if password != confirm_password and confirm_password != "":
        st.error("Passwords do not match")
    else:
        user_details['password'] = password

    user_details['voucher_amount'] = st.text_input("Enter voucher amount ($) :red[(required)]")

    if user_details['voucher_amount'] != "":
        try:
            user_details['voucher_amount'] = int(user_details['voucher_amount'])
        except Exception as e:
            st.error("Please enter a number")

    user_details['voucher_type'] = st.radio("Select voucher type :red[(required)]", ['Section 8 NYCHA', 'Section 8 EHV', 'Section 8 HPD', 'CityFHEPS', 'FHEPS'])

    if user_details['voucher_type'] == "Other":
        user_details['voucher_type'] = st.text_input("Enter other voucher type")

    user_details['number_beds'] = st.number_input("Select number of beds the voucher is for (zero beds denotes studio) :red[(required)]", value=0, min_value=0, max_value=10, step=1)

    user_details['preferred_boroughs'] = st.multiselect("Select your preferred boroughs :red[(required)]",
        ['Manhattan', 'Brooklyn', 'Queens', 'Bronx'])
    #household_size = st.number_input("How many people are in your household? :red[(required)]", value=1, min_value=0, max_value=10, step=1)

    user_details['household_children'] = st.number_input(f"How many ***{'children (under 18 years old)'}*** are in your household? :red[(required)]", value=0, min_value=0, max_value=10, step=1)
    user_details['household_adults'] = st.number_input(f"How many ***{'adults (18 to 64 years old)'}*** are in your household? :red[(required)]", value=1, min_value=0, max_value=10, step=1)
    user_details['household_seniors'] = st.number_input(f"How many ***{'seniors (65 years old and over)'}*** are in your household? :red[(required)]", value=0, min_value=0, max_value=10, step=1)

    st.subheader("Demographic questions (optional)")
    st.info("Each question below is optional, but we highly appreciate any information you are willing to provide. Your information will help us better help you.")
    
    # age

    age = st.number_input("Age: What is your age?", value=0, min_value=0, max_value=150, step=1)

    user_details['age'] = age

    # citizenship

    cit_names = {0: "U.S. Citizen", 1: "Permanent Resident/'Green Card' Holder", 2: "Asylee/Refugee",
                 3: "On an Authorized Work Visa", 4: "In process of applying for immigration benefits",
                 5: "Other. Please explain", 6: "Prefer not to say"}
    cit_values = [False] * 7

    st.write("Citezenship: Which best describes you? Select all the apply.")
    cit_descriptions = []
    for i in range(len(cit_names)):
        cit_values[i] = st.checkbox(cit_names.get(i), key=str(i) + "_cit")
        if cit_values[i]:
            cit_descriptions.append(cit_names.get(i))

    if "Other. Please explain" in cit_descriptions:
        cit_descriptions[cit_descriptions.index("Other. Please explain")] = st.text_input("Please explain your citizenship situation here:")

    user_details['citizenship'] = cit_descriptions

    st.write("")

    # ethnicity

    eth_names = {0: "African American or Black", 1: "Caucasian or White", 2: "Hispanic",
                 3: "Asian, South Asian or Pacific Islander, including Native Hawaiian",
                 4: "Native American/Alaskan Native", 5: "Middle Eastern or North African", 
                 6: "Other. Please explain", 7: "Prefer not to say"}
    eth_values = [False] * 8

    st.write("Ethnicity: What do you consider yourself as? Select all that apply")
    eth_descriptions = []
    for i in range(len(eth_names)):
        eth_values[i] = st.checkbox(eth_names.get(i), key=str(i) + "_eth")
        if eth_values[i]:
            eth_descriptions.append(eth_names.get(i))

    if "Other. Please explain" in eth_descriptions:
        eth_descriptions[eth_descriptions.index("Other. Please explain")] = st.text_input("Please explain your ethnicity here:")

    user_details['ethnicity'] = eth_descriptions

    st.write("")

    # sexuality

    sex_names = {0: "Heterosexual/Straight", 1: "Bisexual", 2: "Other. Please explain", 3: "Prefer not to say"}
    sex_values = [False] * 4

    st.write("Sexuality: What do you consider yourself as? Select all that apply")
    sex_descriptions = []
    for i in range(len(sex_names)):
        sex_values[i] = st.checkbox(sex_names.get(i), key=str(i) + "_sex")
        if sex_values[i]:
            sex_descriptions.append(sex_names.get(i))

    if "Other. Please explain" in sex_descriptions:
        sex_descriptions[sex_descriptions.index("Other. Please explain")] = st.text_input("Please explain your sexuality here:")

    user_details['sexuality'] = sex_descriptions

    st.write("")

    # gender

    gen_names = {0: "Female", 1: "Male", 2: "Transgender Female", 3: "Transgender Male", 4: "Non-Binary",
                 5: "Other. Please explain", 6: "Prefer not to say"}
    gen_values = [False] * 7

    st.write("Gender: What do you identify as? Select all that apply")
    gen_descriptions = []
    for i in range(len(gen_names)):
        gen_values[i] = st.checkbox(gen_names.get(i), key=str(i) + "_gen")
        if gen_values[i]:
            gen_descriptions.append(gen_names.get(i))

    if "Other. Please explain" in gen_descriptions:
        gen_descriptions[gen_descriptions.index("Other. Please explain")] = st.text_input("Please explain your gender here:")

    user_details['gender'] = gen_descriptions

    st.write("")

    # disability

    dis_names = {0: "Visual", 1: "Learning", 2: "Speech", 3: "Mobility", 4: "Medical", 5: "Mental Health", 6: "Physical",
                 7: "Other. Please explain", 8: "Prefer not to say", 9: "No disability"}
    dis_values = [False] * 10

    st.write("Disability: Do you have a disability? Check all that apply.")
    dis_descriptions = []
    for i in range(len(dis_names)):
        dis_values[i] = st.checkbox(dis_names.get(i), key=str(i) + "_dis")
        if dis_values[i]:
            dis_descriptions.append(dis_names.get(i))

    if "Other. Please explain" in dis_descriptions:
        dis_descriptions[dis_descriptions.index("Other. Please explain")] = st.text_input("Please explain your disability here:")

    user_details['disability'] = dis_descriptions

    st.write("")

    # credit score

    credit_score = st.radio("Credit Score: What is your credit score?", ["300-579", "580-669", "670-739", "740-799", "800-850", "Don't know", "Prefer not to say"], index=None)

    user_details['credit_score'] = credit_score

    st.write("")

    # employment

    emp_names = {0: "In school/training", 1: "Not looking for a job right now", 2: "Disabled and not working",
                  3: "Looking for a job", 4: "Working full-time (30+ hours/week)", 5: "Working part-time or seasonal work",
                  6: "Freelancing", 7: "Retired", 8: "Other. Please explain", 9: "Prefer not to say"}
    emp_values = [False] * 10

    st.write("Employment: Select the options that best describe you. Select all that apply.")
    emp_descriptions = []
    for i in range(len(emp_names)):
        emp_values[i] = st.checkbox(emp_names.get(i), key=str(i) + "_emp")
        if emp_values[i]:
            emp_descriptions.append(emp_names.get(i))


    if "Other. Please explain" in emp_descriptions:
        emp_descriptions[emp_descriptions.index("Other. Please explain")] = st.text_input("Please explain your employment here:")

    user_details['employment'] = emp_descriptions

    keys_to_validate = {'user_email', 'password', 'voucher_amount', 
                        'voucher_type', 'number_beds', 'preferred_boroughs',
                        'household_children', 'household_adults', 'household_seniors'}

    if st.button("Create account"):
        required = True
        for key in keys_to_validate:
            if user_details[key] == "" or user_details[key] == None or user_details[key] == []:
                error = key
                if key == "voucher_amount":
                    error = "voucher amount"
                elif key == "voucher_type":
                    error = "voucher type"
                elif key == "number_beds":
                    error = "preferred number of beds"
                elif key == "preferred_boroughs":
                    error = "preferred boroughs"
                required = False
                st.error(f"Please enter a {error}")
        
        if user_details['voucher_amount'] != None and isinstance(user_details['voucher_amount'], (float, int)) == False:
            required = False
            st.error("Please enter a number for voucher amount")

        if password != confirm_password:
            required = False
            st.error("Please make sure that your password is correct")

        if required == True:
            st.success("Account created sucessfully!")
            email = user_details["user_email"]
            password = user_details["password"]
            user_details.pop('user_email')
            user_details.pop('password')
            create_user(email, password, user_details)
            log_in(email)


if not st.session_state.get("authenticated", False):
    hide_pages(["app", "profile"])