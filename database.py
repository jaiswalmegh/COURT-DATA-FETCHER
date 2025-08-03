import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('queries.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS case_queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_type TEXT,
            case_number TEXT,
            case_year TEXT,
            query_time TEXT,
            raw_html TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_query(case_type, case_number, year, raw_html):
    conn = sqlite3.connect('queries.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO case_queries (case_type, case_number, case_year, query_time, raw_html)
        VALUES (?, ?, ?, ?, ?)
    ''', (case_type, case_number, year, datetime.now().isoformat(), raw_html))
    conn.commit()
    conn.close()
