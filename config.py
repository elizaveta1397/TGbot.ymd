import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
CARE_TEAM_CHAT_ID = int(os.getenv("CARE_TEAM_CHAT_ID", "8673829586"))
