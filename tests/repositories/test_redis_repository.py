import phonenumbers
import pytest
from faker import Faker
from repositories.redis_repository import RedisRepository


class TestRedisRepository:
    @pytest.fixture
    def redis_key(
        self,
        faker: Faker,
    ) -> str:
        phone_obj = phonenumbers.parse(faker.phone_number(), 'RU')
        phone = phonenumbers.format_number(
            phone_obj,
            phonenumbers.PhoneNumberFormat.E164,
        )
        return phone

    @pytest.fixture
    def address(
        self,
        faker: Faker,
    ) -> str:
        return faker.address()

    @pytest.mark.asyncio
    async def test_get_wrong_key(
        self,
        redis_repo: RedisRepository,
        redis_key: str,
    ) -> None:
        result = await redis_repo.get(key=redis_key)

        assert result is None

    @pytest.mark.asyncio
    async def test_get_correct_key(
        self,
        redis_repo: RedisRepository,
        redis_key: str,
        address: str,
    ) -> None:
        await redis_repo.set(
            key=redis_key,
            value=address,
        )

        result = await redis_repo.get(
            key=redis_key,
        )

        assert result.decode() == address

    @pytest.mark.asyncio
    async def test_set(
        self,
        redis_repo: RedisRepository,
        redis_key: str,
        address: str,
    ):
        result = await redis_repo.set(
            key=redis_key,
            value=address,
        )

        address_in_db = await redis_repo.get(
            key=redis_key,
        )
        assert result is None
        assert address_in_db.decode() == address
