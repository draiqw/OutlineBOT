# database.py

import sqlite3
from datetime import datetime, timedelta
from constants import DATABASE

def init_db():
    """Инициализирует базу данных и создаёт таблицу, если её нет."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            phone TEXT,
            outline_key TEXT,
            subscription_expiry TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_user(user_id: int, phone: str, trial_expiry: str):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id, phone, subscription_expiry) VALUES (?, ?, ?)",
        (user_id, phone, trial_expiry)
    )
    conn.commit()
    conn.close()

def get_user(user_id: int):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT user_id, phone, outline_key, subscription_expiry FROM users WHERE user_id = ?",
        (user_id,)
    )
    user = cursor.fetchone()
    conn.close()
    return user

def update_user_key(user_id: int, outline_key: str):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET outline_key = ? WHERE user_id = ?",
        (outline_key, user_id)
    )
    conn.commit()
    conn.close()

def update_subscription(user_id: int, new_expiry: str):
    """Обновляет дату окончания подписки для пользователя."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET subscription_expiry = ? WHERE user_id = ?",
        (new_expiry, user_id)
    )
    conn.commit()
    conn.close()
