import psycopg2
from datetime import datetime
from psycopg2 import extras


def open_connection_db(database_url: str):
    conn = psycopg2.connect(database_url)
    cur = conn.cursor(cursor_factory=extras.DictCursor)
    return conn, cur


def select_query(cur, query: str, params: tuple = (), all_matched=True):
    cur.execute(query, params)
    return cur.fetchall() if all_matched else cur.fetchone()


def insert_query(cur, table: str, query: str, params: tuple = ()) -> str:
    cur.execute(query, params)
    cur.execute(f'SELECT id FROM {table} ORDER BY id DESC LIMIT 1;')
    return cur.fetchone()[0]


def close_connection_db(cur, conn) -> None:
    conn.commit()
    cur.close()
    conn.close()


def get_all_urls(cur):
    query = """
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
            """
    return select_query(cur, query)


def get_url_from_urls_by_id(cur, search: int):
    query = """
            SELECT *
            FROM urls
            HERE id = %s;
            """
    return select_query(cur, query, params=(search,), all_matched=False)


def get_url_from_urls_by_name(cur, name: str):
    query = """
            SELECT *
            FROM urls
            WHERE name = %s;
            """
    return select_query(cur, query, params=(name,), all_matched=False)


def insert_url(cur, url: str) -> str:
    query = """
            INSERT INTO urls 
            (name, created_at)
            VALUES 
            (%s, %s);
            """
    return insert_query(cur, 'urls', query, params=(url, datetime.now()))


def get_url_checks(cur, url_id: int):
    query = """
            SELECT *
            FROM url_checks
            WHERE url_id = %s
            ORDER BY id DESC;
            """
    return select_query(cur, query, params=(url_id,))


def insert_check(cur, url_check: dict) -> str:
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
    return insert_query(cur, 'url_checks', query, params=params)
