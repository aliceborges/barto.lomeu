import sqlite3

from backend import Config


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
    conn.execute('CREATE INDEX IF NOT EXISTS idx_code ON urls(code)')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS click_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url_id INTEGER NOT NULL,
            location json
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(url_id) REFERENCES urls(id)
        )
    ''')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_click_url_id ON click_history(url_id)')

    return conn
