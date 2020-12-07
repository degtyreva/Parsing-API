# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import scrapy
from scrapy.pipelines.images import ImagesPipeline

class InstaparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.instagram

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one({'user_id': item['user_id'], 'username': item['username'], 'account': item['account'],
                               'type': item['type'], 'photo': item['photo']})
        # print(item)
        return item

class InstaparserPhotoPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photo']:
            try:
                yield scrapy.Request(item['photo'])
            except Exception as e:
                print(e)
        return item

    def file_path(self, requests, response=None, info=None, *, item=None):
        return f"{item['account']}/{item['username']}.jpg"

