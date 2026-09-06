from aiogram import Router, F
from aiogram.types import Message

from bot_services.admin_notifications import notify_care_team

router = Router()

ADMIN_WORDS = ("адм", "админ", "admin", "adm")

# content_type -> имя атрибута Message, в котором лежит объект с file_id.
# "photo" сюда не входит — там список PhotoSize, обрабатывается отдельно.
MEDIA_CONTENT_TYPE_TO_ATTR = {
    "voice": "voice",
    "video_note": "video_note",
    "video": "video",
    "audio": "audio",
    "animation": "animation",
    "document": "document",
    "sticker": "sticker",
}


def is_admin_command(text: str) -> bool:
    if not text:
        return False
    tl = text.strip().lower()
    return any(tl.startswith(w) for w in ADMIN_WORDS)


def get_media_file_id(message: Message) -> str | None:
    """
    file_id медиа-вложения сообщения, определённый по content_type
    (не по hasattr/truthiness самих полей — они есть у любого Message).
    None, если content_type не медиа с file_id (пришли, например,
    контакт или локация).
    """

    if message.content_type == "photo":
        photo = message.photo
        return photo[-1].file_id if photo else None

    attr = MEDIA_CONTENT_TYPE_TO_ATTR.get(message.content_type)
    if not attr:
        return None

    obj = getattr(message, attr, None)
    return obj.file_id if obj else None


@router.message(F.text)
async def process_unknown(message: Message):

    # --- Админ-команда ---
    if is_admin_command(message.text):
        from handlers.admin import admin_entry
        await admin_entry(message)
        return

    # --- Обычный unknown ---
    await message.answer(
        "Я не понял сообщение. Используйте кнопки меню или нажмите /start.\n\n"
        "Если вам нужна помощь, вы можете написать в отдел Заботы @goncharova_help ♥️"
    )

    # --- Уведомление в отдел Заботы ---
    await notify_care_team(
        bot=message.bot,
        user=message.from_user,
        text=message.text
    )


# ============================
# Нетекстовые сообщения (фото, видео, кружки, войсы, аудио, гифки, ...)
#
# Обычный пользователь: тот же unknown-сценарий, что и для текста.
# Админ (is_admin() == True, см. handlers/admin.py): вместо unknown —
# возвращает file_id вложения, чтобы не искать его вручную в логах.
# ============================
@router.message(~F.text)
async def process_unknown_media(message: Message):

    from handlers.admin import is_admin

    if is_admin(message.from_user.id):
        file_id = get_media_file_id(message)

        if file_id:
            await message.answer(f"file_id: {file_id}")
        else:
            await message.answer(
                f"Не нашёл file_id для этого типа сообщения "
                f"(content_type={message.content_type})."
            )
        return

    # --- Обычный unknown ---
    await message.answer(
        "Я не понял сообщение. Используйте кнопки меню или нажмите /start.\n\n"
        "Если вам нужна помощь, вы можете написать в отдел Заботы @goncharova_help ♥️"
    )

    # --- Уведомление в отдел Заботы ---
    await notify_care_team(
        bot=message.bot,
        user=message.from_user,
        text=f"[{message.content_type}]"
    )
