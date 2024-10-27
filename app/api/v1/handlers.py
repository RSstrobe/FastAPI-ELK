from deps import UserDataService
from fastapi import APIRouter, Query, status
from schemas.user_info import PhoneDataSchema, UserInfoSchema

api_router = APIRouter(prefix='/address', tags=['Address'])


@api_router.post(
    path='',
    status_code=status.HTTP_201_CREATED,
    description='Записать информацию и номере и адресе',
    summary='Записать информацию и номере и адресе',
    response_model=PhoneDataSchema,
)
async def write_data(
    service: UserDataService,
    request: UserInfoSchema = UserInfoSchema,
):
    await service.write_data(request)
    return PhoneDataSchema(phone=request.phone)


@api_router.patch(
    path='',
    status_code=status.HTTP_200_OK,
    description='Изменить информацию и номере и адресе',
    summary='Изменить информацию и номере и адресе',
    response_model=UserInfoSchema,
)
async def change_data(
    service: UserDataService,
    request: UserInfoSchema = UserInfoSchema,
):
    await service.change_data(request)
    return request


@api_router.get(
    path='',
    status_code=status.HTTP_200_OK,
    description='Получить сведения о адресе',
    summary='Получить сведения о адресе',
    response_model=UserInfoSchema,
)
async def get_data(
    service: UserDataService,
    phone: str = Query(description='Номер телефона'),
):
    address = await service.get_data(phone)
    return UserInfoSchema(
        phone=phone,
        address=address,
    )
