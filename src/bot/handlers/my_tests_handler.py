from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.types import BufferedInputFile

from src.db.database import SessionLocal
from src.services.test_service import TestService
from src.services.qr_service import QrService
from src.services.export_service import ExportService
from src.bot.keyboards import my_tests_kb, test_manage_kb, start_kb, back_kb, delete_confirm_kb, close_kb
from src.bot.texts import BotTexts

router = Router()

@router.callback_query(F.data.in_(["my_tests", "back_to_my_tests"]))
async def my_tests(cb: CallbackQuery):
    await cb.answer()

    with SessionLocal() as db:
        tests = TestService.get_my_tests(db, cb.from_user.id)

    if not tests:
        await cb.answer(BotTexts.MY_TESTS_EMPTY_MSG)
        return

    await cb.message.edit_text(
        BotTexts.MY_TESTS_TITLE,
        reply_markup=my_tests_kb(tests, page=1)
    )
    
    
@router.callback_query(F.data.startswith("my_tests_page:"))
async def my_tests_page(cb: CallbackQuery):
    page = int(cb.data.split(":")[1])
    
    await cb.answer()

    with SessionLocal() as db:
        tests = TestService.get_my_tests(db, cb.from_user.id)

    await cb.message.edit_text(
        BotTexts.MY_TESTS_TITLE,
        reply_markup=my_tests_kb(tests, page)
    )


@router.callback_query(F.data.startswith("my_test:"))
async def my_test_detail(cb: CallbackQuery, bot: Bot):
    slug = cb.data.split(":", 1)[1]
    await cb.answer()

    with SessionLocal() as db:
        test = TestService.get_test(db, slug)

    if not test or test["owner_id"] != cb.from_user.id:
        await cb.message.edit_text(BotTexts.TEST_NOT_FOUND_MSG)
        return

    text = BotTexts.TEST_DETAILS_TEMPLATE.format(
        topic=test['topic'],
        questions_count=len(test['questions']),
        test_link=f"https://t.me/{(await bot.me()).username}?start={test['slug']}"
    )

    await cb.message.edit_text(
        text,
        reply_markup=test_manage_kb(slug)
    )


@router.callback_query(F.data.startswith("delete_test:"))
async def delete_test_ask(cb: CallbackQuery):
    slug = cb.data.split(":", 1)[1]
    await cb.answer()

    await cb.message.edit_text(
        BotTexts.DELETE_TEST_CONFIRM_MSG,
        reply_markup=delete_confirm_kb(slug)
    )
    
    
@router.callback_query(F.data.startswith("delete_test_confirm:"))
async def delete_test_confirm(cb: CallbackQuery):
    slug = cb.data.split(":", 1)[1]
    await cb.answer()

    with SessionLocal() as db:
        success = TestService.delete_test(db, slug, cb.from_user.id)

    if not success:
        await cb.message.edit_text(
            BotTexts.DELETE_TEST_ERROR_MSG,
            reply_markup=back_kb("my_tests")
        )
        return

    await cb.message.edit_text(
        BotTexts.DELETE_TEST_SUCCESS_MSG,
        reply_markup=back_kb("start")
    )


@router.callback_query(F.data == "delete_test_cancel")
async def delete_test_cancel(cb: CallbackQuery):
    await cb.answer()
    await cb.message.edit_text(
        BotTexts.DELETE_TEST_CANCEL_MSG,
        reply_markup=back_kb("my_tests")
    )


@router.callback_query(F.data.startswith("export_results:"))
async def export_results(cb: CallbackQuery):
    slug = cb.data.split(":", 1)[1]
    
    await cb.answer(BotTexts.EXPORT_PROCESSING_MSG)

    with SessionLocal() as db:
        stream = ExportService.export_test_results_to_excel(
            db=db,
            slug=slug,
            owner_id=cb.from_user.id,
        )

    file = BufferedInputFile(
        stream.getvalue(),
        filename=f"results_{slug}.xlsx"
    )

    await cb.message.answer_document(
        document=file,
        reply_markup=close_kb()
    )


@router.callback_query(F.data.startswith("download_qr:"))
async def download_qr(cb: CallbackQuery, bot: Bot):
    slug = cb.data.split(":", 1)[1]
    await cb.answer(BotTexts.QR_PROCESSING_MSG)

    with SessionLocal() as db:
        test = TestService.get_test(db, slug)

    if not test or test["owner_id"] != cb.from_user.id:
        await cb.answer("Тест не найден", show_alert=True)
        return

    test_link = f"https://t.me/{(await bot.me()).username}?start={slug}"

    qr_bytes = QrService.generate_qr_bytes(test_link)
    qr_file = BufferedInputFile(qr_bytes, filename=f"qr_{slug}.png")

    await cb.message.answer_photo(
        qr_file,
        reply_markup=close_kb()
    )


# заглушка
@router.callback_query(F.data == "noop")
async def noop(cb: CallbackQuery):
    await cb.answer()