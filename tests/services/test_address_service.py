from contextlib import nullcontext as does_not_raise

import phonenumbers
import pytest
from api.v1.exceptions import NumberDoesNotExist, NumberIsAlreadyExist
from faker import Faker
from repositories.redis_repository import RedisRepository
from schemas.user_info import UserInfoSchema
from services.address_service import AddressService


class TestAddressService:
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

    @pytest.mark.parametrize(
        ('raise_if_not_exists', 'expected_exception'),
        [
            (False, does_not_raise()),
            (True, pytest.raises(NumberDoesNotExist)),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_address_not_exist_key(
        self,
        address_service: AddressService,
        redis_key: str,
        raise_if_not_exists: bool,
        expected_exception,
    ) -> None:
        with expected_exception:
            result = await address_service.get_address(
                phone_number=redis_key,
                raise_if_not_exists=raise_if_not_exists,
            )

            assert result is None

    @pytest.mark.asyncio
    async def test_get_address_success(
        self,
        address_service: AddressService,
        redis_repo: RedisRepository,
        redis_key: str,
        address: str,
    ) -> None:
        await redis_repo.set(
            key=redis_key,
            value=address,
        )

        result = await address_service.get_address(
            phone_number=redis_key,
        )

        assert result == address

    @pytest.mark.asyncio
    async def test_write_data_success(
        self,
        address_service: AddressService,
        redis_repo: RedisRepository,
        redis_key: str,
        address: str,
    ) -> None:
        result = await address_service.write_data(
            dto=UserInfoSchema(
                phone=redis_key,
                address=address,
            ),
        )

        address_in_db = await redis_repo.get(
            key=redis_key,
        )
        assert result is None
        assert address_in_db.decode() == address

    @pytest.mark.asyncio
    async def test_write_data_with_exist_key(
        self,
        address_service: AddressService,
        redis_repo: RedisRepository,
        redis_key: str,
        address: str,
    ) -> None:
        await redis_repo.set(
            key=redis_key,
            value=address,
        )

        with pytest.raises(NumberIsAlreadyExist):
            await address_service.write_data(
                dto=UserInfoSchema(
                    phone=redis_key,
                    address=address,
                ),
            )

    @pytest.mark.asyncio
    async def test_change_data_not_exist_key(
        self,
        address_service: AddressService,
        redis_key: str,
        address: str,
    ) -> None:
        with pytest.raises(NumberDoesNotExist):
            await address_service.change_data(
                dto=UserInfoSchema(
                    phone=redis_key,
                    address=address,
                ),
            )

    @pytest.mark.asyncio
    async def test_change_data_success(
        self,
        address_service: AddressService,
        redis_repo: RedisRepository,
        redis_key: str,
        address: str,
    ) -> None:
        new_address = 'new_address'
        await redis_repo.set(
            key=redis_key,
            value=address,
        )

        result = await address_service.change_data(
            dto=UserInfoSchema(
                phone=redis_key,
                address=new_address,
            ),
        )

        address_in_db = await redis_repo.get(
            key=redis_key,
        )
        assert result is None
        assert address_in_db.decode() == new_address
