import psycopg2
from psycopg2 import extras
import os
import validators
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
from dotenv import load_dotenv
from urllib.parse import urlparse

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
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM urls ORDER BY id DESC;')
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
    messages = get_flashed_messages(with_categories=True)
    return render_template('url.html', url=url, messages=messages)
