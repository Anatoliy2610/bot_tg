install:
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt

run:
	uvicorn app.main:app --reload

bot:
	python3 bot.py

migrate:
	alembic revision --autogenerate -m "Initial migration"

check:
	ruff check

format:
	ruff format
