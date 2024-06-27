import psycopg2
from datetime import datetime
from psycopg2 import extras


def open_connection_db(database_url: str):
    return psycopg2.connect(database_url)


def insert_query(cur, table: str, query: str, params=tuple()) -> str:
    cur.execute(query, params)
    cur.execute(f'SELECT id FROM {table} ORDER BY id DESC LIMIT 1;')
    return cur.fetchone()[0]


def close_connection_db(conn) -> None:
    conn.close()


def get_all_urls(conn):
    query = """
            SELECT
                urls.id,
                urls.name
            FROM urls
            ORDER BY urls.id DESC;
            """

    with conn.cursor(cursor_factory=extras.DictCursor) as cur:
        cur.execute(query)
        return cur.fetchall()


def get_all_checks(conn):
    query = """
            SELECT DISTINCT ON (url_id)
                url_id,
                created_at,
                status_code
            FROM url_checks
            ORDER BY url_id DESC;
            """
    with conn.cursor(cursor_factory=extras.DictCursor) as cur:
        cur.execute(query)
        return cur.fetchall()


def get_url_from_urls_by_id(conn, url_id: int):
    query = """
            SELECT *
            FROM urls
            WHERE id = %s;
            """
    with conn.cursor(cursor_factory=extras.DictCursor) as cur:
        cur.execute(query, (url_id,))
        return cur.fetchone()


def get_url_from_urls_by_name(conn, name: str):
    query = """
            SELECT *
            FROM urls
            WHERE name = %s;
            """
    with conn.cursor(cursor_factory=extras.DictCursor) as cur:
        cur.execute(query, (name,))
        return cur.fetchone()


def insert_url(conn, url: str) -> str:
    query = """
            INSERT INTO urls
            (name, created_at)
            VALUES
            (%s, %s);
            """
    with conn.cursor(cursor_factory=extras.DictCursor) as cur:
        cur.execute(query, (url, datetime.now()))
        conn.commit()
        cur.execute('SELECT id FROM urls ORDER BY id DESC LIMIT 1;')
        return cur.fetchone()[0]


def get_url_checks(conn, url_id: int):
    query = """
            SELECT *
            FROM url_checks
            WHERE url_id = %s
            ORDER BY id DESC;
            """
    with conn.cursor(cursor_factory=extras.DictCursor) as cur:
        cur.execute(query, (url_id,))
        return cur.fetchall()


def insert_check(conn, url_check: dict) -> str:
    query = """
            INSERT INTO url_checks
            (url_id, h1, title, status_code, description, created_at)
            VALUES
            (%s, %s, %s, %s, %s, %s);
            """
    params = (url_check['url_id'],
              url_check['h1'],
              url_check['title'],
              url_check['status_code'],
              url_check['description'],
              datetime.now())

    with conn.cursor(cursor_factory=extras.DictCursor) as cur:
        cur.execute(query, params)
        conn.commit()
        cur.execute('SELECT id FROM url_checks ORDER BY id DESC LIMIT 1;')
        return cur.fetchone()[0]
