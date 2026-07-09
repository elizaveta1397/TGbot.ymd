#!/bin/bash

BACKUP_DIR="/home/botuser/telegram-bot/backups"
DB_FILE="/home/botuser/telegram-bot/data/bot.db"
LOG_FILE="/home/botuser/telegram-bot/logs/backup.log"

mkdir -p "$BACKUP_DIR"
mkdir -p "/home/botuser/telegram-bot/logs"

DATE=$(date +"%Y-%m-%d_%H-%M-%S")

if [ ! -f "$DB_FILE" ]; then
    echo "[$DATE] ERROR: bot.db not found" >> "$LOG_FILE"
    exit 1
fi

cp "$DB_FILE" "$BACKUP_DIR/bot_$DATE.db"

gzip -f "$BACKUP_DIR/bot_$DATE.db"

find "$BACKUP_DIR" -name "*.gz" -mtime +30 -delete

cd "$BACKUP_DIR" || exit 1

git add .

git commit -m "Backup $DATE" >/dev/null 2>&1 || true

git push origin main >> "$LOG_FILE" 2>&1

echo "[$DATE] Backup completed" >> "$LOG_FILE"
