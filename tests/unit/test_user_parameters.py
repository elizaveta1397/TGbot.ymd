"""
Тесты для bot_services/user_parameters.py — обёртки над database.py,
используемой всеми процессами бота (в т.ч. handlers/admin.py).
"""

from bot_services.user_parameters import (
    delete_parameter,
    get_parameter,
    set_parameter,
)


def test_get_missing_parameter_returns_none(db):
    assert get_parameter(1, "admin_mode") is None


def test_set_then_get_parameter(db):
    set_parameter(1, "admin_mode", "on")

    assert get_parameter(1, "admin_mode") == "on"


def test_delete_parameter_roundtrip(db):
    set_parameter(1, "admin_mode", "on")
    delete_parameter(1, "admin_mode")

    assert get_parameter(1, "admin_mode") is None
