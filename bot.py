from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from database import Database


import asyncio
import json


token = input("Type a bot's TOKEN: ")

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
db = Database()

print("Bot have been started")

@dp.message(Command(commands=['start']))
async def send_welcome(message: types.Message):
    await message.reply("Привет!\nОтправь мне входные данные в формате:\n"
                        "{\n"
                        "   \"dt_from\": \"2022-02-01T00:00:00\",\n"
                        "   \"dt_upto\": \"2022-02-02T00:00:00\",\n"
                        "   \"group_type\": \"hour\"\n"
                        "}\n")

@dp.message()
async def process_json(message: types.Message):
    try:
        data = json.loads(message.text)
        # если данные содержат нужные ключи
        if 'dt_from' in data and 'dt_upto' in data and 'group_type' in data:
            result = await db.aggregate_salaries(data['dt_from'], data['dt_upto'], data['group_type'])
            await message.reply(result)
        else:
            await message.reply("Ошибка: Некорректный формат данных.")
    except json.JSONDecodeError:
        await message.reply("Ошибка: Некорректный формат данных.")


async def main():
    # Регистрация хендлеров
    dp.message.register(send_welcome, Command(commands=['start']))
    dp.message.register(process_json)

    # Запуск бота
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
