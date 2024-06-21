import requests
from bs4 import BeautifulSoup
from page_analyzer.formatters import format_data_for_db, get_info_from_tag


def get_seo(url, url_id):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        status_code = response.status_code
        title = format_data_for_db(get_info_from_tag(soup.find('title')))
        description = format_data_for_db(get_info_from_tag(soup.find(
            'meta', attrs={'name': 'description'})))
        h1 = format_data_for_db(get_info_from_tag(soup.find('h1')))
        return {'status_code': status_code,
                'title': title,
                'description': description,
                'h1': h1,
                'url_id': url_id}
    except requests.exceptions.RequestException:
        raise ValueError('Произошла ошибка при проверке')
