import os
from flask import Flask, jsonify
from src.db import wait_for_db, init_db, record_visit, count_visits


wait_for_db()
init_db()

app = Flask(__name__)

@app.get("/health")
def health():
    return jsonify(status="ok"), 200

@app.get("/")
def home():
    visit = record_visit()
    total = count_visits()
    return jsonify(
        message="Flask API running in Docker + Compose",
        last_visit=dict(visit),
        total_visits=total,
    ), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
