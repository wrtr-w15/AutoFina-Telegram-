from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import yaml
import os

router = Router()

def load_response_config(filename: str):
    path = os.path.join("config", filename)
    if not os.path.exists(path):
        return {
            "title": "❌ Ошибка",
            "subtitle": f"Файл {filename} не найден",
            "buttons": []
        }
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

@router.callback_query(lambda c: c.data.startswith("open_network_menu:"))
async def handle_open_network_menu(callback: types.CallbackQuery):
    mode = callback.data.split(":")[1]  # mainnet или testnet

    # Сохраняем выбранный режим в message.chat.id → просто печатаем в ответ (можно FSM)
    filename = f"{mode}_networks.yaml"
    config = load_response_config(filename)

    title = config.get("title", "⚠️ Нет заголовка")
    subtitle = f"{config.get('subtitle', '')} ({mode})"
    buttons = config.get("buttons", [])

    full_text = f"{title}\n{subtitle}"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=btn["text"],
                callback_data=btn["callback"] if btn["callback"] == "go_back" else f"select_net:{btn['callback']}:{mode}"
            )]
            for btn in buttons
        ]
    ) if buttons else None

    try:
        await callback.message.delete()
    except Exception as e:
        await callback.message.answer("⚠️ Не удалось удалить старое меню.")

    await callback.message.answer(full_text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith("select_net:"))
async def handle_selected_network(callback: types.CallbackQuery):
    parts = callback.data.split(":")
    network = parts[1] if len(parts) > 1 else "unknown"
    mode = parts[2] if len(parts) > 2 else "unknown"

    await callback.message.answer(f"✅ Вы выбрали сеть: {network} в режиме: {mode}")
    await callback.answer()

@router.callback_query(lambda c: c.data == "go_back")
async def handle_go_back(callback: types.CallbackQuery):
    try:
        # Удаляем текущее сообщение
        await callback.message.delete()
    except Exception as e:
        # В случае, если сообщение нельзя удалить (например, недостаточно прав)
        await callback.message.answer("⚠️ Не удалось удалить сообщение.")

    await callback.answer()

@router.callback_query()
async def handle_dynamic_menu(callback: types.CallbackQuery):
    callback_id = callback.data

    if callback_id == "go_back":
        return
    
    filename = f"{callback_id}.yaml"

    config = load_response_config(filename)

    title = config.get("title", "⚠️ Нет заголовка")
    subtitle = config.get("subtitle", "")
    buttons = config.get("buttons", [])

    full_text = f"{title}\n{subtitle}"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=btn["text"], callback_data=btn["callback"])]
            for btn in buttons
        ]
    ) if buttons else None

    await callback.message.answer(full_text, reply_markup=keyboard)
    await callback.answer()

def register_handlers(dp):
    dp.include_router(router)