"""
Агрегаты аналитики бота поверх user_events/users — витрина для
дашбордов (см. docs/ANALYTICS_DASHBOARD.md). Чистые функции, ничего
не знают про Google Sheets — это отдельно, в sheets_export.py.

Читаем bot_services.database.DB_PATH динамически при каждом вызове
(через сам модуль, не `from ... import DB_PATH`), чтобы в тестах
работала подмена пути фикстурой `db` — см. предупреждение об этом же
в bot_services/cinemalogy/materials.py.
"""

import sqlite3

from bot_services import database

# Шаги воронки Cinemalogy в порядке прохождения. Имена — ровно те,
# что передаются в add_event() по коду (см. docs/NEW_PROCESS_CHECKLIST.md
# про важность точных имён событий).
FUNNEL_STEPS = [
    "cinemalogy_start",
    "choose_frame",
    "confirm_frame",
    "cinemalogy_result",
    "cinemalogy_invitation",
    "cinemalogy_tariff_selected",
    "cinemalogy_payment_opened",
    "cinemalogy_payment_done",
]


def _connect():
    return sqlite3.connect(database.DB_PATH)


def funnel_counts():
    """
    Уникальных пользователей на каждом шаге воронки, по всем данным
    (без фильтра по дате — это добавим, когда понадобится сравнение
    периодов).
    """

    conn = _connect()
    cursor = conn.cursor()

    rows = []
    for step in FUNNEL_STEPS:
        cursor.execute(
            "SELECT COUNT(DISTINCT telegram_id) FROM user_events WHERE event_type = ?",
            (step,),
        )
        rows.append({"step": step, "unique_users": cursor.fetchone()[0]})

    conn.close()
    return rows


def conversion_rates(counts):
    """
    Добавляет к каждому шагу % конверсии от предыдущего шага. Первый
    шаг и шаг с нулём пользователей на предыдущем шаге — None
    (нет от чего считать проценты).
    """

    result = []

    for i, row in enumerate(counts):
        if i == 0:
            conversion = None
        else:
            previous = counts[i - 1]["unique_users"]
            conversion = (
                round(row["unique_users"] / previous * 100, 1)
                if previous
                else None
            )

        result.append({**row, "conversion_from_previous": conversion})

    return result


def registrations_by_source():
    """
    Сколько регистраций пришло с каждого source (deep-link из /start).
    """

    conn = _connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COALESCE(source, 'не указан') AS source, COUNT(*)
        FROM users
        GROUP BY source
        ORDER BY COUNT(*) DESC
        """
    )
    rows = [
        {"source": source, "registrations": count}
        for source, count in cursor.fetchall()
    ]

    conn.close()
    return rows


def sales_by_tariff():
    """
    Сколько раз подтверждена оплата (cinemalogy_payment_done) по
    каждому тарифу — событие несёт тариф в event_data.
    """

    conn = _connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COALESCE(event_data, 'неизвестно'), COUNT(*)
        FROM user_events
        WHERE event_type = 'cinemalogy_payment_done'
        GROUP BY event_data
        ORDER BY event_data
        """
    )
    rows = [
        {"tariff": tariff, "payments_done": count}
        for tariff, count in cursor.fetchall()
    ]

    conn.close()
    return rows



# Не воронка (нет строгого порядка/единого предыдущего шага) — просто
# "сколько раз нажали"/"сколько раз попросили" вне Cinemalogy.
# Имена — те же, что передаются в add_event() по коду.
OTHER_ENGAGEMENT_EVENTS = [
    "menu_about_me",
    "menu_lullabies",
    "consultation_request",
]


def other_engagement_counts():
    """
    Уникальных пользователей и общее число срабатываний для процессов
    вне воронки Cinemalogy — кнопки главного меню, запись на
    консультацию (оба входа в неё, см. handlers/consultation.py).
    """

    conn = _connect()
    cursor = conn.cursor()

    rows = []
    for event_type in OTHER_ENGAGEMENT_EVENTS:
        cursor.execute(
            """
            SELECT COUNT(DISTINCT telegram_id), COUNT(*)
            FROM user_events
            WHERE event_type = ?
            """,
            (event_type,),
        )
        unique_users, total = cursor.fetchone()
        rows.append({
            "event_type": event_type,
            "unique_users": unique_users,
            "total_events": total,
        })

    conn.close()
    return rows


def daily_active_users():
    """
    Уникальных пользователей по дням — по любому событию в
    user_events (включая "message" от ActivityMiddleware), не только
    по шагам Cinemalogy.
    """

    conn = _connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT date(created_at) AS day, COUNT(DISTINCT telegram_id)
        FROM user_events
        GROUP BY day
        ORDER BY day
        """
    )
    rows = [
        {"date": day, "unique_users": count}
        for day, count in cursor.fetchall()
    ]

    conn.close()
    return rows
