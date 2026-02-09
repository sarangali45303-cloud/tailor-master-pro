import streamlit as st
import json
import uuid
from datetime import date
from database import get_connection

def add_order_ui():
    shop_name = st.session_state.get("shop_name", "Tailor Master")
    
    st.markdown(f"""
        <style>
        .main-header {{ font-size: 26px; font-weight: bold; color: #000080; text-align: center; margin-bottom: 20px; border-bottom: 2px solid #FFD700; padding-bottom: 10px; }}
        .section-header {{ background-color: #f0f2f6; padding: 5px 15px; border-radius: 5px; margin: 15px 0; font-weight: bold; color: #000080; }}
        </style>
        <div class="main-header">🧵 {shop_name} - Master Measurement Chart</div>
    """, unsafe_allow_html=True)

    # ---------------- HEADER INFO ----------------
    with st.container():
        c1, c2, c3, c4 = st.columns([1.5, 1, 1, 1])
        order_no = str(uuid.uuid4())[:6].upper()
        order_date = c1.date_input("📅 Order Date", date.today())
        delivery_date = c2.date_input("📦 Delivery Date", date.today())
        suits_qty = c3.number_input("No. of Suits", 1, step=1)
        st.text_input("🆔 Order ID", value=f"AT-{order_no}", disabled=True)

    # ---------------- CUSTOMER DETAILS ----------------
    st.markdown('<div class="section-header">👤 Customer Details</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        name = st.text_input("Customer Name (English)")
        phone1 = st.text_input("Primary Mobile Number")
    with col_b:
        name_urdu = st.text_input("Customer Name (Urdu / Sindhi)")
        phone2 = st.text_input("Secondary Mobile / Address")

    st.markdown("---")

    # ---------------- MEASUREMENTS & STITCHING ----------------
    left_col, right_col = st.columns([1, 1.2], gap="large")

    with left_col:
        st.subheader("📏 Measurements (Naap)")
        m1, m2 = st.columns(2)
        meas_labels = [
            ("Length (Lambai)", "42 ½"), ("Sleeves (Asteen)", "25 ½"), ("Shoulder (Teera)", "20 ½"), 
            ("Collar (Gala)", "17 ½"), ("Chest (Chaati)", "48"), ("Waist (Kamar)", "28"), 
            ("Hip", "28"), ("Shalwar Length", "40"), ("Bottom (Paincha)", "20"), ("Shirt Length", "---")
        ]
        measurements = {}
        for i, (label, placeholder) in enumerate(meas_labels):
            target = m1 if i < 5 else m2
            measurements[label] = target.text_input(label, placeholder=placeholder)

    with right_col:
        st.subheader("🪡 Stitching Options")
        styles = {}
        st.markdown("**Types**")
        s1, s2 = st.columns(2)
        styles["shirt_collar"] = s1.checkbox("Shirt Collar", value=True)
        styles["cuff_astin"] = s2.checkbox("Cuff Astin", value=True)
        styles["gol_daman"] = s1.checkbox("Gol Daman", value=True)
        styles["chest_pocket"] = s2.checkbox("Chest Pocket", value=True)
        styles["side_pockets"] = st.number_input("Side Pockets", 0, 5, value=2)

    # ---------------- VERBAL & BILLING ----------------
    st.markdown("---")
    v1, v2 = st.columns(2)
    verbal = v1.text_area("🗣️ Verbal Instructions")
    extra = v2.text_area("➕ Extra Notes")

    st.markdown('<div class="section-header">💰 Billing Details</div>', unsafe_allow_html=True)
    b1, b2, b3 = st.columns(3)
    total = b1.number_input("Total Bill (Rs.)", 0)
    adv = b2.number_input("Advance (Rs.)", 0)
    rem = total - adv
    b3.markdown(f"### Balance: {rem}")

    if st.button("💾 SAVE & SYNC ORDER", use_container_width=True, type="primary"):
        if name and phone1:
            try:
                conn = get_connection()
                conn.execute("""INSERT INTO orders (order_no, order_date, delivery_date, customer_name, customer_name_urdu, 
                             phone_1, phone_2, suit_qty, total_price, advance_paid, remaining_balance, 
                             measurements_json, styles_json, verbal_instructions) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                             (f"AT-{order_no}", str(order_date), str(delivery_date), name, name_urdu, phone1, phone2, 
                              suits_qty, total, adv, rem, json.dumps(measurements), json.dumps(styles), f"{verbal} | {extra}"))
                conn.commit()
                conn.close()
                st.success("✅ Order Saved Locally!")
                st.balloons()
            except Exception as e:
                st.error(f"❌ Database Error: {e}")
        else:
            st.error("⚠️ Name and Phone are required!")
