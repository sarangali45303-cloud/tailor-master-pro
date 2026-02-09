import streamlit as st
import urllib.parse

def generate_receipt_ui(order_data):
    st.success("Order Saved!")
    
    # WhatsApp Message Format
    msg = f"""
    *AZAD TAILORS - RECEIPT*
    Customer: {order_data['name']}
    Total Bill: {order_data['total']}
    Advance: {order_data['advance']}
    Remaining: {order_data['rem']}
    Delivery Date: {order_data['delivery']}
    """
    encoded_msg = urllib.parse.quote(msg)
    wa_link = f"https://wa.me/{order_data['phone']}?text={encoded_msg}"

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<a href="{wa_link}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px;">Send WhatsApp</button></a>', unsafe_allow_html=True)
    
    with col2:
        if st.button("🖨️ Print Thermal Receipt"):
            st.info("Thermal Printer Command Sent!")
            # Yahan thermal printer ka ESC/POS code ayega