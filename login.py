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

login, create, guest = st.tabs(["Login to existing account", "Create a new account", "Continue as guest"])

def log_in(user_email = "guest", user_pw = "guestpw"):
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
        log_in(email, password)

with create:

    st.info("Please fill out all required information below, then click 'Create account'")

    email = st.text_input("Email :red[(required)]", key="create_email")
    password = st.text_input("Password :red[(required)]", key="create_pw", type="password")
    confirm_password = st.text_input("Confirm password :red[(required)]", type="password")
    if password != confirm_password and confirm_password != "":
        st.error("Passwords do not match")

    voucher_amount = st.text_input("Enter voucher amount ($) :red[(required)]")
    type_of_voucher = st.radio("Select voucher type :red[(required)]", ['Section 8 NYCHA', 'Section 8 EHV', 'Section 8 HPD', 'CityFHEPS', 'FHEPS'])

    if type_of_voucher == "Other":
        type_of_voucher = st.text_input("Enter other voucher type")

    number_beds = st.number_input("Select number of beds the voucher is for (zero beds denotes studio) :red[(required)]", value=0, min_value=0, max_value=10, step=1)

    preferred_borough = st.multiselect("Select your preferred boroughs :red[(required)]",
        ['Manhattan', 'Brooklyn', 'Queens', 'Bronx'])

    #household_size = st.number_input("How many people are in your household? :red[(required)]", value=1, min_value=0, max_value=10, step=1)

    household_desc_children = st.number_input(f"How many ***{'children (under 18 years old)'}*** are in your household? :red[(required)]", value=0, min_value=0, max_value=10, step=1)
    household_desc_adults = st.number_input(f"How many ***{'adults (18 to 65 years old)'}*** are in your household? :red[(required)]", value=1, min_value=0, max_value=10, step=1)
    household_desc_senior = st.number_input(f"How many ***{'seniors (over 65 years old)'}*** are in your household? :red[(required)]", value=0, min_value=0, max_value=10, step=1)

    st.subheader("Demographic questions (optional)")
    st.info("Each question below is optional, but we highly appreciate any information you are willing to provide.")
    
    st.write("Citezenship: Which best describes you? Select all the apply.")
    cit_us = st.checkbox("U.S. Citizen")
    cit_permres = st.checkbox("Permanent Resident/'Green Card' Holder")
    cit_asylee = st.checkbox("Asylee/Refugee")
    cit_workvisa = st.checkbox("On an Authorized Work Visa")
    cit_inprocess = st.checkbox("In process of applying for immigration benefits")
    cit_other = st.checkbox("Other. Please explain", key=0)
    cit_none = st.checkbox("Prefer not to say", key=1)

    cit_other_desc = ""

    if cit_other == True:
        cit_other_desc = st.text_input("Please explain your citizenship situation:")

    st.write("")

    st.write("Ethnicity: What do you consider yourself as? Select all that apply")
    eth_afr = st.checkbox("African American or Black")
    eth_white = st.checkbox("Caucasian or White")
    eth_hisp = st.checkbox("Hispanic")
    eth_asian = st.checkbox("Asian, South Asian or Pacific Islander, including Native Hawaiian")
    eth_natam = st.checkbox("Native American/Alaskan Native")
    eth_mideast = st.checkbox("Middle Eastern or North African")
    eth_other = st.checkbox("Other. Please explain", key=2)
    eth_none = st.checkbox("Prefer not to say", key=3)

    eth_other_desc = ""

    if eth_other == True:
        eth_other_desc = st.text_input("Please explain your ethnicity here:")

    st.write("")

    st.write("Sexuality: What do you consider yourself as? Select all that apply")
    sex_straight = st.checkbox("Heterosexual/Straight")
    sex_bi = st.checkbox("Bisexual")
    sex_gay = st.checkbox("Lesbian/Gay")
    sex_other = st.checkbox("Other. Please explain", key=4)
    sex_none = st.checkbox("Prefer not to say", key=5)

    sex_other_desc = ""

    if sex_other == True:
        sex_other_desc = st.text_input("Please explain your sexuality here:")

    st.write("")

    st.write("Gender: What do you identify as? Select all that apply")
    gen_fem = st.checkbox("Female")
    gen_male = st.checkbox("Male")
    gen_transfem = st.checkbox("Transgender Female")
    gen_transmale = st.checkbox("Transgender Male")
    gen_nonbin = st.checkbox("Non-Binary")
    gen_other = st.checkbox("Other. Please explain", key=6)
    gen_none = st.checkbox("Prefer not to say", key=7)

    gen_other_desc = ""

    if gen_other == True:
        gen_other_desc = st.text_input("Please explain your gender here:")

    st.write("")

    st.write("Disability: Do you have a disability? Check all that apply.")
    dis_vis = st.checkbox("Visual")
    dis_learn = st.checkbox("Learning")
    dis_speech = st.checkbox("Speech")
    dis_mob = st.checkbox("Mobility")
    dis_med = st.checkbox("Medical")
    dis_mental = st.checkbox("Mental Health")
    dis_phys = st.checkbox("Physical")
    dis_other = st.checkbox("Other. Please explain", key=8)
    dis_none = st.checkbox("Prefer not to say", key=9)
    dis_nothing = st.checkbox("No disability")

    dis_other_desc = ""

    if dis_other == True:
        dis_other_desc = st.text_input("Please explain your disability here:")

    st.write("")

    st.radio("Credit Score: What is your credit score?", ["300-579", "580-669", "670-739", "740-799", "800-850", "Don't know", "Prefer not to say"], index=None)

    st.write("")

    emp_names = {0: "In school/training", 1: "Not looking for a job right now", 2: "Disabled and not working",
                  3: "Looking for a job", 4: "Working full-time (30+ hours/week)", 5: "Working part-time or seasonal work",
                  6: "Freelancing", 7: "Retired", 8: "Other. Please explain", 9: "Prefer not to say"}
    emp_values = [False, False, False, False, False, False, False, False, False, False]

    st.write("Employment: Select the options that best describe you. Select all that apply.")
    emp_values[0] = st.checkbox(emp_names.get(0))
    emp_values[1] = st.checkbox(emp_names.get(1))
    emp_values[2] = st.checkbox(emp_names.get(2))
    emp_values[3] = st.checkbox(emp_names.get(3))
    emp_values[4] = st.checkbox(emp_names.get(4))
    emp_values[5] = st.checkbox(emp_names.get(5))
    emp_values[6] = st.checkbox(emp_names.get(6))
    emp_values[7] = st.checkbox(emp_names.get(7))
    emp_values[8] = st.checkbox(emp_names.get(8), key=10) # other
    emp_values[9] = st.checkbox(emp_names.get(9), key=11)

    emp_other_desc = ""

    if emp_values[8] == True:
        emp_other_desc = st.text_input("Please explain your employment here:")

    age = st.number_input("Age: What is your age?", value=1, min_value=1, max_value=150, step=1)

    if st.button("Create account"):
        log_in(email, password)

with guest:
    if st.button("Continue as guest"):
        log_in()



if not st.session_state.get("authenticated", False):
    hide_pages(["app", "profile"])