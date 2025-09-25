import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import json
import requests
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode, GridUpdateMode

# Set the page configuration for a wide layout and a light grey background
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

if "selected_campaign" in st.session_state:
    selected_campaign = st.session_state["selected_campaign"]

#query_ads = st.query_params["cid"] if "cid" in st.query_params else None
st.write(selected_campaign)
selected_campaign_ad_id = "No Campaign Selected"
# if "selected_camp_from_ad" in st.session_state and st.session_state["selected_camp_from_ad"]:
#     selected_campaign_ad_id = st.session_state.get("selected_camp_from_ad", "No Campaign Selected")
    #st.write(f"Selected Campaign from Advertisers Page: {selected_campaign}")
if selected_campaign is not None:
    selected_campaign_ad_id = selected_campaign
else:
    selected_campaign_ad_id = "No Campaign Selected"

# def get_db_target_connection():
#     return psycopg2.connect(
#         host="adops-postgres-us-east1.crcvkuetqx1f.us-east-1.rds.amazonaws.com",
#         database="adops",
#         user="postgres",
#         password="qVxoqr[B*AGU4mx<)5GANna4DXP>"
#     )
# def get_ad_data():
#     conn1 = get_db_target_connection()
#     cursor = conn1.cursor()
#     cursor.execute("SELECT * FROM campaign_metrics advertiser_id = %s;")
#     ad_data = cursor.fetchall()
#     ad_data_list = []
#     for row in ad_data:
#         row_data = {
#             'id': row['campaign_id'],
#             'camp_name': row['campaign_name'],
#             'ad': row['advertiser_id'],
#             'budget': row['booked_budget'],
#             'status': row['status'],
#             'deal': row['deal_type'],
#         }
#         ad_data_list.append(row_data)
#     return ad_data_list
#     #st.write(data)
#     return ad_data
#     conn1.close()
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
    </style>
    """,
    unsafe_allow_html=True,
)


with st.container(key="header_container"):
    #st.markdown('<div class="white-background-container">', unsafe_allow_html=True)
    
    # Create columns for the row layout
    col1, mid, col2 = st.columns([1, 7, 2]) # Adjust column widths as needed

    with col1:
        st.image("assets/tavant_logo.jpg",  width=100)
    with col2:
          # Create a nested
        col3, col4 = st.columns([1, 1])
        with col3:
            st.markdown('<div class="header-bot"><i class="fa-solid fa-robot fa-2xl"></i></div>', unsafe_allow_html=True)
        with col4:
            st.markdown("""<div class="header-right-icons"><i class="fa-solid fa-bell fa-xl"></i><i class="fa-solid fa-gear fa-xl"></i> <i class="fa-solid fa-user fa-xl"></i></div>""", unsafe_allow_html=True)


st.markdown(
    """
    <style>
    .st-key-campaign_banner_container {
        border: 1px solid grey;
        border-radius: 10px;
        padding: 20px;
        background-color: #ffffff;
    }
    .st-key-campaign_banner_container .campaign-banner-data {
        font-weight: bold;
        font-size: 1.2em;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
# A section with five columns, white background, and curved edges
# st.markdown('<div class="five-column-section">', unsafe_allow_html=True)

with st.container(key="campaign_details_main_container"):
    left, right = st.columns([3,1])

    with left:

        with st.container(key="campaign_banner_container"):

            st.write(f"### {selected_campaign.get("campaign_name")[0]}",unsafe_allow_html=True)
            st.write(f"#### {selected_campaign.get("campaign_id")[0]}",unsafe_allow_html=True)


        def call_reconsilation_api(input_data):

            try:
                headers = {'Content-Type': 'application/json'}
                # Example API call using requests library
                response = requests.post("https://uwuoh1qnzf.execute-api.us-east-1.amazonaws.com/test", data=input_data, headers=headers)
                return response
                response.raise_for_status()  # Raise an exception for bad status codes
                
            except requests.exceptions.RequestException as e:
                st.error(f"API call failed: {e}")
                return None  
        if st.button('Run Agent Evaluation'):
                with st.spinner("Fetching data from API... Please wait."):

                    input_set = {
                            'inputText': {
                            'campaign_id': 'camp-7789',
                            'dsp': 'The Trade Desk',
                            'publisher': 'Hulu',
                            'creative_id': 'C-5567',
                            'dsp_imps': 850000,
                            'ssai_imps': 680000,
                            'gap_percent': 25,
                            'deal_type': 'PG',
                            'case_id': 'REC-2025-0915-001',
                            'case_title': 'Hulu PG Deal Impression Discrepancy Analysis'
                            }}
                    input_data = json.dumps(input_set)
                    resp = call_reconsilation_api(input_data)
                    if resp.status_code == 200:
                        #st.success("API request successful! Status code: 200 OK")
                        st.subheader("Agent Recommendation")
                        st.write(resp.json()['output']['content'][0]['text'])
                    else:
                        #st.error(f"API request failed with status code: {resp.status_code}")
                        st.text(resp.text['message']) # Display the error message if available
        
        # st.markdown("""<style>
        #     .st-key-footer_container {
        #         display: flex;
        #         justify-content: end;
        #         flex-direction: row;
        #     }
        #     .st-key-footer_container .stPageLink {
        #         width: 100%;
        #         background-color: #C0C0C0;
        #         border: 1px solid #d1d5db; /* Light gray border */
        #         padding: 10px 30px;
        #         border-radius: 8px;
        #     }
        #     .st-key-footer_container .stPageLink p{
        #         font-weight: bold;
        #         color: #111111;
        #     }
        #     </style>""", unsafe_allow_html=True)

        # if 'selected_option' not in st.session_state:
        #     st.session_state.selected_option = None

        # st.markdown("""
        # <style>
        #     .st-key-action_select_container {
        #         border: 1px solid grey;
        #         border-radius: 10px;
        #         padding: 20px;
        #         background-color: #ffffff;
        #         height: 700px;
        #     }
        #     /* Use a container with flexbox to arrange items horizontally */
        #     .stRadio > div[role="radiogroup"] {
        #         flex-direction: row;
        #         gap: 300px;
        #     }

        #     /* Style the labels (the clickable boxes) */
        #     .stRadio > div[role="radiogroup"] label {
        #         flex-grow: 1;
        #         text-align: center;
        #         padding: 10px;
        #         border: 1px solid #ccc;
        #         border-radius: 5px;
        #         cursor: pointer;
        #         width: 350px;
        #         height: 120px;
        #         background-color: #f0f2f6; /* Default background color */
        #     }

        #     /* Style the selected label */
        #     .stRadio > div[role="radiogroup"] label:has(input:checked) {
        #         background-color: #007bff; /* Color when clicked */
        #         color: white; /* Text color when clicked */
        #         border-color: #007bff;
        #     }

        #     /* Hide the original radio button circle */
        #     .stRadio > div[role="radiogroup"] label input {
        #         display: none;
        #     }
        # </style>
        # """, unsafe_allow_html=True)

        # with st.container(key="action_select_container"):
        #     st.write("#### Select Action")
        #     selected_option = st.radio(
        #     "",
        #     ("Make Good", "Accept", "Escalate"),
        #     index=None, # Set a default selected option
        #     key="custom_radio_buttons"
        # )

        # # Display the selected option
        # st.write(f"You selected: **{selected_option}**")

        # # Use columns to place the buttons horizontally
        # col1, col2, col3 = st.columns(3)

        # with col1:
        #     if st.button("Option 1", use_container_width=True):
        #         st.session_state.selected_option = "Option 1"

        # with col2:
        #     if st.button("Option 2", use_container_width=True):
        #         st.session_state.selected_option = "Option 2"

        # with col3:
        #     if st.button("Option 3", use_container_width=True):
        #         st.session_state.selected_option = "Option 3"

        # st.write(f"You have selected: **{st.session_state.selected_option}**")
        # st.markdown(
        #     """
        #     <style>
        #     .st-key-campaign_details_container {
        #         border: 1px solid grey;
        #         border-radius: 10px;
        #         padding: 20px;
        #         background-color: #ffffff;
        #         height: 700px;
        #     }
        #     .st-key-campaign_banner_container .campaign-banner-data {
        #         font-weight: bold;
        #         font-size: 1.2em;
        #         }
        #     </style>
        #     """,
        #     unsafe_allow_html=True,
        # )


        # Create the radio buttons


        # with st.expander("Agent Evaluation"):
        #     if st.button('Run Agent Evaluation'):
        #         with st.spinner("Fetching data from API... Please wait."):
        #             input_set = {
        #                     'inputText': {
        #                     'campaign_id': 'camp-7789',
        #                     'dsp': 'The Trade Desk',
        #                     'publisher': 'Hulu',
        #                     'creative_id': 'C-5567',
        #                     'dsp_imps': 850000,
        #                     'ssai_imps': 680000,
        #                     'gap_percent': 25,
        #                     'deal_type': 'PG',
        #                     'case_id': 'REC-2025-0915-001',
        #                     'case_title': 'Hulu PG Deal Impression Discrepancy Analysis'
        #                     }}
        #             input_data = json.dumps(input_set)
        #             resp = call_reconsilation_api(input_data)
        #             if resp.status_code == 200:
        #                 #st.success("API request successful! Status code: 200 OK")
        #                 st.subheader("Agent Recommendation")
        #                 st.write(resp.json()['output']['content'][0]['text'])
        #             else:
        #                 #st.error(f"API request failed with status code: {resp.status_code}")
        #                 st.text(resp.text['message']) # Display the error message if available
                

        with st.container(key="footer_container"):
            st.page_link("pages/campaigns.py", label="Back")
            #st.page("app.py", label="")
            
            st.page_link("pages/campaigns.py", label="Submit Evaluation")


    with right:
        
        st.markdown(
            """
            <style>
            .st-key-campaign_details_container {
                border: 1px solid grey;
                border-radius: 10px;
                padding: 20px;
                background-color: #ffffff;
                height: 700px;
            }
            .st-key-campaign_banner_container .campaign-banner-data {
                font-weight: bold;
                font-size: 1.2em;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
        # A section with five columns, white background, and curved edges
        # st.markdown('<div class="five-column-section">', unsafe_allow_html=True)

        with st.container(key="campaign_details_container"):

            col1, col2, col3, col4 = st.columns([5,5,5,5])

        # Example content for each column
            with col1:
                # inner_column = st.columns([1])
                # # with inner_column[0]:
                # #     st.image("assets/coke.jpg",  width=100)
                # with inner_column[1]:
                st.write("#### Details")
                st.markdown("Deal Type")

            with col2:
                st.markdown("Deal Type")
            with col3:
                st.markdown("Booked Imprewssion")
            with col4:
                st.markdown("Delivered Impression")