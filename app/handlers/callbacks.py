"""Обработчик callback кнопок."""

import logging
from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(lambda c: c.data.startswith("play_"))
async def play_button_callback(callback: types.CallbackQuery) -> None:
    """Обработчик кнопки 'Играть'."""
    try:
        db = callback.bot.get("db")
        if not db:
            await callback.answer("❌ Ошибка: БД не инициализирована")
            return
        
        user_id = callback.from_user.id
        
        # Логировать клик
        db.log_event(user_id, "play_button_click")
        
        # Получить реферальную ссылку из конфига
        from app.config import REFERRAL_LINK
        
        # Ответить на callback
        await callback.answer("✅ Переходим на казино...", show_alert=False)
        
        # Отправить сообщение с ссылкой
        message_text = (
            "🎰 *Переходите на казино!*\n\n"
            "Используйте нашу реферальную ссылку для бонусов:\n\n"
        )
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎰 Играть", url=REFERRAL_LINK)],
            [InlineKeyboardButton(text="← Назад", callback_data="back_to_signals")]
        ])
        
        await callback.message.answer(message_text, reply_markup=keyboard)
        
        logger.info(f"✅ Клик на кнопку 'Играть' от пользователя {user_id}")
    except Exception as e:
        logger.error(f"❌ Ошибка обработки play_button: {e}", exc_info=True)
        await callback.answer(f"❌ Ошибка: {str(e)}")


@router.callback_query(lambda c: c.data == "back_to_signals")
async def back_to_signals_callback(callback: types.CallbackQuery) -> None:
    """Вернуться к сигналам."""
    try:
        db = callback.bot.get("db")
        if not db:
            await callback.answer("❌ Ошибка: БД не инициализирована")
            return
        
        user_id = callback.from_user.id
        
        # Логировать событие
        db.log_event(user_id, "back_to_signals")
        
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
        
        # Создать кнопки
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎰 Играть", callback_data="play_signal")]
        ])
        
        await callback.message.edit_text(signals_text, reply_markup=keyboard)
        await callback.answer("✅ Вернулись к сигналам")
        
        logger.info(f"✅ Вернулись к сигналам для пользователя {user_id}")
    except Exception as e:
        logger.error(f"❌ Ошибка обработки back_to_signals: {e}", exc_info=True)
        await callback.answer(f"❌ Ошибка: {str(e)}")
