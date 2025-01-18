import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
import asyncio
from config import TOKEN
from get_yani import get_course


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

KEYBOARD_START = [
    [types.KeyboardButton(text="ОФОРМИТЬ ЗАКАЗ")],
    [types.KeyboardButton(text="КАЛЬКУЛЯТОР СТОИМОСТИ")],
    [types.KeyboardButton(text="ПОМОЩЬ")],
]

@dp.message(Command('start'))
async def start_message(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=KEYBOARD_START,
        resize_keyboard=True,
        input_field_placeholder="Нажмите на необходимую кнопку"
    )
    await message.answer('Добро пожаловать! Данный тг бот поможет вам оформить заказ с Poizon. Нажмите на '
                         'одну из кнопок ниже для продолжения работы:', reply_markup=keyboard)

@dp.message(F.text.lower() == "помощь")
async def help_message(message: types.Message):
    await message.answer('Здесь будет размещена помощь. Чтобы вернуться назад нажмите /start')


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        print("Bot's working has been started...")
        asyncio.run(main())
    except:
        print("Something is going wrong, please wait...")
