from bs4 import BeautifulSoup
import requests
import json
import time


def timer(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        print(f'Func spend {time.time() - t1} seconds')
        return result

    return wrapper


@timer
def to_json(url):
    """parsing function of all data to json format"""

    urls = []
    for category in range(1, 6):
        for page in range(1, 5):
            cur_url = f'{url}index{category}_page_{page}.html'

            response = requests.get(url=cur_url)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'lxml')

            sale_buttons = soup.find_all('div', class_='sale_button')
            for x in sale_buttons:
                urls.append(url + x.find('a')['href'])

    result_json = []

    for cur_url in urls:
        response = requests.get(url=cur_url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')

        descr_dict = {}
        description = soup.find('ul', id='description').find_all('li')
        li_id = [x['id'] for x in description]
        for cur_id in li_id:
            descr_dict[cur_id] = soup.find('li', id=cur_id).text.split(':')[1].strip()

        cur_json = {
            'categories': cur_url.split('/')[4],
            'name': soup.find('p', id='p_header').text.strip(),
            'article': soup.find('p', class_='article').text.split(':')[1].strip(),
            'description': descr_dict,
            'count': soup.find('span', id='in_stock').text.split(':')[1].strip(),
            'price': soup.find('span', id='price').text,
            'old_price': soup.find('span', id='old_price').text,
            'link': cur_url
        }

        result_json.append(cur_json)
    with open('result.json', 'w', encoding='utf-8') as file:
            json.dump(result_json, file, indent=4, ensure_ascii=False)
    return 'Файл создан'


def main():
    url_to_json = 'https://parsinger.ru/html/'
    print(to_json(url_to_json))


if __name__ == '__main__':
    main()