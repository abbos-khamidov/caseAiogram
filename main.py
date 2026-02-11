import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN = ''
bot = Bot(token=TOKEN)
dp = Dispatcher()



async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())