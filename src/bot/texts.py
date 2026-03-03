class BotTexts: 
    # /info
    INFO_MSG = """
<tg-emoji emoji-id=\"5373098009640836781\">📚</tg-emoji> <b>Telegram бот для образовательных тестирований</b>

<b>Возможности:</b>

<b>Создание тестов</b> - Генерируйте тесты по любой теме с помощью ИИ. Просто укажите тему и количество вопросов

<b>Прохождение тестов</b> - Решайте тесты и получайте оценку в конце

<b>QR-коды</b> - Создавайте QR-коды для своих тестов, чтобы поделиться ими

<b>Результаты</b> - Скачивайте результаты прохождений тестов в формате Excel

<b>Управление тестами</b> - Просматривайте все свои тесты и управляйте ими

<b>Как начать:</b>
1. Нажмите "Создать тест" для новой проверки
2. Или выберите "Мои тесты" для управления существующими

<i>Тесты создаются искусственным интеллектом и содержат актуальную информацию</i>
"""
    
    # /start menu
    START_MSG = "Привет, {first_name}!\n\nЯ бот для создания образовательных тестирований."
    TEST_PREVIEW = "<b>{topic}</b>\n\nКоличество вопросов: {questions_count}"

    # my tests
    MY_TESTS_EMPTY_MSG = "У вас пока нет тестов... Создайте новый тест в главном меню."
    MY_TESTS_TITLE = "Ваши тесты"
    TEST_NOT_FOUND_MSG = "<tg-emoji emoji-id=\"5467928559664242360\">❗️</tg-emoji> Тест не найден"
    DELETE_TEST_CONFIRM_MSG = "<tg-emoji emoji-id=\"5467596412663372909\">⁉️</tg-emoji> Вы уверены, что хотите удалить этот тест?\n<b>Это действие будет необратимо</b>."
    DELETE_TEST_ERROR_MSG = "Произошла ошибка при удалении теста"
    DELETE_TEST_SUCCESS_MSG = "<tg-emoji emoji-id=\"5363850326577259091\">🆗</tg-emoji> Тест успешно удален."
    DELETE_TEST_CANCEL_MSG = "Удаление отменено."
    EXPORT_PROCESSING_MSG = "Формирую Excel..."
    QR_PROCESSING_MSG = "Формирую QR..."
    TEST_DETAILS_TEMPLATE = "<b>{topic}</b>\n\nКоличество вопросов: <code>{questions_count}</code>\n\nСсылка для прохождения: {test_link}"

    # create test
    CREATE_TEST_PROMPT = "Введите тему тестирования\n\nНапример:\n<code>Создай тест по теме: Физика 8 класс, кипение воды. 5 Вопросов</code>"
    ENTER_QUESTION_COUNT = "Сколько вопросов?"
    INVALID_NUMBER_INPUT = "Введите число"
    GENERATION_ERROR = "Ошибка генерации"
    TEST_PREVIEW_TEMPLATE = "<tg-emoji emoji-id=\"5334882760735598374\">📝</tg-emoji> <b>Предпросмотр теста</b>\n\nТема: <i>{topic}</i>\n\n"
    TEST_CREATED_TEMPLATE = "<b>Тест успешно создан</b>\nСсылка для прохождения теста:\n{test_link}"
    TEST_SAVE_ERROR = "Ошибка при сохранении теста"
    REVISION_PROMPT = "Опишите, что нужно изменить в тесте:\n\nНапример: \"Добавь еще 2 вопроса\", \"Сделай вопросы сложнее\", \"Измени тему на ...\""
    REVISION_ERROR = "Не удалось внести правки. Попробуйте еще раз."
    REVISION_PROCESSING = "🔄"
    BACK_TO_PREVIEW = "↩️ Возвращаемся к просмотру теста"

    # answer test
    TEST_NOT_FOUND_ALERT = "<tg-emoji emoji-id=\"5465665476971471368\">❌</tg-emoji> Тест не найден.\nВозможно он был удален создателем..."
    ENTER_FULLNAME_PROMPT = "<tg-emoji emoji-id=\"5334673106202010226\">✏️</tg-emoji> Введите ваше <b>ФИО</b>:"
    INVALID_FULLNAME_WARNING = "<tg-emoji emoji-id=\"5467928559664242360\">❗️</tg-emoji> Введите корректное <b>ФИО</b>!\nПример: <i>Иванов Иван Иванович</i>"
    SESSION_EXPIRED_ALERT = "Сессия истекла"
    TEST_COMPLETED_TEMPLATE = "<tg-emoji emoji-id=\"5427009714745517609\">✅</tg-emoji> <b>Тест завершен!</b>\n\nВаш результат: <code>{score}/{total}</code> <b>{percent}</b>%"
    RESULT_TO_OWNER_TEMPLATE = """
<tg-emoji emoji-id=\"5242628160297641831\">🔔</tg-emoji> <b>Результат теста</b>

Тема: <i>{topic}</i>

ФИО: {fullname}
Telegram: {telegram_name} @{username}

Баллы: {score}/{total}
Процент: {percent}%
Оценка: {grade}
    """
    CANCEL_TEST_MSG = "Прохождение теста отменено"
    ALREADY_PASSED_MSG = "Вы уже проходили этот тест."
    
    
    # Клавиатуры
    BTN_CREATE_TEST = "Создать тест"
    BTN_MY_TESTS = "Мои тесты"
    BTN_CANCEL = "Отмена"
    BTN_CLOSE = "Закрыть"
    BTN_BACK = "Назад"
    BTN_CONFIRM = "Подтвердить"
    BTN_CANCEL_TEST = "Отменить"
    BTN_REVISE_TEST = "Внести правки"
    BTN_START_TEST = "Начать прохождение"
    BTN_YES_DELETE = "Да, удалить"
    BTN_NO_DELETE = "Отмена"
    BTN_DOWNLOAD_RESULTS = "Скачать результаты"
    BTN_CREATE_QR = "Создать QR-Код"
    BTN_DELETE = "Удалить"
    BTN_PREV_PAGE = "⬅️"
    BTN_NEXT_PAGE = "➡️"
