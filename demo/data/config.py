from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS", subcast=int, default=[])

DB_HOST = env.str("DB_HOST", "localhost")
DB_PORT = env.int("DB_PORT", 5432)
DB_USER = env.str("DB_USER")
DB_PASSWORD = env.str("DB_PASSWORD")
DB_NAME = env.str("DB_NAME")

REDIS_URL = env.str("REDIS_URL", "redis://localhost:6379/0")
