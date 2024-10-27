FROM python:3.11.9

WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

COPY uv.lock uv.lock
COPY pyproject.toml pyproject.toml

RUN apt-get update \
    && apt-get install --no-install-recommends -y build-essential libpq-dev gcc python3-dev musl-dev

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
ADD ./app /src/app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

ENV PATH="/src/app/.venv/bin:$PATH"
ENV PYTHONPATH=/src/app

# Run the application.
CMD ["/src/.venv/bin/fastapi", "run", "app/app.py", "--port", "80", "--host", "0.0.0.0"]
