# Аналитика → Google Sheets → Looker Studio

Как устроен экспорт аналитики бота на дашборд, и что нужно сделать
один раз через Google-аккаунт, чтобы он заработал (это не может
сделать Клод — только вы, через веб-интерфейс Google).

## Как это работает

```
data/bot.db (sqlite, на сервере)
        │
        │  bot_services/analytics/funnel.py — агрегация:
        │  воронка Cinemalogy, регистрации по source,
        │  продажи по тарифам, активность по дням
        ▼
bot_services/analytics/sheets_export.py — собирает 4 таблицы
        │
        │  scripts/export_analytics.py — точка входа, запускается по cron
        ▼
Google Sheet (4 вкладки, перезаписываются целиком при каждом запуске)
        │
        ▼
Looker Studio — дашборд, подключённый к этому Sheet как источнику
```

Вкладки в таблице после первого запуска (создаются автоматически,
если их ещё нет):

- **Воронка** — уникальных пользователей на каждом шаге Cinemalogy +
  % конверсии от предыдущего шага;
- **Источники** — регистраций по `source` (deep-link из `/start`);
- **Продажи** — оплаченных билетов (`cinemalogy_payment_done`) по
  тарифам;
- **Активность по дням** — уникальных активных пользователей в день.

Каждый запуск **полностью перезаписывает** данные во всех вкладках —
это витрина текущего состояния, не архив истории по дням (кроме
вкладки «Активность по дням», которая сама по себе уже разбивка по
дням).

## Настройка (разово, через ваш Google-аккаунт)

Код уже готов и умеет писать в таблицу — не хватает только доступа.
Шаги:

1. **Создать проект** в [Google Cloud Console](https://console.cloud.google.com/)
   (или использовать существующий).
2. **Включить Google Sheets API** для этого проекта: в консоли —
   «APIs & Services» → «Library» → найти «Google Sheets API» →
   Enable.
3. **Создать Service Account**: «APIs & Services» → «Credentials» →
   «Create Credentials» → «Service Account». Имя — любое, например
   `bot-analytics-export`.
4. **Скачать JSON-ключ** для этого service account: на странице
   service account → «Keys» → «Add Key» → «Create new key» → JSON.
   Скачается файл вида `project-name-xxxxx.json`.
5. **Загрузить этот файл на сервер** (например,
   `/home/botuser/telegram-bot/google_sheets_credentials.json` — файл
   не должен попасть в git, добавить в `.gitignore`, если ещё не там).
6. **Создать Google-таблицу** (пустую, обычная Google Sheet) — это и
   будет источник для Looker Studio.
7. **Расшарить таблицу на service account**: открыть JSON-ключ,
   найти поле `client_email` (что-то вроде
   `bot-analytics-export@project-name.iam.gserviceaccount.com`) —
   расшарить Google-таблицу на этот email с правами **Редактор**
   (без этого шага экспорт будет падать с ошибкой доступа).
8. **Взять ID таблицы** — это часть её URL:
   `https://docs.google.com/spreadsheets/d/`**`ЭТА_ЧАСТЬ`**`/edit`.
9. **Прописать в `.env` на сервере**:
   ```
   ANALYTICS_SPREADSHEET_ID=<ID таблицы из шага 8>
   GOOGLE_SHEETS_CREDENTIALS_PATH=/home/botuser/telegram-bot/google_sheets_credentials.json
   ```
10. **Проверить руками**:
    ```
    cd /home/botuser/telegram-bot
    ./venv/bin/python scripts/export_analytics.py
    ```
    Должно вывести `Аналитика выгружена в Google Sheets` и появиться
    4 вкладки в таблице.
11. **Добавить в cron** (`crontab -e` под `botuser`), например раз в
    сутки в 3 ночи:
    ```
    0 3 * * * /home/botuser/telegram-bot/venv/bin/python /home/botuser/telegram-bot/scripts/export_analytics.py >> /home/botuser/telegram-bot/logs/analytics_export.log 2>&1
    ```

## Дашборд в Looker Studio

1. [Looker Studio](https://lookerstudio.google.com/) → «Create» →
   «Report».
2. Источник данных — «Google Sheets», выбрать таблицу из шага 6.
3. По одному графику на вкладку:
   - **Воронка** — bar chart (шаг × уникальных пользователей),
     подписи — % конверсии из третьей колонки;
   - **Источники** — pie chart или bar chart;
   - **Продажи** — bar chart по тарифам;
   - **Активность по дням** — line chart (тренд).

## Если что-то не так

- **`ANALYTICS_SPREADSHEET_ID и/или GOOGLE_SHEETS_CREDENTIALS_PATH не
  заданы`** — не выполнены шаги 9 выше, проверить `.env`.
- **Ошибка доступа / `PERMISSION_DENIED`** — не выполнен шаг 7
  (таблица не расшарена на `client_email` из JSON-ключа).
- **Цифры выглядят подозрительно** (например, воронка резко
  обрывается на каком-то шаге) — сверить с `docs/NEW_PROCESS_CHECKLIST.md`,
  возможно, у одного из шагов отвалилась аналитика (как было с
  `payment_done` — см. историю коммитов).
