.PHONY: install run test lint compose-up compose-down

install:
	pip install -r requirements-dev.txt

run:
	uvicorn app.main:app --reload

test:
	pytest

lint:
	ruff check .

compose-up:
	docker compose up --build

compose-down:
	docker compose down

