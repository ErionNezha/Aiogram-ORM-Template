from tortoise import Tortoise

from data.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


async def init():
    await Tortoise.init(
        db_url=f"asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        modules={"models": ["models.models"]},
        _enable_global_fallback=True,
    )
    await Tortoise.generate_schemas()
