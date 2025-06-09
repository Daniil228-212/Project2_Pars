from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from TG_Bot.keyboards.inline import main_menu_keyboard

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Добро пожаловать в BetBoom Helper!\n\n"
        "Я помогу вам отслеживать актуальные матчи и коэффициенты.",
        reply_markup=main_menu_keyboard()
    )
