import asyncio
import logging
import sys

import aiogram.exceptions

import config
from db import create_tables_funcs
from handlers import routers
from loader import dp, bot, db_connector
from middlewares import UserMiddleware


async def send_start_msg_to_admin():
    if not config.ADMIN_ID:
        raise ValueError('Вы не указали ADMIN_ID в файле .env!')

    try:
        await bot.send_message(chat_id=int(config.ADMIN_ID), text='Бот запущен! Напишите команду /start')
    except aiogram.exceptions.TelegramForbiddenError:
        logging.error(
            'Не удалось отправить сообщение о запуске чат-бота администратору! Администратор заблокировал чат-бота'
        )
    except aiogram.exceptions.TelegramBadRequest:
        logging.error(
            'Не удалось отправить сообщение о запуске чат-бота администратору! Администратор пока не разрешил '
            'отправлять сообщения чат-боту или указан некорректный ADMIN_ID в файле .env!'
        )


async def main():
    for func in create_tables_funcs:
        await func(db_connector)

    await send_start_msg_to_admin()
    await dp.start_polling(bot)


if __name__ == '__main__':
    for router in routers:
        router.message.middleware(UserMiddleware())

    dp.include_routers(*routers)

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
