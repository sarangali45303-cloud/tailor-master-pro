import streamlit as st
import json
import uuid
from datetime import date
from database import get_connection

def add_order_ui():
    # CSS for making it look more like a professional form
    st.markdown("""
        <style>
        .main-header { font-size: 24px; font-weight: bold; color: #3b8ed0; text-align: center; margin-bottom: 20px; }
        .section-header { background-color: #f0f2f6; padding: 5px 15px; border-radius: 5px; margin: 15px 0; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-header">🧵 () Master Measurement Chart</div>', unsafe_allow_html=True)

    # ---------------- HEADER INFO ----------------
    with st.container():
        c1, c2, c3, c4 = st.columns([1.5, 1, 1, 1])
        order_no = str(uuid.uuid4())[:6].upper()
        order_date = c1.date_input("📅 Order Date", date.today())
        delivery_date = c2.date_input("📦 Delivery Date", date.today())
        suits_qty = c3.number_input("No. of Suits", 1, step=1)
        order_id_display = c4.text_input("🆔 Order ID", value=f"AT-{order_no}", disabled=True)

    # ---------------- CUSTOMER DETAILS ----------------
    st.markdown('<div class="section-header">👤 Customer Details</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("Customer Name (English)")
        phone1 = st.text_input("Primary Mobile Number")
    with c2:
        name_urdu = st.text_input("Customer Name (Urdu / Sindhi)")
        phone2 = st.text_input("Secondary Mobile / Address")

    st.markdown("---")

    # ---------------- MAIN LAYOUT: LEFT (NAAP) | RIGHT (STYLE) ----------------
    left_col, right_col = st.columns([1, 1.2], gap="large")

    # --- LEFT SIDE: MEASUREMENTS (NAAP) ---
    with left_col:
        st.subheader("📏 Measurements (Naap)")
        m1, m2 = st.columns(2)
        
        # Labels mapping for database consistency
        meas_labels = [
            ("Length (Lambai)", "42 ½"), ("Sleeves (Asteen)", "25 ½"), 
            ("Shoulder (Teera)", "20 ½"), ("Collar (Gala)", "17 ½"), 
            ("Chest (Chaati)", "48"), ("Waist (Kamar)", "28"), 
            ("Hip", "28"), ("Shalwar Length", "40"), 
            ("Bottom (Paincha)", "20"), ("Shirt Length", "---")
        ]
        
        measurements = {}
        for i, (label, placeholder) in enumerate(meas_labels):
            target_col = m1 if i < 5 else m2
            measurements[label] = target_col.text_input(label, placeholder=placeholder)

        # Extra Naaps
        st.write("**Other Measurements**")
        e1, e2 = st.columns(2)
        measurements["Pajama Length"] = e1.text_input("Pajama Length")
        measurements["Thigh (Raan)"] = e2.text_input("Thigh (Raan)")

    # --- RIGHT SIDE: STITCHING OPTIONS (TICK/CROSS) ---
    with right_col:
        st.subheader("🪡 Stitching Options")
        
        styles = {}
        
        # Row 1: Collar
        st.markdown("**Collar Type**")
        sc1, sc2 = st.columns(2)
        styles["shirt_collar"] = sc1.checkbox("Shirt Collar (Kakool)", value=True)
        styles["sherwani_collar"] = sc2.checkbox("Sherwani Collar")

        # Row 2: Sleeves
        st.markdown("**Sleeve Type**")
        sl1, sl2 = st.columns(2)
        styles["cuff_astin"] = sl1.checkbox("Cuff Astin (✓)", value=True)
        styles["kurta_astin"] = sl2.checkbox("Kurta Astin")

        # Row 3: Daman
        st.markdown("**Daman Type**")
        dm1, dm2 = st.columns(2)
        styles["gol_daman"] = dm1.checkbox("Gol Daman (✓)", value=True)
        styles["chakor_daman"] = dm2.checkbox("Chakor Daman")

        # Row 4: Pockets & Extras
        st.markdown("**Pockets & Fitting**")
        p1, p2 = st.columns(2)
        styles["side_pocket_qty"] = p1.number_input("Side Pockets", 0, 5, value=2)
        styles["front_pocket"] = p2.checkbox("Chest Pocket (✓)", value=True)
        
        f1, f2 = st.columns(2)
        styles["shalwar_gher"] = f1.checkbox("Bara Gher (✓)", value=True)
        styles["double_silai"] = f2.checkbox("Double Silai")

    st.markdown("---")
    
    # ---------------- VERBAL & EXTRA ----------------
    c_extra1, c_extra2 = st.columns(2)
    with c_extra1:
        verbal_instructions = st.text_area("🗣️ Verbal Instructions (Zubani Hidayat)", height=100, placeholder="Gahak ki khusoosi baat...")
    with c_extra2:
        extra_requirements = st.text_area("➕ Extra Requirements / Handwritten Notes", height=100, placeholder="Cuff: 6, Patti: 2.5x10.25...")

    # ---------------- BILLING ----------------
    st.markdown('<div class="section-header">💰 Billing Details</div>', unsafe_allow_html=True)
    b1, b2, b3 = st.columns(3)
    total_price = b1.number_input("Total Bill (Rs.)", 0)
    advance_paid = b2.number_input("Advance (Rs.)", 0)
    remaining_balance = total_price - advance_paid
    b3.markdown(f"### Balance: {remaining_balance}")

    # ---------------- SAVE ACTION ----------------
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💾 SAVE & SYNC ORDER", use_container_width=True, type="primary"):
        if not name or not phone1:
            st.error("⚠️ Customer Name aur Mobile Number lazmi hai!")
        else:
            try:
                conn = get_connection()
                conn.execute("""
                    INSERT INTO orders (
                        order_no, order_date, delivery_date,
                        customer_name, customer_name_urdu,
                        phone_1, phone_2, suit_qty, 
                        total_price, advance_paid, remaining_balance,
                        measurements_json, styles_json, verbal_instructions,
                        is_synced
                    )
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,0)
                """, (
                    f"AT-{order_no}", str(order_date), str(delivery_date),
                    name, name_urdu, phone1, phone2, suits_qty,
                    total_price, advance_paid, remaining_balance,
                    json.dumps(measurements),
                    json.dumps(styles),
                    f"{verbal_instructions} | Extra: {extra_requirements}"
                ))
                conn.commit()
                conn.close()
                
                st.balloons()
                st.success(f"✅ Order AT-{order_no} Saved Locally & Ready to Sync!")
            except Exception as e:

                st.error(f"❌ Database Error: {e}")


