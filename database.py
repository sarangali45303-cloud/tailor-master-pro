import sqlite3
from supabase import create_client

# --- CLOUD SETTINGS ---
URL = "https://maadjojvbpewengqojpp.supabase.co" 
KEY = "sb_publishable_clmdak087QAnyOP0Irny0g_jeFwkLYt" 

try:
    supabase = create_client(URL, KEY)
except Exception as e:
    print(f"Supabase Connection Error: {e}")

def get_connection():
    return sqlite3.connect('tailor_pro.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Orders Table with ALL Columns
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
         order_no TEXT, order_date TEXT, delivery_date TEXT,
         customer_name TEXT, customer_name_urdu TEXT, phone_1 TEXT, phone_2 TEXT, 
         suit_qty INTEGER, total_price REAL, advance_paid REAL, remaining_balance REAL,
         measurements_json TEXT, styles_json TEXT, verbal_instructions TEXT, is_synced INTEGER DEFAULT 0)''')
    
    # --- AUTO-FIX: Missing Column 'delivery_date' check ---
    try:
        cursor.execute("SELECT delivery_date FROM orders LIMIT 1")
    except:
        cursor.execute("ALTER TABLE orders ADD COLUMN delivery_date TEXT DEFAULT ''")
    
    # 2. Users Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, role TEXT, shop_name TEXT)''')
    
    # Default Admin
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role, shop_name) VALUES (?, ?, ?, ?)",
                   ('admin', '123', 'admin', 'AZAD TAILOR'))
    
    conn.commit()
    conn.close()

def save_order_cloud(data):
    try:
        response = supabase.table("orders").insert(data).execute()
        return True, "Cloud Saved ✅"
    except Exception as e:
        return False, str(e)

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
        return True, "✅ Account Created!"
    except Exception as e:
        return False, f"❌ Username exists! {str(e)}"
    finally:
        conn.close()

def reset_database_completely():
    conn = get_connection()
    conn.execute("DROP TABLE IF EXISTS orders")
    conn.close()
    init_db()
    return "✅ Database Updated to v5.0!"
