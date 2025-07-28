from typing import Any

import validators

from backend.db import get_db
from backend.models import url_model
from backend.utils.generator import generate_code


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

def get_long_url_and_clicks(code) -> tuple[Any, Any] | None:
    if not code:
        return None
    conn = get_db()
    data = url_model.find_by_code(conn, code)
    if not data:
        return None
    long_url, clicks = data
    conn.close()
    return long_url, clicks

def update_clicks(code, clicks):
    conn = get_db()
    url_model.update_clicks(conn, code, clicks)
    conn.close()

def update_history(code, ip):
    conn = get_db()
    url_id = url_model.find_by_code(conn, code)
    if not url_id:
        conn.close()
        return
    url_model.insert_click_history(conn, url_id[0], ip)
    conn.close()

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
