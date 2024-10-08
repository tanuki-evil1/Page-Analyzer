install:
	poetry install

dev:
	poetry run flask --app page_analyzer:app --debug run

PORT ?= 8000
start:
	poetry run gunicorn -w 4 -b 0.0.0.0:$(PORT) page_analyzer:app

lint:
	poetry run flake8

build:
	./build.sh