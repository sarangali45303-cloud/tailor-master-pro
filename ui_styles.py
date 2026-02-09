import streamlit as st

def apply_custom_ui(theme_choice, wallpaper_url=None):
    # --- 1. SET COLORS & DESIGN VARIABLES ---
    navy_blue = "#000080"      # Main Content Fonts
    gold_color = "#FFD700"     # Sidebar Highlights
    sidebar_bg = "#000033"     # Deep Navy Sidebar
    white = "#FFFFFF"
    
    # Theme specific settings
    if theme_choice == "Night Mode":
        main_bg = "#121212"; card_bg = "#1e1e1e"
        pattern = "https://www.transparenttextures.com/patterns/dark-leather.png"
    elif theme_choice == "Golden Pro":
        main_bg = "#1c1c1c"; card_bg = "#2d2d2d"
        pattern = "https://www.transparenttextures.com/patterns/carbon-fibre.png"
    elif theme_choice == "Fabric Texture":
        main_bg = "#f5f5f5"; card_bg = "#ffffff"
        pattern = "https://www.transparenttextures.com/patterns/linen.png"
    else: # Day Mode
        main_bg = "#f0f2f6"; card_bg = "#ffffff"
        pattern = ""

    # Wallpaper override
    bg_img = wallpaper_url if wallpaper_url else pattern

    # --- 2. THE ULTIMATE CSS ---
    st.markdown(f"""
    <style>
        /* Global Font Visibility (Navy Blue & Bold) */
        html, body, [class*="st-"], .stMarkdown, p, label {{
            color: {navy_blue} !important;
            font-weight: bold !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}

        /* Main App Background */
        .stApp {{
            background-color: {main_bg};
            background-image: url("{bg_img}");
            background-attachment: fixed;
        }}

        /* --- SIDEBAR VISIBILITY (DARK NAVY & GOLD) --- */
        [data-testid="stSidebar"] {{
            background-color: {sidebar_bg} !important;
            border-right: 3px solid {gold_color};
        }}

        /* Make everything in sidebar WHITE/GOLD */
        [data-testid="stSidebarContent"] *, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {{
            color: {white} !important;
        }}

        /* Sidebar Radio Menu (Navigate) Styling */
        div[data-testid="stSidebar"] .stRadio label {{
            background-color: rgba(255, 255, 255, 0.1);
            color: {gold_color} !important;
            padding: 12px !important;
            border-radius: 8px !important;
            margin-bottom: 8px !important;
            font-size: 16px !important;
            transition: 0.3s;
        }}
        
        div[data-testid="stSidebar"] .stRadio label:hover {{
            background-color: rgba(255, 215, 0, 0.2);
        }}

        /* --- CARDS & METRICS --- */
        .order-card, div[data-testid="metric-container"] {{
            background-color: {card_bg} !important;
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
            border: 2px solid {gold_color};
            font-weight: bold;
            height: 48px;
            transition: 0.3s;
        }}
        
        .stButton>button:hover {{
            background-color: #0000CD !important;
            transform: translateY(-2px);
            box-shadow: 0px 4px 10px {gold_color};
        }}

        /* Profile Image Border */
        .stSidebar [data-testid="stImage"] {{
            border: 3px solid {gold_color};
            border-radius: 50%;
        }}
    </style>
    """, unsafe_allow_html=True)

def apply_tailor_theme(choice):
    # Backward compatibility
    apply_custom_ui(choice)