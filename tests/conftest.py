import asyncio
import logging

import pytest
import pytest_asyncio
from faker import Faker
from redis.asyncio import Redis
from repositories.redis_repository import RedisRepository
from services.address_service import AddressService
from testcontainers.redis import AsyncRedisContainer


@pytest.fixture(scope='session', autouse=True)
def redis_container() -> AsyncRedisContainer:
    container = AsyncRedisContainer(
        image='redis:7.2.5',
    )
    container.start()
    yield container
    container.stop()


@pytest_asyncio.fixture(scope='session', autouse=True)
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def redis_client(redis_container: AsyncRedisContainer) -> Redis:
    client = await redis_container.get_async_client()
    yield client
    await client.close()


@pytest.fixture(scope='session')
def redis_repo(redis_client: Redis) -> RedisRepository:
    repo = RedisRepository(
        redis_client=redis_client,
    )
    return repo


@pytest.fixture(scope='session')
def address_service(redis_repo: RedisRepository) -> AddressService:
    service = AddressService(
        redis_repo=redis_repo,
        logger=logging.getLogger(''),
    )
    return service


@pytest.fixture(scope='session')
def faker() -> Faker:
    Faker.seed(0)
    fake = Faker(locale='ru_RU')
    return fake
