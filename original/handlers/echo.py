from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from data import strings
from keyboard import numbers_keyboard

router = Router()


@router.message(CommandStart(), StateFilter("*"))
async def start_handler(message: Message, state: FSMContext, user):
    await state.clear()
    await message.answer(strings.start)


@router.message(F.text, StateFilter("*"))
async def echo_handler(message: Message, user):
    await message.answer(
        strings.echo.format(text=message.text),
        reply_markup=numbers_keyboard(),
    )


@router.callback_query(F.data.startswith("num:"))
async def number_callback_handler(callback: CallbackQuery, user):
    number = callback.data.split(":", 1)[1]
    # RateLimitMiddleware sinovi uchun: bir necha marta ketma-ket bosilsa,
    # limitdan oshib "kutib turing" degan alert chiqishi kerak.
    await callback.answer(f"✅ Siz {number} tugmasini bosdingiz")
