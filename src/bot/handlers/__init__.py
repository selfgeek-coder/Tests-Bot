from .answer_test_handler import router as answer_router
from .create_test_handler import router as create_router
from .start_handler import router as start_router
from .my_tests_handler import router as my_tests_router
from .info_handler import router as info_router

routers = [
    info_router,
    start_router,
    create_router,
    answer_router,
    my_tests_router
]