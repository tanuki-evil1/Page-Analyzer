import psycopg2
from datetime import datetime
from psycopg2 import extras


def get_all_urls(database_url: str):
    with psycopg2.connect(database_url) as conn:
        with conn.cursor(cursor_factory=extras.DictCursor) as cur:
            cur.execute("""
            SELECT
                urls.id,
                urls.name,
                url_checks.created_at,
                url_checks.status_code
            FROM urls
            LEFT JOIN (
                SELECT DISTINCT ON (url_id)
                    url_id,
                    created_at,
                    status_code
                FROM url_checks
                ORDER BY url_id, created_at DESC
                    ) AS url_checks ON urls.id = url_checks.url_id
            ORDER BY urls.id DESC;
            """)
            return cur.fetchall()


def get_url_from_urls(database_url: str, search: int or str):
    with psycopg2.connect(database_url) as conn:
        with conn.cursor(cursor_factory=extras.DictCursor) as cur:
            if isinstance(search, int):
                cur.execute("""
                        SELECT *
                        FROM urls
                        WHERE id = %s
                        """, (search,))
            else:
                cur.execute("""
                        SELECT *
                        FROM urls
                        WHERE name = %s
                        """, (search,))
            return cur.fetchone()


def insert_url(database_url: str, url: str):
    with psycopg2.connect(database_url) as conn:
        with conn.cursor(cursor_factory=extras.DictCursor) as cur:
            cur.execute("""
                        INSERT INTO urls (
                            name,
                            created_at
                        )
                        VALUES (%s, %s);
                        """, (url, datetime.now()))
            cur.execute('SELECT id FROM urls ORDER BY id DESC LIMIT 1;')
            return cur.fetchone()[0]


def get_url_checks(database_url: str, url_id: int):
    with psycopg2.connect(database_url) as conn:
        with conn.cursor(cursor_factory=extras.DictCursor) as cur:
            cur.execute('SELECT * '
                        'FROM url_checks '
                        'WHERE url_id = %s '
                        'ORDER BY id DESC;',
                        (url_id,))
            return cur.fetchall()


def insert_check(database_url: str, url_check: dict):
    with psycopg2.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                    INSERT INTO url_checks
                    (url_id, h1, title, status_code, description, created_at)
                    VALUES
                    (%s, %s, %s, %s, %s, %s);
                    """, (url_check['url_id'],
                          url_check['h1'],
                          url_check['title'],
                          url_check['status_code'],
                          url_check['description'],
                          datetime.now()))
