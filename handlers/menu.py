from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import FSInputFile
import yaml
import os

router = Router()

def load_menu(path="config/main_menu.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def build_menu():
    config = load_menu()
    buttons = [
        [InlineKeyboardButton(text=btn["text"], callback_data=btn["callback"])]
        for btn in config["buttons"]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return config.get("title", ""), config.get("subtitle", ""), config.get("photo"), keyboard

@router.message(CommandStart())
async def start_handler(message: types.Message):
    title, subtitle, photo_path, keyboard = build_menu()
    text = f"{title}\n{subtitle}"

    if photo_path and os.path.exists(photo_path):
        photo = FSInputFile(photo_path)
        await message.answer_photo(photo=photo, caption=text, reply_markup=keyboard)
    else:
        await message.answer(text, reply_markup=keyboard)

def register_handlers(dp):
    dp.include_router(router)