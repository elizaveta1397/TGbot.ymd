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

# Политика обработки ПДн — открывается пользователю как веб-страница
# по ссылке, а не документом в чат (см. handlers/start.py, п.10/12
# docs/IDEAS.md). Публикуется/обновляется через
# scripts/publish_privacy_policy.py — не секрет, поэтому прямо в коде,
# а не в .env; сам access_token для редактирования страницы — в .env
# (TELEGRAPH_ACCESS_TOKEN), в git не попадает.
PRIVACY_POLICY_URL = (
    "https://telegra.ph/Politika-obrabotki-personalnyh-dannyh-09-10-3"
)
