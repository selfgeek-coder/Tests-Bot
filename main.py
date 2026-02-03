import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage

from src.bot.handlers import routers
from src.db.database import init_db
from config import Config_obj

logging.basicConfig(level=logging.INFO)

bot = Bot(token=Config_obj.bot_token)
dp = Dispatcher(storage=MemoryStorage())

async def main():
    init_db()
    
    for router in routers:
        dp.include_router(router)
    
    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="info", description="Информация о боте")
    ]
    await bot.set_my_commands(commands)
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())