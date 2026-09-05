"""
Тесты для bot_services/current_step.py — используется всеми процессами
бота для возврата пользователя на последний экран после неизвестной
команды (handlers/unknown.py).
"""

from bot_services.current_step import get_current_step, set_current_step


def test_get_current_step_defaults_to_none(db):
    assert get_current_step(user_id=1) is None


def test_set_and_get_current_step(db):
    set_current_step(user_id=1, step="cinemalogy_choose_frame")

    assert get_current_step(user_id=1) == "cinemalogy_choose_frame"


def test_set_current_step_overwrites_previous_value(db):
    set_current_step(user_id=1, step="cinemalogy_start")
    set_current_step(user_id=1, step="cinemalogy_result")

    assert get_current_step(user_id=1) == "cinemalogy_result"
