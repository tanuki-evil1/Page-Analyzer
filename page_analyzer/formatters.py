import bs4


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
