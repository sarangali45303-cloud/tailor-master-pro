import streamlit as st
import pandas as pd
from datetime import date

def show_dashboard_stats():
    # Ye data DB se ayega, filhal demo hai
    daily_income = 15000 
    new_orders = 8
    pending_delivery = 12

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Daily Income", f"Rs. {daily_income}")
    col2.metric("🧵 New Orders", new_orders)
    col3.metric("📦 Pending", pending_delivery)

    st.markdown("### 📋 Recent Clients Detail")
    # Table Data
    data = {
        "Name": ["Aslam", "Irfan", "Sajid"],
        "Mobile": ["03001234567", "03117654321", "03459876543"],
        "Total Suits": [2, 1, 5],
        "Order Date": ["2024-02-08", "2024-02-09", "2024-02-09"],
        "Delivery": ["2024-02-15", "2024-02-18", "2024-02-25"],
        "Total": [4000, 2500, 12000],
        "Advance": [2000, 1000, 5000],
        "Remaining": [2000, 1500, 7000]
    }
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)