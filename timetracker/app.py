from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import os
import json
from werkzeug.security import check_password_hash
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

DATA_DIR = 'data'
TRACK_FILE = os.path.join(DATA_DIR, 'track.json')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
SETTINGS_FILE = os.path.join(DATA_DIR, 'settings.json')
HISTORY_FILE = os.path.join(DATA_DIR, 'history.json')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

def load_json(filepath, default=None):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return default if default is not None else {}

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f)

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    data = load_json(TRACK_FILE, {})
    settings = load_json(SETTINGS_FILE, {})
    history = load_json(HISTORY_FILE, [])

    start_time = data.get('start_time')
    status = data.get('status', 'Stopped')
    display_start_time = None
    elapsed = ''
    if start_time:
        start_dt = datetime.fromisoformat(start_time).astimezone(ZoneInfo("Europe/Berlin"))
        display_start_time = start_dt.strftime("%Y-%m-%d %H:%M:%S")
        delta = datetime.now(ZoneInfo("Europe/Berlin")) - start_dt
        elapsed = str(delta).split('.')[0]

    # Calculate today and week totals
    now = datetime.now(ZoneInfo("Europe/Berlin"))
    start_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    start_of_week = start_of_today - timedelta(days=now.weekday())

    worked_today = timedelta()
    worked_week = timedelta()

    for entry in history:
        s = datetime.fromisoformat(entry['start']).astimezone(ZoneInfo("Europe/Berlin"))
        e = datetime.fromisoformat(entry['end']).astimezone(ZoneInfo("Europe/Berlin"))
        dur = e - s
        if s >= start_of_today:
            worked_today += dur
        if s >= start_of_week:
            worked_week += dur

    daily_hours = float(settings.get('daily_hours', 8))
    weekly_hours = float(settings.get('weekly_hours', 40))

    expected_today = timedelta(hours=daily_hours)
    expected_week = timedelta(hours=weekly_hours)

    percent_today = round(100 * worked_today.total_seconds() / expected_today.total_seconds(), 1)
    percent_week = round(100 * worked_week.total_seconds() / expected_week.total_seconds(), 1)

    return render_template('index.html',
                           start_time=display_start_time,
                           elapsed=elapsed,
                           status=status,
                           worked_today=str(worked_today).split('.')[0],
                           worked_week=str(worked_week).split('.')[0],
                           expected_today=str(expected_today),
                           expected_week=str(expected_week),
                           percent_today=percent_today,
                           percent_week=percent_week)

@app.route('/start', methods=['POST'])
def start():
    if 'username' not in session:
        return redirect(url_for('login'))

    data = load_json(TRACK_FILE, {})
    if data.get('status') != 'Started':
        data['start_time'] = datetime.now(ZoneInfo("Europe/Berlin")).isoformat()
        data['status'] = 'Started'
        save_json(TRACK_FILE, data)
    return redirect(url_for('index'))

@app.route('/stop', methods=['POST'])
def stop():
    if 'username' not in session:
        return redirect(url_for('login'))

    data = load_json(TRACK_FILE, {})
    if data.get('status') == 'Started':
        start_time = datetime.fromisoformat(data['start_time']).astimezone(ZoneInfo("Europe/Berlin"))
        end_time = datetime.now(ZoneInfo("Europe/Berlin"))
        duration = str(end_time - start_time).split('.')[0]

        history = load_json(HISTORY_FILE, [])
        history.append({
            'start': data['start_time'],
            'end': end_time.astimezone(ZoneInfo("Europe/Berlin")).isoformat(),
            'duration': duration
        })
        save_json(HISTORY_FILE, history)

        data['status'] = 'Stopped'
        data['start_time'] = None
        save_json(TRACK_FILE, data)
    return redirect(url_for('index'))

@app.route('/history')
def history():
    if 'username' not in session:
        return redirect(url_for('login'))

    entries = load_json(HISTORY_FILE, [])
    return render_template('history.html', entries=entries)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'username' not in session:
        return redirect(url_for('login'))

    settings = load_json(SETTINGS_FILE, {
        'daily_hours': 8,
        'weekly_hours': 40,
        'break_minutes': 30,
        'dark_mode': 0
    })

    if request.method == 'POST':
        settings['daily_hours'] = float(request.form.get('daily_hours', 8))
        settings['weekly_hours'] = float(request.form.get('weekly_hours', 40))
        settings['break_minutes'] = int(request.form.get('break_minutes', 30))
        settings['dark_mode'] = int(request.form.get('dark_mode', 0))
        save_json(SETTINGS_FILE, settings)
        session['dark_mode'] = settings['dark_mode']
        return redirect(url_for('index'))

    return render_template('settings.html', settings=settings)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = load_json(USERS_FILE, {})
        stored_hash = users.get(username)

        if stored_hash and check_password_hash(stored_hash, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
