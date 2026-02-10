import streamlit as st
from database import init_db, reset_db
from orders import add_order_ui
from ui_styles import apply_custom_ui
from analytics import show_dashboard_stats, show_all_orders, show_accounts_summary
from auth import login_system, user_profile_ui
from lang_engine import get_text

# 1. Page Configuration
st.set_page_config(page_title="Tailor Master Pro", page_icon="🧵", layout="wide")

# 2. Database Initialize
init_db()

# 3. Session Management
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 4. Multi-Language Selection
lang = st.sidebar.selectbox("🌐 Language / زبان", ["English", "Roman Urdu", "Sindhi"])
T = get_text(lang)

# 5. Stealth Master Access (?p=admin786)
query_params = st.query_params
is_master_mode = query_params.get("p") == "admin786"

# 6. Theme Selection
theme_choice = st.sidebar.selectbox("🎨 Style", ["Day Mode", "Night Mode", "Golden Pro"])
apply_custom_ui(theme_choice)

# 7. App Logic
if not st.session_state.logged_in:
    login_system()
else:
    shop = st.session_state.get("shop_name", "Tailor Master")
    st.sidebar.markdown(f"### 🧵 {shop}")
    user_profile_ui()

    st.sidebar.markdown(f"#### 📌 Menu")
    menu = st.sidebar.radio("Navigate", ["📊 Dashboard", "🧵 New Order", "📦 All Orders", "💰 Accounts"])

    if menu == "📊 Dashboard":
        show_dashboard_stats()
    elif menu == "🧵 New Order":
        add_order_ui()
    elif menu == "📦 All Orders":
        show_all_orders()
    elif menu == "💰 Accounts":
        show_accounts_summary()

    # --- STEALTH MASTER PANEL ---
    if is_master_mode:
        st.sidebar.markdown("---")
        st.sidebar.error("🔐 MASTER ADMIN PANEL")
        
        # FIX FOR ORDER_DATE ERROR
        if st.sidebar.button("🛠️ Fix Database (Fix Order Date Error)"):
            reset_db()
            st.sidebar.success("Database Fixed! Restarting...")
            st.rerun()

        master_op = st.sidebar.selectbox("Master Control", ["View All Shops", "System Status"])
        
        if master_op == "View All Shops":
            st.subheader("👥 Registered Shop Owners (Cloud)")
            from database import supabase
            try:
                res = supabase.table("users").select("username, shop_name, role").execute()
                st.table(res.data)
            except:
                st.info("No shops found or API Key error.")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("Tailor Master Pro v1.0 | Powered by Supabase Cloud")
