"""
Тесты слоя БД (bot_services/database.py) — фундамент, от которого
зависит вся остальная бизнес-логика бота.
"""

import sqlite3

from bot_services.database import (
    add_user,
    get_user,
    get_all_users,
    update_last_activity,
    add_event,
    cleanup_old_events,
    get_user_parameter,
    set_user_parameter,
    delete_user_parameter,
    delete_user,
)


def test_get_user_missing_returns_none(db):
    assert get_user(999) is None


def test_add_and_get_user(db):
    add_user(
        telegram_id=1,
        username="liza",
        first_name="Liza",
        last_name="S",
        source="ads",
    )

    user = get_user(1)

    assert user is not None
    assert user[1] == 1          # telegram_id
    assert user[2] == "liza"     # username
    assert user[8] == "ads"      # source


def test_get_all_users_orders_by_registration_date(db):
    add_user(telegram_id=2, username="second", first_name="B", last_name=None)
    add_user(telegram_id=1, username="first", first_name="A", last_name=None)

    conn = sqlite3.connect(db.DB_PATH)
    conn.execute(
        "UPDATE users SET registration_date = '2020-01-01 00:00:00' WHERE telegram_id = 1"
    )
    conn.execute(
        "UPDATE users SET registration_date = '2021-01-01 00:00:00' WHERE telegram_id = 2"
    )
    conn.commit()
    conn.close()

    users = get_all_users()

    assert [u[1] for u in users] == [1, 2]  # telegram_id, старые сначала


def test_update_last_activity_does_not_error(db):
    add_user(telegram_id=1, username="liza", first_name="Liza", last_name="S")

    update_last_activity(1)

    user = get_user(1)
    assert user[6] is not None   # last_activity


def test_add_event_is_stored(db):
    add_event(telegram_id=1, event_type="start", event_data="{}")

    conn = sqlite3.connect(db.DB_PATH)
    rows = conn.execute(
        "SELECT telegram_id, event_type, event_data FROM user_events"
    ).fetchall()
    conn.close()

    assert rows == [(1, "start", "{}")]


def test_cleanup_old_events_keeps_recent_events(db):
    add_event(telegram_id=1, event_type="start")

    cleanup_old_events()

    conn = sqlite3.connect(db.DB_PATH)
    count = conn.execute("SELECT COUNT(*) FROM user_events").fetchone()[0]
    conn.close()

    assert count == 1


def test_cleanup_old_events_removes_events_older_than_30_days(db):
    conn = sqlite3.connect(db.DB_PATH)
    conn.execute(
        """
        INSERT INTO user_events (telegram_id, event_type, event_data, created_at)
        VALUES (1, 'start', NULL, datetime('now', '-31 days'))
        """
    )
    conn.commit()
    conn.close()

    cleanup_old_events()

    conn = sqlite3.connect(db.DB_PATH)
    count = conn.execute("SELECT COUNT(*) FROM user_events").fetchone()[0]
    conn.close()

    assert count == 0


class TestDeleteUser:
    def test_deletes_user_events_and_parameters(self, db):
        add_user(telegram_id=1, username="liza", first_name="Liza", last_name="S")
        add_event(telegram_id=1, event_type="start")
        set_user_parameter(1, "current_step", "cinemalogy_start")

        assert delete_user(1) is True

        assert get_user(1) is None
        assert get_user_parameter(1, "current_step") is None

        conn = sqlite3.connect(db.DB_PATH)
        count = conn.execute(
            "SELECT COUNT(*) FROM user_events WHERE telegram_id = ?", (1,)
        ).fetchone()[0]
        conn.close()
        assert count == 0

    def test_does_not_touch_other_users(self, db):
        add_user(telegram_id=1, username="liza", first_name="Liza", last_name="S")
        add_user(telegram_id=2, username="other", first_name="Other", last_name=None)
        set_user_parameter(2, "current_step", "keep_me")

        delete_user(1)

        assert get_user(2) is not None
        assert get_user_parameter(2, "current_step") == "keep_me"

    def test_missing_user_returns_false(self, db):
        assert delete_user(999) is False


class TestUserParameters:
    def test_get_missing_parameter_returns_none(self, db):
        assert get_user_parameter(1, "current_step") is None

    def test_set_then_get(self, db):
        set_user_parameter(1, "current_step", "cinemalogy_start")

        assert get_user_parameter(1, "current_step") == "cinemalogy_start"

    def test_set_overwrites_existing_value(self, db):
        set_user_parameter(1, "current_step", "a")
        set_user_parameter(1, "current_step", "b")

        assert get_user_parameter(1, "current_step") == "b"

    def test_delete_parameter(self, db):
        set_user_parameter(1, "current_step", "a")
        delete_user_parameter(1, "current_step")

        assert get_user_parameter(1, "current_step") is None

    def test_parameters_are_isolated_per_user(self, db):
        set_user_parameter(1, "current_step", "user1_step")
        set_user_parameter(2, "current_step", "user2_step")

        assert get_user_parameter(1, "current_step") == "user1_step"
        assert get_user_parameter(2, "current_step") == "user2_step"
