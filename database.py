import sqlite3
from supabase import create_client

URL = "https://maadjojvbpewengqojpp.supabase.co" 
KEY = "sb_publishable_clmdak087QAnyOP0Irny0g_jeFwkLYt" 
supabase = create_client(URL, KEY)

def get_connection():
    return sqlite3.connect('tailor_pro.db', check_same_thread=False)

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
        # 1. Local Database mein save karen
        cursor.execute("INSERT INTO users (username, password, role, shop_name) VALUES (?, ?, 'admin', ?)",
                       (username, password, shop_name))
        conn.commit()
        
        # 2. Supabase Cloud mein bhi user save karen (Optional)
        # supabase.table("users").insert({"username": username, "password": password, "shop_name": shop_name}).execute()
        
        return True, f"✅ Account for '{shop_name}' created! Please Login."
    except Exception as e:
        return False, f"❌ Error: {str(e)}"
    finally:
        conn.close()
