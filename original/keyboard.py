from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder as kb


def numbers_keyboard():
    # RateLimitMiddleware'ni sinash uchun test tugmalari: 1 dan 5 gacha,
    # bittasi bir qatorda joylashadi.
    keyboard = kb()
    for number in range(1, 6):
        keyboard.add(InlineKeyboardButton(
            text=str(number),
            callback_data=f"num:{number}"))
    keyboard.adjust(5)
    return keyboard.as_markup()
