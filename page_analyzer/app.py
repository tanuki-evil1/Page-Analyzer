import psycopg2
import os
from flask import Flask, render_template
from dotenv import load_dotenv

app = Flask(__name__)


@app.route('/')
def hello_world():
    load_dotenv()
    DATABASE_URL = os.getenv('DATABASE_URL')
    conn = psycopg2.connect(DATABASE_URL)
    return render_template('index.html')


@app.get('/urls')
def get_urls():
    pass


@app.get('/urls/<url_id>')
def get_url(url_id):
    pass
