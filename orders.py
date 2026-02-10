import streamlit as st
import json
import uuid
from datetime import date
from database import get_connection, save_order_cloud

def add_order_ui():
    shop = st.session_state.get("shop_name", "Tailor Master")
    st.markdown(f"### 🧵 {shop} - Master Measurement Chart")

    # --- HEADER ---
    c1, c2, c3,c4 = st.columns(4)
    order_no = str(uuid.uuid4())[:6].upper()
    cust_name = c1.text_input("Naam", placeholder="Customer Name")
    phone = c2.text_input("Mobile Number")
    order = c3.date_input("Order Date", date.today())
    delivery = c4.date_input("Delivery Date", date.today())

    st.markdown("---")

    # --- MEASUREMENTS (NAAP) ---
    st.subheader("📏 Measurements (Naap)")
    m1, m2, m3 = st.columns(3)
    
    meas = {}
    with m1:
        meas['len'] = st.text_input("Length (Lambai)")
        meas['slv'] = st.text_input("Sleeves (Asteen)")
        meas['shl'] = st.text_input("Shoulder (Teera)")
        meas['col'] = st.text_input("Collar (Gala)")
        meas['chest'] = st.text_input("Chest (Chaati)")
        meas['l_chest'] = st.text_input("Lower Chest")
    with m2:
        meas['wst'] = st.text_input("Waist (Kamar)")
        meas['hip'] = st.text_input("Hip")
        meas['shl_len'] = st.text_input("Shalwar Length")
        meas['shirt_len'] = st.text_input("Shirt Length")
        meas['bottom'] = st.text_input("Bottom (Paincha)")
        meas['pajama_len'] = st.text_input("Pajama Length")
    with m3:
        meas['paj_wst'] = st.text_input("Pajama Waist")
        meas['paj_hip'] = st.text_input("Pajama Hip")
        meas['thigh'] = st.text_input("Thigh (Raan)")
        meas['paj_bot'] = st.text_input("Pajama Bottom")
        meas['fly'] = st.text_input("Fly")

    st.markdown("---")

    # --- STITCHING OPTIONS (SILAI) ---
    st.subheader("🪡 Stitching Options (Hidayat)")
    s1, s2, s3 = st.columns(3)
    
    styles = {}
    with s1:
        styles['sw_col'] = st.checkbox("Sherwani Collar")
        styles['sh_col'] = st.checkbox("Shirt Collar")
        styles['kur_slv'] = st.checkbox("Kurta Asteen")
        styles['cuf'] = st.checkbox("Cuff Asteen")
        styles['square'] = st.checkbox("Chakor Daman")
        styles['round'] = st.checkbox("Gol Daman")
    with s2:
        styles['side_pocket'] = st.number_input("Side Pocket", 0, 2, 2)
        styles['front_pocket'] = st.checkbox("Chest Pocket")
        styles['shl_pocket'] = st.checkbox("Shalwar Pocket")
        styles['paj_pocket'] = st.checkbox("Pajama Pocket")
        styles['sada'] = st.checkbox("Sada Silai")
        styles['gum'] = st.checkbox("Gum Silai")
        styles['double'] = st.checkbox("Double Silai")
    with s3:
        styles['gher'] = st.checkbox("Shalwar Gher Wali")
        styles['design'] = st.text_input("Design (Details)")
        styles['design_no'] = st.text_input("Design Number")
        fit = st.radio("Fitting", ["Loose", "Normal", "Smart Fit"], index=1)
        styles['fitting'] = fit

    st.markdown("---")
    
    # --- BILLING ---
    b1, b2, b3 = st.columns(3)
    total = b1.number_input("Total Bill", 0)
    adv = b2.number_input("Advance Paid", 0)
    rem = total - adv
    b3.markdown(f"#### Balance: Rs. {rem}")

    if st.button("💾 SAVE ORDER", use_container_width=True, type="primary"):
        if cust_name and phone:
            order_data = {
                "order_no": f"AT-{order_no}",
                "order_date": str(date.today()),
                "delivery_date": str(delivery),
                "customer_name": cust_name,
                "phone_1": phone,
                "total_price": total,
                "advance_paid": adv,
                "remaining_balance": rem,
                "measurements_json": json.dumps(meas),
                "styles_json": json.dumps(styles)
            }
            
            try:
                # 1. Save Locally
                conn = get_connection()
                query = """INSERT INTO orders (order_no, order_date, delivery_date, customer_name, phone_1, 
                           total_price, advance_paid, remaining_balance, measurements_json, styles_json) 
                           VALUES (?,?,?,?,?,?,?,?,?,?)"""
                conn.execute(query, (order_data['order_no'], order_data['order_date'], order_data['delivery_date'], 
                                   order_data['customer_name'], order_data['phone_1'], total, adv, rem, 
                                   order_data['measurements_json'], order_data['styles_json']))
                conn.commit()
                conn.close()
                
                # 2. Sync to Cloud
                success, msg = save_order_cloud(order_data)
                if success: 
                    st.success("Order Saved & Cloud Synced! ✅")
                    st.balloons()
                else: 
                    st.warning(f"Saved Locally. Cloud Sync Pending (Check Keys).")
            except Exception as e:
                st.error(f"Database Error: {e}")
        else:
            st.error("Gahak ka naam aur phone number lazmi hai!")

