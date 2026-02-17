import uuid
import logging
import asyncio

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, BufferedInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from src.services.ai_service import AiService
from src.services.test_service import TestService
from src.services.qr_service import QrService
from src.bot.states import CreateTestFSM
from src.bot.keyboards import preview_kb, cancel_kb
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
        reply_markup=cancel_kb("test")
    )
    
    await state.set_state(CreateTestFSM.topic)


@router.message(CreateTestFSM.topic)
async def generate_test_from_prompt(message: Message, state: FSMContext):
    user_prompt = message.text.strip()
    if not user_prompt:
        await message.answer(BotTexts.INVALID_NUMBER_INPUT)
        return

    wait = await message.answer("⌛")

    data_from_ai = await AiService.get_answer(Config_obj.groq_api_key, user_prompt)

    if not data_from_ai or "questions" not in data_from_ai:
        await state.clear()
        await wait.edit_text(BotTexts.GENERATION_ERROR)
        return

    questions = data_from_ai["questions"]
    topic = data_from_ai.get("topic", "Тест")

    await state.update_data(topic=topic, questions=questions)

    preview = BotTexts.TEST_PREVIEW_TEMPLATE.format(topic=topic)
    for i, q in enumerate(questions, 1):
        preview += f"{i}. {q['question']}\n"
        
    preview += "\nПродолжить?"

    await wait.edit_text(preview, reply_markup=preview_kb())
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
            caption=BotTexts.TEST_CREATED_TEMPLATE.format(test_link=test_link)
        )

        await cb.message.edit_media(media)

    except Exception as e:
        logging.error(e, exc_info=True)
        await cb.message.edit_text(BotTexts.TEST_SAVE_ERROR)

    await state.clear()
    await cb.answer()