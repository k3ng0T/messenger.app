
import sqlite3
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
DB_FILE = APP_DIR / "messages.db"


def init_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Таблица пользователей
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Таблица сообщений
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Таблица чатов
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    conn.commit()
    return conn

def get_user_by_credentials(conn, username, password):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return cursor.fetchone()

def create_user(conn, username, password):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

# database.py
def get_all_chats(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM chats")
    return [row[0] for row in cursor.fetchall()]

def add_chat(conn, name):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO chats (name) VALUES (?)", (name,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def get_last_message(conn, chat_name):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT content FROM messages
        WHERE chat=?
        ORDER BY timestamp DESC
        LIMIT 1
    """, (chat_name,))
    row = cursor.fetchone()
    return row[0] if row else ""
