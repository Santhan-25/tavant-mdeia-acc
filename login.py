import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd # Or other data structures
import psycopg2
from streamlit_card import card
from psycopg2.extras import RealDictCursor
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode, GridUpdateMode
import datetime
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from PIL import Image
from streamlit_authenticator.utilities import LoginError


def get_db_source_connection():
    return psycopg2.connect(
        host="adops-postgres-us-east1.crcvkuetqx1f.us-east-1.rds.amazonaws.com",
        database="adops",
        user="postgres",
        password="qVxoqr[B*AGU4mx<)5GANna4DXP>"
    )
def get_ad_data():
    conn1 = get_db_source_connection()
    cursor = conn1.cursor(cursor_factory=RealDictCursor)
    cursor.execute("select advertiser_id,  count(advertiser_id) total_campaigns, Sum(booked_budget) as bookedb, SUM(revenue_at_risk) as rar, COUNT(CASE WHEN status = 'Pending Review' THEN 1 END) AS PR_Count, COUNT(CASE WHEN status = 'Ready for Invoice' THEN 1 END) AS RFI_Count from campaign_metrics  group by advertiser_id, status")
    ad_data = cursor.fetchall()
    ad_data_list = []
    for row in ad_data:
        row_data = {
            #'image_path': next((item["logo"] for item in logos_list if item["name"].casefold() == row['advertiser_id'].replace("ADV_", "").casefold()), "https://upload.wikimedia.org/wikipedia/en/c/cb/Placeholder_logo.png"), #next(item.logo for item in logos_list if item.name == row['advertiser_id'].replace("ADV_", "").casefold()),
            'ad': row['advertiser_id'].replace("ADV_", "").capitalize(),
             #[item.logo for item in logos_list if item.name == ], #'https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Bill_Gates_-_Nov._8%2C_2019.jpg/390px-Bill_Gates_-_Nov._8%2C_2019.jpg',
            'budget': row['bookedb'],
            'total_campaigns': row['total_campaigns'],
            'revenue_risk': row['rar'],
            'pending_review': row['pr_count'],
            'ready_for_invoice': row['rfi_count'],
        }
        ad_data_list.append(row_data)
    return ad_data_list
    #st.write(data)
    return ad_data
    conn1.close()

ad_data_list = get_ad_data()
# print(ad_data_list)
st.set_page_config(layout="wide", page_title="Tavant Campaigns Assistant", page_icon="📊")

hide_streamlit_style = """
            <style>
                /* Hide the Streamlit header and menu */
                header {visibility: hidden;}
                /* Optionally, hide the footer */
                .streamlit-footer {display: none;}
                /* Hide your specific div class, replace class name with the one you identified */
                .st-emotion-cache-uf99v8 {display: none;}
                .stMainBlockContainer {padding-top: 0rem;}
                # .stMainBlockContainer .stVerticalBlock {gap: 0rem;}

            </style>
            """

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown(
    """
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css">
    """,
    unsafe_allow_html=True
)

