"""
Экспорт агрегатов аналитики в Google Sheets — источник данных для
дашборда в Looker Studio (см. docs/ANALYTICS_DASHBOARD.md).

Разделено на 3 слоя специально ради тестируемости:
- build_export_data() — чистая функция, никакого Google API;
- write_to_sheets(client, ...) — принимает уже открытую таблицу
  (или фейк с тем же интерфейсом в тестах), не создаёт клиента сама;
- run_export(...) — единственное место, которое реально обращается к
  Google (через service account) и поэтому не покрыто юнит-тестами.
"""

from gspread.exceptions import WorksheetNotFound

from bot_services.analytics import funnel


def build_export_data():
    """
    Собирает все вкладки экспорта как {имя_вкладки: [[строка], ...]}
    (первая строка каждой вкладки — заголовки).
    """

    funnel_rows = funnel.conversion_rates(funnel.funnel_counts())
    funnel_sheet = [
        ["Шаг", "Уникальных пользователей", "Конверсия с предыдущего шага, %"]
    ]
    for row in funnel_rows:
        funnel_sheet.append([
            row["step"],
            row["unique_users"],
            row["conversion_from_previous"]
            if row["conversion_from_previous"] is not None
            else "",
        ])

    sources_sheet = [["Источник", "Регистраций"]]
    for row in funnel.registrations_by_source():
        sources_sheet.append([row["source"], row["registrations"]])

    sales_sheet = [["Тариф", "Оплаченных билетов"]]
    for row in funnel.sales_by_tariff():
        sales_sheet.append([row["tariff"], row["payments_done"]])

    dau_sheet = [["Дата", "Уникальных активных пользователей"]]
    for row in funnel.daily_active_users():
        dau_sheet.append([row["date"], row["unique_users"]])

    engagement_sheet = [
        ["Событие", "Уникальных пользователей", "Всего срабатываний"]
    ]
    for row in funnel.other_engagement_counts():
        engagement_sheet.append([
            row["event_type"],
            row["unique_users"],
            row["total_events"],
        ])

    return {
        "Воронка": funnel_sheet,
        "Источники": sources_sheet,
        "Продажи": sales_sheet,
        "Активность по дням": dau_sheet,
        "Вовлечённость": engagement_sheet,
    }


def write_to_sheets(client, export_data):
    """
    client — открытая Google-таблица (gspread.Spreadsheet или
    совместимый по интерфейсу фейк: нужны только worksheet(title),
    add_worksheet(title, rows, cols) и объект вкладки с clear()/
    update(rows)).

    Каждая вкладка перезаписывается целиком — это витрина, не архив,
    хранить историю тут не пытаемся.
    """

    for sheet_name, rows in export_data.items():
        try:
            worksheet = client.worksheet(sheet_name)
        except WorksheetNotFound:
            worksheet = client.add_worksheet(
                title=sheet_name,
                rows=max(len(rows), 10) + 10,
                cols=max(len(row) for row in rows) + 2,
            )

        worksheet.clear()
        worksheet.update(rows)


def run_export(spreadsheet_id, credentials_path):
    """
    Точка входа для cron (см. scripts/export_analytics.py): открывает
    таблицу через service account и заливает в неё свежие агрегаты.
    """

    import gspread

    from bot_services.analytics.users_export import sync_users_sheet

    gc = gspread.service_account(filename=credentials_path)
    spreadsheet = gc.open_by_key(spreadsheet_id)

    write_to_sheets(spreadsheet, build_export_data())

    # "Пользователи" — единственный лист, который не перезаписывается
    # целиком (см. users_export.py: там ручные "Комментарий").
    sync_users_sheet(spreadsheet)
