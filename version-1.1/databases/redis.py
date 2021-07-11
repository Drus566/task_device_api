import aioredis
from config import * 

async def redis_connect():
    redis = await aioredis.from_url(REDIS_URL)
    return redis
