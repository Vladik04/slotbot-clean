"""
SlotSignalsBot - Telegram бот для сигналов слотов.
Чистая архитектура: только polling, без webhook.
"""

import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode

from app.config import BOT_TOKEN, LOG_FILE
from app.database import Database
from app.handlers import start, signals, funnel, vip

# Загрузить переменные окружения
load_dotenv()

# Логирование в файл и консоль
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


async def main() -> None:
    """Главная функция бота."""
    try:
        logger.info("=" * 60)
        logger.info("🚀 Запуск SlotSignalsBot")
        logger.info("=" * 60)
        
        # Инициализировать БД
        db = Database()
        logger.info("✅ База данных инициализирована")
        
        # Инициализировать бота
        bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.MARKDOWN)
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)
        
        # Сохранить БД в контекст бота
        bot["db"] = db
        
        logger.info("✅ Бот инициализирован")
        
        # Регистрировать роутеры
        dp.include_router(start.router)
        dp.include_router(signals.router)
        dp.include_router(funnel.router)
        dp.include_router(vip.router)
        
        logger.info("✅ Роутеры зарегистрированы")
        
        # Удалить webhook и очистить очередь
        logger.info("🧹 Удаление webhook и очистка очереди...")
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("✅ Webhook удален, очередь очищена")
        
        # Запустить polling
        logger.info("📡 Запуск polling...")
        logger.info("✅ БОТ ГОТОВ К РАБОТЕ!")
        logger.info("=" * 60)
        
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
            skip_updates=False
        )
    
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}", exc_info=True)
        raise
    
    finally:
        logger.info("🛑 Бот завершил работу")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⏹️ Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"❌ Неожиданная ошибка: {e}", exc_info=True)
