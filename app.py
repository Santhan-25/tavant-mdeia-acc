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
        st.image("assets/tavant_logo.jpg",  width=100)
        st.markdown('<div class="header-logo-text"> AdOps Financial Assistant </div>', unsafe_allow_html=True)
    with col2:
        # Create a nested
        col3, col4 = st.columns([1, 1])
        with col3:
            st.markdown('<div class="header-bot"><i class="fa-solid fa-robot fa-2xl"></i></div>', unsafe_allow_html=True)
        with col4:
            st.markdown("""<div class="header-right-icons"><i class="fa-solid fa-bell fa-xl"></i><i class="fa-solid fa-gear fa-xl"></i> <i class="fa-solid fa-user fa-xl"></i></div>""", unsafe_allow_html=True)
            
ad_data_list = pd.DataFrame(ad_data_list)
st.header("Advertisers")

st.markdown(
    """
    <style>
    .st-key-search_container {
        border: 1px solid grey;
        border-radius: 10px;
        padding: 20px;
        background-color: #ffffff;
    }
    .st-key-search_container .stDateInput>div>div {
        width: 70%;
    }
    .st-key-search_container .stTextInput>div>div {
        width: 70%;
    } 
    .st-key-search_container .stButton>button {
        background-color: #4a5568;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 5px;
        cursor: pointer;
        width: 100%;
        margin-top: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
with st.container(key="search_container"):
    #st.markdown('<div class="white-background-container">', unsafe_allow_html=True)
    
    # Create columns for the row layout
    col1, col2, col3, col4 = st.columns([1, 1, 1, 3]) # Adjust column widths as needed

    with col1:
        from_date = st.date_input("From Date", value=None)
        button_from_disabled = from_date is None
    with col2:
        to_date = st.date_input("To Date", value=None)
        to_from_disabled = to_date is None

    with col3:
        search_query = st.text_input("Advertiser", value=st.session_state.search_query, placeholder="Search ...")

    with col4:
        st.write("") # Placeholder for vertical alignment
        if st.button("Search", disabled=button_from_disabled or to_from_disabled):
            st.session_state.search_query = search_query

    st.markdown('</div>', unsafe_allow_html=True)
ad_data_list = pd.DataFrame(ad_data_list)




# Filter and Search Inputs
#search_input = st.text_input("Search by Name:", value=st.session_state.search_query)
# category_filter = st.selectbox("Filter by Category:", ["All"] + list(ad_data_list['Category'].unique()), index=["All"] + list(ad_data_list['Category'].unique()).index(st.session_state.selected_category))

# Search Button
# if st.button("Apply Filters"):
#     st.session_state.search_query = search_query
    #st.session_state.selected_category = category_filter

# Filtering Logic
filtered_data = ad_data_list.copy()

if st.session_state.search_query:
    filtered_data = filtered_data[filtered_data['ad'].str.contains(st.session_state.search_query, case=False)]

# if st.session_state.selected_category != "All":
#     filtered_data = filtered_data[filtered_data['ad'] == st.session_state.selected_category]

js_code = JsCode("""
    function(params) {
        console.log("Cell clicked:", params.data);
        window.open("https://www.example.com/new-page", "_self");
    //window.location.replace("https://www.example.com/new-page");
        //return '<a href=${params.value} target="_blank">${params.value}</a>'
        //return '<a href="https://google.com" target="_top"></a>';
        // You could potentially send data back to Streamlit using a custom component if needed
    };
""")

gb = GridOptionsBuilder.from_dataframe(filtered_data)
gb.configure_selection('single', use_checkbox=False)
gb.configure_grid_options(rowHeight=65, tooltipShowDelay=0, tooltipHideDelay=2000, cellStyle={'text-align': 'center'},configure_selectable=True, onRowDoubleClicked=js_code)

image_nation = JsCode("""

        class ImageCellRenderer {
        init(params) {
            
            const imageElement = document.createElement('img');
            
            
            imageElement.setAttribute('src', params.value);
            imageElement.setAttribute('width', '60');
            imageElement.setAttribute('height', '60');
            const anchorElement = document.createElement('a');
            anchorElement.setAttribute('href', '/campaigns?ad_id=' + params.data.ad);
            anchorElement.setAttribute('target', "_parent");
            anchorElement.appendChild(imageElement);
            this.eGui = anchorElement;
            }
        getGui() {
            return this.eGui;
        }
        }
        """)
cell_click_callback = JsCode("""
    function cellClickCallback(event) {
        const adId = event.data.ad;
        const url = `/campaigns?ad_id=${adId}`;
        window.location.href = "https://example.com";

    }   """)
gb.configure_column("ad",
                headerName="Advertiser",
                cellStyle={'text-align': 'left', 'font-weight': 'bold', 'font-size': '20px', 'align-content': 'center'},
                #onCellClicked=cell_click_callback,
                cellRenderer=JsCode(
        """
        class UrlCellRenderer {
        init(params) {
            console.log(params);
            this.eGui = document.createElement('a');
            this.eGui.innerText = params.value;
            this.eGui.setAttribute('href', '/campaigns?ad_id=' + params.value);
            this.eGui.setAttribute('style', "text-decoration:none");
            this.eGui.setAttribute('target', "_blank");
        }
        getGui() {
            return this.eGui;
        }
        }
        """
    ),
#      cellRenderer=JsCode("""
#     class ViewDetailRenderer {
#         init(params) {
#             this.eGui = document.createElement('div');
#             this.eGui.innerHTML = `
#                 <button class="btn btn-primary" style="color:white; background-color:#34495e; border:none; padding: 5px 10px; border-radius:4px; cursor:pointer;">View Details</button>
#             `;
#             this.btnClickedHandler = this.btnClickedHandler.bind(this);
#             this.eGui.addEventListener('click', this.btnClickedHandler);
#             this.params = params;
#         }

#         getGui() {
#             return this.eGui;
#         }

#         btnClickedHandler() {
#             const rowData = this.params.node.data;
#             const rowId = rowData.id;
#             const newUrl = `http://localhost:8501/campaigns?ad_id=Coca-cola`;
#             window.parent.location.href = newUrl;
#         }

#         destroy() {
#             this.eGui.removeEventListener('click', this.btnClickedHandler);
#         }
#     }
# """), allow_unsafe_jscode=True,
                width=200)

