import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from handlers import menu, user_input, check_balance # твои хэндлеры

from dotenv import load_dotenv
import os

load_dotenv("data.env")
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")

async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрация хэндлеров
    menu.register_handlers(dp)
    user_input.register_handlers(dp)
    check_balance.register_handlers(dp)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())