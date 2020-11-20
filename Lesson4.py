
# Написать приложение, которое собирает основные новости с сайтов
# Для парсинга использовать XPath. Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.
# Сложить собранные данные в БД

import requests

from lxml import html
from pprint import pprint
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
client = MongoClient('127.0.0.1', 27017)
db = client['news']
collection_news = db.collection_news


main_link = 'https://lenta.ru/'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
}
response = requests.get(main_link, headers=headers)
dom = html.fromstring(response.text)
lenta_news = dom.xpath("//div[contains(@class,'span8')]//div[contains(@class,'span4')]/div[contains(@class,'item')]")
for element in lenta_news:
    name = str(element.xpath(".//a/text()")).replace('xa0', ' ').replace("['", "").replace("']", "")
    link = str(element.xpath("./a/@href")).replace("['", "").replace("']", "")
    date = str(element.xpath("./a/time/@title")).replace("['", "").replace("']", "")
    source = 'lenta.ru'
    link = "https://lenta.ru" + link
    collection_news.insert_one({'news': name, 'link': link, 'date': date, 'source': source})


main_link2 = 'https://www.newkaliningrad.ru/'
response2 = requests.get(main_link2, headers=headers)
dom2 = html.fromstring(response2.text)
nk_news = dom2.xpath("//div[@class='row detail-list']//div[@class='publication-box']/h4")

# не знаю как вытянуть дату новости с соседней страницы, буду искать, пока подставлю текущую дату
from datetime import datetime
current_date = str(datetime.now().date())

for el in nk_news:

    name2 = str(el.xpath(".//a/text()")).replace("[", "").replace("]", "").replace("'", "")
    link2 = str(el.xpath("./a/@href")).replace("['", "").replace("']", "")
    link2 = 'https://www.newkaliningrad.ru' + link2
    source2 = 'https://www.newkaliningrad.ru/'
    collection_news.insert_one({'news': name2, 'link': link2, 'date': current_date, 'source': source2})



main_link3 = 'https://www.onliner.by/'
response3 = requests.get(main_link3, headers=headers)
dom3 = html.fromstring(response3.text)
onliner_news = dom3.xpath("//div[@class='b-tiles cfix ']//div[contains(@class,'b-tile m-1x1 m-info')]")


for el in onliner_news:

    name3 = str(el.xpath(".//span[@class='txt max-lines-4']/text()")).replace("[", "").replace("]", "").replace("'", "")
    link3 = str(el.xpath("./a[@class='b-tile-main']/@href")).replace("['", "").replace("']", "")
    link3 = 'https://www.onliner.by' + link3
    source3 = 'https://www.onliner.by'
    collection_news.insert_one({'news': name3, 'link': link3, 'date': current_date, 'source': source3})


for news in collection_news.find({}):
    print(news)