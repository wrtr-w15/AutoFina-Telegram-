from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.enums import ParseMode
import os
import yaml

router = Router()

REQUIRED_CHANNEL = "@autofina"

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

@router.message(F.text == "/start")
async def send_welcome(message: types.Message):
    user_id = message.from_user.id

    try:
        member = await message.bot.get_chat_member(REQUIRED_CHANNEL, user_id)
        if member.status not in ["member", "administrator", "creator"]:
            raise Exception()
    except:
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 Подписаться", url=f"https://t.me/{REQUIRED_CHANNEL[1:]}")],
            [InlineKeyboardButton(text="🔄 Проверить подписку", callback_data="check_subscription")]
        ])
        await message.answer("❗️Для использования бота подпишитесь на канал:", reply_markup=markup)
        return

    title, subtitle, photo_path, keyboard = build_menu()
    text = f"{title}\n{subtitle}"

    if photo_path and os.path.exists(photo_path):
        photo = FSInputFile(photo_path)
        await message.answer_photo(photo=photo, caption=text, reply_markup=keyboard)
    else:
        await message.answer(text, reply_markup=keyboard)

@router.callback_query(F.data == "check_subscription")
async def check_subscription(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    try:
        member = await callback.bot.get_chat_member(REQUIRED_CHANNEL, user_id)
        if member.status in ["member", "administrator", "creator"]:
            await callback.message.delete()
            await send_welcome(callback.message)
        else:
            raise Exception()
    except:
        await callback.answer("❌ Вы не подписаны на канал", show_alert=True)