import streamlit as st
from database import init_db, reset_db
from orders import add_order_ui
from ui_styles import apply_custom_ui
from analytics import show_dashboard_stats, show_all_orders, show_accounts_summary
from auth import login_system, user_profile_ui
from lang_engine import get_text # Purani translations file

# 1. Page Configuration
st.set_page_config(page_title="Tailor Master Pro", page_icon="🧵", layout="wide")

# 2. Database Initialize
init_db()

# 3. Session Management
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 4. Multi-Language Selection (SIDEBAR)
lang = st.sidebar.selectbox("🌐 Language / زبان", ["English", "Roman Urdu", "Sindhi"])
T = get_text(lang) # Translation dictionary

# 5. Stealth Master Access
query_params = st.query_params
is_master_mode = query_params.get("p") == "admin786"

# 6. Theme Selection
theme_choice = st.sidebar.selectbox("🎨 Style", ["Day Mode", "Night Mode", "Golden Pro"])
apply_custom_ui(theme_choice)

if not st.session_state.logged_in:
    login_system()
else:
    shop = st.session_state.get("shop_name", "Tailor Master")
    st.sidebar.markdown(f"### 🧵 {shop}")
    user_profile_ui()

    st.sidebar.markdown(f"#### 📌 {T['title']}")
    menu = st.sidebar.radio("Navigate", ["📊 Dashboard", "🧵 New Order", "📦 All Orders", "💰 Accounts"])

    if menu == "📊 Dashboard":
        show_dashboard_stats()
    elif menu == "🧵 New Order":
        add_order_ui()
    elif menu == "📦 All Orders":
        show_all_orders()
    elif menu == "💰 Accounts":
        show_accounts_summary()

    # --- MASTER PANEL ---
    if is_master_mode:
        st.sidebar.markdown("---")
        st.sidebar.error("🔐 MASTER PANEL")
        if st.sidebar.button("🛠️ RESET DATABASE (Fix Order Date Error)"):
            reset_db()
        
        master_op = st.sidebar.selectbox("Control", ["View Shops", "Cloud Status"])
        if master_op == "View Shops":
            st.subheader("👥 Registered Tailors")
            # Database se shops fetch karne ka logic
