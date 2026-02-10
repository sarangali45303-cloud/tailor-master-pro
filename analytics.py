import streamlit as st
import pandas as pd
from database import get_connection

def show_dashboard_stats():
    """Main Dashboard: Metrics aur Recent Clients"""
    st.markdown("### 📊 Shop Overview")
    try:
        conn = get_connection()
        df = pd.read_sql_query("SELECT total_price, advance_paid, remaining_balance FROM orders", conn)
        conn.close()

        if not df.empty:
            col1, col2, col3 = st.columns(3)
            col1.metric("💰 Total Income", f"Rs. {df['total_price'].sum()}")
            col2.metric("🧵 Total Orders", len(df))
            col3.metric("📦 Pending Payments", len(df[df['remaining_balance'] > 0]))
        else:
            st.info("No data available yet.")
    except Exception as e:
        st.error(f"Error loading dashboard: {e}")

def show_all_orders():
    """Tamam orders ki list with delivery_date fix"""
    st.markdown("### 📦 Purane Orders History")
    try:
        conn = get_connection()
        # Query matching ALL columns including delivery_date
        df = pd.read_sql_query("""
            SELECT order_no, customer_name, phone_1, delivery_date, total_price, remaining_balance 
            FROM orders 
            ORDER BY id DESC
        """, conn)
        conn.close()

        if not df.empty:
            search = st.text_input("🔍 Search by Name or Phone")
            if search:
                df = df[df['customer_name'].str.contains(search, case=False) | df['phone_1'].str.contains(search)]
            
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No orders found.")
    except Exception as e:
        st.error(f"Error loading orders: {e}")

def show_accounts_summary():
    """Financial Summary"""
    st.markdown("### 💰 Accounts Summary")
    try:
        conn = get_connection()
        df = pd.read_sql_query("SELECT total_price, advance_paid, remaining_balance FROM orders", conn)
        conn.close()

        if not df.empty:
            c1, c2, c3 = st.columns(3)
            total = df['total_price'].sum()
            adv = df['advance_paid'].sum()
            rem = df['remaining_balance'].sum()

            c1.metric("Kul Bill", f"Rs. {total}")
            c2.metric("Wasool Shuda", f"Rs. {adv}")
            c3.metric("Baqaya Raqam", f"Rs. {rem}")
            
            st.bar_chart(df[['total_price', 'advance_paid']])
        else:
            st.info("No financial data found.")
    except Exception as e:
        st.error(f"Error loading accounts: {e}")