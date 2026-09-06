"""
Экспорт списка пользователей на лист "Пользователи" в Google Sheets.

В отличие от вкладок в sheets_export.py (Воронка/Источники/Продажи/
Активность — перезаписываются целиком при каждом запуске), этот лист
только ДОПОЛНЯЕТСЯ новыми пользователями. Причина: колонка
"Комментарий" — ручные заметки, которые Лиза проставляет прямо в
таблице, и полная перезапись стёрла бы их при следующем запуске.
"""

from bot_services.database import get_all_users

USERS_SHEET_NAME = "Пользователи"

# Telegram ID — не то, что просили, но без устойчивого ключа нельзя
# понять, кто уже внесён (username может отсутствовать или смениться).
# Последней колонкой, чтобы не сдвигать заказанный порядок.
USERS_HEADER = [
    "Никнейм в тг",
    "Имя",
    "Дата входа",
    "Откуда пришёл",
    "Комментарий",
    "Telegram ID",
]


def build_user_rows():
    """
    Все пользователи из БД в виде строк для листа "Пользователи" (без
    заголовка). "Комментарий" всегда пустой при первом добавлении —
    это поле только для ручных заметок, экспорт его не трогает.
    """

    rows = []

    for row in get_all_users():
        # id, telegram_id, username, first_name, last_name, phone,
        # registration_date, last_activity, source
        (
            _id,
            telegram_id,
            username,
            first_name,
            _last_name,
            _phone,
            registration_date,
            _last_activity,
            source,
        ) = row

        rows.append([
            f"@{username}" if username else "не указан",
            first_name or "",
            registration_date,
            source or "не указан",
            "",
            str(telegram_id),
        ])

    return rows


def sync_users_sheet(client):
    """
    client — открытая Google-таблица (см. sheets_export.write_to_sheets).

    Читает уже внесённые Telegram ID (последняя колонка) и дописывает
    только тех пользователей, которых там ещё нет. Существующие
    строки (и ручные "Комментарий" в них) не трогает.

    Возвращает число реально добавленных пользователей.
    """

    from gspread.exceptions import WorksheetNotFound

    all_rows = build_user_rows()

    try:
        worksheet = client.worksheet(USERS_SHEET_NAME)
    except WorksheetNotFound:
        worksheet = client.add_worksheet(
            title=USERS_SHEET_NAME,
            rows=len(all_rows) + 50,
            cols=len(USERS_HEADER) + 2,
        )
        worksheet.update([USERS_HEADER] + all_rows)
        return len(all_rows)

    existing = worksheet.get_all_values()

    if not existing:
        worksheet.update([USERS_HEADER])
        existing = [USERS_HEADER]

    known_ids = {row[-1] for row in existing[1:] if row}

    new_rows = [row for row in all_rows if row[-1] not in known_ids]

    if new_rows:
        worksheet.append_rows(new_rows, value_input_option="USER_ENTERED")

    return len(new_rows)
