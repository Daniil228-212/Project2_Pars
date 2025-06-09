from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from TG_Bot.services.parser_service import BetBoomService
service = BetBoomService()
def get_main_kb():
    builder = ReplyKeyboardBuilder()
    if service.language == "ru":
        builder.button(text="Текущие матчи")
        builder.button(text="Рекомендации")
        builder.button(text="Поиск команды")
        builder.button(text="Перевод на English")
    else:
        builder.button(text="Current matches")
        builder.button(text="Recommendations")
        builder.button(text="Search team")
        builder.button(text="Switch to Russian")
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
def get_match_keyboard(url: str, lang: str):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Сделать ставку" if lang == "ru" else "Place bet",
        url=url
    )
    return builder.as_markup()