# Apply custom CSS to the app
st.markdown("""
<style>
/* Main container for the whole app */
.stApp {
    background-color: #f0f2f6; /* Light grey background */
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Header styling */
.header-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
    background-color: #ffffff;
    border-radius: 15px;
    margin-bottom: 20px;
}
.header-container .logo {
    height: 40px;
}
.header-icons {
    display: flex;
    gap: 15px;
}
.header-icons .icon {
    font-size: 24px;
    color: #4a5568; /* Darker grey for icons */
    cursor: pointer;
}
.stHorizontalBlock {
    background-color: #ffffff;
    border-radius: 10px;
    }

/* Section 2 styling (five columns) */
.five-column-section {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
}

/* Data Grid styling */
.data-grid-container {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 15px;
}
.data-grid-title {
    text-align: left;
    font-size: 1.5em;
    font-weight: bold;
    margin-bottom: 15px;
    color: #2d3748; /* Dark title color */
}

/* Pagination and button container */
.bottom-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
}


</style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .st-key-header_container {
        border: 1px solid grey;
        border-radius: 10px;
        padding: 20px;
        background-color: #ffffff;
    }

    # .st-key-hedaer_container >div>div> [data-testid="stHorizontalBlock"] > div:nth-of-type(1) >div > [data-testid="stVerticalBlock"] > div:nth-of-type(2) { 
    #     position: absolute;
    #     margin-top: 30px;
    #     margin-left: 8px;
    # }
    .st-key-header_container >div>div .stVerticalBlock{
        gap:0;
    }
    .st-key-header_container .header-right-icons {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 25px;
        margin-top: 25px;
    }
    .st-key-header_container .stVerticalBlock {
        gap: 25px;
    }
    .st-key-header_container .header-bot {
        align-items: center;
        gap: 25px;
        margin-top: 8px;
        padding-left: 60px;
    } 
    .st-key-header_container .st_header_right_col {
        display: flex;
        flex-direction: column;
        justify-content: flex-end; /* Align items to the right */
        align-items: center;
        gap: 20px; /* Space between items */
    }
    .st-key-header_container .header-logo-text {
        width: 220px;
        font-weight: 600;
        font-size: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.container(key="header_container"):
    #st.markdown('<div class="white-background-container">', unsafe_allow_html=True)
    
    # Create columns for the row layout
    col1, mid, col2 = st.columns([1, 6, 3]) # Adjust column widths as needed

    with col1:
        image = Image.open("assets/brand_logo.png")
        # Define new dimensions
        new_width = 1150
        new_height = 200

        # Resize the image
        resized_image = image.resize((new_width, new_height))
        st.image("assets/brand_logo.png", width=1150)
        # st.markdown('<div class="header-logo-text"> AdOps Financial Assistant </div>', unsafe_allow_html=True)
    with col2:
        # Create a nested
        col3, col4 = st.columns([1, 1])
        with col3:
            # st.markdown('<div class="header-bot"><i class="fa-solid fa-robot fa-2xl"></i></div>', unsafe_allow_html=True)
            st.markdown('<div class="header-bot">', unsafe_allow_html=True)
            st.image("assets/ai_bot.png", width=50)
            st.markdown('</div>', unsafe_allow_html=True)
        with col4:
            st.markdown("""<div class="header-right-icons"><i class="fa-solid fa-bell fa-xl"></i><i class="fa-solid fa-gear fa-xl"></i> <i class="fa-solid fa-user fa-xl"></i></div>""", unsafe_allow_html=True)
            
st.markdown("""
<style>
/* Target the input elements within Streamlit's text input widgets */
div.stTextInput > div > div > input {
    /*border: 2px solid ;  Example: Green border */
    border-radius: 5px; /* Optional: Rounded corners */
    padding: 10px; /* Optional: Add some internal padding */
}

/* Optional: Style the password input specifically */
div.stTextInput > div > div > input[type="password"] {
    /*border: 2px solid ;  Example: Orange border for password */
}
</style>
""", unsafe_allow_html=True)
# Set page configuration for better layout
# st.set_page_config(layout="centered")
col1, mid, col3 = st.columns([1, 2, 1]) # Adjust ratios as needed for desired form width and centering

with mid: # All content within this 'with' block will be in the middle column
    st.write("### Login Form")

    # Create a form to group the input widgets
    with st.form(key='login_form',):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        # Create two columns for the buttons to place them side-by-side
        col1, col2 = st.columns(2)

        with col1:
            submit_button = st.form_submit_button(label='Submit')
        

    # Logic for handling form submission
    if submit_button:
        # A placeholder for your authentication logic
        if username == "admin" and password == "password123":
            st.switch_page("pages/advertiser.py")
            # You would typically redirect or set a session state variable here
        else:
            st.error("Invalid username or password.")

