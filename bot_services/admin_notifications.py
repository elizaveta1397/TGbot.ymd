from config import NOTIFY_ADMIN_ID, CARE_TEAM_CHAT_ID


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
        chat_id=NOTIFY_ADMIN_ID,
        text=text,
        disable_notification=True  # тихое по умолчанию — см. CLAUDE.md
    )


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
        NOTIFY_ADMIN_ID,
        (
            "💳 Пользователь перешел к оплате\n\n"
            f"Имя: {user.first_name}\n"
            f"Username: {username}\n"
            f"Telegram ID: {user.id}\n"
            f"Тариф: {tariff}"
        ),
        disable_notification=True  # тихое по умолчанию — см. CLAUDE.md
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
        NOTIFY_ADMIN_ID,
        (
            "✅ Пользователь нажал «Билет оплачен»\n\n"
            f"Имя: {user.first_name}\n"
            f"Username: {username}\n"
            f"Telegram ID: {user.id}\n"
            f"Тариф: {tariff}"
        )
    )


async def notify_admin_consultation_request(bot, user):
    username = (
        f"@{user.username}"
        if user.username
        else "не указан"
    )

    await bot.send_message(
        NOTIFY_ADMIN_ID,
        (
            "📩 Запрос на консультацию\n\n"
            f"Имя: {user.first_name}\n"
            f"Username: {username}\n"
            f"Telegram ID: {user.id}"
        ),
        disable_notification=True  # тихое по умолчанию — см. CLAUDE.md
    )


async def notify_admin_tariff_viewed(bot, user, tariff_name):
    username = (
        f"@{user.username}"
        if user.username
        else "не указан"
    )

    await bot.send_message(
        NOTIFY_ADMIN_ID,
        (
            "👀 Пользователь просмотрел тариф\n\n"
            f"Имя: {user.first_name}\n"
            f"Username: {username}\n"
            f"Telegram ID: {user.id}\n"
            f"Тариф: {tariff_name}"
        ),
        disable_notification=True  # тихое по умолчанию — см. CLAUDE.md
    )


async def notify_care_team(bot, user, text):
    username = (
        f"@{user.username}"
        if user.username
        else "не указан"
    )

    await bot.send_message(
        chat_id=CARE_TEAM_CHAT_ID,
        text=(
            "🫶 Новый запрос в отдел Заботы\n\n"
            f"Имя: {user.first_name}\n"
            f"Фамилия: {user.last_name if user.last_name else 'не указана'}\n"
            f"Username: {username}\n"
            f"Telegram ID: {user.id}\n"
            f"Язык: {user.language_code if user.language_code else 'не указан'}\n\n"
            "Текст пользователя:\n"
            f"{text}"
        )
    )
