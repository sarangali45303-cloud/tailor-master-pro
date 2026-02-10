import sqlite3
import streamlit as st
from supabase import create_client

# --- 1. CLOUD SETTINGS (Supabase) ---
# Note: Agar 401 error aaye to Supabase dashboard se "anon public" key check karen.
URL = "https://maadjojvbpewengqojpp.supabase.co" 
KEY = "sb_publishable_clmdaKO87QAnyOP0Irny0g_jeFwkLYt" 

# Supabase Client Initialize (Safe Connection)
try:
    supabase = create_client(URL, KEY)
except Exception as e:
    st.error(f"Supabase Connection Error: {e}")

# --- 2. LOCAL CONNECTION (SQLite) ---
def get_connection():
    """Local database connection banata hai (Offline mode ke liye)."""
    return sqlite3.connect('tailor_pro.db', check_same_thread=False)

# --- 3. DATABASE INITIALIZE (Tables Setup) ---
def init_db():
    """App shuru hote hi tables banata hai (order_date error yahan fix kiya gaya hai)."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Orders Table: 16 Columns total (Sahi order mein)
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
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
         username TEXT UNIQUE, 
         password TEXT, 
         role TEXT, 
         shop_name TEXT)''')
    
    # Default Admin User (Agar pehle se na ho)
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role, shop_name) VALUES (?, ?, ?, ?)",
                   ('admin', '123', 'admin', 'AZAD TAILOR'))
    
    conn.commit()
    conn.close()

# --- 4. AUTHENTICATION FUNCTIONS ---
def verify_login(user, pwd):
    """Username aur Password check karta hai."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role, shop_name FROM users WHERE username=? AND password=?", (user, pwd))
    result = cursor.fetchone()
    conn.close()
    return result

def add_new_user(username, password, shop_name):
    """Naye tailor/shop owner ka account banata hai."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role, shop_name) VALUES (?, ?, 'admin', ?)",
                       (username, password, shop_name))
        conn.commit()
        return True, "✅ Account Created Successfully! Please Login."
    except Exception as e:
        return False, f"❌ Username already exists or Database Error: {str(e)}"
    finally:
        conn.close()

# --- 5. CLOUD SYNC FUNCTION ---
def save_order_cloud(data):
    """Data ko seedha Supabase Cloud par bhejta hai."""
    try:
        response = supabase.table("orders").insert(data).execute()
        return True, "Cloud Saved ✅"
    except Exception as e:
        return False, str(e)
