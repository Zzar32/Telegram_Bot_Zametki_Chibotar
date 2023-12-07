import datetime
import aiogram
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


TOKEN = '6930938494:AAE_wIPMvHkxrdeDRcSr5NLb_RpKLv0Ytgw'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Для записи заметки введите /note <текст заметки>")


@dp.message_handler(commands=['note'])
async def note(message: types.Message):
    try:
        note_text = message.text.split('/note ', maxsplit=1)[1]
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        with open(f"notes_{date}.txt", 'a') as file:
            file.write(f"{date}: {note_text}\n")
        await message.reply("Заметка сохранена!")
    except IndexError:
        await message.reply("Пожалуйста, введите текст заметки после команды /note")


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    help_text = """
    Доступные команды:
    /start - начать работу с ботом
    /help - список команд
    /note <текст заметки> - добавить заметку
    """
    await message.reply(help_text)


if __name__ == '__main__':
    executor.start_polling(dp)