from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
import os
import json
import pytz

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATA_FILE = 'data.json'
TIMEZONE = pytz.timezone('Europe/Berlin')  # CEST/UTC+2

DEFAULT_SETTINGS = {
    "expected_daily_hours": 8,
    "expected_weekly_hours": 40,
    "break_minutes": 30,
    "dark_mode": False
}

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_user():
    return session.get('username', 'default')

@app.route('/')
def index():
    user = get_user()
    data = load_data()
    start_time = data.get(user, {}).get('start_time')
    is_tracking = start_time is not None
    settings = data.get(user, {}).get('settings', DEFAULT_SETTINGS)
    return render_template('index.html', is_tracking=is_tracking, settings=settings)

@app.route('/start', methods=['POST'])
def start():
    user = get_user()
    data = load_data()
    if user not in data:
        data[user] = {}
    data[user]['start_time'] = datetime.now(TIMEZONE).isoformat()
    save_data(data)
    return redirect(url_for('index'))

@app.route('/stop', methods=['POST'])
def stop():
    user = get_user()
    data = load_data()
    user_data = data.get(user, {})
    start_time = user_data.pop('start_time', None)
    if start_time:
        start_dt = datetime.fromisoformat(start_time)
        end_dt = datetime.now(TIMEZONE)
        duration = (end_dt - start_dt).total_seconds()
        history = user_data.setdefault('history', [])
        history.append({
            'start': start_time,
            'end': end_dt.isoformat(),
            'duration': duration
        })
    save_data(data)
    return redirect(url_for('index'))

@app.route('/history')
def history():
    user = get_user()
    data = load_data()
    history = data.get(user, {}).get('history', [])
    settings = data.get(user, {}).get('settings', DEFAULT_SETTINGS)

    # Calculate total work time this week
    this_week = datetime.now(TIMEZONE).isocalendar().week
    total_seconds = sum(e['duration'] for e in history if datetime.fromisoformat(e['start']).isocalendar().week == this_week)
    percent = round((total_seconds / (settings['expected_weekly_hours'] * 3600)) * 100, 1)

    return render_template('history.html', history=history[::-1], total_seconds=total_seconds, percent=percent, settings=settings)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    user = get_user()
    data = load_data()
    user_data = data.setdefault(user, {})
    if request.method == 'POST':
        user_data['settings'] = {
            'expected_daily_hours': float(request.form['daily_hours']),
            'expected_weekly_hours': float(request.form['weekly_hours']),
            'break_minutes': int(request.form['break_minutes']),
            'dark_mode': 'dark_mode' in request.form
        }
        save_data(data)
        return redirect(url_for('index'))
    settings = user_data.get('settings', DEFAULT_SETTINGS)
    return render_template('settings.html', settings=settings)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
