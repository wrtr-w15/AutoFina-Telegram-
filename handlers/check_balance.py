from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import yaml

router = Router()

def load_response_config(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

@router.callback_query(lambda c: c.data == "check_balance")
async def handle_balance(callback: types.CallbackQuery):
    config = load_response_config("config/balance_menu.yaml")
    text = config.get("title",[])
    buttons = config.get("buttons", [])

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=btn["text"], callback_data=btn["callback"])]
            for btn in buttons
        ]
    ) if buttons else None

    await callback.message.answer(text, reply_markup=keyboard)
    await callback.answer()

# 👇 Этого раньше не хватало!
def register_handlers(dp):
    dp.include_router(router)