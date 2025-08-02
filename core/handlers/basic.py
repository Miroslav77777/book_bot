from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from core.keyboards.reply import reply_keyboard
from core.keyboards.inline import get_inline_keyboard, get_inline_books, get_book_url, get_subscription
from core.settings import settings
from googlesheettable import Getlists
from aiogram.exceptions import TelegramForbiddenError

async def check_user_subscription(user_id: int, bot: Bot):
    try:
        user_channel_status = await bot.get_chat_member(settings.bots.channel_id, user_id=user_id)
        return user_channel_status.status != 'left'
    except TelegramForbiddenError:
        print(f"Пользователь {user_id} заблокировал бота.")
        return False
    except Exception as e:
        print(f"Ошибка при проверке подписки пользователя {user_id}: {e}")
        return False

async def get_start(message: Message, bot: Bot):
    if await check_user_subscription(message.from_user.id, bot):
        await bot.send_message(message.from_user.id, f'Привет {message.from_user.first_name}! Рады тебя видеть 👋. Чтобы скачать электронную книгу, выберите нужный раздел. 👇', reply_markup=get_inline_keyboard())
    else:
        await bot.send_message(message.from_user.id, f'Чтобы получить доступ к контенту и иметь возможность \nскачивать электронные книги, подпишитесь на наш Телеграм \nканал. ', reply_markup=get_subscription())

async def select_book(call: CallbackQuery, bot: Bot):
    if await check_user_subscription(call.from_user.id, bot):
        genreid = call.data.split('/')[1]
        await bot.send_message(call.from_user.id, f'Выберите нужную книгу. 👇', reply_markup=get_inline_books(genreid))
        await call.answer()
    else:
        await bot.send_message(call.from_user.id, f'Чтобы получить доступ к контенту и иметь возможность \nскачивать электронные книги, подпишитесь на наш Телеграм \nканал. ', reply_markup=get_subscription())

async def get_book(call: CallbackQuery, bot: Bot):
    if await check_user_subscription(call.from_user.id, bot):
        genreid = call.data.split('/')[1]
        book_id = call.data.split('/')[2]
        getlists = Getlists()
        book_data = getlists.get_book_by_id(genreid, book_id)
        book_name = book_data['title'].split('_')[1]
        await bot.send_message(call.from_user.id, f'Скачайте книгу 👇', reply_markup=get_book_url(genreid, book_id))
        await bot.send_message(settings.bots.admin_id, f'Пользователь @{call.from_user.username} скачал книгу {book_name}')
        await call.answer()
    else:
        await bot.send_message(call.from_user.id, f'Чтобы получить доступ к контенту и иметь возможность \nскачивать электронные книги, подпишитесь на наш Телеграм \nканал. ', reply_markup=get_subscription())

async def answer(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, f'Прости, {message.from_user.first_name}, не понял тебя.')

async def admin(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, f'Вы вошли в режим администратора', reply_markup=reply_keyboard)

async def check_subscribtion(call: CallbackQuery, bot: Bot):
    if await check_user_subscription(call.from_user.id, bot):
        await bot.send_message(call.from_user.id, f'Отлично! Вы подписаны! \nВыберите раздел:', reply_markup=get_inline_keyboard())
    else:
        await bot.send_message(call.from_user.id, f'Чтобы получить доступ к контенту и иметь возможность \nскачивать электронные книги, подпишитесь на наш Телеграм \nканал. ', reply_markup=get_subscription())