import streamlit as st

def apply_styling(shop_name: str):
    # Page config (Streamlit 1.30+ safe)
    st.set_page_config(
        page_title=shop_name,
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown(f"""
    <style>
    /* Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');

    /* Base App Styling */
    html, body, [class*="css"] {{
        font-family: 'Poppins', sans-serif;
        background-color: #0f1116;
    }}

    /* Remove Streamlit default padding */
    .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }}

    /* Top Branding */
    .company-header {{
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 2px;
        margin-bottom: 5px;
    }}

    .shop-title {{
        color: #d4af37;
        font-size: 38px;
        font-weight: 800;
        text-align: center;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.5);
        margin-bottom: 25px;
    }}

    /* Metric Cards */
    .stMetric {{
        background: rgba(255, 255, 255, 0.05);
        padding: 18px;
        border-radius: 14px;
        border: 1px solid rgba(58, 123, 213, 0.6);
        box-shadow: 0 8px 20px rgba(0,0,0,0.35);
    }}

    /* Buttons */
    .stButton > button {{
        border-radius: 8px;
        font-weight: 600;
    }}

    /* WhatsApp Button */
    .whatsapp-btn {{
        background-color: #25D366;
        color: white !important;
        padding: 10px 18px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }}

    .whatsapp-btn:hover {{
        background-color: #1ebe5d;
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }}

    </style>

    <div class="company-header">
        POWERED BY SAHIL & ARMAN IT COMPANY
    </div>
    <div class="shop-title">
        {shop_name}
    </div>
    """, unsafe_allow_html=True)
# main.py mein
from modules.styling import apply_styling

# Sidebar se theme select ho
theme_choice = st.sidebar.selectbox("Select Design", ["Day Mode", "Night Mode", "Fabric Texture", "Wooden Shop", "Golden Pro"])
apply_styling(theme_choice)