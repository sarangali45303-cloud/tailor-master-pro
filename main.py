import streamlit as st
from modules.database import init_db
from modules.orders import add_order_ui
from modules.ui_styles import apply_custom_ui
from modules.analytics import show_dashboard_stats
from modules.auth import login_system, user_profile_ui

# 1. Page Configuration (Mobile Friendly & Professional)
st.set_page_config(
    page_title="Tailor Master Pro", 
    page_icon="🧵", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. Database Initialize (Create tables if they don't exist)
init_db()

# 3. Session State Management
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "shop_name" not in st.session_state:
    st.session_state.shop_name = "AZAD TAILOR"

# 4. Sidebar - Themes & Styling (Top of the sidebar)
st.sidebar.markdown("<h2 style='text-align: center; color: #FFD700;'>🎨 THEMES</h2>", unsafe_allow_html=True)
theme_choice = st.sidebar.selectbox(
    "Select Interface Style", 
    ["Day Mode", "Night Mode", "Golden Pro", "Fabric Texture"]
)

# Apply CSS Styling (This ensures font visibility for Day/Night)
apply_custom_ui(theme_choice)

# 5. Application Logic Flow
if not st.session_state.logged_in:
    # --- SHOW LOGIN PAGE ---
    login_system()
else:
    # --- LOGGED IN DASHBOARD AREA ---
    
    # Sidebar: Shop Header with Golden Border
    st.sidebar.markdown(
        f"<h1 style='text-align: center; color: #FFD700; border-bottom: 2px solid #FFD700; padding-bottom: 10px;'>🧵 {st.session_state.shop_name}</h1>", 
        unsafe_allow_html=True
    )
    
    # User Profile (Profile Pic & Logout Button)
    user_profile_ui()

    st.sidebar.markdown("<br><h4 style='color: #FFD700; font-weight: bold;'>📌 MAIN MENU</h4>", unsafe_allow_html=True)
    
    # Navigation Radio Menu
    menu = st.sidebar.radio(
        "Navigate", 
        ["📊 Dashboard", "🧵 New Order", "📦 All Orders", "💰 Accounts"]
    )

    # --- PAGES ROUTING ---
    if menu == "📊 Dashboard":
        st.markdown(f"<h2 style='color: #000080;'>📊 {st.session_state.shop_name} - Shop Overview</h2>", unsafe_allow_html=True)
        show_dashboard_stats()

    elif menu == "🧵 New Order":
        # Professional Measurements Form (Tailor Master Layout)
        add_order_ui()

    elif menu == "📦 All Orders":
        st.markdown("<h2 style='color: #000080;'>📦 Order History</h2>", unsafe_allow_html=True)
        st.info("Tamam orders ki list yahan fetch ho rahi hai...")
        # Future function: show_all_orders()

    elif menu == "💰 Accounts":
        st.markdown("<h2 style='color: #000080;'>💰 Daily Accounts Summary</h2>", unsafe_allow_html=True)
        st.write("Daily Income, Advance aur Pending Payments ka record.")

# 6. Sidebar Footer (Separated correctly to avoid SyntaxError)
st.sidebar.markdown("---")
st.sidebar.caption("Tailor Master Pro v1.0 | Powered by Supabase Cloud")