from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time

from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['mvideo']
collection_mvideo = db.collection_mvideo

main_link = 'https://mvideo.ru/'

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(options=chrome_options)
driver.get(main_link)

n = 0
while n <= 3:
    time.sleep(3)
    button = driver.find_element_by_xpath("//a[@class='next-btn c-btn c-btn_scroll-horizontal c-btn_icon i-icon-fl-arrow-right']")
    button.click()
    n += 1

best_goods = driver.find_element_by_xpath("//div[text()[contains(.,'Хиты продаж')]]/../../../..")

goods = best_goods.find_elements_by_css_selector('li.gallery-list-item')

list = []

collection_mvideo.delete_many({})

for good in goods:
    item = {}
    info = good.find_element_by_css_selector('a.sel-product-tile-title').get_attribute('data-product-info')
    info_item = json.loads(info)
    good_name = info_item['productName']
    good_id = info_item['productId']
    good_price = info_item['productPriceLocal']
    good_link = good.find_element_by_css_selector('a.sel-product-tile-title').get_attribute('href')
    item['name'] = good_name
    item['_id'] = good_id
    item['price'] = good_price
    item['link'] = good_link
    list.append(item)
    collection_mvideo.insert_one({'_id': good_id, 'name': good_name, 'price': good_price, 'link': good_link})

for item in collection_mvideo.find({}):
    print(item)

