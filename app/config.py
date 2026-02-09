"""Конфигурация приложения."""

import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не установлен!")

TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Database
DATABASE_PATH = "app/data/bot.db"

# Реферальная ссылка (заполнить вашей ссылкой)
REFERRAL_LINK = os.getenv("REFERRAL_LINK", "https://1win.uz/ref123")

# CryptoBot
CRYPTOBOT_TOKEN = os.getenv("CRYPTOBOT_TOKEN", "")
CRYPTOBOT_API_URL = "https://pay.crypt.bot/api"

# VIP цена (в TON)
VIP_PRICE_TON = 1.0

# Логирование
LOG_FILE = "app/data/bot.log"
