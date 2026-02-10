import streamlit as st

def apply_custom_ui(theme_choice):
    # --- NATURAL THEMES PALETTE ---
    palettes = {
        "Natural Linen (Sada)": {"bg": "#F5F5DC", "side": "#E8E4C9", "txt": "#4E342E", "img": "https://www.transparenttextures.com/patterns/linen.png"},
        "Dark Denim (Night)": {"bg": "#1A1A1D", "side": "#252839", "txt": "#C5C6C7", "img": "https://www.transparenttextures.com/patterns/denim.png"},
        "Royal Silk (Golden)": {"bg": "#1C1C1C", "side": "#000000", "txt": "#FFD700", "img": "https://www.transparenttextures.com/patterns/carbon-fibre.png"},
        "Classic Wood": {"bg": "#D7CCC8", "side": "#A1887F", "txt": "#3E2723", "img": "https://www.transparenttextures.com/patterns/wood-pattern.png"}
    }
    
    p = palettes.get(theme_choice, palettes["Natural Linen (Sada)"])
    
    st.markdown(f"""
    <style>
        .stApp {{ background-color: {p['bg']}; background-image: url("{p['img']}"); }}
        
        /* SIDEBAR: DARK BLUE REMOVED - Set to Natural/Light */
        [data-testid="stSidebar"] {{
            background-color: {p['side']} !important;
            border-right: 2px solid #FFD700;
        }}
        
        /* Text Visibility */
        h1, h2, h3, label, p, [data-testid="stSidebar"] * {{
            color: {p['txt']} !important;
            font-weight: bold !important;
        }}

        /* VERTICAL BUTTONS FOR LOGIN (Custom Styling) */
        .stButton>button {{
            width: 100%;
            border-radius: 10px;
            height: 50px;
            background-color: #000080 !important;
            color: white !important;
            border: 2px solid #FFD700;
        }}
    </style>
    """, unsafe_allow_html=True)