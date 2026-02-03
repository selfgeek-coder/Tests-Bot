from math import ceil

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.bot.texts import BotTexts

def start_kb() -> InlineKeyboardMarkup:
    """
    Клавиатура для стартового меню.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=BotTexts.BTN_CREATE_TEST, callback_data="create_test")],
            [InlineKeyboardButton(text=BotTexts.BTN_MY_TESTS, callback_data="my_tests")]
        ]
    )

def cancel_kb(a: str) -> InlineKeyboardMarkup:
    """
    Универсальная клавиатура отмены.
    
    :param a: суффикс для callback_data
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=BotTexts.BTN_CANCEL,
                    callback_data=f"cancel_{a}"
                )
            ]
        ]
    )
    
def close_kb() -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой закрыть.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=BotTexts.BTN_CLOSE,
                    callback_data=f"close"
                )
            ]
        ]
    )
    
    
def back_kb(a: str) -> InlineKeyboardMarkup:
    """
    Универсальная клавиатура назад.
    
    :param a: суффикс для callback_data
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=BotTexts.BTN_BACK,
                    callback_data=f"back_to_{a}"
                )
            ]
        ]
    )    
    

def delete_confirm_kb(slug: str) -> InlineKeyboardMarkup:
    """
    Генерирует клавиатуру для подтверждения удаления теста.
    
    :param slug: ID теста
    :return: InlineKeyboardMarkup с кнопками "Да, удалить" и "Отмена"
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=BotTexts.BTN_YES_DELETE,
                    callback_data=f"delete_test_confirm:{slug}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=BotTexts.BTN_NO_DELETE,
                    callback_data="delete_test_cancel"
                )
            ]
        ]
    )
    

def answers_kb(slug: str, q_index: int, options: dict) -> InlineKeyboardMarkup:
    """
    Генерирует клавиатуру с вариантами ответа для вопроса.
    
    :param slug: ID теста
    :param q_index: индекс текущего вопроса
    :param options: словарь вариантов {ключ: текст}
    :return: InlineKeyboardMarkup
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{v}",
                    callback_data=f"answer:{slug}:{q_index}:{k}"
                )
            ]
            for k, v in options.items()
        ]
    )


def preview_kb() -> InlineKeyboardMarkup:
    """
    Клавиатура для предпросмотра теста.
    """
    
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=BotTexts.BTN_CONFIRM, callback_data="confirm_test")],
            [InlineKeyboardButton(text=BotTexts.BTN_CANCEL_TEST, callback_data="cancel_test")]
        ]
    )
    
    
def start_test_kb(slug: str) -> InlineKeyboardMarkup:
    """
    Клавиатура для начала теста.
    """
    
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=BotTexts.BTN_START_TEST, callback_data=f"start_test:{slug}")]
        ]
    )
    
def my_tests_kb(all_tests: list, page: int) -> InlineKeyboardMarkup:
    """
    Клавиатура моих тестов с пагинацией

    :param all_tests: Массив тестов
    :param page: Страница
    """

    keyboard = []

    total = len(all_tests)
    pages = max(1, ceil(total / 4))

    page = max(1, min(page, pages))
    start = (page - 1) * 4
    end = start + 4

    tests = all_tests[start:end]

    for t in tests:
        keyboard.append([
            InlineKeyboardButton(
                text=t["topic"],
                callback_data=f"my_test:{t['slug']}"
            )
        ])

    nav = []

    if page > 1:
        nav.append(
            InlineKeyboardButton(
                text=BotTexts.BTN_PREV_PAGE,
                callback_data=f"my_tests_page:{page - 1}"
            )
        )

    nav.append(
        InlineKeyboardButton(
            text=f"{page} / {pages}",
            callback_data="noop"
        )
    )

    if page < pages:
        nav.append(
            InlineKeyboardButton(
                text=BotTexts.BTN_NEXT_PAGE,
                callback_data=f"my_tests_page:{page + 1}"
            )
        )

    keyboard.append(nav)

    keyboard.append([
        InlineKeyboardButton(text=BotTexts.BTN_BACK, callback_data="back_to_start")
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def test_manage_kb(slug: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=BotTexts.BTN_DOWNLOAD_RESULTS,
                    callback_data=f"export_results:{slug}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=BotTexts.BTN_CREATE_QR,
                    callback_data=f"download_qr:{slug}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=BotTexts.BTN_DELETE,
                    callback_data=f"delete_test:{slug}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=BotTexts.BTN_BACK,
                    callback_data="my_tests"
                )
            ]
        ]
    )