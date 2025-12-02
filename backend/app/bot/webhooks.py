"""
Webhook для приёма обновлений от Telegram
"""
from fastapi import Request
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram.fsm.storage.memory import MemoryStorage
import logging

from backend.app.config import settings
from backend.app.bot.router import get_bot_router

logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Подключаем router'ы
main_router = get_bot_router()
dp.include_router(main_router)


async def handle_telegram_update(request: Request):
    """Обработка вебхука от Telegram"""
    try:
        update_data = await request.json()
        update = Update(**update_data)
        
        logger.info(f"📨 Update получен: {update.update_id}")
        
        # Отправляем update в диспетчер
        await dp.feed_update(bot, update)
        
        return {"ok": True}
    except Exception as e:
        logger.error(f"❌ Ошибка обработки webhook: {str(e)}", exc_info=True)
        return {"ok": False, "error": str(e)}
