"""
Работа с параметром current_step пользователя.

Используется всеми процессами бота для возврата
пользователя на последний экран после неизвестной команды.
"""

from bot_services.database import (
    get_user_parameter,
    set_user_parameter
)


def set_current_step(user_id: int, step: str):
    """
    Сохранить текущий шаг пользователя.
    """

    set_user_parameter(
        user_id=user_id,
        key="current_step",
        value=step
    )


def get_current_step(user_id: int):
    """
    Получить текущий шаг пользователя.
    """

    return get_user_parameter(
        user_id=user_id,
        key="current_step"
    )
