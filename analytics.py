import streamlit as st
import pandas as pd
from database import get_connection

def show_dashboard_stats():
    """Main Dashboard Metrics"""
    conn = get_connection()
    df = pd.read_sql_query("SELECT total_price, advance_paid, remaining_balance FROM orders", conn)
    conn.close()

    daily_income = df['total_price'].sum() if not df.empty else 0
    new_orders = len(df)
    pending_delivery = len(df[df['remaining_balance'] > 0])

    col1, col2, col3 = st.columns(3)
    with col1: st.metric("💰 Total Income", f"Rs. {daily_income}")
    with col2: st.metric("🧵 Total Orders", new_orders)
    with col3: st.metric("📦 Pending Payments", pending_delivery)

    st.markdown("### 📋 Recent Clients Detail")
    if not df.empty:
        st.dataframe(df.tail(5), use_container_width=True)

def show_all_orders():
    """Full Order History from Database"""
    st.markdown("### 📦 All Orders History")
    conn = get_connection()
    df = pd.read_sql_query("SELECT order_no, customer_name, delivery_date, total_price, remaining_balance FROM orders ORDER BY id DESC", conn)
    conn.close()
    
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Abhi tak koi order mojood nahi hai.")

def show_accounts_summary():
    """Financial Summary"""
    st.markdown("### 💰 Accounts & Billing Summary")
    conn = get_connection()
    df = pd.read_sql_query("SELECT total_price, advance_paid, remaining_balance FROM orders", conn)
    conn.close()
    
    if not df.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("Kul Bill", f"Rs. {df['total_price'].sum()}")
        c2.metric("Wasool Shuda", f"Rs. {df['advance_paid'].sum()}")
        c3.metric("Baqaya Raqam", f"Rs. {df['remaining_balance'].sum()}")
        st.bar_chart(df[['total_price', 'advance_paid']])
    else:
        st.info("Hisab kitab ka data khali hai.")
