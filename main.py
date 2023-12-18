import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN_API
from db import Session, User, Message

TOKEN = TOKEN_API

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    session = Session()
    user_list = session.query(User).filter(User.user_telegram_id == str(message.from_user.id)).first()
    if not user_list:
        user_telegram_id = message.from_user.id
        username = message.from_user.username
        created = message.date
        user = User(user_telegram_id=user_telegram_id, username=username, created=created)
        session = Session()
        session.add(user)
        session.commit()
        await message.reply("Ma'lumotlaringiz saqlandi")
    else:
        await message.answer("Siz oldin ro'yhatdan o'tgansiz")


@dp.message()
async def user_chat_handler(message: Message):
    user_id = message.from_user.id
    text = message.text
    created = message.date
    mes = Message(user_id=user_id, text=text, created=created)
    session = Session()
    session.add(mes)
    session.commit()
    if message.from_user.username:
        await message.answer(f"{message.from_user.username}  Xabaringiz saqlandi")
    elif message.from_user.last_name:
        await message.answer(f"{message.from_user.first_name} {message.from_user.last_name} Xabaringiz saqlandi")
    else:
        await message.answer(f"{message.from_user.first_name} Xabaringiz saqlandi")


async def main():
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
