import streamlit as st
from database import init_db
from orders import add_order_ui
from ui_styles import apply_custom_ui
from analytics import show_dashboard_stats, show_all_orders, show_accounts_summary
from auth import login_system, user_profile_ui

# 1. Page Configuration
st.set_page_config(page_title="Tailor Master Pro", page_icon="🧵", layout="wide")

# 2. Database Initialize
init_db()

# 3. Session Management
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "shop_name" not in st.session_state:
    st.session_state.shop_name = "Tailor Master"

# 4. Stealth Access Detection (Khufia Code)
# URL ke aakhir mein likhen: ?p=admin786
query_params = st.query_params
is_master_mode = query_params.get("p") == "admin786"

# 5. Theme Selection (Always Visible)
st.sidebar.markdown("<h3 style='text-align: center; color: #FFD700;'>🎨 THEMES</h3>", unsafe_allow_html=True)
theme_choice = st.sidebar.selectbox("Select Style", ["Day Mode", "Night Mode", "Golden Pro", "Fabric Texture"])
apply_custom_ui(theme_choice)

# 6. Login / App Logic
if not st.session_state.logged_in:
    login_system()
else:
    # Sidebar shop header
    shop = st.session_state.get("shop_name", "Tailor Master")
    st.sidebar.markdown(f"<h1 style='text-align: center; color: #FFD700; border-bottom: 2px solid #FFD700;'>🧵 {shop}</h1>", unsafe_allow_html=True)
    
    user_profile_ui()

    st.sidebar.markdown("<br><h4 style='color: #FFD700;'>📌 MAIN MENU</h4>", unsafe_allow_html=True)
    menu = st.sidebar.radio("Navigate", ["📊 Dashboard", "🧵 New Order", "📦 All Orders", "💰 Accounts"])

    # Routing
    if menu == "📊 Dashboard":
        st.markdown(f"## 📊 {shop} Overview")
        show_dashboard_stats()
    elif menu == "🧵 New Order":
        add_order_ui()
    elif menu == "📦 All Orders":
        show_all_orders()
    elif menu == "💰 Accounts":
        show_accounts_summary()

    # --- KHUFIA MASTER PANEL (Stealth Mode) ---
    # Kisi ko nazar nahi ayega, sirf URL code wale ko dikhega
    if is_master_mode:
        st.sidebar.markdown("---")
        st.sidebar.error("🔐 MASTER ADMIN PANEL")
        admin_op = st.sidebar.selectbox("Master Control", ["View All Tailors", "System Reset", "Cloud Status"])
        if admin_op == "View All Tailors":
            st.subheader("👥 Registered Shop Owners")
            st.info("Listing all registered shops from Supabase...")
