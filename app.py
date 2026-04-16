from flask import Flask, request, jsonify
import logging
import os
from datetime import datetime

from config import API_KEY, LOG_FOLDER, LOG_FILE
from models import init_db, get_connection

app = Flask(__name__)

def setup_logging():
    os.makedirs(LOG_FOLDER, exist_ok=True)

    logging.basicConfig(
        filename=os.path.join(LOG_FOLDER, LOG_FILE),
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s"
    )

def check_api_key(req):
    return req.headers.get("X-API-Key") == API_KEY

@app.before_request
def log_request():
    logging.info(f"{request.method} {request.path}")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Monitoring API is running"}), 200

@app.route("/api/metrics", methods=["POST"])
def create_metric():
    if not check_api_key(request):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO monitoring_metrics (hostname, metric_name, metric_value, unit, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data.get("hostname"),
        data.get("metric_name"),
        data.get("metric_value"),
        data.get("unit"),
        data.get("timestamp")
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Stored"}), 201

@app.route("/api/metrics", methods=["GET"])
def get_metrics():
    if not check_api_key(request):
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM monitoring_metrics")
    rows = cursor.fetchall()

    result = []
    for row in rows:
        result.append(dict(row))

    conn.close()

    return jsonify(result), 200

if __name__ == "__main__":
    setup_logging()
    init_db()
    app.run(host="0.0.0.0", port=5000)