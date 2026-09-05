"""
Общие фикстуры для тестов.
"""

import os

# config.py требует BOT_TOKEN/ADMIN_ID из окружения (обычно из .env,
# который не попадает в репозиторий и в CI отсутствует). Подставляем
# безопасные заглушки ДО импорта любых модулей, тянущих config.py —
# setdefault, чтобы не перебивать реальный .env при локальном запуске.
os.environ.setdefault("BOT_TOKEN", "test-token")
os.environ.setdefault("ADMIN_ID", "1")
os.environ.setdefault("NOTIFY_ADMIN_ID", "1")
os.environ.setdefault("CARE_TEAM_CHAT_ID", "1")

import pytest

from bot_services import database
from bot_services.cinemalogy import materials as cinemalogy_materials


@pytest.fixture
def db(tmp_path, monkeypatch):
    """
    Изолированная sqlite БД на каждый тест.

    Подменяет bot_services.database.DB_PATH на временный файл и
    создаёт в нём все таблицы, чтобы тесты никогда не трогали
    боевую data/bot.db и не зависели друг от друга.

    bot_services/cinemalogy/materials.py держит собственную константу
    DATABASE_PATH (не переиспользует database.DB_PATH) — подменяем и
    её на тот же файл, иначе get_material() читал бы боевую БД.
    """

    db_path = tmp_path / "test.db"
    monkeypatch.setattr(database, "DB_PATH", str(db_path))
    monkeypatch.setattr(cinemalogy_materials, "DATABASE_PATH", str(db_path))

    database.create_tables()

    return database
