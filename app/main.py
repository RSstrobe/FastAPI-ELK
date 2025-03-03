from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from api.v1.handlers import api_router
from core.config import settings
from core.logger import setup_root_logger
from deps import create_redis_repository
from elasticapm.contrib.starlette import ElasticAPM, make_apm_client
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

setup_root_logger()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis_repo = create_redis_repository()
    yield
    await redis_repo.close_connection()


def make_middleware() -> list[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        ),
        Middleware(
            ElasticAPM,
            client=make_apm_client(
                {
                    'SERVICE_NAME': 'address-app',
                    'SERVER_URL': 'http://apm-server:8200',
                    'ENVIRONMENT': 'dev',
                },
            ),
        ),
    ]
    return middleware


def create_app() -> FastAPI:
    app_ = FastAPI(
        title=settings.service_name,
        description='Address service',
        default_response_class=ORJSONResponse,
        version='0.0.1',
        lifespan=lifespan,
        middleware=make_middleware(),
    )
    app_.include_router(router=api_router)
    return app_


app = create_app()
