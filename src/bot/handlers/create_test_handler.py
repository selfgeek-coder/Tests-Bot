import uuid
import logging
import asyncio
import json

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, BufferedInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from src.services.ai_service import AiService
from src.services.test_service import TestService
from src.services.qr_service import QrService
from src.bot.states import CreateTestFSM
from src.bot.keyboards import preview_kb, cancel_kb, revision_kb
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

    await state.update_data(original_prompt=user_prompt)
    
    data_from_ai = await AiService.get_answer(Config_obj.groq_api_key, user_prompt)

    if not data_from_ai or "questions" not in data_from_ai:
        await state.clear()
        await wait.edit_text(BotTexts.GENERATION_ERROR)
        return

    questions = data_from_ai["questions"]
    topic = data_from_ai.get("topic", "Тест")

    await state.update_data(topic=topic, questions=questions)

    await show_preview(wait, topic, questions)
    await state.set_state(CreateTestFSM.preview)


async def show_preview(message: Message, topic: str, questions: list):
    """Показывает предпросмотр теста"""
    preview = BotTexts.TEST_PREVIEW_TEMPLATE.format(topic=topic)
    for i, q in enumerate(questions, 1):
        preview += f"{i}. {q['question']}\n"
        if "options" in q:
            for opt, text in q["options"].items():
                preview += f"   {opt}) {text}\n"
        preview += f"   Правильный ответ: {q['correct']}\n\n"
        
    preview += "\nПродолжить?"

    await message.edit_text(preview, reply_markup=preview_kb())


@router.callback_query(F.data == "revise_test", CreateTestFSM.preview)
async def revise_test(cb: CallbackQuery, state: FSMContext):
    """Переход в режим правок"""
    await cb.answer()
    await cb.message.edit_text(
        BotTexts.REVISION_PROMPT,
        reply_markup=revision_kb()
    )
    await state.set_state(CreateTestFSM.revision)


@router.message(CreateTestFSM.revision)
async def process_revision(message: Message, state: FSMContext, bot: Bot):
    """Обработка правок пользователя"""
    revision_text = message.text.strip()
    if not revision_text:
        await message.answer(BotTexts.INVALID_NUMBER_INPUT)
        return

    wait = await message.answer(BotTexts.REVISION_PROCESSING)

    data = await state.get_data()
    original_prompt = data.get("original_prompt", "")
    current_topic = data.get("topic", "Тест")
    current_questions = data.get("questions", [])

    revision_prompt = (
        f"Исходный запрос: {original_prompt}\n\n"
        f"Текущая тема: {current_topic}\n"
        f"Текущие вопросы: {json.dumps(current_questions, ensure_ascii=False, indent=2)}\n\n"
        f"Правки пользователя: {revision_text}\n\n"
        "Внеси правки в тест в соответствии с запросом пользователя. "
        "Верни ТОЛЬКО JSON с обновленным тестом в том же формате."
    )

    data_from_ai = await AiService.get_answer(Config_obj.groq_api_key, revision_prompt)

    if not data_from_ai or "questions" not in data_from_ai:
        await wait.edit_text(
            BotTexts.REVISION_ERROR,
            reply_markup=revision_kb()
        )
        return

    new_questions = data_from_ai["questions"]
    new_topic = data_from_ai.get("topic", current_topic)

    await state.update_data(topic=new_topic, questions=new_questions)

    await show_preview(wait, new_topic, new_questions)
    await state.set_state(CreateTestFSM.preview)


@router.callback_query(F.data == "back_to_preview", CreateTestFSM.revision)
async def back_to_preview(cb: CallbackQuery, state: FSMContext):
    """Возврат к предпросмотру без изменений"""

    await cb.answer()
    data = await state.get_data()
    
    await show_preview(
        cb.message,
        data.get("topic", "Тест"),
        data.get("questions", [])
    )
    await state.set_state(CreateTestFSM.preview)


@router.callback_query(F.data == "confirm_test", CreateTestFSM.preview)
async def confirm_test(cb: CallbackQuery, state: FSMContext, bot: Bot):
    """Подтверждение и сохранение теста"""

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


@router.callback_query(F.data == "cancel_test")
async def cancel_creation(cb: CallbackQuery, state: FSMContext):
    """Отмена создания теста"""
    await cb.answer()
    await state.clear()
    await cb.message.edit_text("Создание теста отменено")