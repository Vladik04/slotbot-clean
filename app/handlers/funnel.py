"""Обработчик команды /funnel."""

import logging
from aiogram import Router, types
from aiogram.filters import Command

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("funnel"))
async def funnel_command(message: types.Message) -> None:
    """Обработчик команды /funnel."""
    try:
        db = message.bot.get("db")
        if not db:
            await message.answer("❌ Ошибка: БД не инициализирована")
            return
        
        user_id = message.from_user.id
        
        # Логировать событие
        db.log_event(user_id, "funnel_command")
        
        funnel_text = (
            "🎯 *Специальное предложение:*\n\n"
            "Получите доступ к премиум сигналам!\n\n"
            "✨ Премиум функции:\n"
            "• Сигналы за 30 минут до события\n"
            "• Точность 85%+\n"
            "• Поддержка 24/7\n\n"
            "Стоимость: 1 TON/месяц\n\n"
            "Нажмите /vip для оплаты\n"
        )
        
        await message.answer(funnel_text)
        logger.info(f"✅ /funnel от пользователя {user_id}")
    except Exception as e:
        logger.error(f"❌ Ошибка /funnel: {e}", exc_info=True)
        await message.answer(f"❌ Ошибка: {str(e)}")
