from redis import asyncio as aioredis
from environs import Env

env = Env()
REDIS_URL = env("REDIS_URL", "redis://hippopotamus-redis")

redis = aioredis.from_url(REDIS_URL, decode_responses=True)

async def get_last_tap_amount(user_id: int) -> int:
    value = await redis.get(f"tap_hippo:{user_id}")
    return int(value) if value else 0

async def set_last_tap_amount(user_id: int, amount: int):
    await redis.set(f"tap_hippo:{user_id}", str(amount))

async def increment_cheat_counter(user_id: int) -> int:
    key = f"cheat_counter:{user_id}"
    value = await redis.incr(key)
    return int(value)

async def get_cheat_counter(user_id: int) -> int:
    key = f"cheat_counter:{user_id}"
    value = await redis.get(key)
    return int(value) if value else 0

async def increment_cheat_counter(user_id: int) -> int:
    key = f"cheat_counter:{user_id}"
    return await redis.incr(key)

async def reset_cheat_counter(user_id: int):
    key = f"cheat_counter:{user_id}"
    await redis.delete(key)

async def is_user_cheater(user_id: int) -> bool:
    """
    Проверяет, является ли пользователь читером на основе счетчика в Redis
    """
    cheat_count = await get_cheat_counter(user_id)
    return cheat_count >= 5  # Считаем читером после 5 нарушений