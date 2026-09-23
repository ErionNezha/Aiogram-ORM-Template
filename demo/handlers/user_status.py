from aiogram import Router
from aiogram.types import ChatMemberUpdated

from models.models import Users

router = Router()


@router.my_chat_member()
async def on_bot_membership_changed(update: ChatMemberUpdated):
    # Foydalanuvchi botni bloklagan yoki shaxsiy suhbatni tark etgan bo'lsa —
    # is_active ni False qilib qo'yamiz. Keyinroq foydalanuvchi botga qayta
    # yozganda UserCheckMiddleware buni avtomatik "qaytib keldi" deb belgilaydi
    # (is_active=True, returned_at=hozirgi vaqt).
    if update.chat.type != "private":
        return

    if update.new_chat_member.status in ("kicked", "left"):
        await Users.filter(chat_id=update.from_user.id).update(is_active=False)
