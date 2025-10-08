.PHONY: help install run test clean docker-up docker-down migrate

help:
	@echo "Available commands:"
	@echo "  make install     - Install dependencies"
	@echo "  make run         - Run development server"
	@echo "  make test        - Run tests"
	@echo "  make clean       - Clean generated files"
	@echo "  make docker-up   - Start Docker containers"
	@echo "  make docker-down - Stop Docker containers"
	@echo "  make migrate     - Run database migrations"
	@echo "  make format      - Format code with black"
	@echo "  make lint        - Lint code with ruff"

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest

test-cov:
	pytest --cov=app --cov-report=html --cov-report=term

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -f invoices.db

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

migrate:
	alembic upgrade head

migrate-create:
	alembic revision --autogenerate -m "$(msg)"

format:
	black app tests
	isort app tests

lint:
	ruff check app tests

db-init:
	python -c "from app.database import init_db; init_db()"

db-reset:
	rm -f invoices.db
	python -c "from app.database import init_db; init_db()"