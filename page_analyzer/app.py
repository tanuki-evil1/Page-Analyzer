import psycopg2
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
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
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s);', (url, datetime.now()))
            cur.execute('SELECT * FROM urls ORDER BY id DESC LIMIT 1;')
            url_id = cur.fetchone()[0]
    return redirect(url_for('get_url', url_id=url_id), 302)


@app.get('/urls/<int:url_id>')
def get_url(url_id):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM urls WHERE id = %s;', (url_id,))
            url = cur.fetchone()
    url_id, name, created_at = url
    return render_template('url.html', id=url_id, name=name, created_at=created_at)
