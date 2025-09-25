import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import math
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
if "selected_advertiser" in st.session_state:
    selected_advertiser = st.session_state["selected_advertiser"]
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
#query_ads = st.query_params["ad_id"] if "ad_id" in st.query_params else None
query_ads =  selected_advertiser.get("ad")[0]

selected_campaign_ad_id = "No Campaign Selected"
# if "selected_camp_from_ad" in st.session_state and st.session_state["selected_camp_from_ad"]:
#     selected_campaign_ad_id = st.session_state.get("selected_camp_from_ad", "No Campaign Selected")
    #st.write(f"Selected Campaign from Advertisers Page: {selected_campaign}")
if query_ads is not None:
    selected_campaign_ad_id = query_ads
else:
    selected_campaign_ad_id = "No Campaign Selected"

def get_status_icons():
    return [
        {"name": "ready",  "logo": "assets/green_tick.png"},
        {"name": "pending", "logo": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg"},
        {"name": "escalated", "logo": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg"},
    ]

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

with st.container(key="campaign_banner_container"):

    col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 1.5, 1.5, 1, 1, 1, 1])

# Example content for each column
    with col1:
        # inner_column = st.columns([1])
        # # with inner_column[0]:
        # #     st.image("assets/coke.jpg",  width=100)
        # with inner_column[1]:
        st.subheader(selected_advertiser.get('ad')[0])

    with col2:
        st.markdown("Booked Budget ($)")
        budget = selected_advertiser.get('budget')[0]
        st.write(f"<bold style='font-weight:bold'>{budget}</bold>", unsafe_allow_html=True)

    with col3:
        st.markdown("Revenue at Risk ($)")
        revenue_risk = selected_advertiser.get('revenue_risk')[0]
        st.write(f"<bold style='font-weight:bold'>{revenue_risk}</bold>", unsafe_allow_html=True)

    with col4:
        st.markdown("Total Campaigns")
        total_campaigns = selected_advertiser.get('total_campaigns')[0]
        st.write(f"<bold style='font-weight:bold'>{total_campaigns}</bold>", unsafe_allow_html=True)

    with col5:
        st.markdown("Ready for Invoice")
        ready_for_invoice = selected_advertiser.get('ready_for_invoice')[0]
        st.write(f"<bold style='font-weight:bold'>{ready_for_invoice}</bold>", unsafe_allow_html=True)

    with col6:
        st.markdown("Pending Review")
        pending_review = selected_advertiser.get('pending_review')[0]
        st.write(f"<bold style='font-weight:bold'>{pending_review}</bold>", unsafe_allow_html=True)

    with col7:
        st.markdown("Escalated")
        st.write(f"<bold style='font-weight:bold'>0</bold>", unsafe_allow_html=True)



conn = st.connection("postgresql", type="sql")
params = {'id_param': "ADV_"+selected_campaign_ad_id.upper()}

#df = conn.query('SELECT campaign_name, campaign_id, number_of_impression, pacing_target_impressions, start_date, end_date,  gap_percent, revenue_at_risk, status FROM campaign_metrics where advertiser_id = :id_param', ttl="10m", params=params)
df = conn.query('SELECT * FROM campaign_metrics where advertiser_id = :id_param', ttl="10m", params=params)

st.markdown('<h4 class="data-grid-title">Campaigns</h4>', unsafe_allow_html=True)
# df = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/airline-safety/airline-safety.csv')

# df['flight_date'] = df['start_date'] + '-' + df['end_date']

# grid_options_df = {
#        "columnDefs": [
#            {"field": "flight_date", "headerName": "Flight date"},
#            {"field": "campaign_name", "headerName": "Campaign Name"},
#            # Optionally hide original columns
#            {"field": "start_date", "hide": True},
#            {"field": "end_date", "hide": True},
#        ]
#    }
# st.markdown(
#     """
#     <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css">
#     """,
#     unsafe_allow_html=True
# )
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">', unsafe_allow_html=True)

