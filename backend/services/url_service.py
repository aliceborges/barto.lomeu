import validators
from ..db import get_db
from ..utils.generator import generate_code
from ..models import url_model

def create_short_url(long_url, desired_code=None):
    if not validators.url(long_url):
        return {"error": "The informed URL is not valid."}, 400

    conn = get_db()

    if desired_code:
        if url_model.code_exists(conn, desired_code):
            return {"error": "The code is already in use."}, 409
        code = desired_code
    else:
        code = generate_code()
        while url_model.code_exists(conn, code):
            code = generate_code()

    url_model.insert_url(conn, code, long_url)
    conn.close()
    return {"code": code}, 201

def get_long_url(code):
    conn = get_db()
    data = url_model.find_by_code(conn, code)
    if not data:
        return None
    long_url, clicks = data
    url_model.update_clicks(conn, code, clicks + 1)
    conn.close()
    return long_url

def get_stats(code):
    conn = get_db()
    data = url_model.find_by_code(conn, code)
    conn.close()
    if not data:
        return None
    long_url, clicks = data
    return {"code": code, "long_url": long_url, "clicks": clicks}

def get_all_stats():
    conn = get_db()
    rows = url_model.find_all(conn)
    conn.close()
    return [{"code": code, "long_url": long_url, "clicks": clicks} for long_url, code, clicks in rows]
