from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.services.test_service import TestService
from src.bot.keyboards import start_kb, start_test_kb
from src.bot.texts import BotTexts
from src.db.database import SessionLocal


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
                await message.answer(BotTexts.TEST_NOT_FOUND_ALERT)
                return

            await message.answer(
                BotTexts.TEST_PREVIEW.format(
                    topic=test['topic'],
                    questions_count=len(test['questions'])
                ),
                parse_mode="HTML",
                reply_markup=start_test_kb(slug)
            )
            return

        await message.answer("🤖")

        # обычный /start
        await message.answer(
            BotTexts.START_MSG.format(first_name=message.from_user.first_name),
            reply_markup=start_kb()
        )
        
        
@router.callback_query(F.data == "back_to_start")
async def back_to_start(cb: CallbackQuery):
    await cb.answer()
    
    await cb.message.edit_text(
        BotTexts.START_MSG.format(first_name=cb.from_user.first_name),
        reply_markup=start_kb()
    )


@router.callback_query(F.data == "cancel_create_test")
async def cancel_test(cb: CallbackQuery, state: FSMContext):
    await state.clear()

    await cb.message.edit_text(
        BotTexts.START_MSG.format(first_name=cb.from_user.first_name),
        reply_markup=start_kb()
    )

    await cb.answer("Создание теста отменено")
    
    
@router.callback_query(F.data == "close")
async def close(cb: CallbackQuery):
    await cb.answer()
    await cb.message.delete()