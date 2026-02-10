import sqlite3
import streamlit as st
import pandas as pd
from supabase import create_client

# --- 1. CLOUD SETTINGS ---
URL = "https://maadjojvbpewengqojpp.supabase.co" 
KEY = "sb_publishable_clmdaKO87QAnyOP0IrnY0g_jEfwkLYt" 

try:
    supabase = create_client(URL, KEY)
except Exception as e:
    st.error(f"Supabase Connection Failed: {e}")

# --- 2. LOCAL CONNECTION ---
def get_connection():
    return sqlite3.connect('tailor_pro.db', check_same_thread=False)

# --- 3. DATABASE INITIALIZE (Local) ---
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    # Orders Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
         order_no TEXT, order_date TEXT, delivery_date TEXT,
         customer_name TEXT, customer_name_urdu TEXT, phone_1 TEXT, phone_2 TEXT, 
         suit_qty INTEGER, total_price REAL, advance_paid REAL, remaining_balance REAL,
         measurements_json TEXT, styles_json TEXT, verbal_instructions TEXT, 
         is_synced INTEGER DEFAULT 0)''')
    
    # Users Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, role TEXT, shop_name TEXT)''')
    
    # Default Admin
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role, shop_name) VALUES ('admin', '123', 'admin', 'AZAD TAILOR')")
    conn.commit()
    conn.close()

# --- 4. REPAIR/RESET (Local Error Fix karne ke liye) ---
def reset_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS orders")
    conn.commit()
    conn.close()
    init_db()
    st.success("Local Database Fixed! Naye columns active ho gaye. ✅")

# --- 5. AUTH FUNCTIONS ---
def verify_login(user, pwd):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role, shop_name FROM users WHERE username=? AND password=?", (user, pwd))
    result = cursor.fetchone()
    conn.close()
    return result

def add_new_user(username, password, shop_name):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # A. Local Save
        cursor.execute("INSERT INTO users (username, password, role, shop_name) VALUES (?, ?, 'admin', ?)",
                       (username, password, shop_name))
        conn.commit()
        
        # B. Cloud Save (Sync with Master Panel)
        user_data = {
            "username": username,
            "password": password,
            "role": "admin",
            "shop_name": shop_name
        }
        supabase.table("users").insert(user_data).execute()
        
        return True, f"✅ Account for '{shop_name}' created on Cloud & Local!"
    except Exception as e:
        return False, f"❌ Error: {str(e)}"
    finally:
        conn.close()

# --- 6. ORDER SYNC FUNCTIONS ---
def save_order_cloud(data):
    try:
        # Cloud data dict banate waqt 'id' agar local hai to mita den
        if 'id' in data: del data['id']
        supabase.table("orders").insert(data).execute()
        return True, "Cloud Saved ✅"
    except Exception as e:
        return False, str(e)
