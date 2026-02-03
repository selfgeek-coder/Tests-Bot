from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from src.bot.keyboards import answers_kb, cancel_kb
from src.bot.states import PassTestFSM
from src.db.database import SessionLocal
from src.services.session_service import SessionService
from src.services.test_service import TestService
from src.bot.texts import BotTexts

router = Router()


@router.callback_query(F.data.startswith("start_test:"))
async def start_test(cb: CallbackQuery, state: FSMContext):
    slug = cb.data.split(":")[1]

    with SessionLocal() as db:
        test = TestService.get_test(db, slug)
        if not test:
            await cb.answer(
                BotTexts.TEST_NOT_FOUND_ALERT,
                show_alert=True
            )
            return

    await state.set_state(PassTestFSM.waiting_fullname)
    await state.update_data(slug=slug)

    await cb.message.edit_text(
        BotTexts.ENTER_FULLNAME_PROMPT,
        reply_markup=cancel_kb("answer_test"),
        parse_mode="HTML"
    )
    
    await cb.answer()


@router.message(PassTestFSM.waiting_fullname)
async def input_fullname(message: Message, state: FSMContext):
    fullname = message.text.strip()

    if len(fullname.split()) < 2:
        await message.answer(
            BotTexts.INVALID_FULLNAME_WARNING,
            parse_mode="HTML"
        )
        return

    data = await state.get_data()
    slug = data["slug"]

    with SessionLocal() as db:
        SessionService.start_session(
            db=db,
            user_id=message.from_user.id,
            slug=slug,
            fullname=fullname
        )

        test = TestService.get_test(db, slug)
        first_question = test["questions"][0]

    await state.clear()

    await message.answer(
        first_question["question"],
        reply_markup=answers_kb(slug, 0, first_question["options"])
    )


@router.callback_query(F.data.startswith("answer:"))
async def answer_test(cb: CallbackQuery, bot: Bot):
    _, slug, q_index, choice = cb.data.split(":")
    q_index = int(q_index)

    with SessionLocal() as db:
        session = SessionService.get_session(db, cb.from_user.id)
        if not session:
            await cb.answer(BotTexts.SESSION_EXPIRED_ALERT, show_alert=True)
            return

        test = TestService.get_test(db, slug)
        question = test["questions"][q_index]

        score = session["score"]
        if choice == question["correct"]:
            score += 1

        next_index = session["question_index"] + 1

        if next_index >= len(test["questions"]):
            total = len(test["questions"])
            percent = round(score / total * 100)

            if percent >= 90:
                grade = "5"
            elif percent >= 75:
                grade = "4"
            elif percent >= 50:
                grade = "3"
            elif percent >= 40:
                grade = "2"
            else:
                grade = "1"

            await cb.message.edit_text(
                BotTexts.TEST_COMPLETED_TEMPLATE.format(
                    score=score,
                    total=total,
                    percent=percent
                ),
                parse_mode="HTML"
            )

            await bot.send_message(
                test["owner_id"],
                BotTexts.RESULT_TO_OWNER_TEMPLATE.format(
                    topic=test['topic'],
                    fullname=session['fullname'],
                    telegram_name=cb.from_user.full_name,
                    username=cb.from_user.username or "",
                    score=score,
                    total=total,
                    percent=percent,
                    grade=grade
                ),
                parse_mode="HTML"
            )

            SessionService.finish_test(db, cb.from_user.id)

            await cb.answer()
            return

        SessionService.update_session(
            db=db,
            user_id=cb.from_user.id,
            question_index=next_index,
            score=score
        )

        next_question = test["questions"][next_index]

        await cb.message.edit_text(
            next_question["question"],
            reply_markup=answers_kb(
                slug,
                next_index,
                next_question["options"]
            )
        )

    await cb.answer()


@router.callback_query(F.data == "cancel_answer_test")
async def cancel_test(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    await cb.message.delete()
    await cb.answer(BotTexts.CANCEL_TEST_MSG)