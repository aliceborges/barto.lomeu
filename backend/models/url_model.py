from datetime import datetime

def insert_url(conn, code, long_url):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO urls(code, long_url) VALUES (?, ?)", (code, long_url))
    conn.commit()

def find_by_code(conn, code):
    cursor = conn.cursor()
    return cursor.execute("SELECT long_url, clicks FROM urls WHERE code = ?", (code,)).fetchone()

def update_clicks(conn, code, clicks):
    cursor = conn.cursor()
    cursor.execute("UPDATE urls SET clicks = ? WHERE code = ?", (clicks, code))
    conn.commit()

def code_exists(conn, code):
    cursor = conn.cursor()
    return cursor.execute("SELECT 1 FROM urls WHERE code = ?", (code,)).fetchone()

def find_all(conn):
    cursor = conn.cursor()
    return cursor.execute("SELECT long_url, code, clicks FROM urls").fetchall()

def insert_click_history(conn, url_id, location):
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:00')
    cursor.execute("INSERT INTO click_history(url_id, location, timestamp) VALUES (?, ?, ?)", (url_id, location, timestamp))
    conn.commit()
