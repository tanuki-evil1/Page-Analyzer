install:
	poetry install

dev:
	poetry run flask --app page_analyzer:app --debug run

PORT ?= 3000
start:
	poetry run gunicorn -w 5 -b 127.0.0.1:$(PORT) page_analyzer:app

lint:
	poetry run flake8

build:
	./build.sh