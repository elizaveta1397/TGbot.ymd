"""
Работа с кадрами Cinemalogy.
"""

FRAME_COUNT = 12


def next_frame(index: int) -> int:
    """
    Следующий кадр.
    """

    return (index + 1) % FRAME_COUNT


def previous_frame(index: int) -> int:
    """
    Предыдущий кадр.
    """

    return (index - 1) % FRAME_COUNT


def normalize(index: int) -> int:
    """
    Исправить номер кадра.
    """

    return index % FRAME_COUNT


def frame_material(index: int) -> str:
    """
    Возвращает ключ материала.

    Пока используются заглушки.
    Позже здесь будет чтение из БД.
    """

    return f"frame_{index + 1}"


