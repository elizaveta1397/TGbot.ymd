"""
Публикует/обновляет docs/PRIVACY_POLICY.md как страницу на telegra.ph —
чтобы политика открывалась пользователю как веб-страница по ссылке
(/policy, кнопка «Читать политику»), а не приходила файлом в чат.
См. docs/IDEAS.md, п.10 и п.12.

Использование:
    ./venv/bin/python scripts/publish_privacy_policy.py

Первый запуск создаёт страницу и печатает TELEGRAPH_ACCESS_TOKEN и
TELEGRAPH_PAGE_PATH — их нужно один раз положить в .env (не в git,
см. .gitignore), чтобы повторные запуски редактировали ТУ ЖЕ страницу,
а не плодили новые. Дальше при каждом изменении PRIVACY_POLICY.md
достаточно просто перезапустить скрипт — ссылка не меняется.
"""

import json
import os
import re
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

POLICY_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "docs",
    "PRIVACY_POLICY.md"
)

TELEGRAPH_ACCESS_TOKEN = os.getenv("TELEGRAPH_ACCESS_TOKEN")
TELEGRAPH_PAGE_PATH = os.getenv("TELEGRAPH_PAGE_PATH")

API = "https://api.telegra.ph"


def inline_nodes(text):
    """'**жирный** и `код`' -> ['и обычный ', {tag:'b', ...}, ...]"""

    parts = re.split(r"(\*\*.+?\*\*|`.+?`)", text)
    nodes = []

    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            nodes.append({"tag": "b", "children": [part[2:-2]]})
        elif part.startswith("`") and part.endswith("`"):
            nodes.append({"tag": "code", "children": [part[1:-1]]})
        else:
            nodes.append(part)

    return nodes or [""]


def parse_table(rows):
    """Markdown-таблица -> ul (Telegraph не поддерживает тег table)."""

    cells = [[c.strip() for c in row.strip("|").split("|")] for row in rows]
    header, _, *data = cells

    items = []
    for row in data:
        pairs = [f"{h}: {v}" for h, v in zip(header, row) if v]
        items.append({"tag": "li", "children": [" — ".join(pairs)]})

    return {"tag": "ul", "children": items}


def markdown_to_nodes(text):
    lines = text.splitlines()
    title = lines[0].lstrip("#").strip()

    nodes = []
    buf = []
    list_buf = []
    table_buf = []

    def flush_paragraph():
        if buf:
            joined = " ".join(line.strip() for line in buf)
            nodes.append({"tag": "p", "children": inline_nodes(joined)})
            buf.clear()

    def flush_list():
        if list_buf:
            items = []
            for parts in list_buf:
                joined = " ".join(p.strip() for p in parts)
                items.append({"tag": "li", "children": inline_nodes(joined)})
            nodes.append({"tag": "ul", "children": items})
            list_buf.clear()

    def flush_table():
        if table_buf:
            nodes.append(parse_table(table_buf))
            table_buf.clear()

    for raw_line in lines[1:]:
        line = raw_line.rstrip()

        if not line.strip():
            flush_paragraph()
            flush_list()
            flush_table()
            continue

        if line.startswith("## "):
            flush_paragraph()
            flush_list()
            flush_table()
            nodes.append({"tag": "h3", "children": [line[3:].strip()]})
            continue

        if line.startswith("|"):
            flush_paragraph()
            flush_list()
            table_buf.append(line)
            continue

        if line.startswith("- "):
            flush_paragraph()
            flush_table()
            list_buf.append([line[2:]])
            continue

        if line.startswith("  ") and list_buf:
            list_buf[-1].append(line.strip())
            continue

        flush_list()
        flush_table()
        buf.append(line)

    flush_paragraph()
    flush_list()
    flush_table()

    return title, nodes


def main():
    with open(POLICY_PATH, encoding="utf-8") as f:
        text = f.read()

    title, nodes = markdown_to_nodes(text)

    token = TELEGRAPH_ACCESS_TOKEN
    if not token:
        resp = requests.post(
            f"{API}/createAccount",
            data={
                "short_name": "ГончароваБот",
                "author_name": "Елизавета Гончарова"
            },
            timeout=15
        ).json()
        if not resp.get("ok"):
            sys.exit(f"createAccount failed: {resp}")
        token = resp["result"]["access_token"]
        print(f"Новый TELEGRAPH_ACCESS_TOKEN (добавить в .env): {token}")

    payload = {
        "access_token": token,
        "title": title,
        "author_name": "Елизавета Гончарова",
        "content": json.dumps(nodes, ensure_ascii=False),
        "return_content": "false"
    }

    if TELEGRAPH_PAGE_PATH:
        url_path = f"{API}/editPage/{TELEGRAPH_PAGE_PATH}"
    else:
        url_path = f"{API}/createPage"

    resp = requests.post(url_path, data=payload, timeout=15).json()

    if not resp.get("ok"):
        sys.exit(f"telegra.ph API error: {resp}")

    print(f"Опубликовано: {resp['result']['url']}")
    if not TELEGRAPH_PAGE_PATH:
        print(f"Добавить в .env: TELEGRAPH_PAGE_PATH={resp['result']['path']}")


if __name__ == "__main__":
    main()
