# Деплой бота на VPS через git

Первоначальная настройка и последующие обновления бота выполняются
через `git clone` / `git pull` на самом сервере — облачная сессия Claude
Code не имеет прямого SSH-доступа к серверу, поэтому команды выполняются
вручную в терминале VPS.

## Первоначальная настройка (один раз)

```bash
mkdir -p /home/botuser
useradd -m -d /home/botuser -s /bin/bash botuser 2>/dev/null || true
su - botuser
git clone https://github.com/elizaveta1397/tgbot.ymd.git /home/botuser/telegram-bot
cd /home/botuser/telegram-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Создать `.env` с секретами (не попадает в git, см. `.gitignore`):

```bash
cat > /home/botuser/telegram-bot/.env <<'EOF'
BOT_TOKEN=ваш_токен_бота
ADMIN_ID=ваш_telegram_id
EOF
```

Установить systemd-сервис (от пользователя с правами sudo, не от botuser):

```bash
sudo cp /home/botuser/telegram-bot/deploy/telegram-bot.service /etc/systemd/system/telegram-bot.service
sudo systemctl daemon-reload
sudo systemctl enable --now telegram-bot
sudo systemctl status telegram-bot
```

## Обновление бота (каждый раз при новом коде)

```bash
cd /home/botuser/telegram-bot
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart telegram-bot
sudo systemctl status telegram-bot
```

## Логи

```bash
sudo journalctl -u telegram-bot -f
```
