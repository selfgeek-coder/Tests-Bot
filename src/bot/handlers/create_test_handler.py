import uuid
import logging
import time

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.services.ai_service import AiService
from src.services.test_service import TestService
from src.bot.states import CreateTestFSM
from src.bot.keyboards import preview_kb, cancel_kb, start_kb
from src.db.database import SessionLocal

from config import Config_obj

router = Router()


@router.callback_query(F.data == "create_test")
async def create_test(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
        
    await cb.message.delete()
    
    await cb.message.answer(
        "🖊 <i>Введите тему тестирования</i>\n\n"
        "Например:\n<code>Физика 8 класс, кипение воды</code>",
        parse_mode="HTML",
        reply_markup=cancel_kb("create_test")
    )
    
    await state.set_state(CreateTestFSM.topic)


@router.message(CreateTestFSM.topic)
async def set_topic(message: Message, state: FSMContext):
    await state.update_data(topic=message.text)
    await message.answer(
        "Сколько вопросов?",
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
        await message.answer("⚠ Введите число")
        return

    prompt = f"Создай тест по теме: {topic}. {count} вопросов."
    wait = await message.answer("⌛")

    questions = await AiService.get_answer(Config_obj.groq_api_key, prompt)

    if not questions:
        await state.clear()
        await wait.edit_text("Ошибка генерации")
        return

    await state.update_data(questions=questions)

    preview = (
        f"👁‍🗨 <b>Предпросмотр теста</b>\n\n"
        f"Тема: <i>{topic}</i>\n\n"
    )

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

    slug = uuid.uuid4().hex[:8] # генерация уникального id теста (SLUG)

    try:
        with SessionLocal() as db:
            TestService.create_test(
                db,
                slug,
                cb.from_user.id,
                data["topic"],
                data["questions"]
            )

        await cb.message.edit_text(
            "<b>Тестирование создано</b>\n\nСсылка для прохождения теста:\n"
            f"https://t.me/{(await bot.me()).username}?start={slug}",
            parse_mode="HTML"
        )

    except Exception as e:
        logging.error(e, exc_info=True)
        await cb.message.edit_text("Ошибка при сохранении теста")

    await state.clear()
    await cb.answer()


@router.callback_query(F.data == "cancel_create_test")
async def cancel_test(cb: CallbackQuery, state: FSMContext):
    await state.clear()

    await cb.message.edit_text(
        f"Привет {cb.from_user.first_name}!\n\nЯ - бот для образовательных тестирований.",
        reply_markup=start_kb()
    )

    await cb.answer("Создание теста отменено")