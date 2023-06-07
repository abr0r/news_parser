import json

import requests
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}
url = 'https://qalampir.uz/uz/news/category/bu-qiziq'


def get_first_news():
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    news = soup.find_all('div', class_='col-lg-4 col-md-6')
    
    news_data = {}
    for i in news:
        news_text = i.find('p', class_='news-card-content-text').text.strip()
        news_link = f'https://qalampir.uz{i.find("a").get("href")}'
        news_date = i.find('span', class_='date').text.strip()

        news_id = news_link.split('/')[-1]
        id = news_id.split('-')[-1]

        news_data[id] = {
            'text': news_text,
            'link': news_link,
            'date': news_date
        }
    with open('news.json', 'w') as file:
        json.dump(news_data, file, indent=4, ensure_ascii=False)

def check_news_update():
    with open('news.json') as file:
        news_data = json.load(file)

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    news = soup.find_all('div', class_='col-lg-4 col-md-6')

    fresh_news = {}
    for i in news:
        news_link = f'https://qalampir.uz{i.find("a").get("href")}'

        news_id = news_link.split('/')[-1]
        id = news_id.split('-')[-1]

        if id in news_data:
            continue
        else:
            news_text = i.find('p', class_='news-card-content-text').text.strip()
            news_date = i.find('span', class_='date').text.strip()

            news_data[id] = {
                'text': news_text,
                'link': news_link,
                'date': news_date
            }
            fresh_news[id] = {
                'text': news_text,
                'link': news_link,
                'date': news_date
            }
    with open('news.json', 'w') as file:
        json.dump(news_data, file, indent=4, ensure_ascii=False)

    return fresh_news

def main():
    get_first_news()
    check_news_update()

if __name__ == '__main__':
    main()