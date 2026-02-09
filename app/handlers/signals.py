"""Обработчик команды /signals."""

import logging
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("signals"))
async def signals_command(message: types.Message) -> None:
    """Обработчик команды /signals."""
    try:
        db = message.bot.get("db")
        if not db:
            await message.answer("❌ Ошибка: БД не инициализирована")
            return
        
        user_id = message.from_user.id
        
        # Логировать событие
        db.log_event(user_id, "signals_command")
        
        # Проверить VIP статус
        is_vip = db.is_vip(user_id)
        
        # Разные сигналы для VIP и обычных
        if is_vip:
            signals_text = (
                "⭐ *VIP СИГНАЛЫ* ⭐\n\n"
                "🎰 *Book of Ra Deluxe*\n"
                "Коэффициент: 1:5\n"
                "Время: 14:30 UTC\n\n"
                "🎰 *Sweet Bonanza*\n"
                "Коэффициент: 1:8\n"
                "Время: 15:00 UTC\n\n"
                "🎰 *Gates of Olympus*\n"
                "Коэффициент: 1:10\n"
                "Время: 16:00 UTC\n"
            )
        else:
            signals_text = (
                "📊 *ТЕКУЩИЕ СИГНАЛЫ*\n\n"
                "🎰 *Book of Ra Deluxe*\n"
                "Коэффициент: 1:3\n"
                "Время: 14:30 UTC\n\n"
                "Хотите больше сигналов? Подпишитесь на VIP! /vip"
            )
        
        # Создать inline кнопки
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎰 Играть", callback_data="play_signal")]
        ])
        
        await message.answer(signals_text, reply_markup=keyboard)
        logger.info(f"✅ /signals от пользователя {user_id} (VIP: {is_vip})")
    except Exception as e:
        logger.error(f"❌ Ошибка /signals: {e}", exc_info=True)
        await message.answer(f"❌ Ошибка: {str(e)}")
