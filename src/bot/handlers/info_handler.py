from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.bot.texts import BotTexts
from src.bot.keyboards import close_kb

router = Router()


@router.message(Command("info"))
async def info_handler(message: Message):
    await message.answer("🤖")
    await message.answer(BotTexts.INFO_MSG, parse_mode="HTML", reply_markup=close_kb())
        