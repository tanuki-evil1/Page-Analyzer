from urllib.parse import urlparse

import bs4

from page_analyzer.db import get_url_from_urls


def format_data_for_db(string: str) -> str:
    if isinstance(string, bs4.element.Tag):
        if string.get('content'):
            string = string.get('content')
        else:
            string = string.get_text()

    if string is None:
        return ''
    elif len(string) > 255:
        return string[:252] + '...'
    else:
        return string


def normalize_url(url):
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.hostname}'
