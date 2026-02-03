from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.bot.keyboards import start_kb, start_test_kb
from src.db.database import SessionLocal
from src.services.test_service import TestService

router = Router()

START_MSG = "👋🏻 Привет {first_name}!\n\nЯ - бот для образовательных тестирований."
TEST_PREVIEW = "Тест <b>{topic}</b>\nВопросов: {questions_count}"

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
                TEST_PREVIEW_TEMPLATE.format(
                    topic=test['topic'],
                    questions_count=len(test['questions'])
                ),
                parse_mode="HTML",
                reply_markup=start_test_kb(slug)
            )
            return

        # обычный /start
        await message.answer(
            START_MSG.format(first_name=message.from_user.first_name),
            reply_markup=start_kb()
        )
        
        
@router.callback_query(F.data == "back_to_start")
async def back_to_start(cb: CallbackQuery):
    await cb.answer()
    
    await cb.message.edit_text(
        START_MSG.format(first_name=cb.from_user.first_name),
        reply_markup=start_kb()
    )


@router.callback_query(F.data == "cancel_create_test")
async def cancel_test(cb: CallbackQuery, state: FSMContext):
    await state.clear()

    await cb.message.edit_text(
        START_MSG.format(first_name=cb.from_user.first_name),
        reply_markup=start_kb()
    )

    await cb.answer("Создание теста отменено")