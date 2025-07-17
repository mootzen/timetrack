import json
import os
from werkzeug.security import generate_password_hash

DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.json')

os.makedirs(DATA_DIR, exist_ok=True)

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

def add_user(username, password):
    users = load_users()
    if username in users:
        print("User already exists.")
        return
    users[username] = generate_password_hash(password)
    save_users(users)
    print(f"User '{username}' added successfully.")

if __name__ == '__main__':
    username = input("Enter username: ")
    password = input("Enter password: ")
    add_user(username, password)
