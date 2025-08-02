from aiogram import Bot, Dispatcher
from aiogram.filters import Command, StateFilter
from core.handlers.basic import answer, admin, get_start, select_book, get_book, check_subscribtion
from core.handlers.books import del_books, delete_book, getting_deleted, create_new_list, succesful_created, delete_list, list_getting_deleted, add_a_book, add_a_new_book, add_a_book_link, book_added_succesfully
from core.settings import settings
import asyncio
import logging
from aiogram import F
from core.utils.states import StepsForm
from core.utils.bookstates import StepsFormBook





async def start_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот запущен !')

async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот остановлен !')

async def start():

    bot = Bot(token=settings.bots.bot_token)

    dp = Dispatcher()
    dp.message.register(get_start, Command(commands=['start', 'run']))
    dp.callback_query.register(select_book, F.data.startswith('1/'))
    dp.callback_query.register(get_book, F.data.startswith('2/'))
    dp.message.register(admin, Command(commands='admin'), F.chat.id == settings.bots.admin_id)
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.message.register(answer, F.text != 'Удалить книги', F.text != 'Добавить разделы', F.text != 'Добавить книгу', F.text != 'Удалить разделы', F.text != 'Получить книгу', StateFilter(None))
    dp.message.register(del_books, F.text == 'Удалить книги', F.chat.id == settings.bots.admin_id)
    dp.message.register(create_new_list, F.text == 'Добавить разделы', F.chat.id == settings.bots.admin_id)
    dp.message.register(delete_list, F.text == 'Удалить разделы', F.chat.id == settings.bots.admin_id)
    dp.message.register(add_a_book, F.text == 'Добавить книгу', F.chat.id == settings.bots.admin_id)
    dp.callback_query.register(delete_book, F.data.startswith('11/'))
    dp.callback_query.register(getting_deleted, F.data.startswith('22/'))
    dp.callback_query.register(list_getting_deleted, F.data.startswith('111/'))
    dp.message.register(succesful_created, StepsForm.GET_NAME)
    dp.callback_query.register(add_a_new_book, F.data.startswith('1111/'), StepsFormBook.GET_ID_LIST)
    dp.message.register(add_a_book_link, StepsFormBook.GET_NAME_BOOK)
    dp.message.register(book_added_succesfully, StepsFormBook.GET_LINK_BOOK)
    dp.callback_query.register(check_subscribtion, F.data == 'check_subscribtion')


    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__=="__main__":
    asyncio.run(start())