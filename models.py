import sqlite3
from config import DATABASE_NAME

def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS monitoring_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hostname TEXT,
            metric_name TEXT,
            metric_value REAL,
            unit TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()