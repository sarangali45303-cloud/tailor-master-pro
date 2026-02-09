import sqlite3
from supabase import create_client

# --- 1. CLOUD SETTINGS ---
URL = "https://maadjojvbpewengqojpp.supabase.co" 
KEY = "sb_publishable_clmdak087QAnyOP0Irny0g_jeFwkLYt" 

try:
    supabase = create_client(URL, KEY)
except Exception as e:
    print(f"Supabase Connection Error: {e}")

# --- 2. GET CONNECTION (Isay hona chahiye) ---
def get_connection():
    return sqlite3.connect('tailor_pro.db', check_same_thread=False)

# --- 3. INITIALIZE DB ---
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, order_no TEXT, customer_name TEXT, 
         customer_name_urdu TEXT, phone_1 TEXT, phone_2 TEXT, suit_qty INTEGER,
         total_price REAL, advance_paid REAL, remaining_balance REAL,
         measurements_json TEXT, styles_json TEXT, verbal_instructions TEXT,
         is_synced INTEGER DEFAULT 0)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, 
         password TEXT, role TEXT, shop_name TEXT)''')
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role, shop_name) VALUES (?, ?, ?, ?)",
                   ('admin', '123', 'admin', 'AZAD TAILOR'))
    conn.commit()
    conn.close()

# --- 4. SAVE TO CLOUD ---
def save_order_cloud(data):
    try:
        response = supabase.table("orders").insert(data).execute()
        return True, "Cloud Saved ✅"
    except Exception as e:
        return False, str(e)

# --- 5. VERIFY LOGIN ---
def verify_login(user, pwd):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role, shop_name FROM users WHERE username=? AND password=?", (user, pwd))
    result = cursor.fetchone()
    conn.close()
    return result
def add_new_user(username, password, shop_name, role="admin"):
    """Naya user (account) banane ke liye."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, role, shop_name) VALUES (?, ?, ?, ?)",
                       (username, password, role, shop_name))
        conn.commit()
        conn.close()
        return True, "Account Created! Ab Login karen."
    except Exception as e:
        return False, f"Error: Username shayad pehle se mujood hai."