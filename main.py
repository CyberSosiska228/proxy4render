import os
import asyncio
from aiogram import Bot, Dispatcher, types

# Загрузка токена из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("Переменная окружения BOT_TOKEN не установлена!")

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message()
async def echo(message: types.Message):
    """Обработчик всех текстовых сообщений — отправляет обратно тот же текст."""
    if message.text:  # если сообщение содержит текст
        await message.answer(message.text)


async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
