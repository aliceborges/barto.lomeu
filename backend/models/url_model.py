from datetime import datetime

def insert_url(conn, code, long_url):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO urls(code, long_url) VALUES (?, ?)", (code, long_url))
    conn.commit()

def find_by_code(conn, code)-> tuple[int, str, int] | None:
    if not code:
        return None
    cursor = conn.cursor()
    return cursor.execute("SELECT id, long_url, clicks FROM urls WHERE code = ?", (code,)).fetchone()

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

def get_history(conn, code):
    cursor = conn.cursor()
    url_id = cursor.execute("SELECT id FROM urls WHERE code = ?", (code,)).fetchone()
    if not url_id:
        return []
    return cursor.execute("SELECT location, timestamp FROM click_history WHERE url_id = ? order by timestamp asc", (url_id[0],)).fetchall()

def get_all_history(conn):
    cursor = conn.cursor()
    return cursor.execute("SELECT urls.code, click_history.location, click_history.timestamp FROM urls JOIN click_history ON urls.id = click_history.url_id order by timestamp asc").fetchall()