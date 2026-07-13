from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
import sqlite3

from bot_services.database import (
    get_user_parameter,
    set_user_parameter,
    delete_user_parameter
)

# --- Роутер для сообщений (НЕ ПОДКЛЮЧАЕМ В bot.py) ---
router_admin_messages = Router()

# --- Роутер для callback-кнопок (ПОДКЛЮЧАЕМ В bot.py) ---
router_admin_callbacks = Router()

ADMIN_ID = 250428280


# ============================
# Вход в админ — вызывается через unknown
# ============================
async def admin_entry(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Вы не админ.")
        return

    await show_admin_menu(message)


# ============================
# Сборка текста и клавиатуры
# ============================
async def build_admin_menu_text_and_keyboard(telegram_id: int):
    my_status = get_user_parameter(telegram_id, "admin_mode")
    my_status = "on" if my_status == "on" else "off"

    connection = sqlite3.connect("/home/botuser/telegram-bot/data/bot.db")
    connection.row_factory = sqlite3.Row
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
    return text, admin_keyboard()


# ============================
# Показать меню админа
# ============================
async def show_admin_menu(message: Message):
    text, keyboard = await build_admin_menu_text_and_keyboard(message.from_user.id)
    await message.answer(text, reply_markup=keyboard)


# ============================
# Переключить режим администратора
# ============================
@router_admin_callbacks.callback_query(F.data == "admin_toggle")
async def admin_toggle(callback: CallbackQuery):

    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Вы не админ.")
        return

    telegram_id = callback.from_user.id
    status = get_user_parameter(telegram_id, "admin_mode")

    if status == "on":
        delete_user_parameter(telegram_id, "admin_mode")
    else:
        set_user_parameter(telegram_id, "admin_mode", "on")

    await callback.answer("Статус обновлён")

    # обновляем меню через edit_text — НЕ улетает в unknown
    text, keyboard = await build_admin_menu_text_and_keyboard(telegram_id)
    await callback.message.edit_text(text, reply_markup=keyboard)


# ============================
# Дать доступ
# ============================
@router_admin_callbacks.callback_query(F.data == "admin_grant")
async def admin_grant(callback: CallbackQuery):

    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Вы не админ.")
        return

    await callback.answer()
    await callback.message.answer("Введите username пользователя, которому дать доступ:")
    set_user_parameter(callback.from_user.id, "admin_waiting_action", "grant")


# ============================
# Забрать доступ
# ============================
@router_admin_callbacks.callback_query(F.data == "admin_revoke")
async def admin_revoke(callback: CallbackQuery):

    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Вы не админ.")
        return

    await callback.answer()
    await callback.message.answer("Введите username пользователя, у которого забрать доступ:")
    set_user_parameter(callback.from_user.id, "admin_waiting_action", "revoke")


# ============================
# Обработка ввода username
# ============================
@router_admin_messages.message(F.text & (F.from_user.id == ADMIN_ID))
async def admin_username_input(message: Message):

    action = get_user_parameter(message.from_user.id, "admin_waiting_action")
    if action not in ("grant", "revoke"):
        return  # unknown поймает

    username = message.text.replace("@", "").strip()

    connection = sqlite3.connect("/home/botuser/telegram-bot/data/bot.db")
    connection.row_factory = sqlite3.Row
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
        delete_user_parameter(message.from_user.id, "admin_waiting_action")
        await show_admin_menu(message)
        return

    target_id = row["telegram_id"]

    if action == "grant":
        set_user_parameter(target_id, "admin_mode", "on")
        await message.answer(f"Доступ выдан @{username}.")
    else:
        delete_user_parameter(target_id, "admin_mode")
        await message.answer(f"Доступ забран у @{username}.")

    delete_user_parameter(message.from_user.id, "admin_waiting_action")
    await show_admin_menu(message)
