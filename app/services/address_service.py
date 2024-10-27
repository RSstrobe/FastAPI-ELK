import logging

from api.v1.exceptions import NumberDoesNotExist, NumberIsAlreadyExist
from repositories.base import BaseRepository
from schemas.user_info import UserInfoSchema


class AddressService:
    def __init__(
        self,
        redis_repo: BaseRepository,
        logger: logging.Logger,
    ) -> None:
        self.redis_repo = redis_repo
        self.logger = logger

    async def get_address(
        self,
        phone_number: str,
        *,
        raise_if_not_exists: bool = True,
    ) -> str:
        self.logger.info(f'[get_address] {phone_number=}')
        address = await self.redis_repo.get(phone_number)

        if address is None and raise_if_not_exists:
            raise NumberDoesNotExist(phone_number)

        if address is not None:
            address = address.decode()

        self.logger.info(f'[get_address] {address=}')
        return address

    async def get_data(
        self,
        phone_number: str,
    ) -> str:
        address = await self.get_address(phone_number)
        return address

    async def change_data(
        self,
        dto: UserInfoSchema,
    ):
        self.logger.info(f'[change_data] {dto=}')
        await self.get_address(dto.phone)
        await self.redis_repo.set(dto.phone, dto.address)

    async def write_data(
        self,
        dto: UserInfoSchema,
    ) -> None:
        self.logger.info(f'[write_data] {dto=}')
        address = await self.get_address(
            phone_number=dto.phone,
            raise_if_not_exists=False,
        )

        if address is not None:
            raise NumberIsAlreadyExist(dto.phone)

        await self.redis_repo.set(dto.phone, dto.address)
