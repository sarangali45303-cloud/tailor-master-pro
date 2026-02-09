import streamlit as st

def apply_custom_ui(theme_choice, wallpaper_url=None):
    # --- 1. THEME PALETTE ---
    palettes = {
        "Day Mode": {"bg": "#F0F2F6", "sidebar": "#F8F9FA", "text": "#333333", "accent": "#007BFF"},
        "Night Mode": {"bg": "#121212", "sidebar": "#1E1E1E", "text": "#E0E0E0", "accent": "#FFD700"},
        "Golden Pro": {"bg": "#1C1C1C", "sidebar": "#262626", "text": "#FFD700", "accent": "#FFD700"},
    }
    
    p = palettes.get(theme_choice, palettes["Day Mode"])
    # Hum dark blue ki jagah theme ka text color use karenge
    main_text = p['text']
    accent_color = p['accent']

    st.markdown(f"""
    <style>
        /* Main Background */
        .stApp {{
            background-color: {p['bg']};
            background-image: url("{wallpaper_url if wallpaper_url else ""}");
            background-attachment: fixed;
        }}

        /* --- SIDEBAR CLEAN LOOK (Blue Background Deleted) --- */
        [data-testid="stSidebar"] {{
            background-color: {p['sidebar']} !important;
            border-right: 1px solid rgba(0,0,0,0.1);
        }}

        /* --- REMOVE "keyboard_double" & ADD ARROW ICON --- */
        /* Ye code sidebar ke top header se faltu text hatayega aur arrow lagayega */
        [data-testid="stSidebarNav"]::before {{
            content: "◀ MENU"; /* Aap yahan ⬅ bhi laga sakte hain */
            font-size: 20px;
            font-weight: bold;
            color: {accent_color};
            display: block;
            padding: 20px;
            border-bottom: 1px solid rgba(0,0,0,0.1);
        }}

        /* Faltu text (keyboard_double) ko hide karne ke liye */
        header[data-testid="stHeader"] {{
            background-color: rgba(0,0,0,0) !important;
        }}

        /* Sidebar Text Colors */
        [data-testid="stSidebarContent"] *, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {{
            color: {main_text} !important;
            font-weight: bold;
        }}

        /* Radio Buttons Menu Visibility */
        div[data-testid="stSidebar"] .stRadio label {{
            background-color: rgba(0, 0, 0, 0.03);
            color: {main_text} !important;
            padding: 8px 15px;
            border-radius: 8px;
            margin-bottom: 5px;
            border-left: 3px solid transparent;
        }}
        
        div[data-testid="stSidebar"] .stRadio label:hover {{
            border-left: 3px solid {accent_color};
            background-color: rgba(0, 0, 0, 0.05);
        }}

        /* Main Content Titles */
        h1, h2, h3, label, .stMarkdown p {{
            color: {main_text} !important;
            font-weight: bold !important;
        }}

        /* Buttons Styling */
        .stButton>button {{
            background-color: {accent_color} !important;
            color: #000 !important;
            border-radius: 10px;
            font-weight: bold;
            border: none;
        }}
    </style>
    """, unsafe_allow_html=True)

def apply_tailor_theme(choice):
    apply_custom_ui(choice)
