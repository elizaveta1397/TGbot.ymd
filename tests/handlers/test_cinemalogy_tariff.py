"""
Шаг 7. Экран выбранного тарифа (handlers/cinemalogy/tariff.py).
"""

import sqlite3

from bot_services.user_parameters import get_parameter
from handlers.cinemalogy.tariff import tariff_maxi, tariff_midi, tariff_mini


async def test_tariff_mini_sends_ticket_photo(db, fake_callback, material):
    material("ticket_mini_image", telegram_file_id="TICKET_MINI")
    material("ticket_mini_text", text="Мини-билет")

    await tariff_mini(fake_callback)

    fake_callback.message.answer_photo.assert_awaited_once()
    kwargs = fake_callback.message.answer_photo.await_args.kwargs
    assert kwargs["photo"] == "TICKET_MINI"
    assert kwargs["caption"] == "Мини-билет"

    telegram_id = fake_callback.from_user.id
    assert get_parameter(telegram_id, "cinemalogy_tariff") == "mini"
    assert get_parameter(telegram_id, "current_step") == "tariff_mini"


async def test_tariff_notifies_admin(db, fake_callback, material):
    material("ticket_midi_image", telegram_file_id="TICKET_MIDI")
    material("ticket_midi_text", text="Миди-билет")

    await tariff_midi(fake_callback)

    fake_callback.bot.send_message.assert_awaited_once()


async def test_tariff_maxi_logs_analytics_event(db, fake_callback, material):
    material("ticket_maxi_image", telegram_file_id="TICKET_MAXI")
    material("ticket_maxi_text", text="Макси-билет")

    await tariff_maxi(fake_callback)

    conn = sqlite3.connect(db.DB_PATH)
    rows = conn.execute(
        "SELECT event_type, event_data FROM user_events"
    ).fetchall()
    conn.close()

    # Именно это упало бы, вернись баг с опечаткой в имени события
    # (cinemalogy_tariff_selectd вместо cinemalogy_tariff_selected).
    assert ("cinemalogy_tariff_selected", "maxi") in rows
