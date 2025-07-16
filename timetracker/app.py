from flask import Flask, request, jsonify, render_template_string, redirect, url_for
from datetime import datetime
import os
import json

app = Flask(__name__)

DATA_FILE = 'timelog.json'
start_time = None

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Uhrensohn</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f0f0f0; text-align: center; padding: 50px; }
        h1 { color: #333; }
        .button { padding: 10px 20px; margin: 10px; font-size: 16px; }
        .elapsed { margin-top: 20px; font-size: 18px; color: green; }
    </style>
</head>
<body>
    <h1>⏱️ Uhrensohn - AZ-Erfassung</h1>
    <form action="/start" method="post">
        <button class="button" type="submit">▶️ Start</button>
    </form>
    <form action="/stop" method="post">
        <button class="button" type="submit">⏹️ Stop</button>
    </form>
    <form action="/health" method="get">
        <button class="button" type="submit">❤️ Health</button>
    </form>
    {% if elapsed %}
    <div class="elapsed">
        <strong>Elapsed Time:</strong> {{ elapsed }}
    </div>
    {% endif %}
</body>
</html>
"""

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_TEMPLATE, elapsed=None)

@app.route("/start", methods=["POST"])
def start():
    global start_time
    start_time = datetime.now()
    return redirect(url_for('index'))

@app.route("/stop", methods=["POST"])
def stop():
    global start_time
    if start_time is None:
        return redirect(url_for('index'))

    end_time = datetime.now()
    elapsed = end_time - start_time
    log_entry = {
        "start": start_time.isoformat(),
        "end": end_time.isoformat(),
        "elapsed": str(elapsed)
    }
    data = load_data()
    data.append(log_entry)
    save_data(data)
    start_time = None
    return render_template_string(HTML_TEMPLATE, elapsed=str(elapsed))

@app.route("/health", methods=["GET"])
def health():
    return "Service healthy ✅", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
