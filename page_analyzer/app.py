import psycopg2
import requests
from psycopg2 import extras
import os
import validators
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
from dotenv import load_dotenv
from urllib.parse import urlparse
from bs4 import BeautifulSoup

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.get('/urls')
def get_urls():
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=extras.DictCursor) as cur:
            cur.execute('SELECT urls.id, name, url_checks.created_at, url_checks.status_code FROM urls INNER JOIN url_checks ON urls.id = url_checks.url_id GROUP BY urls.id, name;')
            all_urls = cur.fetchall()
    return render_template('urls.html', urls=all_urls)


@app.post('/urls')
def post_urls():
    url = request.form.get('url')
    if validators.url(url):
        parsed_url = urlparse(url)
        normalized_url = f'{parsed_url.scheme}://{parsed_url.hostname}'
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s);', (normalized_url, datetime.now()))
                cur.execute('SELECT * FROM urls ORDER BY id DESC LIMIT 1;')
                url_id = cur.fetchone()[0]
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('get_url', url_id=url_id), 302)
    else:
        flash('Некорректный URL', 'danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', url=url, messages=messages)


@app.get('/urls/<int:url_id>')
def get_url(url_id):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=extras.DictCursor) as cur:
            cur.execute('SELECT * FROM urls WHERE id = %s;', (url_id,))
            url = cur.fetchone()
            cur.execute('SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC;', (url_id,))
            checks = cur.fetchall()
    messages = get_flashed_messages(with_categories=True)  # Сделать ли словарем
    return render_template('url.html', url=url, checks=checks, messages=messages)


@app.post('/urls/<url_id>/checks')
def post_url(url_id):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM urls WHERE id = %s;', (url_id,))
            url = cur.fetchone()[1]
            response = requests.get(url, allow_redirects=False)
            status_code = response.status_code
            cur.execute('INSERT INTO url_checks (url_id, status_code, created_at) VALUES (%s, %s, %s);',
                        (url_id, status_code, datetime.now()))
    return redirect(url_for('get_url', url_id=url_id), 302)
