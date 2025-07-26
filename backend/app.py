import random
import sqlite3
import string

import validators
from dotenv import load_dotenv
import os

from flask import Flask, request, jsonify, redirect

app = Flask(__name__)
load_dotenv()

DB_NAME = os.getenv("DB_NAME", "urls.db")
BASE_URL = os.getenv("BASE_URL", "http://localhost/")

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute('''
    CREATE TABLE IF NOT EXISTS urls(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        code text not null,
        long_url not null,
        clicks int default 0
    );
    ''')
    return conn


def generate_code(length=6):
    char = string.digits + string.ascii_letters
    return "".join(random.choices(char, k=length))


@app.route('/shorten_url', methods=["POST"])
def shorten_url():
    conn = get_db()
    cursor = conn.cursor()
    data = request.get_json()

    if not data or "long_url" not in data:
        return jsonify({"error": "Missing parameter: long_url"})
    long_url = data["long_url"]
    if not validators.url(long_url):
        return jsonify({"error": "The informed url is not valid."}), 400
    code = ""

    if "code" in data:
        desired_code = data["code"]
        used_long_url = cursor.execute("SELECT long_url FROM urls WHERE code = ?", (desired_code,)).fetchone()
        if used_long_url:
            return jsonify({"error": f"The code is been already used for this url: {used_long_url[0]}"}), 409
        code = desired_code
    else:
        code = generate_code()
        while cursor.execute("SELECT 1 FROM urls WHERE code = ?", (code,)).fetchone():
            code = generate_code()

    cursor.execute("INSERT INTO urls(code, long_url) VALUES (?, ?)", (code, long_url))
    conn.commit()
    conn.close()
    return jsonify({"code": code})


@app.route('/<code>', methods=["GET"])
def access_url(code):
    conn = get_db()
    cursor = conn.cursor()
    long_url, clicks = cursor.execute("SELECT long_url, clicks FROM urls WHERE code = ?", (code,)).fetchone()

    if not long_url:
        return jsonify({"error": "This code isn't registered"}), 404

    cursor.execute("UPDATE urls SET clicks = ? WHERE code = ?", (clicks+1, code))
    conn.commit()
    return redirect(long_url)


@app.route('/stats/<code>', methods=["GET"])
def code_status(code):
    conn = get_db()
    cursor = conn.cursor()
    long_url, clicks = cursor.execute("SELECT long_url, clicks FROM urls WHERE code = ?", (code,)).fetchone()

    if not long_url:
        return jsonify({"error": "This code isn't registered"}), 404

    return jsonify({"long_url": long_url, "code": code, "clicks": clicks})


@app.route('/all/stats', methods=["GET"])
def all_status():
    conn = get_db()
    cursor = conn.cursor()
    rows = cursor.execute("SELECT long_url, code, clicks FROM urls").fetchall()
    result = []
    for row in rows:
        long_url, code, clicks = row
        result.append({
            "code": code,
            "long_url": long_url,
            "clicks": clicks
        })

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=80)