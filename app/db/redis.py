import redis.asyncio as redis

from app.core.config import settings

JTI_EXPIRY = 3600

token_blacklist = redis.from_url(settings.REDIS_URL)


async def add_jti_to_blacklist(jti: str) -> None:
    await token_blacklist.set(name=jti, value="", ex=JTI_EXPIRY)


async def token_in_blacklist(jti: str) -> bool:
    jti = await token_blacklist.get(jti)

    return jti is not None
