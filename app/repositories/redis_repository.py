import logging
from typing import Any

from core.config import settings
from redis.asyncio import Redis
from repositories.base import BaseRepository

logger = logging.getLogger(__name__)

LIFETIME = settings.redis.ttl_redis


class RedisRepository(BaseRepository):
    _instance: 'RedisRepository | None' = None

    def __init__(
        self,
        redis_client: Redis,
    ) -> None:
        self.redis_client = redis_client

    async def get(
        self,
        key: str,
    ) -> bytes | None:
        return await self.redis_client.get(name=str(key))

    async def set(
        self,
        key: str,
        value: str,
    ) -> None:
        await self.redis_client.set(key, value, ex=LIFETIME)

    @classmethod
    def create_singleton(
        cls,
        **kw: Any,
    ) -> 'RedisRepository':
        if cls._instance is None:
            cls._instance = cls(redis_client=kw.pop('redis_client'))
        return cls._instance

    def close_connection(self) -> None:
        self.redis_client.close()
