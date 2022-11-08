# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FpvItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    shop = scrapy.Field()
    name = scrapy.Field()
    can_buy = scrapy.Field()
    category = scrapy.Field()
    category_id = scrapy.Field()
    producer = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()

    pass
