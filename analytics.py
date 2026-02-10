import streamlit as st
import pandas as pd
from database import supabase, get_connection

def get_combined_data():
    """Pehle Cloud check karega, agar error ho ya khali ho toh Local check karega."""
    df_final = pd.DataFrame()
    
    # 1. Try Cloud (Supabase)
    try:
        response = supabase.table("orders").select("*").execute()
        df_final = pd.DataFrame(response.data)
    except Exception as e:
        pass # Internet/Key error par chup chap skip karega
    
    # 2. Agar Cloud khali hai ya fail hua, toh Local uthayen
    if df_final.empty:
        try:
            conn = get_connection()
            df_final = pd.read_sql_query("SELECT * FROM orders", conn)
            conn.close()
        except:
            pass
            
    return df_final

def show_dashboard_stats():
    """Main Dashboard with Hybrid Data"""
    st.markdown("### 📊 Shop Overview (Hybrid Mode)")
    df = get_combined_data()

    if not df.empty:
        # Data clean karna
        df['total_price'] = pd.to_numeric(df['total_price'], errors='coerce').fillna(0)
        df['advance_paid'] = pd.to_numeric(df['advance_paid'], errors='coerce').fillna(0)
        df['remaining_balance'] = pd.to_numeric(df['remaining_balance'], errors='coerce').fillna(0)
        
        total_income = df['total_price'].sum()
        total_orders = len(df)
        pending_count = len(df[df['remaining_balance'] > 0])

        # Fancy UI Cards
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div style="background-color:#f0f2f6;padding:15px;border-radius:10px;border-left:5px solid #000080;">💰 Total Income<br><h2>Rs. {total_income}</h2></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div style="background-color:#f0f2f6;padding:15px;border-radius:10px;border-left:5px solid #FFD700;">🧵 Total Orders<br><h2>{total_orders}</h2></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div style="background-color:#f0f2f6;padding:15px;border-radius:10px;border-left:5px solid #FF0000;">📦 Pending<br><h2>{pending_count}</h2></div>', unsafe_allow_html=True)
        
        st.markdown("### 📋 Recent Orders List")
        display_cols = ['customer_name', 'phone_1', 'total_price', 'remaining_balance']
        st.dataframe(df[display_cols].tail(10), use_container_width=True)
    else:
        st.info("ℹ️ Dashboard active karne ke liye pehla order save karen.")

def show_all_orders():
    """Display all orders from combined source"""
    st.markdown("### 📦 All Orders History")
    df = get_combined_data()
    if not df.empty:
        cols = ['order_no', 'customer_name', 'delivery_date', 'total_price', 'remaining_balance']
        st.dataframe(df[cols], use_container_width=True)
    else:
        st.warning("Abhi tak koi order record nahi mila.")

def show_accounts_summary():
    """Financial area with charts"""
    st.markdown("### 💰 Accounts & Billing Summary")
    df = get_combined_data()
    if not df.empty:
        df['total_price'] = pd.to_numeric(df['total_price'], errors='coerce')
        df['advance_paid'] = pd.to_numeric(df['advance_paid'], errors='coerce')
        
        total_v = df['total_price'].sum()
        paid_v = df['advance_paid'].sum()
        rem_v = df['remaining_balance'].sum()

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Business", f"Rs. {total_v}")
        c2.metric("Total Collected", f"Rs. {paid_v}")
        c3.metric("Outstanding", f"Rs. {rem_v}")

        st.area_chart(df[['total_price', 'advance_paid']])
    else:
        st.info("No financial data available yet.")
