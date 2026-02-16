from math import ceil

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.bot.texts import BotTexts

def start_kb() -> InlineKeyboardMarkup:
    """
    Клавиатура для стартового меню.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=BotTexts.BTN_CREATE_TEST,
                callback_data="create_test",
                icon_custom_emoji_id="5879841310902324730")
            ],
            [InlineKeyboardButton(
                text=BotTexts.BTN_MY_TESTS,
                callback_data="my_tests",
                icon_custom_emoji_id="5875206779196935950")
            ]
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
                    callback_data=f"cancel_{a}",
                    icon_custom_emoji_id="5985346521103604145"
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
                    callback_data=f"close",
                    icon_custom_emoji_id="5985346521103604145"
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
                    callback_data=f"back_to_{a}",
                    icon_custom_emoji_id="5875082500023258804"
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
                    callback_data=f"delete_test_confirm:{slug}",
                    icon_custom_emoji_id="5985596818912712352"
                )
            ],
            [
                InlineKeyboardButton(
                    text=BotTexts.BTN_NO_DELETE,
                    callback_data="delete_test_cancel",
                    icon_custom_emoji_id="5985346521103604145"
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
            [InlineKeyboardButton(
                text=BotTexts.BTN_CONFIRM,
                callback_data="confirm_test",
                icon_custom_emoji_id="5985596818912712352"),
            ],
            [InlineKeyboardButton(
                text=BotTexts.BTN_CANCEL_TEST,
                callback_data="cancel_test",
                icon_custom_emoji_id="5985346521103604145")
            ]
        ]
    )
    
    
def start_test_kb(slug: str) -> InlineKeyboardMarkup:
    """
    Клавиатура для начала теста.
    """
    
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=BotTexts.BTN_START_TEST,
                callback_data=f"start_test:{slug}"
            )]
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
        InlineKeyboardButton(
            text=BotTexts.BTN_BACK,
            callback_data="back_to_start",
            icon_custom_emoji_id="5875082500023258804"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def test_manage_kb(slug: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=BotTexts.BTN_DOWNLOAD_RESULTS,
                    callback_data=f"export_results:{slug}",
                    icon_custom_emoji_id="5879883461711367869"
                )
            ],
            [
                InlineKeyboardButton(
                    text=BotTexts.BTN_CREATE_QR,
                    callback_data=f"download_qr:{slug}",
                    icon_custom_emoji_id="5987917196469213507"
                )
            ],
            [
                InlineKeyboardButton(
                    text=BotTexts.BTN_DELETE,
                    callback_data=f"delete_test:{slug}",
                    icon_custom_emoji_id="5879896690210639947"
                )
            ],
            [
                InlineKeyboardButton(
                    text=BotTexts.BTN_BACK,
                    callback_data="my_tests",
                    icon_custom_emoji_id="5875082500023258804"
                )
            ]
        ]
    )