import asyncio
import logging
import sys

from handlers import register_all_routes
from loader import dp, bot, storage
from middleware import UserCheckMiddleware
from misc.bot_commands import set_commands
from models import init
from throttling import RateLimitMiddleware


async def main():
    await init.init()

    register_all_routes(dp)

    # RateLimitMiddleware bitta instance sifatida yaratiladi va HAM message,
    # HAM callback_query'ga OUTER sifatida ulanadi — shunda foydalanuvchining
    # xabar yuborishi va tugma bosishi birgalikda bitta limitga hisoblanadi
    # (aks holda xabar bilan bloklangan spamer tugma bosishga o'tib
    # limitni aylanib o'tishi mumkin edi). OUTER bo'lgani uchun handler
    # filtridan o'tish-o'tmasligidan qat'iy nazar har doim ishlaydi va
    # UserCheckMiddleware'dan (INNER) oldin ishga tushadi.
    rate_limiter = RateLimitMiddleware(cooldown=3)
    dp.message.outer_middleware(rate_limiter)
    dp.callback_query.outer_middleware(rate_limiter)

    dp.message.middleware(UserCheckMiddleware())
    dp.callback_query.middleware(UserCheckMiddleware())
    dp.my_chat_member.middleware(UserCheckMiddleware())
    dp.chat_member.middleware(UserCheckMiddleware())
    await set_commands(bot)

    try:
        # Webhookni o‘chirish va pollingni boshlash
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(
            bot,
            allowed_updates=['message', 'my_chat_member', 'chat_member', 'callback_query',
                             'edited_message', 'poll', 'channel_post', 'pre_checkout_query']
        )
    except Exception as e:
        logging.error(f"Pollingda xatolik: {e}")
    finally:
        # Botni to‘xtatganda resurslarni tozalash
        await storage.close()
        await bot.session.close()
        logging.info("Bot sessiyasi yopildi.")


if __name__ == '__main__':
    try:
        # Logging sozlamalari
        logging.basicConfig(
            level=logging.INFO,
            stream=sys.stdout,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info('Bot foydalanuvchi tomonidan to‘xtatildi.')
    except Exception as e:
        logging.error(f"Boshlashda xatolik: {e}")
