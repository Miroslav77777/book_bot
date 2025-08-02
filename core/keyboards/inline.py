from aiogram.utils.keyboard import InlineKeyboardBuilder
from googlesheettable import Getlists

# Юзер кнопки
def get_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    # Создаем объект Getlists
    getlists = Getlists()
    # Получаем список названий листов
    topics = getlists.get_topics()
    for namesg in topics:
        keyboard_builder.button(text=namesg.split('_')[1], callback_data='1/'+namesg.split('_')[0])
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def get_inline_books(id):
    keyboard_builder = InlineKeyboardBuilder()
    getlists = Getlists()
    book_name = getlists.get_book_data(id)
    print(book_name)
    for names in book_name:
        book_id = names['title'].split('_')[0]
        book_name_id = names['title'].split('_')[1]
        keyboard_builder.button(text=book_name_id, callback_data='2/'+id+'/'+book_id)

    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()

def get_book_url(id, book_id):
    keyboard_builder = InlineKeyboardBuilder()
    getlists = Getlists()
    book_data = getlists.get_book_by_id(id, book_id)
    book_name = book_data['title'].split('_')[1]
    keyboard_builder.button(text=book_name, url=book_data['link'])


    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()

# Админ кнопки
def get_inline_delboard():
    keyboard_builder = InlineKeyboardBuilder()
    # Создаем объект Getlists
    getlists = Getlists()
    # Получаем список названий листов
    topics = getlists.get_topics()
    for namesg in topics:
        keyboard_builder.button(text=namesg.split('_')[1], callback_data='11/' + namesg.split('_')[0])
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()
def get_book_deleted(id):
    keyboard_builder = InlineKeyboardBuilder()
    getlists = Getlists()
    book_name = getlists.get_book_data(id)

    for names in book_name:
        book_id = names['title'].split('_')[0]
        book_name_id = names['title'].split('_')[1]
        keyboard_builder.button(text=book_name_id, callback_data='22/' + id + '/' + book_id)

    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()

def get_inline_delgenboard():
    keyboard_builder = InlineKeyboardBuilder()
    # Создаем объект Getlists
    getlists = Getlists()
    # Получаем список названий листов
    topics = getlists.get_topics()
    for namesg in topics:
        keyboard_builder.button(text=namesg.split('_')[1], callback_data='111/' + namesg.split('_')[0])
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()

def get_inline_addbookboard():
    keyboard_builder = InlineKeyboardBuilder()
    # Создаем объект Getlists
    getlists = Getlists()
    # Получаем список названий листов
    topics = getlists.get_topics()
    for namesg in topics:
        keyboard_builder.button(text=namesg.split('_')[1], callback_data='1111/' + namesg.split('_')[0])
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()

def get_subscription():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Перейти на канал', url='https://t.me/saentology_obo_vsem')
    keyboard_builder.button(text='Проверить подписку ✅', callback_data='check_subscribtion')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()