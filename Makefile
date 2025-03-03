up:
	docker compose up -d --build --force-recreate

down:
	docker compose down

test:
	pytest -rA --cov-report term-missing --cov=app --cov-report=xml --junitxml=junit.xml

lint:
	uv run pre-commit install
	uv run pre-commit run --all-files
