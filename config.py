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
