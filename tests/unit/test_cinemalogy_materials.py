"""
Тесты для bot_services/cinemalogy/materials.py — единственная точка
доступа к таблице materials_cinemalogy.
"""

import sqlite3

from bot_services.cinemalogy.materials import get_material


def _insert_material(db, **overrides):
    row = {
        "code": "frame_1",
        "type": "photo",
        "telegram_file_id": "FILE_ID_1",
        "text": "Кадр 1",
        "url": None,
        "is_active": 1,
    }
    row.update(overrides)

    conn = sqlite3.connect(db.DB_PATH)
    conn.execute(
        """
        INSERT INTO materials_cinemalogy (code, type, telegram_file_id, text, url, is_active)
        VALUES (:code, :type, :telegram_file_id, :text, :url, :is_active)
        """,
        row,
    )
    conn.commit()
    conn.close()


def test_get_material_missing_returns_none(db):
    assert get_material("frame_1") is None


def test_get_material_returns_active_material(db):
    _insert_material(db, code="frame_1", text="Кадр 1")

    material = get_material("frame_1")

    assert material is not None
    assert material["code"] == "frame_1"
    assert material["text"] == "Кадр 1"
    assert material["telegram_file_id"] == "FILE_ID_1"


def test_get_material_ignores_inactive_material(db):
    _insert_material(db, code="frame_1", is_active=0)

    assert get_material("frame_1") is None


def test_get_material_matches_by_exact_code(db):
    _insert_material(db, code="frame_1", text="Кадр 1")
    _insert_material(db, code="frame_2", text="Кадр 2")

    material = get_material("frame_2")

    assert material["text"] == "Кадр 2"
