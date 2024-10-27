import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Base(BaseModel):
    class Config:
        model_dump_json = orjson.loads
        model_validate_json = orjson_dumps
        strict = True
