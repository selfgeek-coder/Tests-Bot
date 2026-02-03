from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from math import ceil

def start_kb() -> InlineKeyboardMarkup:
    """
    Клавиатура для стартового меню.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Создать тест", callback_data="create_test")],
            [InlineKeyboardButton(text="Мои тесты", callback_data="my_tests")]
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
                    text="Отмена",
                    callback_data=f"cancel_{a}"
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
                    text="‹ Назад",
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
                    text="Да, удалить",
                    callback_data=f"delete_test_confirm:{slug}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Отмена",
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
            [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_test")],
            [InlineKeyboardButton(text="Отменить", callback_data="cancel_test")]
        ]
    )
    
    
def start_test_kb(slug: str) -> InlineKeyboardMarkup:
    """
    Клавиатура для начала теста.
    """
    
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="▶ Начать прохождение", callback_data=f"start_test:{slug}")]
        ]
    )
    
def my_tests_kb(all_tests: list, page: int) -> InlineKeyboardMarkup:
    """
    Клавиатура моих тестов с пагинацией

    :param all_test: Массив тестов
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
                text="⬅️",
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
                text="➡️",
                callback_data=f"my_tests_page:{page + 1}"
            )
        )

    keyboard.append(nav)

    keyboard.append([
        InlineKeyboardButton(text="‹ Назад", callback_data="back_to_start")
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def test_manage_kb(slug: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Скачать результаты",
                    callback_data=f"export_results:{slug}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Удалить",
                    callback_data=f"delete_test:{slug}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="‹ Назад",
                    callback_data="my_tests"
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
                    text="Да, удалить",
                    callback_data=f"delete_test_confirm:{slug}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Отмена",
                    callback_data="delete_test_cancel"
                )
            ]
        ]
    )