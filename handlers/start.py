# handlers/start.py

import os

from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.types import Message, CallbackQuery, FSInputFile

from bot_services.database import (
    get_user,
    add_user,
    add_event,
    delete_user
)
from bot_services.user_parameters import set_parameter

from keyboards.main_menu import main_menu
from keyboards.consent import consent_keyboard
from keyboards.delete_me import delete_confirm_keyboard
from bot_services.admin_notifications import (
    notify_new_user,
    notify_admin_data_deleted
)

router = Router()

POLICY_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "docs",
    "PRIVACY_POLICY.md"
)

CONSENT_TEXT = (
    "Прежде чем продолжить — пара слов про персональные данные.\n\n"
    "Чтобы бот работал (регистрация, аналитика, запись на консультацию "
    "и на Синемалогию), ему нужно хранить ваш Telegram ID, username, "
    "имя/фамилию и действия в диалоге. Полный текст — по кнопке "
    "«Читать политику» ниже или в любой момент командой /policy.\n\n"
    "Нажимая «Согласен(на)», вы подтверждаете, что ознакомились с "
    "Политикой обработки персональных данных, и даёте согласие на "
    "обработку своих персональных данных на условиях, описанных в ней. "
    "Без согласия бот не сможет вас зарегистрировать и продолжить работу."
)

# Источник (/start payload) нового пользователя, пока он не нажал
# «Согласен(на)» — держим в памяти процесса, не в БД: до согласия
# ничего, кроме уже неизбежного (Telegram и так передаёт боту
# telegram_id/username вместе с самим сообщением), не сохраняем.
# Теряется при перезапуске бота — некритично, source в этом случае
# просто останется пустым при последующей регистрации.
_pending_sources: dict[int, str | None] = {}


async def _send_policy(target: Message):
    await target.answer_document(
        FSInputFile(
            POLICY_PATH,
            filename="Политика обработки персональных данных.md"
        )
    )


# ============================
# /policy — доступна всем, без регистрации и без согласия
# ============================
@router.message(Command("policy"))
async def policy_command(message: Message):
    await _send_policy(message)


@router.callback_query(F.data == "policy_view")
async def policy_view(callback: CallbackQuery):
    await _send_policy(callback.message)
    await callback.answer()


# ============================
# START HANDLER
# ============================
@router.message(CommandStart())
async def start_handler(
    message: Message,
    command: CommandObject
):

    telegram_user = message.from_user

    # deep link (/start payload)
    source = command.args

    user = get_user(telegram_user.id)

    # ----------------------------
    # НОВЫЙ ПОЛЬЗОВАТЕЛЬ — сперва согласие на обработку ПДн (152-ФЗ),
    # регистрация (add_user) откладывается до нажатия «Согласен(на)»
    # в consent_accept ниже. Существующего пользователя эта ветка не
    # трогает — обычный /start ниже, как раньше.
    # ----------------------------
    if user is None:
        _pending_sources[telegram_user.id] = source

        await message.answer(
            CONSENT_TEXT,
            reply_markup=consent_keyboard()
        )
        return

    # ----------------------------
    # CINEMALOGY ROUTING
    # ----------------------------
    if source and source.startswith("cinemalogy"):
        from handlers.cinemalogy.start import start_cinemalogy

        await start_cinemalogy(
            message=message,
            source=source
        )
        return

    # ----------------------------
    # USER LOGIC (обычный /start уже существующего пользователя)
    # ----------------------------
    # update_last_activity сюда не добавляем — ActivityMiddleware уже
    # обновил её перед этим хендлером для любого сообщения
    # существующего пользователя, повторный вызов был бы дублем.
    add_event(
        telegram_user.id,
        "start",
        source
    )

    # ----------------------------
    # DEFAULT RESPONSE
    # ----------------------------
    await message.answer(
        "Добро пожаловать",
        reply_markup=main_menu
    )


