from typing import Annotated

from core.config import settings
from core.logger import logger
from fastapi import Depends
from redis.asyncio import Redis
from repositories.redis_repository import RedisRepository
from services.address_service import AddressService
from starlette.requests import Request


def create_redis_client(
    *,
    host=settings.redis.redis_host,
    port=settings.redis.redis_port,
    db=settings.redis.redis_databases,
) -> Redis:
    redis = Redis(
        host=host,
        port=port,
        db=db,
    )
    return redis


def create_redis_repository(
    redis_client=create_redis_client(),
) -> RedisRepository:
    return RedisRepository.create_singleton(
        redis_client=redis_client,
    )


def create_redis_repository_dependency(_: Request):
    return create_redis_repository()


RedisRepositoryType = Annotated[
    RedisRepository,
    Depends(create_redis_repository_dependency),
]


def create_user_info_service(
    redis_repo: RedisRepositoryType,
) -> AddressService:
    return AddressService(
        redis_repo=redis_repo,
        logger=logger,
    )


UserDataService = Annotated[AddressService, Depends(create_user_info_service)]
