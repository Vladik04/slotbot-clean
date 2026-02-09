"""Обработчик команды /vip."""

import logging
from aiogram import Router, types
from aiogram.filters import Command

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("vip"))
async def vip_command(message: types.Message) -> None:
    """Обработчик команды /vip."""
    try:
        db = message.bot.get("db")
        if not db:
            await message.answer("❌ Ошибка: БД не инициализирована")
            return
        
        user_id = message.from_user.id
        
        # Логировать событие
        db.log_event(user_id, "vip_command")
        
        # Проверить VIP статус
        is_vip = db.is_vip(user_id)
        
        if is_vip:
            vip_text = (
                "⭐ *Вы VIP пользователь!* ⭐\n\n"
                "✅ Преимущества VIP:\n"
                "• Эксклюзивные сигналы\n"
                "• Приоритетная поддержка\n"
                "• Расширенная аналитика\n"
                "• Ранний доступ к новым функциям\n"
            )
        else:
            vip_text = (
                "⭐ *VIP Подписка* ⭐\n\n"
                "Стоимость: 1 TON в месяц\n\n"
                "✨ Преимущества VIP:\n"
                "• Эксклюзивные сигналы\n"
                "• Приоритетная поддержка\n"
                "• Расширенная аналитика\n"
                "• Ранний доступ к новым функциям\n\n"
                "Для активации VIP - используйте /vip_pay\n"
            )
        
        await message.answer(vip_text)
        logger.info(f"✅ /vip от пользователя {user_id} (VIP: {is_vip})")
    except Exception as e:
        logger.error(f"❌ Ошибка /vip: {e}", exc_info=True)
        await message.answer(f"❌ Ошибка: {str(e)}")
