"""
Глобальная админ‑панель бота.
Доступна по слову "админ".
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from services.user_parameters import (
    get_parameter,
    set_parameter,
    delete_parameter
)

from services.database import get_connection

# Импортируем твой unknown‑хендлер
from handlers.unknown import process_unknown

router = Router()

# Твой Telegram ID
ADMIN_ID = 250428280


# -------------------------------
# Вход в админ‑панель
# -------------------------------
@router.message(F.text.lower().startswith("админ"))
async def admin_entry(message: Message):

    telegram_id = message.from_user.id

    # Если это не ты → сразу в unknown
    if telegram_id != ADMIN_ID:
        await process_unknown(message)
        return

    await show_admin_menu(message)


# -------------------------------
# Показать меню админа
# -------------------------------
async def show_admin_menu(message: Message):

    telegram_id = message.from_user.id

    # Мой статус
    my_status = get_parameter(telegram_id, "admin_mode")
    my_status = "on" if my_status == "on" else "off"

    # Список всех админов
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT u.username, u.telegram_id
        FROM users u
        JOIN user_parameters p
            ON u.telegram_id = p.telegram_id
        WHERE p.parameter_name = 'admin_mode'
          AND p.parameter_value = 'on'
    """)

    admins = cursor.fetchall()
    connection.close()

    admin_list = "\n".join(
        f"@{row['username']} ({row['telegram_id']})"
        for row in admins
    ) or "Нет других админов"

    text = (
        f"🛠 Админ‑панель\n\n"
        f"Ваш ID: {telegram_id}\n"
        f"Ваш статус: {my_status}\n\n"
        f"Другие админы:\n{admin_list}"
    )

    from keyboards.admin import admin_keyboard
    await message.answer(text, reply_markup=admin_keyboard())


# -------------------------------
# Переключить режим администратора
# -------------------------------
@router.callback_query(F.data == "admin_toggle")
async def admin_toggle(callback: CallbackQuery):

    # Проверка ID
    if callback.from_user.id != ADMIN_ID:
        await process_unknown(callback.message)
        return

    telegram_id = callback.from_user.id
    status = get_parameter(telegram_id, "admin_mode")

    if status == "on":
        delete_parameter(telegram_id, "admin_mode")
    else:
        set_parameter(telegram_id, "admin_mode", "on")

    await callback.answer("Статус обновлён")
    await show_admin_menu(callback.message)


# -------------------------------
# Дать доступ
# -------------------------------
@router.callback_query(F.data == "admin_grant")
async def admin_grant(callback: CallbackQuery):

    if callback.from_user.id != ADMIN_ID:
        await process_unknown(callback.message)
        return

    await callback.message.answer("Введите username пользователя, которому дать доступ:")
    set_parameter(callback.from_user.id, "admin_waiting_action", "grant")
    await callback.answer()


# -------------------------------
# Забрать доступ
# -------------------------------
@router.callback_query(F.data == "admin_revoke")
async def admin_revoke(callback: CallbackQuery):

    if callback.from_user.id != ADMIN_ID:
        await process_unknown(callback.message)
        return

    await callback.message.answer("Введите username пользователя, у которого забрать доступ:")
    set_parameter(callback.from_user.id, "admin_waiting_action", "revoke")
    await callback.answer()


# -------------------------------
# Обработка ввода username
# -------------------------------
@router.message(F.text)   # ← критично: ловим только текст
async def admin_username_input(message: Message):

    # Проверка ID
    if message.from_user.id != ADMIN_ID:
        await process_unknown(message)
        return

    # Если мы НЕ ждём username — выходим
    action = get_parameter(message.from_user.id, "admin_waiting_action")
    if action not in ("grant", "revoke"):
        return

    username = message.text.replace("@", "").strip()

    # Ищем пользователя
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT telegram_id
        FROM users
        WHERE username = ?
    """, (username,))

    row = cursor.fetchone()
    connection.close()

    if not row:
        await message.answer("Пользователь не найден.")
        delete_parameter(message.from_user.id, "admin_waiting_action")
        await show_admin_menu(message)
        return

    target_id = row["telegram_id"]

    if action == "grant":
        set_parameter(target_id, "admin_mode", "on")
        await message.answer(f"Доступ выдан @{username}.")
    else:
        delete_parameter(target_id, "admin_mode")
        await message.answer(f"Доступ забран у @{username}.")

    delete_parameter(message.from_user.id, "admin_waiting_action")
    await show_admin_menu(message)
