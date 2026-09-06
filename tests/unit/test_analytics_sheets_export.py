"""
Тесты для bot_services/analytics/sheets_export.py.

Реальный Google API нигде не трогаем — build_export_data() чистая, а
write_to_sheets() получает фейковый клиент с тем же интерфейсом, что
и gspread.Spreadsheet (worksheet()/add_worksheet(), объект вкладки с
clear()/update()).
"""

from gspread.exceptions import WorksheetNotFound

from bot_services.analytics import sheets_export
from bot_services.database import add_event


def test_build_export_data_has_all_expected_sheets_with_headers(db):
    add_event(1, "cinemalogy_start")

    data = sheets_export.build_export_data()

    assert set(data.keys()) == {
        "Воронка",
        "Источники",
        "Продажи",
        "Активность по дням",
        "Вовлечённость",
    }
    assert data["Воронка"][0] == [
        "Шаг",
        "Уникальных пользователей",
        "Конверсия с предыдущего шага, %",
    ]
    # +1 заголовок + 8 шагов воронки
    assert len(data["Воронка"]) == 1 + len(sheets_export.funnel.FUNNEL_STEPS)

    assert data["Вовлечённость"][0] == [
        "Событие",
        "Уникальных пользователей",
        "Всего срабатываний",
    ]
    # +1 заголовок + все не-воронка события
    assert len(data["Вовлечённость"]) == (
        1 + len(sheets_export.funnel.OTHER_ENGAGEMENT_EVENTS)
    )


class FakeWorksheet:
    def __init__(self):
        self.cleared = False
        self.updated_rows = None

    def clear(self):
        self.cleared = True

    def update(self, rows):
        self.updated_rows = rows


class FakeSpreadsheetWithExistingTabs:
    def __init__(self):
        self.sheets = {}

    def worksheet(self, title):
        return self.sheets.setdefault(title, FakeWorksheet())

    def add_worksheet(self, title, rows, cols):
        raise AssertionError("вкладка уже должна была существовать")


def test_write_to_sheets_clears_and_updates_each_existing_tab(db):
    client = FakeSpreadsheetWithExistingTabs()
    export_data = {"Tab A": [["h1", "h2"], [1, 2]], "Tab B": [["h"]]}

    sheets_export.write_to_sheets(client, export_data)

    assert client.sheets["Tab A"].cleared is True
    assert client.sheets["Tab A"].updated_rows == [["h1", "h2"], [1, 2]]
    assert client.sheets["Tab B"].updated_rows == [["h"]]


class FakeSpreadsheetMissingTabs:
    def __init__(self):
        self.created = {}

    def worksheet(self, title):
        raise WorksheetNotFound(title)

    def add_worksheet(self, title, rows, cols):
        worksheet = FakeWorksheet()
        self.created[title] = worksheet
        return worksheet


def test_write_to_sheets_creates_tabs_missing_on_first_run(db):
    client = FakeSpreadsheetMissingTabs()
    export_data = {"New Tab": [["h1"], ["v1"]]}

    sheets_export.write_to_sheets(client, export_data)

    assert client.created["New Tab"].updated_rows == [["h1"], ["v1"]]
