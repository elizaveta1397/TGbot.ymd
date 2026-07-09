"""
Работа с общей таблицей materials.
"""

import sqlite3

DATABASE_PATH = "data/bot.db"


def get_material(code: str):

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM materials
        WHERE code = ?
        AND is_active = 1
        """,
        (code,)
    )

    material = cursor.fetchone()

    connection.close()

    return material
