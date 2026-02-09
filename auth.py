import streamlit as st
from database import verify_login, add_new_user

def login_system():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        # Sidebar Branding (Login se pehle bhi nazar aye)
        st.sidebar.markdown("---")
        st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3232/3232448.png", width=100)
        st.sidebar.subheader("Tailor Master Pro v1.0")
        st.sidebar.info("Welcome! Please Login or Register to manage your shop.")

        st.markdown("<h2 style='text-align: center;'>🔐 AZAD TAILOR SYSTEM</h2>", unsafe_allow_html=True)
        
        # TEEN TABS: Login, Register, Recovery
        tab1, tab2, tab3 = st.tabs(["Login", "Create Account", "Recovery"])
        
        with tab1:
            email = st.text_input("Username", key="login_user")
            pwd = st.text_input("Password", type="password", key="login_pass")
            if st.button("Login Now", use_container_width=True):
                user_data = verify_login(email, pwd)
                if user_data:
                    st.session_state.logged_in = True
                    st.session_state.user_role = user_data[0]
                    st.session_state.shop_name = user_data[1]
                    st.session_state.username = email
                    st.rerun()
                else:
                    st.error("Ghalat Username ya Password")

        with tab2:
            st.subheader("🆕 Register Your Shop")
            new_u = st.text_input("Choose Username", key="reg_user")
            new_p = st.text_input("Choose Password", type="password", key="reg_pass")
            new_s = st.text_input("Shop Name (e.g. AZAD TAILORS)", key="reg_shop")
            
            if st.button("Create My Account", use_container_width=True):
                if new_u and new_p and new_s:
                    success, msg = add_new_user(new_u, new_p, new_s)
                    if success: st.success(msg)
                    else: st.error(msg)
                else:
                    st.warning("Tamam khane (fields) bharen.")

        with tab3:
            st.info("Apna registered mobile number likhen recovery ke liye.")
            recovery_mob = st.text_input("Mobile Number")
            if st.button("Get Password"):
                st.warning("Password SMS service abhi activate nahi hui.")
                import streamlit as st
from modules.database import verify_login, add_new_user
from PIL import Image

def login_system():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        st.markdown("<h2 style='text-align: center; color: #000080;'>🔐 AZAD TAILOR SYSTEM</h2>", unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Login", "Create Account", "Recovery"])
        
        with tab1:
            email = st.text_input("Username", key="login_user")
            pwd = st.text_input("Password", type="password", key="login_pass")
            if st.button("Login Now", use_container_width=True):
                user_data = verify_login(email, pwd)
                if user_data:
                    st.session_state.logged_in = True
                    st.session_state.user_role = user_data[0]
                    st.session_state.shop_name = user_data[1]
                    st.session_state.username = email
                    st.rerun()
                else:
                    st.error("Ghalat Username ya Password")

        with tab2:
            st.subheader("🆕 Register Your Shop")
            new_u = st.text_input("Choose Username", key="reg_user")
            new_p = st.text_input("Choose Password", type="password", key="reg_pass")
            new_s = st.text_input("Shop Name", key="reg_shop")
            if st.button("Create My Account", use_container_width=True):
                if new_u and new_p and new_s:
                    success, msg = add_new_user(new_u, new_p, new_s)
                    if success: st.success(msg)
                    else: st.error(msg)

        with tab3:
            st.info("Recovery option jald aa raha hai.")

def user_profile_ui():
    """Sidebar mein user ki info dikhane ke liye"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("<h3 style='color: #000080;'>👤 My Profile</h3>", unsafe_allow_html=True)
    
    # Default Image
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    
    st.sidebar.markdown(f"<b style='color: #000080;'>User:</b> {st.session_state.username}", unsafe_allow_html=True)
    st.sidebar.markdown(f"<b style='color: #000080;'>Shop:</b> {st.session_state.shop_name}", unsafe_allow_html=True)
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False

        st.rerun()
