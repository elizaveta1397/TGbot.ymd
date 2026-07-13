"""
Работа с таблицей materials_cinemalogy.

Все материалы процесса Cinemalogy должны
получаться только через этот сервис.
"""

import sqlite3


# Путь к базе данных
DATABASE_PATH = "data/bot.db"


def get_material(code: str):
    """
    Получить материал по его коду.
    """

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM materials_cinemalogy
        WHERE code = ?
        AND is_active = 1
        """,
        (code,)
    )

    material = cursor.fetchone()

    connection.close()

    return material
