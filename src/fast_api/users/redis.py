import redis.asyncio as redis
from fast_api.config import config
from fast_api import config as c_module

JTI_EXPIRY = 3600  # seconds

# Create a global async Redis client

token_blacklist_redis = redis.from_url(c_module.broker_url, decode_responses=True)


async def add_token_to_blacklist(jti: str) -> None:
    """Blacklist a token by storing its JTI with expiry"""
    await token_blacklist_redis.setex(jti, JTI_EXPIRY, "true")


async def is_token_blacklisted(jti: str) -> bool:
    """Check if JTI exists in Redis (means token is blacklisted)"""
    result = await token_blacklist_redis.get(jti)
    return result is not None
