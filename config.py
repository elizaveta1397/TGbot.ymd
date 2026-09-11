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
# docs/IDEAS.md). Не секрет, поэтому прямо в коде, а не в .env.
#
# 2026-09-11, по прямому решению Лизы (после явного предупреждения
# о риске): здесь текст v2 («бот не собирает и не хранит персональные
# данные») ещё ДО того, как код полностью приведён в соответствие
# (activity.py всё ещё логирует текст сообщений, add_user() пишет
# username/имя — выгрузка листа "Пользователи" в Google Sheets уже
# убрана, см. sheets_export.py) и ДО подтверждения юристом — см.
# docs/IDEAS.md, п.1.7/1.8/1.9. Хостинг — teletype.in, не telegra.ph
# (publish_privacy_policy.py его не обновляет, правки — вручную на
# teletype.in).
PRIVACY_POLICY_URL = "https://teletype.in/@your.mental.doc/privacy_policy"
