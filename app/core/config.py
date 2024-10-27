import os

from pydantic import Field
from pydantic_settings import BaseSettings


class _BaseSettings(BaseSettings):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = 'ignore'


class CommonSettings(_BaseSettings):
    service_name: str = Field(
        default='Address service',
        description='Название сервиса авторизации',
    )
    base_dir: str = Field(
        default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        description='Корень проекта',
    )
    debug_mode: bool = Field(
        default=False,
        description='Режим отладки сервиса авторизации',
    )


class RedisSettings(_BaseSettings):  # TODO: redisDSN
    redis_host: str = Field(
        description='Адрес хоста Redis для модуля авторизации',
    )
    redis_port: int = Field(
        description='Порт Redis для сервиса авторизации',
    )
    redis_databases: str = Field(
        description='База данных для хранения токенов',
    )
    redis_password: str = Field(
        description='Пароль от Redis',
    )
    ttl_redis: int = Field(
        description='Время хранения токенов',
    )


class BackendSettings(_BaseSettings):
    backend_host: str = Field(
        default='app',
        description='Адрес хоста',
    )
    backend_port: int = Field(
        default=8000,
        description='Порт сервиса',
    )


class Settings(CommonSettings):
    redis: RedisSettings = RedisSettings()
    backend: BackendSettings = BackendSettings()


settings = Settings()
