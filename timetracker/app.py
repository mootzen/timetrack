from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
import os
import json
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

DATA_DIR = 'data'
TRACK_FILE = os.path.join(DATA_DIR, 'track.json')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
SETTINGS_FILE = os.path.join(DATA_DIR, 'settings.json')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

def load_tracking_data():
    if os.path.exists(TRACK_FILE):
        with open(TRACK_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_tracking_data(data):
    with open(TRACK_FILE, 'w') as f:
        json.dump(data, f)

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f)

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))

    data = load_tracking_data()
    start_time = data.get('start_time')
    status = data.get('status', 'Stopped')

    elapsed = ''
    if start_time:
        start_dt = datetime.fromisoformat(start_time)
        delta = datetime.now() - start_dt
        elapsed = str(delta).split('.')[0]

    return render_template(
        'index.html',
        start_time=start_time,
        elapsed=elapsed,
        status=status
    )

@app.route('/start', methods=['POST'])
def start():
    if 'username' not in session:
        return redirect(url_for('login'))

    data = load_tracking_data()
    if data.get('status') != 'Started':
        data['start_time'] = datetime.now().isoformat()
        data['status'] = 'Started'
        save_tracking_data(data)
    return redirect(url_for('index'))

@app.route('/stop', methods=['POST'])
def stop():
    if 'username' not in session:
        return redirect(url_for('login'))

    data = load_tracking_data()
    if data.get('status') == 'Started':
        start_time = datetime.fromisoformat(data['start_time'])
        end_time = datetime.now()
        duration = str(end_time - start_time).split('.')[0]

        history_file = os.path.join(DATA_DIR, 'history.json')
        history = []
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                history = json.load(f)

        history.append({
            'start': data['start_time'],
            'end': end_time.isoformat(),
            'duration': duration
        })
        with open(history_file, 'w') as f:
            json.dump(history, f)

        data['status'] = 'Stopped'
        data['start_time'] = None
        save_tracking_data(data)
    return redirect(url_for('index'))

@app.route('/history')
def history():
    if 'username' not in session:
        return redirect(url_for('login'))

    history_file = os.path.join(DATA_DIR, 'history.json')
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            entries = json.load(f)
    else:
        entries = []
    return render_template('history.html', entries=entries)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'username' not in session:
        return redirect(url_for('login'))

    settings_data = load_settings()
    user_settings = settings_data.get(session['username'], {
        'daily_hours': 9,
        'weekly_hours': 38,
        'break_minutes': 60,
        'dark_mode': True
    })

    if request.method == 'POST':
        user_settings['daily_hours'] = float(request.form.get('daily_hours', 8))
        user_settings['weekly_hours'] = float(request.form.get('weekly_hours', 40))
        user_settings['break_minutes'] = int(request.form.get('break_minutes', 30))
        user_settings['dark_mode'] = request.form.get('dark_mode') == '1'

        settings_data[session['username']] = user_settings
        save_settings(settings_data)

        session['dark_mode'] = user_settings['dark_mode']  # Update session
        return redirect(url_for('index'))

    return render_template('settings.html', settings=user_settings)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = load_users()
        stored_hash = users.get(username)

        if stored_hash and check_password_hash(stored_hash, password):
            session['username'] = username
            session['dark_mode'] = load_settings().get(username, {}).get('dark_mode', True)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    session.pop('dark_mode', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
