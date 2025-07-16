from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime, timedelta
import os
import json

app = Flask(__name__)

DATA_FILE = 'timelog.json'
start_time = None
break_start_time = None
current_breaks = []

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def str_to_timedelta(s):
    h, m, s = map(int, s.split(":"))
    return timedelta(hours=h, minutes=m, seconds=s)

@app.route("/", methods=["GET"])
def index():
    global start_time, break_start_time

    status = "🔴 Not working"
    start = None
    break_since = None
    elapsed = None

    if start_time:
        start = start_time.strftime("%Y-%m-%d %H:%M:%S")
        if break_start_time:
            status = "🟡 On Break"
            break_since = break_start_time.strftime("%H:%M:%S")
        else:
            status = "🟢 Working"
            elapsed = str(datetime.now() - start_time).split(".")[0]

    return render_template("index.html", elapsed=elapsed, status=status, start=start, break_since=break_since)

@app.route("/start", methods=["POST"])
def start():
    global start_time, current_breaks, break_start_time
    start_time = datetime.now()
    current_breaks = []
    break_start_time = None
    return redirect(url_for('index'))

@app.route("/stop", methods=["POST"])
def stop():
    global start_time, current_breaks, break_start_time
    if not start_time:
        return redirect(url_for('index'))

    end_time = datetime.now()
    worked_time = end_time - start_time
    break_total = sum([b[1] - b[0] for b in current_breaks], timedelta())

    log_entry = {
        "start": start_time.isoformat(),
        "end": end_time.isoformat(),
        "elapsed": str(worked_time - break_total).split(".")[0],
        "breaks": str(break_total).split(".")[0]
    }

    data = load_data()
    data.append(log_entry)
    save_data(data)

    start_time = None
    current_breaks = []
    break_start_time = None

    return redirect(url_for('index'))

@app.route("/break_start", methods=["POST"])
def break_start():
    global break_start_time
    if start_time and not break_start_time:
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

    weeks = list(weekly_summary.keys())
    totals = [round(td.total_seconds() / 3600, 2) for td in weekly_summary.values()]
    weekly_summary_str = {week: str(td) for week, td in weekly_summary.items()}

    return render_template("history.html",
                           entries=parsed_entries,
                           weekly_summary=weekly_summary_str,
                           weeks=weeks,
                           totals=totals)

@app.route("/health", methods=["GET"])
def health():
    return "Service healthy ✅", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
