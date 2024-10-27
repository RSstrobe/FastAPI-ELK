up:
	docker compose up -d --build --force-recreate

down:
	docker compose down

lint:
	uv run pre-commit install
	uv run pre-commit run --all-files
