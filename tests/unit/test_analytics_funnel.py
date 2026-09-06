"""
Тесты для bot_services/analytics/funnel.py.
"""

import sqlite3

from bot_services.analytics import funnel
from bot_services.database import add_event, add_user


def test_funnel_counts_covers_all_known_steps_in_order(db):
    steps = [row["step"] for row in funnel.funnel_counts()]
    assert steps == funnel.FUNNEL_STEPS


def test_funnel_counts_counts_distinct_users_per_step(db):
    add_event(1, "cinemalogy_start")
    add_event(1, "choose_frame")
    add_event(2, "cinemalogy_start")
    add_event(2, "choose_frame")
    add_event(2, "choose_frame")  # тот же юзер дважды — не задвоить

    counts = {row["step"]: row["unique_users"] for row in funnel.funnel_counts()}

    assert counts["cinemalogy_start"] == 2
    assert counts["choose_frame"] == 2
    assert counts["confirm_frame"] == 0


def test_conversion_rates_first_step_has_no_previous(db):
    add_event(1, "cinemalogy_start")

    rows = funnel.conversion_rates(funnel.funnel_counts())

    assert rows[0]["conversion_from_previous"] is None


def test_conversion_rates_computes_percentage_between_steps(db):
    add_event(1, "cinemalogy_start")
    add_event(2, "cinemalogy_start")
    add_event(1, "choose_frame")

    rows = funnel.conversion_rates(funnel.funnel_counts())

    choose_frame_row = next(r for r in rows if r["step"] == "choose_frame")
    assert choose_frame_row["conversion_from_previous"] == 50.0


def test_conversion_rates_handles_zero_previous_step(db):
    rows = funnel.conversion_rates(funnel.funnel_counts())

    # ни одного события нет вообще — 0 пользователей на каждом шаге,
    # делить не на что
    assert all(row["unique_users"] == 0 for row in rows)
    assert rows[1]["conversion_from_previous"] is None


def test_registrations_by_source_groups_and_counts(db):
    add_user(telegram_id=1, username="a", first_name="A", last_name=None, source="cinemalogy_01")
    add_user(telegram_id=2, username="b", first_name="B", last_name=None, source="cinemalogy_01")
    add_user(telegram_id=3, username="c", first_name="C", last_name=None, source=None)

    rows = {r["source"]: r["registrations"] for r in funnel.registrations_by_source()}

    assert rows["cinemalogy_01"] == 2
    assert rows["не указан"] == 1


def test_sales_by_tariff_counts_only_payment_done_events(db):
    add_event(1, "cinemalogy_payment_done", "mini")
    add_event(2, "cinemalogy_payment_done", "mini")
    add_event(3, "cinemalogy_payment_done", "maxi")
    add_event(1, "cinemalogy_payment_opened", "mini")  # не должно попасть

    rows = {r["tariff"]: r["payments_done"] for r in funnel.sales_by_tariff()}

    assert rows == {"mini": 2, "maxi": 1}


def test_other_engagement_counts_covers_all_known_events_in_order(db):
    event_types = [row["event_type"] for row in funnel.other_engagement_counts()]
    assert event_types == funnel.OTHER_ENGAGEMENT_EVENTS


def test_other_engagement_counts_counts_unique_and_total(db):
    add_event(1, "menu_about_me")
    add_event(1, "menu_about_me")  # тот же юзер дважды — не задвоить unique, но total считает оба
    add_event(2, "menu_about_me")
    add_event(1, "consultation_request")

    rows = {
        row["event_type"]: row
        for row in funnel.other_engagement_counts()
    }

    assert rows["menu_about_me"]["unique_users"] == 2
    assert rows["menu_about_me"]["total_events"] == 3
    assert rows["consultation_request"]["unique_users"] == 1
    assert rows["menu_lullabies"]["unique_users"] == 0


def test_daily_active_users_groups_by_day_without_duplicates(db):
    conn = sqlite3.connect(db.DB_PATH)
    conn.executemany(
        """
        INSERT INTO user_events (telegram_id, event_type, event_data, created_at)
        VALUES (?, ?, ?, ?)
        """,
        [
            (1, "message", None, "2026-09-01 10:00:00"),
            (2, "message", None, "2026-09-01 12:00:00"),
            (1, "message", None, "2026-09-01 18:00:00"),  # тот же юзер, тот же день
            (3, "message", None, "2026-09-02 09:00:00"),
        ],
    )
    conn.commit()
    conn.close()

    rows = {r["date"]: r["unique_users"] for r in funnel.daily_active_users()}

    assert rows == {"2026-09-01": 2, "2026-09-02": 1}
