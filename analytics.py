import streamlit as st
import pandas as pd
from database import supabase, get_connection

def show_dashboard_stats():
    """Main Dashboard Metrics from Cloud"""
    try:
        # Cloud se data mangwana
        response = supabase.table("orders").select("*").execute()
        data = response.data
        df = pd.DataFrame(data)

        if not df.empty:
            total_income = df['total_price'].sum()
            total_orders = len(df)
            pending = len(df[df['remaining_balance'] > 0])

            c1, c2, c3 = st.columns(3)
            c1.metric("💰 Total Income", f"Rs. {total_income}")
            c2.metric("🧵 Total Orders", total_orders)
            c3.metric("📦 Pending", pending)
            
            st.markdown("### 📋 Recent Clients")
            st.dataframe(df[['customer_name', 'phone_1', 'total_price', 'remaining_balance']].tail(5), use_container_width=True)
        else:
            st.info("Abhi tak koi data mojood nahi hai.")
    except Exception as e:
        st.error(f"Cloud Error: {e}")

def show_all_orders():
    """Full Order History from Cloud"""
    st.markdown("### 📦 All Orders History (Cloud)")
    try:
        response = supabase.table("orders").select("*").execute()
        df = pd.DataFrame(response.data)
        
        if not df.empty:
            # Columns ko sahi order mein dikhana
            cols = ['order_no', 'customer_name', 'delivery_date', 'total_price', 'remaining_balance']
            st.dataframe(df[cols], use_container_width=True)
        else:
            st.warning("Koi order nahi mila.")
    except:
        st.info("Database se connect nahi ho raha. Pehla order save karen.")

def show_accounts_summary():
    """Financial Summary"""
    st.markdown("### 💰 Accounts & Billing")
    try:
        response = supabase.table("orders").select("total_price, advance_paid, remaining_balance").execute()
        df = pd.DataFrame(response.data)
        
        if not df.empty:
            total = df['total_price'].sum()
            adv = df['advance_paid'].sum()
            rem = df['remaining_balance'].sum()
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Kul Bill", f"Rs. {total}")
            c2.metric("Wasool", f"Rs. {adv}")
            c3.metric("Baqaya", f"Rs. {rem}")
            st.area_chart(df[['total_price', 'advance_paid']])
        else:
            st.write("Hisab khali hai.")
    except:
        st.write("Data fetching error.")