thousand_separator_formatter = JsCode("""
    function(params) {
        if (params.value == null) {
            return params.value;
        }
        const mValue = Math.round(Number(params.value));
        return mValue.toLocaleString('en-US'); 
    }
""")


gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_selection('single', use_checkbox=False)

gb.configure_column("campaign_name",
                headerName="Campaign Name",
                cellStyle={'text-align': 'left', 'font-weight': 'bold', 'font-size': '14px', 'align-content': 'center'},
    #             cellRenderer=JsCode(
    #     """
    #     class UrlCellRenderer {
    #       init(params) {
    #         console.log(params);
    #         this.eGui = document.createElement('a');
    #         this.eGui.innerText = params.value;
    #         this.eGui.setAttribute('target', "_blank");
    #         this.eGui.setAttribute('href', '/campaign-details?cid=' + params.value);
    #         this.eGui.setAttribute('style', "text-decoration:none");
    #       }
    #       getGui() {
    #         return this.eGui;
    #       }
    #     }
    #     """
    # ),
                width=180)
gb.configure_column("number_of_impression",
                headerName="Booked Impressions",
                type="leftAligned",
                valueFormatter=thousand_separator_formatter,
                cellStyle={'text-align': 'left', 'font-size': '14px', 'align-content': 'center'},
                width=150)
gb.configure_column("pacing_target_impressions",
                headerName="Delivered Impressions",
                type="leftAligned",
                valueFormatter=thousand_separator_formatter,
                cellStyle={'text-align': 'left', 'font-size': '14px', 'align-content': 'center'},
                width=150)


# gb.configure_column("flight_date",
#                 headerName="Flight Date",
#                 type="leftAligned",
#                 valueFormatter="params.data.gap_percent + ' - ' + params.data.end_date.toLocaleDateString()",
#                 cellStyle={'text-align': 'left', 'font-size': '14px', 'align-content': 'center'},
#                 width=150)
gb.configure_column("start_date", 
headerName="Flight Date",
    cellRenderer=JsCode(
        """
        class UrlCellRenderer {
        init(params) {
            this.eGui = document.createElement('div');
            this.eGui.innerText = params.data.start_date.toLocaleDateString() + " - " + params.data.end_date.toLocaleDateString();
            
            console.log(params.data.start_date.toLocaleDateString() + "-" + params.data.end_date.toLocaleDateString());
        }
        getGui() {
            return this.eGui;
        }
        }
        """
    ),
    cellStyle={'text-align': 'left', 'font-size': '14px', 'align-content': 'center'},
    width=150)



gb.configure_column("gap_percent",
                headerName="Gap %",
                type="leftAligned",
                valueFormatter=thousand_separator_formatter,
                cellStyle={'text-align': 'left', 'font-size': '14px', 'align-content': 'center'},
                width=150)
gb.configure_column("revenue_at_risk",
                headerName="Revenue at Risk ($)",
                type="leftAligned",
                valueFormatter=thousand_separator_formatter,
                cellStyle={'text-align': 'left', 'font-size': '14px', 'align-content': 'center'},
                width=150)
gb.configure_column("status",
                headerName="Status",
                cellRenderer=JsCode(
        """
        class StatusRenderer {
        init(params) {
            
            var element = document.createElement("div"); // Parent element for image and text
            var element2 = document.createElement("span");
            var textElement = document.createElement("span");

            const imageElement = document.createElement('img');
            
            
            imageElement.setAttribute('src', "../assets/green_tick.png");
            imageElement.setAttribute('width', '30');
            imageElement.setAttribute('height', '30');

            textElement.innerText = params.value; // params.value is the cell's main value
            element2.insertAdjacentHTML('beforeend', ('<i class="fa-solid fa-check" style="color: #24f057;"></i>'));
            /* ('<i class="fa-solid fa-check" style="color: #24f057;"></i>'); */
            /* element.insertHTML('beforeend', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640"><!--!Font Awesome Free v7.0.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2025 Fonticons, Inc.--><path fill="#24f057" d="M530.8 134.1C545.1 144.5 548.3 164.5 537.9 178.8L281.9 530.8C276.4 538.4 267.9 543.1 258.5 543.9C249.1 544.7 240 541.2 233.4 534.6L105.4 406.6C92.9 394.1 92.9 373.8 105.4 361.3C117.9 348.8 138.2 348.8 150.7 361.3L252.2 462.8L486.2 141.1C496.6 126.8 516.6 123.6 530.9 134z"/></svg>');*/
            element.appendChild(imageElement);
            element.appendChild(textElement);
            this.eGui = element;

        }
        getGui() {
            return this.eGui;
        }
        }
        """
    ),
                cellStyle={'text-align': 'left', 'font-size': '14px', 'align-content': 'center'},
                width=150)
