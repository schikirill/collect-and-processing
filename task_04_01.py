from lxml import html
from pymongo import MongoClient
import requests
from pprint import pprint
import time

client = MongoClient('127.0.0.1', 27017)
db = client['news_list']
yandex_news = db['yandex_news']


def yandex_news_observer():

    url = 'https://yandex.by/news/'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.4.727 Yowser/2.5 Safari/537.36'}

    time.sleep(2)
    response = requests.get(url, headers=header)
    print(response)
    dom = html.fromstring(response.text)
    news_list = []

    news_elements = dom.xpath('//div[contains(@class,"news-app__top")]/div')
    for element in news_elements:
        news = {
                'title': str(element.xpath('.//h2/a/text()')[0]).replace('\xa0', ' '),
                'url':  str(element.xpath(".//h2/a/@href")[0]),
                'source': str(element.xpath(".//span[@class='mg-card-source__source']/a/text()")[0]),
                'publication_date': str(element.xpath(".//span[@class='mg-card-source__time']/text()")[0])
                }
        news_list.append(news)

    return news_list


def news_to_db_save(args):
    num = 0
    for element in news_lists:
        if not yandex_news.find_one({'url': element['url']}):
            yandex_news.insert_one(element)
            num += 1

    print(f'Added {num} news')


news_lists = yandex_news_observer()

news_to_db_save(news_lists)