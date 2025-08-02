from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType

reply_keyboard = ReplyKeyboardMarkup(keyboard =[
    [KeyboardButton(text='Удалить книги'), KeyboardButton(text='Удалить разделы'), KeyboardButton(text='Добавить разделы'), KeyboardButton(text='Добавить книгу')]
], resize_keyboard=True, input_field_placeholder="Выбери кнопку")

