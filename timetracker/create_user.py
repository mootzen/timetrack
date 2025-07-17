import hashlib
import json
import os

USER_FILE = '/data/users.json'  # Adjust path if different

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user():
    username = input("Enter new username: ").strip()
    password = input("Enter password: ").strip()
    confirm = input("Confirm password: ").strip()

    if password != confirm:
        print("❌ Passwords do not match.")
        return

    users = load_users()

    if username in users:
        print("❌ User already exists.")
        return

    users[username] = {"password": hash_password(password)}
    save_users(users)
    print(f"✅ User '{username}' created successfully.")

if __name__ == '__main__':
    create_user()
