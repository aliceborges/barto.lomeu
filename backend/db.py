import sqlite3
from .config import Config

def get_db():
    conn = sqlite3.connect(Config.DB_NAME)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS urls(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            code TEXT NOT NULL,
            long_url TEXT NOT NULL,
            clicks INTEGER DEFAULT 0
        );
    ''')
    return conn