cell_renderer =  JsCode("""
    class UrlCellRenderer {
    init(params) {
        this.eGui = document.createElement('a');
        this.eGui.innerText = params.value;
        this.eGui.setAttribute('href', "/" + params.data.ad);
        this.eGui.setAttribute('target', "_top");
        
    }
    getGui() {
        return '<a href="/">Hi</a>';
    }
    }
""")
gb.configure_column("budget",
    headerName="Booked Budget",
    cellStyle={'text-align': 'left', 'font-weight': 'bold', 'font-size': '16px','align-content': 'center'},
    width=200)
gb.configure_column("total_campaigns",
    headerName="Total Campaigns",
    cellStyle={'text-align': 'left', 'font-weight': 'bold', 'font-size': '16px', 'align-content': 'center'},
    type="leftAligned",
    filter=False,
    width=200)
gb.configure_column("revenue_risk",
    headerName="Revenue at Risk ($)",
    cellStyle={'text-align': 'left', 'font-weight': 'bold', 'font-size': '16px', 'align-content': 'center'},
    width=200)
gb.configure_column("pending_review",
    headerName="Pending Review",
    type="leftAligned",
    filter=False,
    cellStyle={'text-align': 'left', 'font-weight': 'bold', 'font-size': '16px', 'align-content': 'center'},
    width=200)
gb.configure_column("ready_for_invoice",
    headerName="Ready for Invoice",
    type="leftAligned",
    filter=False,
    cellStyle={'text-align': 'left', 'font-weight': 'bold', 'font-size': '16px', 'align-content': 'center'},
    width=200)
# gb.configure_column("image_path",
#     headerName="",
#     cellStyle={'text-align': 'center'},
#     width=200,
#     cellRenderer=image_nation)
grid_options = gb.build()
grid_options['pagination'] = True
grid_options['paginationAutoPageSize'] = True
# st.markdown(
#     """
#     <style>
#     .ag-header-cell-label {
#         font-size: 42px !important; /* Adjust font size as needed */
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# css = """
# <style>
#     .my-header-class .ag-header-cell-label {
#         justify-content: center !important;
#         font-size: 10px !important;
#     }
# </style>
# """

# st.markdown(css, unsafe_allow_html=True)

grid_response  = AgGrid(filtered_data, gridOptions=grid_options, enable_enterprise_modules=True, theme='light', height=700, fit_columns_on_grid_load=True,
            allow_unsafe_jscode=True, custom_css={
        ".ag-paging-panel": {
            "justify-content": "center", # Change font
            "height": "50px;"
        },
        ".ag-header-cell-label": {
        "font-size": "20px !important;"
    }
    }, data_return_mode='AS_INPUT',
    update_mode=GridUpdateMode.SELECTION_CHANGED)

# if grid_response['selected_rows']:
#         print("All elements are True")
# if grid_response['selected_rows']:
#     selected_row = grid_response['selected_rows'][0] # Get the first selected row
#     st.write("You clicked on a row!")
#     st.write("Selected Row Data:", selected_row)
#     # Perform further actions with the selected_row data
#     # e.g., display a new table, update a chart, etc.

# if 'button_save_crop_disabled' not in st.session_state:
#     st.session_state.button_save_crop_disabled = True
# def enable_button():
#     st.session_state.button_save_crop_disabled = False
#     #st.experimental_rerun()

# @st.dialog("Add Crops Data",width="medium")
# def add_crops_dialog():
#     with st.container(height=700):
#         with st.form("add_data_form"):
#                 crop = st.text_input("Crop", key="crop_input")
