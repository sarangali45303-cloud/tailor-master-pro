import streamlit as st
# db_cloud se functions import kar rahe hain jo humne pehle fix kiye thay
from db_cloud import verify_login, add_new_user 
from PIL import Image
import io

def login_system():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        st.markdown("<h2 style='text-align: center; color: #000080;'>🔐 TAILOR MASTER PRO v5.0</h2>", unsafe_allow_html=True)
        
        # Options bilkul exact hone chahiye conditions ke sath
        option = st.radio("CHOOSE ACTION:", ["🔑 Login to Shop", "🆕 Register New Shop", "🆘 Account Recovery"])
        st.markdown("---")

        # --- LOGIN SECTION ---
        if option == "🔑 Login to Shop":
            st.subheader("Login to your Shop")
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.button("LOGIN NOW", use_container_width=True):
                user_data = verify_login(u, p)
                if user_data:
                    st.session_state.logged_in = True
                    st.session_state.user_role = user_data[0]
                    st.session_state.shop_name = user_data[1]
                    st.session_state.username = u
                    st.success(f"Welcome back, {u}!")
                    st.rerun()
                else:
                    st.error("Invalid Username or Password")

        # --- REGISTRATION SECTION ---
        elif option == "🆕 Register New Shop":
            st.subheader("Register your New Shop")
            new_u = st.text_input("Choose Username")
            new_p = st.text_input("Choose Password", type="password")
            new_s = st.text_input("Your Shop Name (e.g. Ali Tailors)")
            
            if st.button("CREATE ACCOUNT & LOGIN", use_container_width=True):
                if new_u and new_p and new_s:
                    # db_cloud mein add_new_user function ko call karna
                    success, msg = add_new_user(new_u, new_p, new_s)
                    if success:
                        # --- AUTO LOGIN AFTER REGISTER ---
                        st.session_state.logged_in = True
                        st.session_state.username = new_u
                        st.session_state.shop_name = new_s
                        st.session_state.user_role = 'admin'
                        st.success(f"Shop '{new_s}' Registered Successfully!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(msg)
                else:
                    st.warning("Please fill all details (Username, Password, and Shop Name)")

        # --- RECOVERY SECTION ---
        elif option == "🆘 Account Recovery":
            st.subheader("Help & Support")
            st.info("Contact support at: support@tailormaster.pro to recover your password.")

def user_profile_ui():
    st.sidebar.markdown("---")
    
    if "profile_pic" not in st.session_state:
        st.session_state.profile_pic = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"

    # Display Owner Info
    st.sidebar.image(st.session_state.profile_pic, width=100)
    st.sidebar.write(f"🏪 **{st.session_state.shop_name}**")
    st.sidebar.write(f"👤 Master: {st.session_state.username}")

    # Edit Profile Section
    with st.sidebar.expander("⚙️ Edit Profile"):
        new_name = st.text_input("Edit Shop Name", value=st.session_state.shop_name)
        if st.button("Update Name"):
            st.session_state.shop_name = new_name
            st.success("Shop Name Updated!")
            st.rerun()
            
        uploaded_file = st.file_uploader("Upload Owner Photo", type=["jpg", "png"])
        if uploaded_file:
            st.session_state.profile_pic = uploaded_file
            st.success("Photo Updated!")

    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        # Persistence khatam karne ke liye URL params clear karein
        st.query_params.clear()
        st.rerun()
