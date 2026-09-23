from aiogram import Dispatcher, Router

from filters import ChatTypesFilter
from handlers import echo, user_status


def register_all_routes(dp: Dispatcher):
    master_router = Router()
    check_admin_router = Router()
    dp.include_router(check_admin_router)
    dp.include_router(master_router)


    echo.router.message.filter(ChatTypesFilter("private"))
    echo.router.callback_query.filter(ChatTypesFilter("private"))
    master_router.include_router(echo.router)
    master_router.include_router(user_status.router)
