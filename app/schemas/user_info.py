from pydantic import Field
from pydantic_extra_types.phone_numbers import PhoneNumber
from schemas.base import Base


class PhoneNumberType(PhoneNumber):
    phone_format = 'E164'
    min_length = 11
    default_region_code = 'RU'


class PhoneDataSchema(Base):
    phone: str = Field(description='Номер телефона')


class AddressDataSchema(Base):
    address: str = Field(min_length=1, max_length=255, description='Адрес')


class UserInfoSchema(AddressDataSchema, PhoneDataSchema): ...
