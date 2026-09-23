import logging
import time
from collections import defaultdict, deque
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, limit: int = 2, window: float = 1.0, cooldown: float = 1.0):
        self.limit = limit
        self.window = window
        self.cooldown = cooldown
        self._events: dict[tuple[int, int], deque] = defaultdict(deque)
        self._cooldowns: dict[tuple[int, int], float] = {}

    @staticmethod
    def _extract_key(event: TelegramObject) -> tuple[int, int] | None:
        """Message va CallbackQuery uchun (chat_id, user_id) kalitini chiqarib beradi."""
        if isinstance(event, Message):
            if not event.from_user:
                return None
            return event.chat.id, event.from_user.id

        if isinstance(event, CallbackQuery):
            if not event.from_user:
                return None
            # eski/yetib bo'lmaydigan xabarda event.message None bo'lishi mumkin
            chat_id = event.message.chat.id if event.message else event.from_user.id
            return chat_id, event.from_user.id

        return None

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        key = self._extract_key(event)
        if key is None:
            return await handler(event, data)

        now = time.monotonic()

        until = self._cooldowns.get(key)
        if until is not None:
            if now < until:
                return
            # cooldown muddati allaqachon tugagan — eski yozuvni tozalaymiz
            del self._cooldowns[key]

        q = self._events[key]
        while q and (now - q[0]) > self.window:
            q.popleft()
        q.append(now)

        if len(q) > self.limit:
            self._cooldowns[key] = now + self.cooldown
            logger.debug("Rate limit ishga tushdi: chat=%s user=%s", key[0], key[1])

            if isinstance(event, CallbackQuery):
                text = f"❗ Iltimos, {self.cooldown:g} soniya kutib qayta urinib ko'ring."
                # Callback uchun chat'ga xabar emas, tugma ustida popup ko'rsatiladi
                await event.answer(text, show_alert=True)
            else:
                text = f"<b>❗ Iltimos, {self.cooldown:g} soniya kutib qayta urinib ko'ring.</b>"
                await event.answer(text)
            return

        return await handler(event, data)
