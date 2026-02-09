import streamlit as st
from database import verify_login, add_new_user

def login_system():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        st.markdown("<h2 style='text-align: center; color: #000080;'>🔐 TAILOR MASTER SYSTEM</h2>", unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["🔑 Login", "🆕 Create Account", "🆘 Recovery"])
        
        with tab1:
            u = st.text_input("Username", key="l_u")
            p = st.text_input("Password", type="password", key="l_p")
            if st.button("Login Now", use_container_width=True):
                user_data = verify_login(u, p)
                if user_data:
                    st.session_state.logged_in = True
                    st.session_state.user_role = user_data[0]
                    st.session_state.shop_name = user_data[1] # Ye shop name set ho gaya
                    st.session_state.username = u
                    st.rerun()
                else:
                    st.error("Invalid Username or Password")

        with tab2:
            st.subheader("Register Your Shop")
            new_u = st.text_input("Choose Username", key="r_u")
            new_p = st.text_input("Choose Password", type="password", key="r_p")
            new_s = st.text_input("Shop Name (e.g. Zaryan Tailors)", key="r_s")
            
            if st.button("Create My Account", use_container_width=True):
                if new_u and new_p and new_s:
                    success, msg = add_new_user(new_u, new_p, new_s)
                    if success: st.success(msg)
                    else: st.error(msg)
                else:
                    st.warning("Please fill all fields")

        with tab3:
            st.info("Mobile recovery service coming soon.")

def user_profile_ui():
    st.sidebar.markdown("---")
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=70)
    st.sidebar.write(f"👤 **User:** {st.session_state.username}")
    st.sidebar.write(f"🏪 **Shop:** {st.session_state.shop_name}")
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()
