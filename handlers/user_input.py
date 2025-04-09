from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("wallet"))
async def ask_for_wallet(message: types.Message):
    await message.answer("Пожалуйста, отправь адрес своего кошелька.")

# Здесь ты можешь добавлять больше хэндлеров под другие команды или кнопки

def register_handlers(dp):
    dp.include_router(router)