# ============================
# СОГЛАСИЕ НА ОБРАБОТКУ ПДн — регистрация нового пользователя
# ============================
@router.callback_query(F.data == "consent_accept")
async def consent_accept(callback: CallbackQuery):

    telegram_user = callback.from_user
    source = _pending_sources.pop(telegram_user.id, None)

    add_user(
        telegram_id=telegram_user.id,
        username=telegram_user.username,
        first_name=telegram_user.first_name,
        last_name=telegram_user.last_name,
        source=source
    )

    # Факт согласия — в аналитику, отдельным событием (не раньше: до
    # этой строки пользователь ещё не подтвердил согласие).
    add_event(
        telegram_user.id,
        "consent_given",
        "privacy_policy_v1"
    )

    await notify_new_user(
        callback.bot,
        telegram_user,
        source
    )

    try:
        await callback.message.delete()
    except Exception:
        pass

    await callback.answer()

    if source and source.startswith("cinemalogy"):
        from handlers.cinemalogy.start import start_cinemalogy

        # telegram_id — явно: callback.message тут сообщение бота
        # (экран согласия), а не пользователя.
        await start_cinemalogy(
            message=callback.message,
            source=source,
            telegram_id=telegram_user.id
        )
        return

    await callback.message.answer(
        "Добро пожаловать",
        reply_markup=main_menu
    )


# ============================
# УДАЛЕНИЕ ДАННЫХ ПО ЗАПРОСУ — ст. 14 152-ФЗ, docs/IDEAS.md п.1
# ============================
@router.message(Command("delete_me"))
async def delete_me_command(message: Message):
    telegram_id = message.from_user.id

    if get_user(telegram_id) is None:
        await message.answer(
            "Мы не нашли ваших данных в этом боте — либо вы ещё не "
            "начинали (/start), либо они уже были удалены раньше."
        )
        return

    await message.answer(
        "Удалить все ваши данные из этого бота — регистрацию, историю "
        "действий, сохранённые параметры (тариф, шаг сценария и т.п.)? "
        "Это необратимо.",
        reply_markup=delete_confirm_keyboard()
    )


@router.callback_query(F.data == "delete_me_confirm")
async def delete_me_confirm(callback: CallbackQuery):
    telegram_user = callback.from_user

    existed = delete_user(telegram_user.id)

    try:
        await callback.message.delete()
    except Exception:
        pass

    await callback.answer()

    if not existed:
        await callback.message.answer("Ваших данных уже не было в системе.")
        return

    # Журнал обращений субъектов (152-ФЗ, ст. 14, п.7 чек-листа из
    # памяти ru-legal-compliance-risks) — в лог процесса (journalctl),
    # не в БД: сама БД для этого telegram_id уже стёрта строкой выше.
    print(
        "[PDN] Запрос на удаление обработан: "
        f"telegram_id={telegram_user.id}"
    )

    await notify_admin_data_deleted(callback.bot, telegram_user)

    await callback.message.answer(
        "Готово — все ваши данные удалены. Если снова напишете /start, "
        "регистрация начнётся заново."
    )


@router.callback_query(F.data == "delete_me_cancel")
async def delete_me_cancel(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except Exception:
        pass

    await callback.answer("Отменено")


# ============================
# MAIN MENU BUTTONS
# ============================

# Обо мне → новая ссылка
@router.message(F.text == "Обо мне")
async def about_me(message: Message):
    telegram_id = message.from_user.id

    set_parameter(telegram_id, "current_step", "menu_about_me")
    add_event(telegram_id, "menu_about_me", None)

    await message.answer(
        "Обо мне:\nhttps://telegra.ph/Obo-mne-07-14-13"
    )


# Записаться на консультацию → запускаем consultation_start
@router.message(F.text == "Записаться на консультацию")
async def sign_up(message: Message):
    from handlers.consultation import send_consultation_waitlist

    await send_consultation_waitlist(
        message=message,
        user=message.from_user,
        bot=message.bot
    )


# 12 взрослых колыбельных → ссылка
@router.message(F.text == "12 взрослых колыбельных")
async def lullabies(message: Message):
    telegram_id = message.from_user.id

    set_parameter(telegram_id, "current_step", "menu_lullabies")
    add_event(telegram_id, "menu_lullabies", None)

    await message.answer(
        "12 взрослых колыбельных:\nhttps://t.me/your_mental_doc/131"
    )


# Синемалогия → переход на старт синемалогии
@router.message(F.text == "Синемалогия")
async def cinemalogy_start(message: Message):
    from handlers.cinemalogy.start import start_cinemalogy
    await start_cinemalogy(message)
