# create_user.py
import hashlib
import json
import os

user_file = 'users.json'

username = input("Enter username: ")
password = input("Enter password: ")
hashed_password = hashlib.sha256(password.encode()).hexdigest()

if os.path.exists(user_file):
    with open(user_file, 'r') as f:
        users = json.load(f)
else:
    users = {}

if username in users:
    print("User already exists!")
else:
    users[username] = {"password": hashed_password}
    with open(user_file, 'w') as f:
        json.dump(users, f, indent=4)
    print("✅ User created!")
