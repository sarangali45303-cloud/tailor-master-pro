import streamlit as st
from modules.database import init_db
from modules.orders import add_order_ui
from modules.styling import apply_styling

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
