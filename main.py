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

# 4. Sidebar Themes & Language
st.sidebar.markdown("### ⚙️ Settings")
lang = st.sidebar.selectbox("🌐 Language", ["English", "Roman Urdu", "Sindhi"])
T = get_text(lang)

theme_choice = st.sidebar.selectbox("🎨 Style", ["Day Mode", "Night Mode", "Golden Pro"])
apply_custom_ui(theme_choice)

# 5. Stealth Master Mode (?p=admin786)
is_master_mode = st.query_params.get("p") == "admin786"

# 6. App Logic
if not st.session_state.logged_in:
    login_system()
else:
    # Header with Shop Name
    shop = st.session_state.get("shop_name", "Tailor Master")
    st.sidebar.markdown(f"<h2 style='color:#FFD700; text-align:center;'>🧵 {shop}</h2>", unsafe_allow_html=True)
    
    user_profile_ui()

    st.sidebar.markdown("---")
    menu = st.sidebar.radio(T.get("dash", "Menu"), ["📊 Dashboard", "🧵 New Order", "📦 All Orders", "💰 Accounts"])

    if menu == "📊 Dashboard":
        show_dashboard_stats()
    elif menu == "🧵 New Order":
        add_order_ui()
    elif menu == "📦 All Orders":
        show_all_orders()
    elif menu == "💰 Accounts":
        show_accounts_summary()

    # --- STEALTH MASTER PANEL (Only for SuperAdmin) ---
    if is_master_mode:
        st.sidebar.markdown("---")
        st.sidebar.error("🔐 MASTER ADMIN PANEL")
        
        master_op = st.sidebar.selectbox("Admin Controls", ["System Repair", "View All Shops"])
        
        if master_op == "System Repair":
            st.warning("⚠️ Repair karne se local data delete ho sakta hai.")
            if st.button("🛠️ Full Database Fix"):
                reset_db()
                st.rerun()
        
        elif master_op == "View All Shops":
            st.subheader("👥 Registered Shop Owners (Cloud)")
            from database import supabase
            try:
                res = supabase.table("users").select("username, shop_name, role").execute()
                if res.data:
                    st.table(res.data)
                else:
                    st.info("No shops registered on Cloud yet.")
            except Exception as e:
                st.error(f"Cloud API Error: {e}")

# 7. Sidebar Footer
st.sidebar.markdown("---")
st.sidebar.caption("Tailor Master Pro v1.0 | Powered by Supabase Cloud")
