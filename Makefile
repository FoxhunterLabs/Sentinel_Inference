.PHONY: dev test lint run docker

dev:
	bash scripts/run_dev.sh

run:
	python -m app.main

test:
	pytest

lint:
	python -m ruff check app tests

docker:
	docker build -t sentinel_inference:latest .
