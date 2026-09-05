"""
Тесты для bot_services/analytics/users_export.py.
"""

from gspread.exceptions import WorksheetNotFound

from bot_services.analytics import users_export
from bot_services.database import add_user


def test_build_user_rows_formats_username_and_source_fallbacks(db):
    add_user(
        telegram_id=1,
        username="liza",
        first_name="Liza",
        last_name="S",
        source="cinemalogy_01",
    )
    add_user(
        telegram_id=2,
        username=None,
        first_name="Anon",
        last_name=None,
        source=None,
    )

    rows = users_export.build_user_rows()

    assert rows[0] == ["@liza", "Liza", rows[0][2], "cinemalogy_01", "", "1"]
    assert rows[1] == ["не указан", "Anon", rows[1][2], "не указан", "", "2"]


class FakeWorksheetUsers:
    def __init__(self, initial_rows=None):
        self.rows = initial_rows or []
        self.appended = []
        self.cleared = False

    def get_all_values(self):
        return self.rows

    def update(self, values):
        self.rows = values

    def append_rows(self, values, value_input_option=None):
        self.appended.extend(values)
        self.rows = self.rows + values

    def clear(self):
        self.cleared = True
        self.rows = []


class FakeSpreadsheetNoUsersSheet:
    def __init__(self):
        self.created = {}

    def worksheet(self, title):
        raise WorksheetNotFound(title)

    def add_worksheet(self, title, rows, cols):
        worksheet = FakeWorksheetUsers()
        self.created[title] = worksheet
        return worksheet


class FakeSpreadsheetWithUsersSheet:
    def __init__(self, worksheet):
        self._worksheet = worksheet

    def worksheet(self, title):
        return self._worksheet


def test_sync_users_sheet_creates_sheet_with_header_on_first_run(db):
    add_user(
        telegram_id=1,
        username="liza",
        first_name="Liza",
        last_name=None,
        source="cinemalogy_01",
    )

    client = FakeSpreadsheetNoUsersSheet()
    added = users_export.sync_users_sheet(client)

    worksheet = client.created[users_export.USERS_SHEET_NAME]
    assert worksheet.rows[0] == users_export.USERS_HEADER
    assert worksheet.rows[1][5] == "1"
    assert added == 1


def test_sync_users_sheet_only_appends_new_users_and_keeps_manual_comment(db):
    add_user(
        telegram_id=1,
        username="liza",
        first_name="Liza",
        last_name=None,
        source="cinemalogy_01",
    )
    add_user(
        telegram_id=2,
        username="new_user",
        first_name="New",
        last_name=None,
        source="cinemalogy_01",
    )

    existing = [
        users_export.USERS_HEADER,
        ["@liza", "Liza", "2026-06-09 19:00:06", "cinemalogy_01", "постоянная клиентка", "1"],
    ]
    worksheet = FakeWorksheetUsers(initial_rows=existing)
    client = FakeSpreadsheetWithUsersSheet(worksheet)

    added = users_export.sync_users_sheet(client)

    assert added == 1
    assert worksheet.cleared is False
    # старая строка с ручным комментарием не тронута
    assert worksheet.rows[1] == [
        "@liza", "Liza", "2026-06-09 19:00:06", "cinemalogy_01",
        "постоянная клиентка", "1",
    ]
    # новый юзер дописан именно через append, не через update/clear
    assert len(worksheet.appended) == 1
    assert worksheet.appended[0][5] == "2"


def test_sync_users_sheet_adds_nothing_when_no_new_users(db):
    add_user(
        telegram_id=1,
        username="liza",
        first_name="Liza",
        last_name=None,
        source="cinemalogy_01",
    )

    existing = [
        users_export.USERS_HEADER,
        ["@liza", "Liza", "2026-06-09 19:00:06", "cinemalogy_01", "", "1"],
    ]
    worksheet = FakeWorksheetUsers(initial_rows=existing)
    client = FakeSpreadsheetWithUsersSheet(worksheet)

    added = users_export.sync_users_sheet(client)

    assert added == 0
    assert worksheet.appended == []
