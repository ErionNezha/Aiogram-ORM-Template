from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message, TelegramObject


class ChatTypesFilter(BaseFilter):
    def __init__(self, chat_types: str | list[str]):
        self.chat_types = chat_types

    async def __call__(self, event: TelegramObject) -> bool:
        if isinstance(event, CallbackQuery):
            # eski/yetib bo'lmaydigan xabarlarda event.message None bo'lishi mumkin
            if event.message is None:
                return False
            chat_type = event.message.chat.type
        elif isinstance(event, Message):
            chat_type = event.chat.type
        else:
            return False

        if isinstance(self.chat_types, str):
            return chat_type == self.chat_types
        return chat_type in self.chat_types
