"""Обработчик команды /start."""

import logging
from aiogram import Router, types
from aiogram.filters import Command

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("start"))
async def start_command(message: types.Message) -> None:
    """Обработчик команды /start."""
    try:
        # Получить БД из контекста
        db = message.bot.get("db")
        if not db:
            await message.answer("❌ Ошибка: БД не инициализирована")
            return
        
        user_id = message.from_user.id
        username = message.from_user.username
        
        # Добавить пользователя в БД
        db.add_user(user_id, username)
        
        # Логировать событие
        db.log_event(user_id, "start_command")
        
        # Проверить VIP статус
        is_vip = db.is_vip(user_id)
        vip_badge = "⭐ VIP" if is_vip else "👤 Обычный"
        
        welcome_text = (
            f"🎰 *Добро пожаловать в SlotSignalsBot!* {vip_badge}\n\n"
            "Я помогу вам получать сигналы для игры в слоты.\n\n"
            "*Команды:*\n"
            "/signals - Получить сигналы\n"
            "/vip - Информация о VIP подписке\n"
            "/help - Справка\n"
        )
        
        await message.answer(welcome_text)
        logger.info(f"✅ /start от пользователя {user_id} (@{username})")
    except Exception as e:
        logger.error(f"❌ Ошибка /start: {e}", exc_info=True)
        await message.answer(f"❌ Ошибка: {str(e)}")


@router.message(Command("help"))
async def help_command(message: types.Message) -> None:
    """Обработчик команды /help."""
    try:
        db = message.bot.get("db")
        if db:
            db.log_event(message.from_user.id, "help_command")
        
        help_text = (
            "📖 *Справка по командам:*\n\n"
            "/start - Главное меню\n"
            "/signals - Получить сигналы\n"
            "/vip - VIP подписка\n"
            "/help - Эта справка\n"
        )
        
        await message.answer(help_text)
        logger.info(f"✅ /help от пользователя {message.from_user.id}")
    except Exception as e:
        logger.error(f"❌ Ошибка /help: {e}", exc_info=True)
        await message.answer(f"❌ Ошибка: {str(e)}")
