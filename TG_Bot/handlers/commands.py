from aiogram import Router, types
from aiogram.filters import Command
from TG_Bot.handlers.keyboards import get_main_kb
router = Router()
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🏟️ <b>BetBoom Analyzer</b>\n\n"
        "Выберите действие:",
        reply_markup=get_main_kb()
    )
@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "ℹ️ <b>Помощь по боту</b>\n\n"
        "Используйте кнопки меню для навигации"
    )