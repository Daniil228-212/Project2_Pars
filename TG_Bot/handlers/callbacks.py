from aiogram import Router, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from TG_Bot.services.parser_service import BetBoomService
from TG_Bot.handlers.keyboards import get_main_kb, get_match_keyboard
router = Router()
service = BetBoomService()
class SearchStates(StatesGroup):
    waiting_for_team_name = State()
@router.message(F.text.in_(["Текущие матчи", "Current matches"]))
async def show_matches(message: types.Message):
    df = service.get_cached_matches()
    lang = service.language
    if df.empty:
        text = "Нет данных о матчах" if lang == "ru" else "No matches data"
        await message.answer(text)
        return
    for _, row in df.head(3).iterrows():
        await message.answer(
            f"{row['team1']} vs {row['team2']}\n"
            f"{'П1' if lang == 'ru' else '1'}: {row['coeff_win1']:.2f} | "
            f"X: {row['coeff_draw']:.2f} | "
            f"{'П2' if lang == 'ru' else '2'}: {row['coeff_win2']:.2f}",
            reply_markup=get_match_keyboard(row['betboom_url'], lang)
        )
@router.message(F.text.in_(["Рекомендации", "Recommendations"]))
async def show_recommendations(message: types.Message):
    df = service.get_recommendations()
    lang = service.language
    if df.empty:
        text = "Нет рекомендаций" if lang == "ru" else "No recommendations"
        await message.answer(text)
        return
    for _, row in df.iterrows():
        await message.answer(
            f"{row['team1']} ({'П1' if lang == 'ru' else '1'}: {row['coeff_win1']:.2f})",
            reply_markup=get_match_keyboard(row['betboom_url'], lang)
        )
@router.message(F.text.in_(["Поиск команды", "Search team"]))
async def start_search(message: types.Message, state: FSMContext):
    lang = service.language
    await message.answer(
        "Введите название команды:" if lang == "ru" else "Enter team name:",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(SearchStates.waiting_for_team_name)
@router.message(SearchStates.waiting_for_team_name)
async def process_search(message: types.Message, state: FSMContext):
    lang = service.language
    search_query = message.text.strip()
    if not search_query:
        text = "Пожалуйста, введите название команды:" if lang == "ru" else "Please enter team name:"
        await message.answer(text)
        return
    df = service.search_teams(search_query)
    if df.empty:
        text = f"Команда '{search_query}' не найдена" if lang == "ru" else f"Team '{search_query}' not found"
        await message.answer(text, reply_markup=get_main_kb())
    else:
        for _, row in df.iterrows():
            await message.answer(
                f"{row['team1']} vs {row['team2']}\n"
                f"{'П1' if lang == 'ru' else '1'}: {row['coeff_win1']:.2f} | "
                f"X: {row['coeff_draw']:.2f} | "
                f"{'П2' if lang == 'ru' else '2'}: {row['coeff_win2']:.2f}",
                reply_markup=get_match_keyboard(row['betboom_url'], lang)
            )
    await state.clear()
    text = "Главное меню:" if lang == "ru" else "Main menu:"
    await message.answer(text, reply_markup=get_main_kb())
@router.message(F.text.in_(["Перевод на English", "Switch to Russian"]))
async def switch_language(message: types.Message):
    service.switch_language()
    response = "Язык изменен на русский" if service.language == "ru" else "Language switched to English"
    await message.answer(response, reply_markup=get_main_kb())