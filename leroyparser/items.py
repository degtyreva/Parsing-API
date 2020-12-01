# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
# https://res.cloudinary.com/lmru/image/upload/f_auto,q_90,w_2000,h_2000,c_pad,b_white,d_photoiscoming.png/LMCode/82053121_i_01.jpg большая
# https://res.cloudinary.com/lmru/image/upload/f_auto,q_90,w_82,h_82,c_pad,b_white,d_photoiscoming.png/LMCode/82053121_i_01.jpg маленькая
def change_photo_url(url):
    if url:
        url = url.replace('w_82,h_82', 'w_2000,h_2000')

    return url


class LeroyparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(change_photo_url))
    link = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    unit = scrapy.Field(output_processor=TakeFirst())
    # features = scrapy.Field()
