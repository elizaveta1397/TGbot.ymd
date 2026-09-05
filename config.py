import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ADMIN_ID — владелец бота: даёт доступ к админ-панели (handlers/admin.py).
# Не трогать при смене адресата уведомлений — это разные роли.
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# Куда падают все уведомления админу о действиях пользователей
# (новый юзер, оплата, тарифы и т.д.) — bot_services/admin_notifications.py
NOTIFY_ADMIN_ID = int(os.getenv("NOTIFY_ADMIN_ID", "8673829586"))

CARE_TEAM_CHAT_ID = int(os.getenv("CARE_TEAM_CHAT_ID", "8673829586"))

# Экспорт аналитики в Google Sheets (bot_services/analytics/,
# scripts/export_analytics.py, docs/ANALYTICS_DASHBOARD.md).
# Намеренно БЕЗ значения по умолчанию и без int()/обязательности —
# это опционально и не должно ронять бота, если ещё не настроено.
# Пока не заданы — export_analytics.py откажется работать с понятной
# ошибкой, сам бот эти переменные не читает вообще.
ANALYTICS_SPREADSHEET_ID = os.getenv("ANALYTICS_SPREADSHEET_ID")
GOOGLE_SHEETS_CREDENTIALS_PATH = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH")
