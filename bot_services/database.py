import sqlite3

from datetime import datetime

DB_PATH = "data/bot.db"


def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE NOT NULL,
        username TEXT,
        first_name TEXT,
        last_name TEXT,
        phone TEXT,
        registration_date TEXT NOT NULL,
        last_activity TEXT NOT NULL,
        source TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER NOT NULL,
        event_type TEXT NOT NULL,
        event_data TEXT,
        created_at TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

def get_user(telegram_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE telegram_id = ?",
        (telegram_id,)
    )

    user = cursor.fetchone()

    conn.close()

    return user


def add_user(
    telegram_id,
    username,
    first_name,
    last_name,
    source=None
):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (
            telegram_id,
            username,
            first_name,
            last_name,
            registration_date,
            last_activity,
            source
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        telegram_id,
        username,
        first_name,
        last_name,
        now,
        now,
        source
    ))

    conn.commit()
    conn.close()


def update_last_activity(telegram_id):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET last_activity = ?
        WHERE telegram_id = ?
    """, (
        now,
        telegram_id
    ))

    conn.commit()
    conn.close()


def add_event(
    telegram_id,
    event_type,
    event_data=None
):
    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO user_events (
            telegram_id,
            event_type,
            event_data,
            created_at
        )
        VALUES (?, ?, ?, ?)
    """, (
        telegram_id,
        event_type,
        event_data,
        now
    ))

    conn.commit()
    conn.close()


def cleanup_old_events():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM user_events
        WHERE created_at < datetime(
            'now',
            '-30 days'
        )
    """)

    conn.commit()
    conn.close()

# ==========================================
# Работа с параметрами пользователя
# ==========================================

def get_user_parameter(
    telegram_id,
    parameter_name
):
    """
    Получить значение параметра пользователя.
    Если параметр отсутствует, вернуть None.
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT parameter_value
        FROM user_parameters
        WHERE telegram_id = ?
        AND parameter_name = ?
    """, (
        telegram_id,
        parameter_name
    ))

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return None


def set_user_parameter(
    telegram_id,
    parameter_name,
    parameter_value
):
    """
    Создать новый параметр или обновить существующий.
    """

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO user_parameters (
            telegram_id,
            parameter_name,
            parameter_value,
            updated_at
        )
        VALUES (?, ?, ?, ?)

        ON CONFLICT(telegram_id, parameter_name)
        DO UPDATE SET

            parameter_value = excluded.parameter_value,

            updated_at = excluded.updated_at
    """, (
        telegram_id,
        parameter_name,
        parameter_value,
        now
    ))

    conn.commit()
    conn.close()


def delete_user_parameter(
    telegram_id,
    parameter_name
):
    """
    Удалить параметр пользователя.
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM user_parameters
        WHERE telegram_id = ?
        AND parameter_name = ?
    """, (
        telegram_id,
        parameter_name
    ))

    conn.commit()
    conn.close()


def get_all_user_parameters(
    telegram_id
):
    """
    Получить все параметры пользователя.
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            parameter_name,
            parameter_value
        FROM user_parameters
        WHERE telegram_id = ?
    """, (
        telegram_id,
    ))

    rows = cursor.fetchall()

    conn.close()

    return rows
