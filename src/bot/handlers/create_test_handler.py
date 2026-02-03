import uuid
import logging
import time

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, InputMediaPhoto

from src.services.ai_service import AiService
from src.services.test_service import TestService
from src.services.qr_service import QrService
from src.bot.states import CreateTestFSM
from src.bot.keyboards import preview_kb, cancel_kb, start_kb
from src.bot.texts import BotTexts
from src.db.database import SessionLocal

from config import Config_obj

router = Router()


@router.callback_query(F.data == "create_test")
async def create_test(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
        
    await cb.message.delete()
    
    await cb.message.answer(
        BotTexts.CREATE_TEST_PROMPT,
        parse_mode="HTML",
        reply_markup=cancel_kb("create_test")
    )
    
    await state.set_state(CreateTestFSM.topic)


@router.message(CreateTestFSM.topic)
async def set_topic(message: Message, state: FSMContext):
    await state.update_data(topic=message.text)
    
    await message.answer(
        BotTexts.ENTER_QUESTION_COUNT,
        reply_markup=cancel_kb("test")
    )
    
    await state.set_state(CreateTestFSM.count)


@router.message(CreateTestFSM.count)
async def set_count(message: Message, state: FSMContext):
    data = await state.get_data()
    topic = data["topic"]

    try:
        count = int(message.text)
        
    except ValueError:
        await message.answer(BotTexts.INVALID_NUMBER_INPUT)
        return

    prompt = f"Создай тест по теме: {topic}. {count} вопросов."
    wait = await message.answer("⌛")

    questions = await AiService.get_answer(Config_obj.groq_api_key, prompt)

    if not questions:
        await state.clear()
        await wait.edit_text(BotTexts.GENERATION_ERROR)
        return

    await state.update_data(questions=questions)

    preview = BotTexts.TEST_PREVIEW_TEMPLATE.format(topic=topic)
    
    for i, q in enumerate(questions, 1):
        preview += f"{i}. {q['question']}\n"
        
    preview += "\nПродолжить?"

    await wait.edit_text(
        preview,
        parse_mode="HTML",
        reply_markup=preview_kb()
    )

    await state.set_state(CreateTestFSM.preview)


@router.callback_query(F.data == "confirm_test", CreateTestFSM.preview)
async def confirm_test(cb: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    slug = uuid.uuid4().hex[:8]

    try:
        with SessionLocal() as db:
            TestService.create_test(
                db,
                slug,
                cb.from_user.id,
                data["topic"],
                data["questions"]
            )

        test_link = f"https://t.me/{(await bot.me()).username}?start={slug}"

        qr_bytes = QrService.generate_qr_bytes(test_link)
        qr_file = BufferedInputFile(qr_bytes, filename="test_qr.png")

        media = InputMediaPhoto(
            media=qr_file,
            caption=BotTexts.TEST_CREATED_TEMPLATE.format(test_link=test_link),
            parse_mode="HTML"
        )

        await cb.message.edit_media(media)

    except Exception as e:
        logging.error(e, exc_info=True)
        
        await cb.message.edit_text(TEST_SAVE_ERROR)

    await state.clear()
    await cb.answer()