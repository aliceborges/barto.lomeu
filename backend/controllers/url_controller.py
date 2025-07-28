from flask import Blueprint, request, jsonify, redirect

from backend.services import url_service

url_bp = Blueprint('urls', __name__)

@url_bp.route('/shorten_url', methods=['POST'])
def shorten_url():
    data = request.get_json()
    if not data or "long_url" not in data:
        return jsonify({"error": "Missing parameter: long_url"}), 400

    long_url = data["long_url"]
    desired_code = data.get("code")
    return url_service.create_short_url(long_url, desired_code)

@url_bp.route('/<code>', methods=['GET'])
def access_url(code):
    if not code:
        return jsonify({"error": "Missing parameter: code"}), 400
    data = url_service.get_long_url_and_clicks(code)
    if not data:
        return jsonify({"error": "This code isn't registered"}), 404
    url_id, long_url, clicks = data
    url_service.update_clicks(code, clicks + 1 if clicks is not None else 1)
    url_service.update_history(code, request.remote_addr)
    return redirect(long_url)

@url_bp.route('/stats/<code>', methods=['GET'])
def code_status(code):
    stats = url_service.get_stats(code)
    if not stats:
        return jsonify({"error": "This code isn't registered"}), 404
    return jsonify(stats)

@url_bp.route('/all/stats', methods=['GET'])
def all_status():
    return jsonify(url_service.get_all_stats())

@url_bp.route('/history/<code>', methods=['GET'])
def get_history(code):
    history = url_service.get_history(code)
    if not history:
        return jsonify({"error": "This code isn't registered"}), 404
    return jsonify(history)

@url_bp.route('/all/history', methods=['GET'])
def get_all_history():
    history = url_service.get_all_history()
    if not history:
        return jsonify({"error": "No history found"}), 404
    return jsonify(history)