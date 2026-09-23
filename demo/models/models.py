from tortoise import fields
from tortoise.models import Model


class Users(Model):
    id = fields.IntField(pk=True)
    chat_id = fields.BigIntField(unique=True)  # Telegram user/chat ID (32-bitdan katta bo'lishi mumkin)

    is_premium = fields.BooleanField(default=False)  # Telegram'ning o'z premium obunasi bor-yo'qligi
    is_active = fields.BooleanField(default=True)  # bot bilan faol ishlatayaptimi (bloklamagan/tark etmagan)
    banned = fields.BooleanField(default=False)  # admin tomonidan taqiqlanganmi

    lasted_at = fields.DatetimeField(auto_now_add=True)  # oxirgi marta botdan foydalangan sana (kuniga 1 marta yangilanadi)
    returned_at = fields.DatetimeField(null=True)  # nofaol bo'lib qolgandan keyin qaytib kelgan vaqt

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "users"
        indexes = ["chat_id"]
