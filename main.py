from bs4 import BeautifulSoup
import requests
import time
from fake_useragent import UserAgent


def timer(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        print(f'Func spend {time.time() - t1} seconds')
        return result
    return wrapper


@timer
def parse(url):
    """parsing function of all data"""

    ua = UserAgent()
    fake_ua = {'user-agent': ua.random}
    response = requests.get(url=url, headers=fake_ua)
    response.encoding = 'utf-8'
    print('Status code is: ', response.status_code)
    soup = BeautifulSoup(response.text, 'lxml')

    div = soup.find_all('div', class_='speciality-full')
    res = [line.text for line in div]

    with open('res_file.txt', 'w') as res_file:
        res_file.write('\n'.join(res))

    return 'Выполнено!'


def main():
    url_to_json = 'https://vuzoteka.ru/%D0%B2%D1%83%D0%B7%D1%8B/%D1%81%D0%BF%D0%B5%D1%86%D0%B8%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D1%81%D1%82%D0%B8'
    print(parse(url_to_json))


if __name__ == '__main__':
    main()