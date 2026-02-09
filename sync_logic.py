import socket
import sqlite3

def is_online():
    try:
        # Google DNS se check karega internet hai ya nahi
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def sync_data_to_cloud():
    if is_online():
        conn = sqlite3.connect('tailor_pro.db')
        # Yahan aap Supabase ya kisi bhi online DB ka logic likhenge
        # SELECT * FROM orders WHERE is_synced = 0
        # Upload to Cloud...
        # UPDATE orders SET is_synced = 1
        conn.close()
        return "✅ Data Synced Online!"
    else:
        return "⚠️ Offline: Data saved locally."