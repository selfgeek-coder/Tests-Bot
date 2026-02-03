class BotTexts: 
    # /start menu
    START_MSG = "👋🏻 Привет {first_name}!\n\nЯ - бот для образовательных тестирований."
    TEST_PREVIEW = "<b>{topic}</b>\n\nКоличество вопросов: {questions_count}"

    # my tests
    MY_TESTS_EMPTY_MSG = "У вас пока нет тестов. Создайте новый тест в главном меню."
    MY_TESTS_TITLE = "Ваши тесты"
    TEST_NOT_FOUND_MSG = "Тест не найден"
    DELETE_TEST_CONFIRM_MSG = "‼ Вы уверены, что хотите удалить этот тест?\n<b>Это действие будет необратимо</b>."
    DELETE_TEST_ERROR_MSG = "Ошибка при удалении теста"
    DELETE_TEST_SUCCESS_MSG = "Тест успешно удален."
    DELETE_TEST_CANCEL_MSG = "Удаление отменено."
    EXPORT_PROCESSING_MSG = "Формирую Excel..."
    QR_PROCESSING_MSG = "Формирую QR..."
    TEST_DETAILS_TEMPLATE = "<b>{topic}</b>\n\nВопросов: <code>{questions_count}</code>\n\nСсылка для прохождения: {test_link}"

    # create test
    CREATE_TEST_PROMPT = "<i>Введите тему тестирования</i>\n\nНапример:\n<code>Физика 8 класс, кипение воды</code>"
    ENTER_QUESTION_COUNT = "Сколько вопросов?"
    INVALID_NUMBER_INPUT = "⚠ Введите число"
    GENERATION_ERROR = "Ошибка генерации"
    TEST_PREVIEW_TEMPLATE = "<b>Предпросмотр теста</b>\n\nТема: <i>{topic}</i>\n\n"
    TEST_CREATED_TEMPLATE = "<b>Тестирование создано</b>\n\nСсылка для прохождения теста:\n{test_link}"
    TEST_SAVE_ERROR = "Ошибка при сохранении теста"

    # answer test
    TEST_NOT_FOUND_ALERT = "Тест не найден.\nВозможно он был удален создателем..."
    ENTER_FULLNAME_PROMPT = "Введите ваше <b>ФИО</b>:"
    INVALID_FULLNAME_WARNING = "⚠ Введите корректное <b>ФИО</b>!\nПример: <i>Иванов Иван Иванович</i>"
    SESSION_EXPIRED_ALERT = "Сессия истекла"
    TEST_COMPLETED_TEMPLATE = "<b>Тест завершен!</b>\n\nВаш результат: <code>{score}/{total}</code> <b>{percent}</b>%"
    RESULT_TO_OWNER_TEMPLATE = """
<b>Результат теста</b>

Тема: <i>{topic}</i>

ФИО: {fullname}
Telegram: {telegram_name} @{username}

Баллы: {score}/{total}
Процент: {percent}%
Оценка: {grade}
    """
    CANCEL_TEST_MSG = "Прохождение теста отменено"
    
    
    # Клавиатуры
    BTN_CREATE_TEST = "Создать тест"
    BTN_MY_TESTS = "Мои тесты"
    BTN_CANCEL = "Отмена"
    BTN_CLOSE = "Закрыть"
    BTN_BACK = "‹ Назад"
    BTN_CONFIRM = "Подтвердить"
    BTN_CANCEL_TEST = "Отменить"
    BTN_START_TEST = "Начать прохождение"
    BTN_YES_DELETE = "Да, удалить"
    BTN_NO_DELETE = "Отмена"
    BTN_DOWNLOAD_RESULTS = "Скачать результаты"
    BTN_CREATE_QR = "Создать QR-Код"
    BTN_DELETE = "Удалить"
    BTN_PREV_PAGE = "⬅️"
    BTN_NEXT_PAGE = "➡️"