import streamlit as st
import pandas as pd
from database import supabase

def show_dashboard_stats():
    """Main Dashboard Metrics with 401 Error Handling"""
    try:
        response = supabase.table("orders").select("*").execute()
        df = pd.DataFrame(response.data)

        if not df.empty:
            c1, c2, c3 = st.columns(3)
            c1.metric("💰 Total Income", f"Rs. {df['total_price'].sum()}")
            c2.metric("🧵 Total Orders", len(df))
            c3.metric("📦 Pending", len(df[df['remaining_balance'] > 0]))
            
            st.markdown("### 📋 Recent Clients Detail")
            st.dataframe(df[['customer_name', 'phone_1', 'total_price', 'remaining_balance']].tail(5), use_container_width=True)
        else:
            st.info("ℹ️ Dashboard active karne ke liye pehla order save karen.")
            
    except Exception as e:
        if "401" in str(e):
            st.error("sb_publishable_clmdaKO87QAnyOP0IrnY0g_jEfwkLYt")
        else:
            st.info("ℹ️ Database connection established. Waiting for first order data...")

def show_all_orders():
    """Fetch and display all orders from Cloud"""
    st.markdown("### 📦 All Orders History")
    try:
        response = supabase.table("orders").select("*").execute()
        df = pd.DataFrame(response.data)
        if not df.empty:
            cols = ['order_no', 'customer_name', 'delivery_date', 'total_price', 'remaining_balance']
            st.dataframe(df[cols], use_container_width=True)
        else:
            st.warning("No orders found in database.")
    except Exception as e:
        st.error(f"Error fetching orders: {e}")

def show_accounts_summary():
    """Financial area with charts"""
    st.markdown("### 💰 Accounts & Billing Summary")
    try:
        response = supabase.table("orders").select("total_price, advance_paid").execute()
        df = pd.DataFrame(response.data)
        if not df.empty:
            st.area_chart(df)
            st.write(f"**Total Business Volume:** Rs. {df['total_price'].sum()}")
        else:
            st.info("No financial data available.")
    except:
        st.error("Could not load accounts.")