#gb.configure_column("start_date", hide=True) # Hide original date columns
gb.configure_column("end_date", hide=True)
gb.configure_column("campaign_id", hide=True)
gb.configure_column("booked_budget", hide=True)
#gb.configure_column("pacing_target_impressions", hide=True)
gb.configure_column("pacing_target_spend", hide=True)
#gb.configure_column("number_of_impression", hide=True)
gb.configure_column("number_of_3p_measurements", hide=True)
gb.configure_column("number_of_dsp_delivery", hide=True)
gb.configure_column("number_of_ssp_delivery", hide=True)
gb.configure_column("number_of_lineitem", hide=True)
gb.configure_column("updated_at", hide=True)
gb.configure_column("adserver_creative_viewability_rate", hide=True)
gb.configure_column("publisher_name", hide=True)
gb.configure_column("tp_creative_viewability_rate", hide=True)
gb.configure_column("dsp_creative_viewability_rate", hide=True)
gb.configure_column("ssp_creative_viewable_impressions", hide=True)
gb.configure_column("deal_type", hide=True)
gb.configure_column("advertiser_id", hide=True)
gb.configure_column("end_date", hide=True)
gb.configure_column("billed_impressions", hide=True)
gb.configure_column("end_date", hide=True)
gb.configure_column("matching_status", hide=True)

gb.configure_grid_options(rowHeight=45, tooltipShowDelay=0, tooltipHideDelay=2000, cellStyle={'text-align': 'center'},configure_selectable=True, applyColumnDefOrder=False)

grid_options = gb.build()
grid_options['pagination'] = True
grid_options['paginationAutoPageSize'] = True



grid_response = AgGrid(df, gridOptions=grid_options, enable_enterprise_modules=True, theme='light', height=500, fit_columns_on_grid_load=True,data_return_mode='AS_INPUT',
    update_mode=GridUpdateMode.SELECTION_CHANGED,
            allow_unsafe_jscode=True, custom_css={
        ".ag-paging-panel": {
            "justify-content": "center", # Change font
            "height": "50px;"
        },
        ".ag-header-cell-label": {
        "font-size": "15px !important;"
     },
      ".ag-row-hover": {
        "cursor": "pointer !important;"
    },
    })

    # mid, mid, col_right = st.columns([1, 2, 1])


    # with col_right:
    # Wide button aligned to the right

  
st.markdown("""<style>
    .st-key-footer_container {
        display: flex;
        justify-content: end;
        flex-direction: row;
    }
    .st-key-footer_container .stPageLink {
        width: 100%;
        background-color: #C0C0C0;
        border: 1px solid #d1d5db; /* Light gray border */
        padding: 10px 30px;
        border-radius: 8px;
    }
    .st-key-footer_container .stPageLink p{
        font-weight: bold;
        color: #111111;
    }
    </style>""", unsafe_allow_html=True)
with st.container(key="footer_container"):
    st.page_link("pages/advertiser.py", label="Back to Advertisers")
 
if grid_response['selected_rows'] is not None:
    selected_rows = grid_response['selected_rows']
    if selected_rows is not None and not selected_rows.empty:
            st.session_state["selected_campaign"] = selected_rows
            st.switch_page("pages/campaign-details.py")