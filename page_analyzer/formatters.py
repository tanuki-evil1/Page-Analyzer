from urllib.parse import urlparse


def get_info_from_tag(tag):
    if tag.get('content'):
        return tag.get('content')
    else:
        return tag.get_text()


def format_data_for_db(string: str) -> str:
    if string is None:
        return ''
    elif len(string) > 255:
        return string[:252] + '...'
    else:
        return string


def normalize_url(url):
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.hostname}'
