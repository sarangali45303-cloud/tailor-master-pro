import streamlit as st
from database import init_db
from orders import add_order_ui
from ui_styles import apply_custom_ui
from analytics import show_dashboard_stats
from auth import login_system, user_profile_ui

# 1. Page Configuration (Set only once)
st.set_page_config(
    page_title="Tailor Master Pro", 
    page_icon="🧵", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. Database Initialize
init_db()

# 3. Session State Management
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "shop_name" not in st.session_state:
    st.session_state.shop_name = "Tailor Master"

# 4. Sidebar Themes & Styling
st.sidebar.markdown("<h3 style='text-align: center; color: #FFD700;'>🎨 THEMES</h3>", unsafe_allow_html=True)
theme_choice = st.sidebar.selectbox(
    "Select Style", 
    ["Day Mode", "Night Mode", "Golden Pro", "Fabric Texture"]
)

# Apply CSS Styling based on theme selection
apply_custom_ui(theme_choice)

# 5. Application Logic Flow
if not st.session_state.logged_in:
    # --- SHOW LOGIN & REGISTER PAGE ---
    login_system()
else:
    # --- LOGGED IN AREA ---
    
    # Sidebar: Shop Header with Golden Style
    shop = st.session_state.get("shop_name", "Tailor Master")
    st.sidebar.markdown(
        f"<h1 style='text-align: center; color: #FFD700; border-bottom: 2px solid #FFD700; padding-bottom: 10px;'>🧵 {shop}</h1>", 
        unsafe_allow_html=True
    )
    
    # Show Profile (Pic & Logout)
    user_profile_ui()

    st.sidebar.markdown("<br><h4 style='color: #FFD700;'>📌 MAIN MENU</h4>", unsafe_allow_html=True)
    
    # Navigation Radio Menu
    menu = st.sidebar.radio(
        "Navigate", 
        ["📊 Dashboard", "🧵 New Order", "📦 All Orders", "💰 Accounts"]
    )

    # --- PAGES ROUTING ---
    if menu == "📊 Dashboard":
        st.markdown(f"<h2 style='color: #000080;'>📊 {shop} - Overview</h2>", unsafe_allow_html=True)
        show_dashboard_stats()

    elif menu == "🧵 New Order":
        # Professional Measurements & Billing Form
        add_order_ui()

    elif menu == "📦 All Orders":
        st.markdown("<h2 style='color: #000080;'>📦 Order History</h2>", unsafe_allow_html=True)
        st.info("Fetching all orders from database...")
        # Future function: show_order_list()

    elif menu == "💰 Accounts":
        st.markdown("<h2 style='color: #000080;'>💰 Billing & Accounts</h2>", unsafe_allow_html=True)
        st.write("Daily reports and payment summaries.")

# 6. Sidebar Footer
st.sidebar.markdown("---")
st.sidebar.caption("Tailor Master Pro v1.0 | Powered by Supabase Cloud")
