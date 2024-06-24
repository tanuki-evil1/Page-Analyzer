import os
from dotenv import load_dotenv
from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   url_for,
                   flash,
                   get_flashed_messages)

from page_analyzer import db
from page_analyzer.formatters import normalize_url, validate_url
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
    conn, cur = db.open_connection_db(DATABASE_URL)
    urls = db.get_all_urls(cur)
    all_checks = db.get_all_checks(cur)
    db.close_connection_db(conn, cur)

    urls_join_check = []
    for url in urls:
        urls_join_check.append({'id': url['id'], 'name': url['name']})
        for check in all_checks:
            if url['id'] == check['url_id']:
                urls_join_check[-1].update({'created_at': check['created_at'],
                                            'status_code': check['status_code']})
                break
    return render_template('urls.html', urls=urls_join_check)


@app.post('/urls')
def post_urls():
    url = request.form.get('url')
    if not validate_url(url):
        msg = {'type': 'danger', 'msg': 'Некорректный URL'}
        return render_template('index.html', url=url, messages=msg), 422

    normalized_url = normalize_url(url)
    conn, cur = db.open_connection_db(DATABASE_URL)
    fetched_url = db.get_url_from_urls_by_name(cur, normalized_url)
    db.close_connection_db(conn, cur)

    if fetched_url:
        flash('Страница уже существует', 'info')
        return redirect(url_for('get_url', url_id=fetched_url['id']), 302)

    conn, cur = db.open_connection_db(DATABASE_URL)
    url_id = db.insert_url(cur, normalized_url)
    conn.commit()
    db.close_connection_db(conn, cur)

    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_url', url_id=url_id), 302)


@app.get('/urls/<int:url_id>')
def get_url(url_id: int):
    msg = get_flashed_messages(with_categories=True)
    msg = {'type': msg[0][0], 'msg': msg[0][1]} if msg else ''

    conn, cur = db.open_connection_db(DATABASE_URL)
    url = db.get_url_from_urls_by_id(cur, url_id)
    db.close_connection_db(conn, cur)

    if not url:
        return render_template('404.html'), 404

    conn, cur = db.open_connection_db(DATABASE_URL)
    checks = db.get_url_checks(cur, url_id)
    db.close_connection_db(conn, cur)

    return render_template('url.html', url=url, checks=checks, messages=msg)


@app.post('/urls/<int:url_id>/checks')
def post_url(url_id: int):
    conn, cur = db.open_connection_db(DATABASE_URL)
    url = db.get_url_from_urls_by_id(cur, url_id)['name']
    db.close_connection_db(conn, cur)

    if not url:
        return render_template('404.html'), 404

    try:
        url_check = get_seo(url, url_id)
        flash('Страница успешно проверена', 'success')
        conn, cur = db.open_connection_db(DATABASE_URL)
        db.insert_check(cur, url_check)
        conn.commit()
        db.close_connection_db(conn, cur)
    except ValueError:
        flash('Произошла ошибка при проверке', 'danger')

    return redirect(url_for('get_url', url_id=url_id), 302)


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404
