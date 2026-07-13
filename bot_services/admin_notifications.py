from config import ADMIN_ID


async def notify_new_user(bot, user, source):

    username = (
        f"@{user.username}"
        if user.username
        else "не указан"
    )

    last_name = (
        user.last_name
        if user.last_name
        else "не указана"
    )

    source_text = (
        source
        if source
        else "не указан"
    )

    language = (
        user.language_code
        if user.language_code
        else "не указан"
    )

    text = (
        "🆕 Новый пользователь\n\n"
        f"Имя: {user.first_name}\n"
        f"Фамилия: {last_name}\n"
        f"Username: {username}\n"
        f"Telegram ID: {user.id}\n"
        f"Язык: {language}\n"
        f"Источник: {source_text}"
    )

    await bot.send_message(
        chat_id=ADMIN_ID,
        text=text
    )


async def notify_admin_payment_start(bot, user, tariff):
    text = (
        "💳 Старт оплаты\n\n"
        f"Пользователь: {user.first_name}\n"
        f"Username: @{user.username if user.username else 'нет'}\n"
        f"ID: {user.id}\n"
        f"Тариф: {tariff}"
    )

    await bot.send_message(chat_id=ADMIN_ID, text=text)


async def notify_admin_payment_done(bot, user, tariff):
    text = (
        "✅ Оплата подтверждена\n\n"
        f"Пользователь: {user.first_name}\n"
        f"Username: @{user.username if user.username else 'нет'}\n"
        f"ID: {user.id}\n"
        f"Тариф: {tariff}"
    )

    await bot.send_message(chat_id=ADMIN_ID, text=text)

async def notify_admin_payment_start(
    bot,
    user,
    tariff
):
    username = (
        f"@{user.username}"
        if user.username
        else "не указан"
    )

    await bot.send_message(
        ADMIN_ID,
        (
            "💳 Пользователь перешел к оплате\n\n"
            f"Имя: {user.first_name}\n"
            f"Username: {username}\n"
            f"Telegram ID: {user.id}\n"
            f"Тариф: {tariff}"
        )
    )


async def notify_admin_payment_done(
    bot,
    user,
    tariff
):
    username = (
        f"@{user.username}"
        if user.username
        else "не указан"
    )

    await bot.send_message(
        ADMIN_ID,
        (
            "✅ Пользователь нажал «Билет оплачен»\n\n"
            f"Имя: {user.first_name}\n"
            f"Username: {username}\n"
            f"Telegram ID: {user.id}\n"
            f"Тариф: {tariff}"
        )
    )
