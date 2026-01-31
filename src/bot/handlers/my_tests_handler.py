from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.types import BufferedInputFile

from src.db.database import SessionLocal
from src.services.test_service import TestService
from src.services.export_service import ExportService
from src.bot.keyboards import my_tests_kb, test_manage_kb, start_kb, back_kb, delete_confirm_kb


router = Router()


@router.callback_query(F.data == "my_tests")
async def my_tests(cb: CallbackQuery):
    await cb.answer()

    with SessionLocal() as db:
        tests = TestService.get_my_tests(db, cb.from_user.id)

    if not tests:
        await cb.answer(
            "У вас пока нет тестов. Создайте новый тест в главном меню."
        )
        return

    await cb.message.edit_text(
        "Ваши тесты ⤵",
        reply_markup=my_tests_kb(tests, page=1)
    )
    
@router.callback_query(F.data.startswith("my_tests_page:"))
async def my_tests_page(cb: CallbackQuery):
    page = int(cb.data.split(":")[1])
    
    await cb.answer()

    with SessionLocal() as db:
        tests = TestService.get_my_tests(db, cb.from_user.id)

    await cb.message.edit_text(
        "Ваши тесты ⤵",
        reply_markup=my_tests_kb(tests, page)
    )


@router.callback_query(F.data.startswith("my_test:"))
async def my_test_detail(cb: CallbackQuery, bot: Bot):
    slug = cb.data.split(":", 1)[1]
    await cb.answer()

    with SessionLocal() as db:
        test = TestService.get_test(db, slug)

    if not test or test["owner_id"] != cb.from_user.id:
        await cb.message.edit_text("Тест не найден")
        return

    text = (
        f"<b>{test['topic']}</b>\n\n"
        f"Вопросов: <code>{len(test['questions'])}</code>\n\n"
        f"Ссылка для прохождения: https://t.me/{(await bot.me()).username}?start={test['slug']}"
    )

    await cb.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=test_manage_kb(slug)
    )


@router.callback_query(F.data.startswith("delete_test:"))
async def delete_test_ask(cb: CallbackQuery):
    slug = cb.data.split(":", 1)[1]
    await cb.answer()

    await cb.message.edit_text(
        "❗ <i>Вы уверены, что хотите удалить этот тест</i>?\n"
        "Это действие будет необратимо.",
        reply_markup=delete_confirm_kb(slug),
        parse_mode="HTML"
    )
    
@router.callback_query(F.data.startswith("delete_test_confirm:"))
async def delete_test_confirm(cb: CallbackQuery):
    slug = cb.data.split(":", 1)[1]
    await cb.answer()

    with SessionLocal() as db:
        success = TestService.delete_test(db, slug, cb.from_user.id)

    if not success:
        await cb.message.edit_text(
            "Ошибка при удалении теста",
            reply_markup=back_kb("my_tests")
        )
        return

    await cb.message.edit_text(
        "Тест успешно удален.",
        reply_markup=back_kb("start")
    )
    
@router.callback_query(F.data == "delete_test_cancel")
async def delete_test_cancel(cb: CallbackQuery):
    await cb.answer()
    await cb.message.edit_text(
        "Удаление отменено.",
        reply_markup=back_kb("my_tests")
    )


@router.callback_query(F.data.startswith("export_results:"))
async def export_results(cb: CallbackQuery):
    slug = cb.data.split(":", 1)[1]
    await cb.answer("Формирую Excel…")

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
        caption="Результаты теста"
    )


@router.callback_query(F.data == "noop")
async def noop(cb: CallbackQuery):
    await cb.answer()