#!/usr/bin/env python3
import os
import sys
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.exceptions import TelegramNetworkError, TelegramRetryAfter

# ------------------------------------------------------------
# 1. Настройка логирования ВЕСЬ вывод → stderr
# ------------------------------------------------------------
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Хэндлер, который пишет в stderr
stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setLevel(logging.DEBUG)

# Формат: время, уровень, имя логгера, сообщение
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
stderr_handler.setFormatter(formatter)
logger.addHandler(stderr_handler)

# Также настроим корневой логгер, чтобы aiogram и aiohttp тоже писали в stderr
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
# Удаляем возможные старые хэндлеры, чтобы не дублировало
for h in root_logger.handlers[:]:
    root_logger.removeHandler(h)
root_logger.addHandler(stderr_handler)

# ------------------------------------------------------------
# 2. Чтение токена
# ------------------------------------------------------------
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    logger.critical("Переменная окружения BOT_TOKEN не установлена!")
    sys.exit(1)

# ------------------------------------------------------------
# 3. Инициализация бота и диспетчера
# ------------------------------------------------------------
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ------------------------------------------------------------
# 4. Обработчик всех сообщений (эхо)
# ------------------------------------------------------------
@dp.message()
async def echo_handler(message: types.Message):
    logger.debug(f"Получено сообщение от {message.from_user.id} "
                 f"(username={message.from_user.username}): {message.text}")
    try:
        if message.text:
            await message.answer(message.text)
            logger.debug(f"Ответ отправлен: {message.text}")
        else:
            # Если сообщение без текста (стикер, фото и т.д.) — игнорируем
            logger.info(f"Сообщение без текста от {message.from_user.id}, пропускаем")
    except TelegramNetworkError as e:
        logger.error(f"Сетевая ошибка при ответе пользователю {message.from_user.id}: {e}")
    except TelegramRetryAfter as e:
        logger.warning(f"Flood wait: надо подождать {e.retry_after} сек")
    except Exception as e:
        logger.exception(f"Неожиданная ошибка при обработке сообщения от {message.from_user.id}")

# ------------------------------------------------------------
# 5. Запуск с глобальной обработкой исключений
# ------------------------------------------------------------
async def main():
    logger.info("Бот запускается. Начинаем polling...")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.critical(f"Критическая ошибка в polling: {e}", exc_info=True)
        raise
    finally:
        await bot.session.close()
        logger.info("Сессия бота закрыта")

if __name__ == "__main__":
    logger.debug("Скрипт стартовал, входим в asyncio.run()")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен по Ctrl+C")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Необработанное исключение верхнего уровня: {e}", exc_info=True)
        sys.exit(1)
