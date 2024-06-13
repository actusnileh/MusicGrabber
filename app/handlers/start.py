from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode

from constant.start import CMD_START_TEXT


router = Router()


@router.message(Command("start", "help"))
async def cmd_start(message: Message):
    await message.answer(CMD_START_TEXT, parse_mode=ParseMode.HTML)
