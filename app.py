import streamlit as st
from database import init_db
from orders import add_order_ui
from styling import apply_styling

# ---------------- SYSTEM INIT ----------------
init_db()

# ---------------- UI / STYLING ----------------
apply_styling("AZAD TAILOR – Tailor Master Pro")

# ---------------- SIDEBAR ----------------
menu = st.sidebar.selectbox(
    "📌 Main Menu",
    ["🧵 New Order"]
)

# ---------------- PAGES ----------------
if menu == "🧵 New Order":
    add_order_ui()

