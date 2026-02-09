import streamlit as st

def apply_custom_ui(theme_choice, wallpaper_url=None):
    # --- 1. THEME PALETTE (Yahan aap mazeed rang add kar sakte hain) ---
    palettes = {
        "Day Mode": {"bg": "#F0F2F6", "sidebar": "#000033", "card": "#FFFFFF", "pattern": "https://www.transparenttextures.com/patterns/linen.png"},
        "Night Mode": {"bg": "#121212", "sidebar": "#000000", "card": "#1E1E1E", "pattern": "https://www.transparenttextures.com/patterns/dark-leather.png"},
        "Golden Pro": {"bg": "#1C1C1C", "sidebar": "#1A1A1A", "card": "#2D2D2D", "pattern": "https://www.transparenttextures.com/patterns/carbon-fibre.png"},
        "Fabric Texture": {"bg": "#F5F5F5", "sidebar": "#2C3E50", "card": "#FFFFFF", "pattern": "https://www.transparenttextures.com/patterns/linen.png"},
        "Royal Blue": {"bg": "#002366", "sidebar": "#001233", "card": "#003399", "pattern": ""},
        "Classic Wood": {"bg": "#3E2723", "sidebar": "#2D1B18", "card": "#4E342E", "pattern": ""}
    }
    
    p = palettes.get(theme_choice, palettes["Day Mode"])
    navy_blue = "#000080"
    gold = "#FFD700"
    white = "#FFFFFF"
    bg_img = wallpaper_url if wallpaper_url else p['pattern']

    # --- 2. CSS INJECTION ---
    st.markdown(f"""
    <style>
        /* Main Content Text (Navy Blue & Bold) */
        html, body, [class*="st-"], .stMarkdown, p, label {{
            color: {navy_blue} !important;
            font-weight: bold !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}

        /* App Background */
        .stApp {{
            background-color: {p['bg']};
            background-image: url("{bg_img}");
            background-attachment: fixed;
        }}

        /* --- SIDEBAR (Navy Blue Background, White/Gold Text) --- */
        [data-testid="stSidebar"] {{
            background-color: {p['sidebar']} !important;
            border-right: 3px solid {gold};
        }}

        /* Sidebar Text Visibility */
        [data-testid="stSidebarContent"] *, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {{
            color: {white} !important;
        }}

        /* Sidebar Navigation Menu */
        div[data-testid="stSidebar"] .stRadio label {{
            background-color: rgba(255, 255, 255, 0.1);
            color: {gold} !important;
            padding: 10px !important;
            border-radius: 8px !important;
            margin-bottom: 5px !important;
        }}

        /* --- CARDS & METRICS --- */
        .order-card, div[data-testid="metric-container"] {{
            background-color: {p['card']} !important;
            padding: 20px !important;
            border-radius: 15px !important;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.2) !important;
            border-left: 6px solid {navy_blue} !important;
            margin-bottom: 15px !important;
        }}

        div[data-testid="stMetricValue"] {{
            color: {navy_blue} !important;
            font-size: 28px !important;
        }}

        /* --- BUTTONS --- */
        .stButton>button {{
            width: 100%;
            border-radius: 25px;
            background-color: {navy_blue} !important;
            color: white !important;
            border: 2px solid {gold};
            font-weight: bold;
            height: 48px;
        }}
    </style>
    """, unsafe_allow_html=True)
