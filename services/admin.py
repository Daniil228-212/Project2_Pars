from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.enums import ParseMode
from typing import List, Union
import logging
import time

from config.settings import ADMIN_IDS, DEBUG_MODE

router = Router()


def is_admin(user_id: int) -> bool:
    """Проверка, является ли пользователь администратором"""
    try:
        return user_id in ADMIN_IDS
    except Exception as e:
        logging.error(f"Admin check error: {e}")
        return False


@router.message(Command("admin"))
async def admin_panel(message: Message):
    """Панель администратора"""
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Доступ запрещён")
        return

    admin_commands = [
        "<b>Админ-команды:</b>",
        "/stats - Статистика бота",
        "/users - Список пользователей",
        "/broadcast [текст] - Рассылка",
        "/ban [id] - Блокировка",
        "/log - Получить лог файл",
        "/debug - Режим отладки" + (" (активен)" if DEBUG_MODE else "")
    ]

    await message.answer("\n".join(admin_commands), parse_mode=ParseMode.HTML)


@router.message(Command("stats"))
async def bot_stats(message: Message):
    """Статистика бота"""
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Доступ запрещён")
        return

    stats = [
        "📊 <b>Статистика бота</b>",
        f"🆔 Ваш ID: {message.from_user.id}",
        f"👥 Админов: {len(ADMIN_IDS)}",
        f"🔄 Режим отладки: {'ВКЛ' if DEBUG_MODE else 'ВЫКЛ'}",
        f"🕒 Время работы: {time.strftime('%H:%M:%S')}"
    ]

    await message.answer("\n".join(stats), parse_mode=ParseMode.HTML)


@router.message(Command("broadcast"))
async def broadcast_message(message: Message):
    """Рассылка сообщения всем пользователям"""
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Доступ запрещён")
        return

    text = message.text.replace("/broadcast", "").strip()
    if not text:
        await message.answer("ℹ️ Пример: /broadcast Привет всем!")
        return

    # В реальной реализации здесь должна быть отправка всем пользователям из БД
    await message.answer(f"📢 Рассылка начата:\n\n{text}")


@router.message(Command("log"))
async def send_logs(message: Message):
    """Отправка лог-файла"""
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Доступ запрещён")
        return

    try:
        with open("bot.log", "rb") as log_file:
            await message.answer_document(log_file, caption="📄 Лог файл бота")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}")


@router.message(Command("debug"))
async def toggle_debug(message: Message):
    """Переключение режима отладки"""
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Доступ запрещён")
        return

    global DEBUG_MODE
    DEBUG_MODE = not DEBUG_MODE
    await message.answer(f"🔧 Режим отладки: {'ВКЛЮЧЕН' if DEBUG_MODE else 'ВЫКЛЮЧЕН'}")


@router.message(Command("help"))
async def help_command(message: Message):
    """Обновлённая команда помощи"""
    help_text = [
        "ℹ️ <b>Доступные команды:</b>",
        "/start - Начало работы",
        "/matches - Текущие матчи",
        "/help - Справка по командам"
    ]

    if is_admin(message.from_user.id):
        help_text.append("\n👑 <b>Админ-команды:</b>")
        help_text.append("/admin - Панель управления")

    await message.answer("\n".join(help_text), parse_mode=ParseMode.HTML)
