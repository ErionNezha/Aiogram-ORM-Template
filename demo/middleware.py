from datetime import datetime

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject
from aiogram.types import User as TgUser

from data import strings
from models.models import Users


class UserCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: dict):
        tg_user: TgUser | None = data.get("event_from_user")
        chat = data.get("event_chat")

        if tg_user is None or tg_user.is_bot:
            return await handler(event, data)

        # Faqat shaxsiy suhbatdagi foydalanuvchilarni kuzatamiz
        if chat is not None and chat.type != "private":
            return await handler(event, data)

        now = datetime.utcnow()
        user = await Users.get_or_none(chat_id=tg_user.id)

        # --------- YARATISH ----------
        if user is None:
            user = await Users.create(
                chat_id=tg_user.id,
                is_premium=bool(tg_user.is_premium),
                lasted_at=now,
            )

        # --------- YANGILASH (minimal) ----------
        else:
            updates = {}

            if user.is_premium != bool(tg_user.is_premium):
                updates["is_premium"] = bool(tg_user.is_premium)

            # oxirgi foydalanish sanasi kuniga faqat bir marta yangilanadi
            if user.lasted_at.date() != now.date():
                updates["lasted_at"] = now

            # foydalanuvchi avval nofaol bo'lib qolgan bo'lsa (masalan botni
            # bloklagan/tark etgan bo'lsa) — qaytib kelganini belgilaymiz
            if not user.is_active:
                updates["is_active"] = True
                updates["returned_at"] = now

            if updates:
                await Users.filter(id=user.id).update(**updates)
                for field_name, value in updates.items():
                    setattr(user, field_name, value)

        if user.banned:
            if isinstance(event, CallbackQuery):
                await event.answer(strings.banned, show_alert=True)
            elif isinstance(event, Message):
                await event.answer(strings.banned)
            return

        data["user"] = user
        return await handler(event, data)
