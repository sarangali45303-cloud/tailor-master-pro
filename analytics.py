import streamlit as st
import pandas as pd
from database import supabase

def show_dashboard_stats():
    """Main Dashboard Metrics with Cloud Data"""
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
            c1.metric("💰 Total Income", f"Rs. {total_income}")
            c2.metric("🧵 Total Orders", total_orders)
            c3.metric("📦 Pending Payments", pending_count)
            
            st.markdown("### 📋 Recent Clients Detail")
            # Sirf aham columns dikhana
            display_cols = ['customer_name', 'phone_1', 'total_price', 'remaining_balance']
            st.dataframe(df[display_cols].tail(5), use_container_width=True)
        else:
            st.info("ℹ️ Dashboard active karne ke liye pehla order save karen.")

    except Exception as e:
        # Error handling (e.g. 401 Unauthorized)
        if "401" in str(e):
            st.error("🔑 API Key Error: Aapka Supabase connection sahi nahi hai. Database.py mein keys check karen.")
        else:
            st.info("ℹ️ Waiting for database connection... Please save an order first.")

def show_all_orders():
    """Fetch and display all orders from Cloud"""
    st.markdown("### 📦 All Orders History")
    try:
        response = supabase.table("orders").select("*").execute()
        df = pd.DataFrame(response.data)
        
        if not df.empty:
            # Columns ko sahi order mein dikhana
            cols = ['order_no', 'customer_name', 'delivery_date', 'total_price', 'remaining_balance']
            st.dataframe(df[cols], use_container_width=True)
        else:
            st.warning("Abhi tak koi order record nahi mila.")
    except Exception as e:
        st.error(f"Error fetching orders: {e}")

def show_accounts_summary():
    """Financial area with charts"""
    st.markdown("### 💰 Accounts & Billing Summary")
    try:
        response = supabase.table("orders").select("total_price, advance_paid, remaining_balance").execute()
        df = pd.DataFrame(response.data)
        
        if not df.empty:
            # Totals calculate karna
            total_v = df['total_price'].sum()
            paid_v = df['advance_paid'].sum()
            rem_v = df['remaining_balance'].sum()

            c1, c2, c3 = st.columns(3)
            c1.write(f"**Total Volume:** Rs. {total_v}")
            c2.write(f"**Collected:** Rs. {paid_v}")
            c3.write(f"**Outstanding:** Rs. {rem_v}")

            # Chota sa chart dikhana
            st.area_chart(df[['total_price', 'advance_paid']])
        else:
            st.info("No financial data available yet.")
    except Exception as e:
        st.error(f"Could not load accounts: {e}")
