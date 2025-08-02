from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from core.keyboards.inline import get_inline_delboard, get_book_deleted, get_inline_delgenboard, get_inline_addbookboard
from core.settings import settings
from googlesheettable import Getlists
from core.utils.states import StepsForm
from core.utils.bookstates import StepsFormBook



async def del_books(message: Message, bot: Bot):
    await bot.send_message(settings.bots.admin_id, f'Выберите жанр для удаления книги', reply_markup=get_inline_delboard())

async def delete_book(call: CallbackQuery, bot: Bot):
    genreid = call.data.split('/')[1]
    await bot.send_message(settings.bots.admin_id, f'Выберите книгу, которую хотите удалить', reply_markup=get_book_deleted(genreid))

async def getting_deleted(call: CallbackQuery, bot:Bot):
    genreid = call.data.split('/')[1]
    book_id = call.data.split('/')[2]
    getlists = Getlists()
    book_deleted = getlists.delete_book_by_id(genreid, book_id)
    if book_deleted:
        await bot.send_message(settings.bots.admin_id, f'Книга удалена !')
    else:
        await bot.send_message(settings.bots.admin_id, f'Книга не найдена !')


async def create_new_list(message: Message, state: FSMContext):
    await message.answer(f'Напишите название раздела')
    await state.set_state(StepsForm.GET_NAME)

async def succesful_created(message: Message, state: FSMContext):
    getlists = Getlists()
    getlists.create_new_sheet(str(message.text))
    await message.answer(f'Успешно добавлен новый раздел с названием: {str(message.text)}')
    await state.update_data(name=message.text)
    await state.clear()

async def delete_list(message: Message, bot: Bot):
    await bot.send_message(settings.bots.admin_id, f'Выберите раздел для удаления', reply_markup=get_inline_delgenboard())

async def list_getting_deleted(call: CallbackQuery, bot:Bot):
    genreid = call.data.split('/')[1]
    getlists = Getlists()
    getlists.delete_sheet_by_id(genreid)
    await bot.send_message(settings.bots.admin_id, f'Раздел успешно удален')

async def add_a_book(message: Message, bot: Bot, state: FSMContext):
    await bot.send_message(settings.bots.admin_id, f'Выберите раздел для добавления книги', reply_markup=get_inline_addbookboard())
    await state.set_state(StepsFormBook.GET_ID_LIST)


async def add_a_new_book(call: CallbackQuery, bot: Bot, state: FSMContext):
    genreid = call.data.split('/')[1]
    await bot.send_message(settings.bots.admin_id, f'Напишите название книги:')
    await state.update_data(id=genreid)
    await state.set_state(StepsFormBook.GET_NAME_BOOK)

async def add_a_book_link(message: Message, state: FSMContext):
    await message.answer(f'Отлично ! Теперь пришлите ссылку на книгу {message.text}')
    await state.update_data(book=message.text)
    await state.set_state(StepsFormBook.GET_LINK_BOOK)

async def book_added_succesfully(message: Message, state: FSMContext):
    context_data = await state.get_data()
    id = context_data.get('id')
    book = context_data.get('book')
    link = message.text
    getlists = Getlists()
    getlists.add_book_to_sheet_by_id(id, book, link)
    await message.answer(f'Книга {book} успешно сохранена и имеет ссылку: {link}')
    await state.clear()


