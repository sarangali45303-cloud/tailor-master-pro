import sqlite3
import streamlit as st
from supabase import create_client

# --- 1. CLOUD SETTINGS (Supabase) ---
# ⚠️ 401 Error hal karne ke liye URL aur KEY ko dubara copy-paste karen bina kisi space ke.
URL = "https://maadjojvbpewengqojpp.supabase.co" 
KEY = "sb_publishable_clmdaKO87QAnyOP0Irny0g_jeFwkLYt" 

try:
    supabase = create_client(URL, KEY)
except Exception as e:
    st.error(f"Supabase Connection Failed: {e}")

# --- 2. LOCAL CONNECTION (SQLite) ---
def get_connection():
    """Local SQLite connection for Offline mode."""
    return sqlite3.connect('tailor_pro.db', check_same_thread=False)

# --- 3. DATABASE INITIALIZE ---
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    # Orders Table with all necessary columns for 35+ measurements
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
         order_no TEXT, 
         order_date TEXT, 
         delivery_date TEXT,
         customer_name TEXT, 
         customer_name_urdu TEXT, 
         phone_1 TEXT, 
         phone_2 TEXT, 
         suit_qty INTEGER,
         total_price REAL, 
         advance_paid REAL, 
         remaining_balance REAL,
         measurements_json TEXT, 
         styles_json TEXT, 
         verbal_instructions TEXT, 
         is_synced INTEGER DEFAULT 0)''')
    
    # Users Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, role TEXT, shop_name TEXT)''')
    
    # Default Admin
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role, shop_name) VALUES ('admin', '123', 'admin', 'AZAD TAILOR')")
    conn.commit()
    conn.close()

# --- 4. RESET DATABASE (To fix column errors) ---
def reset_db():
    """Purani database delete karke naye columns banayega"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS orders")
    conn.commit()
    conn.close()
    init_db()
    st.success("Database Reset Successful! New Columns (35+) Activated. ✅")

# --- 5. AUTH & CLOUD FUNCTIONS ---
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
        cursor.execute("INSERT INTO users (username, password, role, shop_name) VALUES (?, ?, 'admin', ?)",
                       (username, password, shop_name))
        conn.commit()
        return True, "✅ Account Created Successfully!"
    except:
        return False, "❌ Username already exists!"
    finally:
        conn.close()

def save_order_cloud(data):
    """Saves order to Supabase"""
    try:
        response = supabase.table("orders").insert(data).execute()
        return True, "Cloud Saved ✅"
    except Exception as e:
        return False, str(e)
