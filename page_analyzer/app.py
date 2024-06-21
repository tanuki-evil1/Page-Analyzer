import os
import validators
from dotenv import load_dotenv
from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   url_for,
                   flash,
                   get_flashed_messages)

from page_analyzer import db
from page_analyzer.formatters import normalize_url
from page_analyzer.parser import get_seo

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


@app.route('/')
def index():
    return render_template('index.html')


@app.get('/urls')
def get_urls():
    urls = db.get_all_urls(DATABASE_URL)
    return render_template('urls.html', urls=urls)


@app.post('/urls')
def post_urls():
    url = request.form.get('url')
    if not validators.url(url):
        flash('Некорректный URL', 'danger')
        flashed_messages = get_flashed_messages(with_categories=True)[0]
        msg = {'type': flashed_messages[0], 'msg': flashed_messages[1]}
        return render_template('index.html', url=url, messages=msg), 422

    normalized_url = normalize_url(url)
    fetched_url = db.get_url_from_urls(DATABASE_URL, normalized_url)

    if fetched_url:
        flash('Страница уже существует', 'info')
        return redirect(url_for('get_url', url_id=fetched_url['id']), 302)

    db.insert_url(DATABASE_URL, normalized_url)
    url_id = db.get_last_url_id(DATABASE_URL, fetched_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_url', url_id=url_id), 302)


@app.get('/urls/<int:url_id>')
def get_url(url_id: int):
    msg = get_flashed_messages(with_categories=True)
    msg = {'type': msg[0][0], 'msg': msg[0][1]} if msg else ''
    url = db.get_url_from_urls(DATABASE_URL, url_id)
    checks = db.get_url_checks(DATABASE_URL, url_id)
    return render_template('url.html', url=url, checks=checks, messages=msg)


@app.post('/urls/<int:url_id>/checks')
def post_url(url_id: int):
    url = db.get_url_from_urls(DATABASE_URL, url_id)['name']
    try:
        url_check = get_seo(url, url_id)
        flash('Страница успешно проверена', 'success')
        db.insert_check(DATABASE_URL, url_check=url_check)
    except ValueError:
        flash('Произошла ошибка при проверке', 'danger')

    return redirect(url_for('get_url', url_id=url_id), 302)
