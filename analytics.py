import streamlit as st
import pandas as pd
from database import supabase

def show_dashboard_stats():
    """Main Dashboard Metrics with Cloud Data & Error Handling"""
    try:
        # 1. Cloud se data mangwana
        response = supabase.table("orders").select("*").execute()
        df = pd.DataFrame(response.data)

        if not df.empty:
            # Metrics calculate karna
            total_income = df['total_price'].sum()
            total_orders = len(df)
            pending_count = len(df[df['remaining_balance'] > 0])

            # UI per metrics dikhana
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f'<div style="background-color:#f0f2f6;padding:15px;border-radius:10px;border-left:5px solid #000080;">💰 Total Income<br><h2>Rs. {total_income}</h2></div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div style="background-color:#f0f2f6;padding:15px;border-radius:10px;border-left:5px solid #FFD700;">🧵 Total Orders<br><h2>{total_orders}</h2></div>', unsafe_allow_html=True)
            with c3:
                st.markdown(f'<div style="background-color:#f0f2f6;padding:15px;border-radius:10px;border-left:5px solid #FF0000;">📦 Pending<br><h2>{pending_count}</h2></div>', unsafe_allow_html=True)
            
            st.markdown("### 📋 Recent Clients Detail")
            display_cols = ['customer_name', 'phone_1', 'total_price', 'remaining_balance']
            st.dataframe(df[display_cols].tail(5), use_container_width=True)
        else:
            st.info("ℹ️ Dashboard active karne ke liye pehla order save karen.")

    except Exception as e:
        if "401" in str(e):
            st.error("🔑 API Key Error: Aapka Supabase connection sahi nahi hai. Database.py mein keys check karen.")
        else:
            st.info("ℹ️ System Ready. Waiting for first data sync...")

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
            st.warning("Abhi tak koi order record nahi mila.")
    except Exception as e:
        if "401" in str(e):
            st.error("🔑 API Key Error: Orders load nahi ho sakay (Check Key).")
        else:
            st.error(f"Error fetching orders: {e}")

def show_accounts_summary():
    """Financial area with charts"""
    st.markdown("### 💰 Accounts & Billing Summary")
    try:
        response = supabase.table("orders").select("total_price, advance_paid, remaining_balance").execute()
        df = pd.DataFrame(response.data)
        
        if not df.empty:
            total_v = df['total_price'].sum()
            paid_v = df['advance_paid'].sum()
            rem_v = df['remaining_balance'].sum()

            c1, c2, c3 = st.columns(3)
            c1.metric("Total Business", f"Rs. {total_v}")
            c2.metric("Total Collected", f"Rs. {paid_v}")
            c3.metric("Total Outstanding", f"Rs. {rem_v}")

            st.area_chart(df[['total_price', 'advance_paid']])
        else:
            st.info("No financial data available yet.")
    except Exception as e:
        st.error("Could not load accounts.")
