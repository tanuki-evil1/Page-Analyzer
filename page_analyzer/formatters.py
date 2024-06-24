import validators
from urllib.parse import urlparse


def validate_url(url: str) -> bool:
    return validators.url(url)


def get_info_from_tag(tag):
    if tag:
        if tag.get('content'):
            return tag.get('content')
        else:
            return tag.get_text()
    return tag


def format_data_for_db(string: str or None) -> str or None:
    if string is None:
        return ''
    elif string and len(string) > 255:
        return string[:252] + '...'
    else:
        return string




def normalize_url(url: str) -> str:
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.hostname}'
