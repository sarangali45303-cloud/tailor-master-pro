import streamlit as st  # <-- Ye line hona lazmi hai!
from database import init_db
from orders import add_order_ui
from ui_styles import apply_custom_ui
from analytics import show_dashboard_stats, show_all_orders, show_accounts_summary
from auth import login_system, user_profile_ui
from lang_engine import get_text

# 1. Page Settings
st.set_page_config(page_title="Tailor Master Pro v5.0", layout="wide")

# 2. Database Init
init_db()

# 3. Session State
if "lang" not in st.session_state: st.session_state.lang = "English"
if "theme" not in st.session_state: st.session_state.theme = "Day Mode"
if "logged_in" not in st.session_state: st.session_state.logged_in = False

# 4. Sidebar Controls
st.sidebar.title("🛠️ SYSTEM CONTROL")
st.session_state.lang = st.sidebar.selectbox("🌐 Language", ["English", "Roman Urdu", "Sindhi"], 
                                          index=["English", "Roman Urdu", "Sindhi"].index(st.session_state.lang))
st.session_state.theme = st.sidebar.selectbox("🎨 Theme", ["Day Mode", "Night Mode", "Golden Pro"], 
                                           index=["Day Mode", "Night Mode", "Golden Pro"].index(st.session_state.theme))
# main.py ke sidebar section mein theme update karen
theme_choice = st.sidebar.selectbox("🎨 SELECT THEME", 
    ["Natural Linen (Sada)", "Dark Denim (Night)", "Royal Silk (Golden)", "Classic Wood"])
# Apply Theme & Get Translations
apply_custom_ui(st.session_state.theme)
T = get_text(st.session_state.lang)

# 5. App Flow
if not st.session_state.logged_in:
    login_system()
else:
    shop = st.session_state.get("shop_name", "AZAD TAILOR")
    st.sidebar.markdown(f"<h1 style='text-align: center; color: #FFD700;'>🧵 {shop}</h1>", unsafe_allow_html=True)
    user_profile_ui()
    
    st.sidebar.markdown("---")
    menu_options = {
        f"📊 {T['dash']}": "dash",
        f"🧵 {T['new_order']}": "new",
        f"📦 {T['all_orders']}": "history",
        f"💰 {T['acc']}": "acc"
    }
    choice = st.sidebar.radio("NAVIGATE", list(menu_options.keys()))

    page = menu_options[choice]
    
    if page == "dash":
        show_dashboard_stats()
    elif page == "new":
        add_order_ui()
    elif page == "history":
        show_all_orders()
    elif page == "acc":
        show_accounts_summary()

st.sidebar.markdown("---")
st.sidebar.caption(f"v5.0 Master Mode | {st.session_state.lang}")