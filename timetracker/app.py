from flask import Flask, request, jsonify, render_template_string, redirect, url_for
from datetime import datetime, timedelta
import os
import json

app = Flask(__name__)

DATA_FILE = 'timelog.json'
start_time = None
break_start_time = None
current_breaks = []

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
        .link { margin: 10px; display: inline-block; }
    </style>
</head>
<body>
    <h1>⏱️ Uhrensohn - AZ-Erfassung</h1>
    <form action="/start" method="post"><button class="button" type="submit">▶️ Start</button></form>
    <form action="/stop" method="post"><button class="button" type="submit">⏹️ Stop</button></form>
    <form action="/break_start" method="post"><button class="button" type="submit">⏸️ Break Start</button></form>
    <form action="/break_end" method="post"><button class="button" type="submit">⏯️ Break End</button></form>
    <form action="/health" method="get"><button class="button" type="submit">❤️ Health</button></form>
    <a class="link" href="/history">📜 View History</a>
    {% if elapsed %}
    <div class="elapsed"><strong>Elapsed Time:</strong> {{ elapsed }}</div>
    {% endif %}
</body>
</html>
"""

HISTORY_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Session History</title>
    <style>
        body { font-family: Arial, sans-serif; background: #fff; padding: 40px; }
        h1 { color: #333; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background: #eee; }
        .summary { margin-top: 20px; font-size: 16px; }
    </style>
</head>
<body>
    <h1>📜 History</h1>
    <a href="/">🔙 Back</a>
    <table>
        <tr><th>Start</th><th>End</th><th>Worked</th><th>Breaks</th></tr>
        {% for entry in entries %}
        <tr>
            <td>{{ entry.start }}</td>
            <td>{{ entry.end }}</td>
            <td>{{ entry.elapsed }}</td>
            <td>{{ entry.breaks | default('0:00:00') }}</td>
        </tr>
        {% endfor %}
    </table>
    <div class="summary">
        <h2>📊 Weekly Summary</h2>
        {% for week, total in weekly_summary.items() %}
        <p><strong>{{ week }}:</strong> {{ total }}</p>
        {% endfor %}
    </div>
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
    global start_time, current_breaks
    start_time = datetime.now()
    current_breaks = []
    return redirect(url_for('index'))

@app.route("/stop", methods=["POST"])
def stop():
    global start_time, current_breaks
    if not start_time:
        return redirect(url_for('index'))

    end_time = datetime.now()
    worked_time = end_time - start_time
    break_total = sum([b[1] - b[0] for b in current_breaks], timedelta())

    log_entry = {
        "start": start_time.isoformat(),
        "end": end_time.isoformat(),
        "elapsed": str(worked_time - break_total),
        "breaks": str(break_total)
    }

    data = load_data()
    data.append(log_entry)
    save_data(data)

    start_time = None
    current_breaks = []
    return render_template_string(HTML_TEMPLATE, elapsed=str(worked_time - break_total))

@app.route("/break_start", methods=["POST"])
def break_start():
    global break_start_time
    break_start_time = datetime.now()
    return redirect(url_for('index'))

@app.route("/break_end", methods=["POST"])
def break_end():
    global break_start_time, current_breaks
    if break_start_time:
        current_breaks.append((break_start_time, datetime.now()))
        break_start_time = None
    return redirect(url_for('index'))

@app.route("/history", methods=["GET"])
def history():
    data = load_data()
    parsed_entries = []
    weekly_summary = {}

    for entry in data:
        start = datetime.fromisoformat(entry['start'])
        end = datetime.fromisoformat(entry['end'])
        elapsed = str_to_timedelta(entry.get('elapsed', '0:00:00'))
        breaks = str_to_timedelta(entry.get('breaks', '0:00:00'))

        week = start.strftime("%Y-W%W")
        weekly_summary[week] = weekly_summary.get(week, timedelta()) + elapsed

        parsed_entries.append({
            "start": start.strftime("%Y-%m-%d %H:%M"),
            "end": end.strftime("%Y-%m-%d %H:%M"),
            "elapsed": str(elapsed),
            "breaks": str(breaks)
        })

    # Format timedelta into H:MM:SS
    weekly_summary = {week: str(td) for week, td in weekly_summary.items()}
    return render_template_string(HISTORY_TEMPLATE, entries=parsed_entries, weekly_summary=weekly_summary)

@app.route("/health", methods=["GET"])
def health():
    return "Service healthy ✅", 200

def str_to_timedelta(s):
    h, m, s = map(int, s.split(":"))
    return timedelta(hours=h, minutes=m, seconds=s)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
