from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat, BotCommandScopeAllPrivateChats

from data.config import ADMINS


async def set_commands(bot: Bot) -> None:
    # Oddiy foydalanuvchilar uchun komandalar (shaxsiy suhbatlar uchun)
    private_commands = [
        BotCommand(command="start", description="Botni ishga tushurish"),

    ]

    await bot.delete_my_commands(scope=BotCommandScopeDefault())
    await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private_commands, scope=BotCommandScopeAllPrivateChats())

    # Adminlar uchun maxsus komandalarni o'rnatamiz (shaxsiy suhbatlar uchun)
    admin_commands = private_commands + [
        BotCommand(
            command="settings",
            description="👨🏻‍💻 Admin sozlamalari"
        ),

    ]

    for admin in ADMINS:
        try:
            await bot.delete_my_commands(scope=BotCommandScopeChat(chat_id=admin))
            await bot.set_my_commands(commands=admin_commands, scope=BotCommandScopeChat(chat_id=admin))
        except:
            pass
