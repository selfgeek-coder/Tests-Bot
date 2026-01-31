from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from src.bot.keyboards import start_kb, start_test_kb
from src.db.database import SessionLocal
from src.services.test_service import TestService

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    args = message.text.split(maxsplit=1)

    with SessionLocal() as db:
        # /start <slug>
        if len(args) == 2:
            slug = args[1]
            test = TestService.get_test(db, slug)

            if not test:
                await message.answer("Тест не найден!")
                return

            await message.answer(
                f"Тест <b>{test['topic']}</b>\n"
                f"Вопросов: {len(test['questions'])}",
                parse_mode="HTML",
                reply_markup=start_test_kb(slug)
            )
            return

        # обычный /start
        await message.answer(
            f"👋🏻 Привет {message.from_user.first_name}!\n\nЯ - бот для образовательных тестирований.",
            reply_markup=start_kb()
        )
        
        
@router.callback_query(F.data == "back_to_start")
async def back_to_start(cb: CallbackQuery):
    await cb.answer()
    await cb.message.edit_text(
        f"👋🏻 Привет {cb.from_user.first_name}!\n\nЯ - бот для образовательных тестирований.",
        reply_markup=start_kb()
    )