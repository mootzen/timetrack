from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
import os
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

DATA_DIR = 'data'
TRACK_FILE = os.path.join(DATA_DIR, 'track.json')

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

        # Save to history
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            session['username'] = request.form['username']
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
