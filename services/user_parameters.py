"""
Работа с параметрами пользователя.

Является оберткой над database.py.
Используется всеми процессами бота.
"""

from services.database import (
    get_user_parameter,
    set_user_parameter,
    delete_user_parameter
)


def get_parameter(user_id: int, name: str):
    """
    Получить параметр пользователя.
    """
    return get_user_parameter(user_id, name)


def set_parameter(user_id: int, name: str, value: str):
    """
    Создать или обновить параметр пользователя.
    """
    set_user_parameter(
        telegram_id=user_id,
        parameter_name=name,
        parameter_value=value
    )


def delete_parameter(user_id: int, name: str):
    """
    Удалить параметр пользователя.
    """
    delete_user_parameter(
        telegram_id=user_id,
        parameter_name=name
    )
