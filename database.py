import sqlite3
import streamlit as st
import pandas as pd
from supabase import create_client

# --- 1. CLOUD SETTINGS (Supabase) ---
URL = "https://maadjojvbpewengqojpp.supabase.co" 
KEY = "sb_publishable_clmdaKO87QAnyOP0IrnY0g_jEfwkLYt" 

try:
    supabase = create_client(URL, KEY)
except Exception as e:
    st.error(f"Supabase Connection Failed: {e}")

# --- 2. LOCAL CONNECTION ---
def get_connection():
    return sqlite3.connect('tailor_pro.db', check_same_thread=False)

# --- 3. DATABASE INITIALIZE ---
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
         order_no TEXT, order_date TEXT, delivery_date TEXT,
         customer_name TEXT, customer_name_urdu TEXT, phone_1 TEXT, phone_2 TEXT, 
         suit_qty INTEGER, total_price REAL, advance_paid REAL, remaining_balance REAL,
         measurements_json TEXT, styles_json TEXT, verbal_instructions TEXT, 
         is_synced INTEGER DEFAULT 0)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, role TEXT, shop_name TEXT)''')
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role, shop_name) VALUES ('admin', '123', 'admin', 'AZAD TAILOR')")
    conn.commit()
    conn.close()

# --- 4. RESET DATABASE (Ye function miss tha, jis se error aaya) ---
def reset_db():
    """Purani database delete karke naye columns banayega"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS orders")
    conn.commit()
    conn.close()
    init_db()
    st.success("Database Reset Successful! ✅")

# --- 5. AUTH & SYNC FUNCTIONS ---
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
    try:
        supabase.table("orders").insert(data).execute()
        return True, "Cloud Saved ✅"
    except Exception as e:
        return False, str(e)

def sync_local_to_cloud():
    try:
        conn = get_connection()
        df = pd.read_sql_query("SELECT * FROM orders WHERE is_synced = 0", conn)
        if df.empty:
            conn.close()
            return False, "Already Synced! ✅"
        success_count = 0
        for _, row in df.iterrows():
            data = row.to_dict()
            if 'id' in data: del data['id']
            supabase.table("orders").insert(data).execute()
            conn.execute("UPDATE orders SET is_synced = 1 WHERE order_no = ?", (row['order_no'],))
            success_count += 1
        conn.commit()
        conn.close()
        return True, f"Successfully Synced {success_count} orders! 🚀"
    except Exception as e:
        return False, f"Sync Failed: {str(e)}"
