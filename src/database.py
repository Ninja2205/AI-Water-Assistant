import sqlite3 
import os
from datetime import datetime
from pathlib import Path

# Get the project root directory (parent of src)
PROJECT_ROOT = Path(__file__).parent.parent
DB_NAME = str(PROJECT_ROOT / "water_tracker.db")

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
       CREATE TABLE IF NOT EXISTS water_intake(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id TEXT,
                   intake_ml INTEGER,
                   date TEXT
                   )

    """)

    conn.commit() 
    conn.close()


def log_intake(user_id, intake_ml):
    conn = None
    try:
        # Ensure tables exist
        create_tables()
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        date_today = datetime.today().strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO water_intake (user_id, intake_ml, date ) VALUES (?, ?, ?)", (user_id, intake_ml, date_today ))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error logging intake: {e}")
        return False
    finally:
        if conn:
            conn.close()


def get_intake_history(user_id):
    conn = None
    try:
        create_tables()
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT intake_ml, date FROM water_intake WHERE user_id = ?", (user_id, ))
        records = cursor.fetchall()
        return records
    except Exception as e:
        print(f"Error getting history: {e}")
        return []
    finally:
        if conn:
            conn.close()

create_tables()