from aiogram.filters import Filter
from aiogram import Bot, types

class ChatTypeFilter(Filter):
    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types