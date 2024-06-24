import psycopg2
from datetime import datetime
from psycopg2 import extras


def open_connection_db(database_url):
    conn = psycopg2.connect(database_url)
    cur = conn.cursor(cursor_factory=extras.DictCursor)
    return conn, cur


def select_query(query, cur, all_matched=True):
    cur.execute(*query) if isinstance(query, tuple) else cur.execute(query)
    return cur.fetchall() if all_matched else cur.fetchone()


def insert_query(query, cur, table):
    cur.execute(*query)
    cur.execute(f'SELECT id FROM {table} ORDER BY id DESC LIMIT 1;')
    return cur.fetchone()[0]


def close_connection_db(conn, cur):
    conn.close()
    cur.close()


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
    return select_query(query, cur)


def get_url_from_urls_by_id(cur, search: int):
    query = """
                        SELECT *
                        FROM urls
                        WHERE id = %s
                        """, (search,)
    return select_query(query, cur, all_matched=False)


def get_url_from_urls_by_name(cur, name: str):
    query = """
                        SELECT *
                        FROM urls
                        WHERE name = %s
                        """, (name,)
    return select_query(query, cur, all_matched=False)


def insert_url(cur, url: str):
    query = """
                        INSERT INTO urls (
                            name,
                            created_at
                        )
                        VALUES (%s, %s);
                        """, (url, datetime.now())
    insert_query(query, cur, 'urls')


def get_url_checks(cur, url_id: int):
    query = """
                    SELECT *
                    FROM url_checks
                    WHERE url_id = %s
                    ORDER BY id DESC;""", (url_id,)
    return select_query(query, cur)


def insert_check(cur, url_check: dict):
    query = """
                    INSERT INTO url_checks
                    (url_id, h1, title, status_code, description, created_at)
                    VALUES
                    (%s, %s, %s, %s, %s, %s);
                    """, (url_check['url_id'],
                          url_check['h1'],
                          url_check['title'],
                          url_check['status_code'],
                          url_check['description'],
                          datetime.now())
    insert_query(query, cur, 'url_checks')
