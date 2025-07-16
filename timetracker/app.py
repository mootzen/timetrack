
from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import sqlite3
import os

app = Flask(__name__)
DB_PATH = "/data/timetracker.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS entries (
                    id INTEGER PRIMARY KEY,
                    start_time TEXT,
                    end_time TEXT,
                    break_start TEXT,
                    break_end TEXT
                )''')
    conn.commit()
    conn.close()

@app.route('/start', methods=['POST'])
def start_work():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO entries (start_time) VALUES (?)", (datetime.now().isoformat(),))
    conn.commit()
    conn.close()
    return jsonify({"message": "Work started"}), 200

@app.route('/stop', methods=['POST'])
def stop_work():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id FROM entries WHERE end_time IS NULL ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    if row:
        c.execute("UPDATE entries SET end_time = ? WHERE id = ?", (datetime.now().isoformat(), row[0]))
        conn.commit()
    conn.close()
    return jsonify({"message": "Work stopped"}), 200

@app.route('/start_break', methods=['POST'])
def start_break():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id FROM entries WHERE end_time IS NULL ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    if row:
        c.execute("UPDATE entries SET break_start = ? WHERE id = ?", (datetime.now().isoformat(), row[0]))
        conn.commit()
    conn.close()
    return jsonify({"message": "Break started"}), 200

@app.route('/end_break', methods=['POST'])
def end_break():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id FROM entries WHERE end_time IS NULL ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    if row:
        c.execute("UPDATE entries SET break_end = ? WHERE id = ?", (datetime.now().isoformat(), row[0]))
        conn.commit()
    conn.close()
    return jsonify({"message": "Break ended"}), 200

@app.route('/status', methods=['GET'])
def status():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    today = datetime.now().date().isoformat()
    c.execute("SELECT start_time, end_time, break_start, break_end FROM entries WHERE date(start_time) = ?", (today,))
    entries = c.fetchall()
    total_work = timedelta()
    for e in entries:
        if e[0] and e[1]:
            start = datetime.fromisoformat(e[0])
            end = datetime.fromisoformat(e[1])
            duration = end - start
            if e[2] and e[3]:
                b_start = datetime.fromisoformat(e[2])
                b_end = datetime.fromisoformat(e[3])
                duration -= (b_end - b_start)
            total_work += duration
    conn.close()
    hours = total_work.total_seconds() / 3600
    return jsonify({"today_hours": round(hours, 2)}), 200

@app.route('/summary', methods=['GET'])
def summary():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    this_week = datetime.now().isocalendar()[1]
    c.execute("SELECT start_time, end_time, break_start, break_end FROM entries")
    entries = c.fetchall()
    total_week = timedelta()
    for e in entries:
        if e[0] and e[1]:
            start = datetime.fromisoformat(e[0])
            end = datetime.fromisoformat(e[1])
            if start.isocalendar()[1] == this_week:
                duration = end - start
                if e[2] and e[3]:
                    b_start = datetime.fromisoformat(e[2])
                    b_end = datetime.fromisoformat(e[3])
                    duration -= (b_end - b_start)
                total_week += duration
    conn.close()
    hours = total_week.total_seconds() / 3600
    overtime = hours - 40 if hours > 40 else 0
    return jsonify({"week_hours": round(hours, 2), "overtime": round(overtime, 2)}), 200

if __name__ == '__main__':
    os.makedirs('/data', exist_ok=True)
    init_db()
    app.run(host='0.0.0.0', port=80)