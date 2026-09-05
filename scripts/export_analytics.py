#!/usr/bin/env python3
"""
Выгружает агрегаты аналитики бота в Google Sheets.

Запускать по cron (пример — в docs/ANALYTICS_DASHBOARD.md), например
раз в сутки ночью. Настройка (создание Google-таблицы, service
account, .env-переменные) — тоже в docs/ANALYTICS_DASHBOARD.md, это
разовое действие через Google-аккаунт Лизы, отдельно от кода.
"""

import os
import sys

# Скрипт лежит в scripts/, а bot_services/config.py — в корне репозитория;
# при запуске `python scripts/export_analytics.py` (в т.ч. из cron, где
# рабочая директория может быть не задана) корень сам по себе в sys.path
# не попадает.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot_services.analytics.sheets_export import run_export
from config import ANALYTICS_SPREADSHEET_ID, GOOGLE_SHEETS_CREDENTIALS_PATH


def main():
    if not ANALYTICS_SPREADSHEET_ID or not GOOGLE_SHEETS_CREDENTIALS_PATH:
        sys.exit(
            "ANALYTICS_SPREADSHEET_ID и/или GOOGLE_SHEETS_CREDENTIALS_PATH "
            "не заданы в .env — см. docs/ANALYTICS_DASHBOARD.md, раздел "
            "«Настройка»."
        )

    run_export(ANALYTICS_SPREADSHEET_ID, GOOGLE_SHEETS_CREDENTIALS_PATH)
    print("Аналитика выгружена в Google Sheets")


if __name__ == "__main__":
    main()
