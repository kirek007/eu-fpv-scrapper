# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import pymongo
from httplib2 import _wsse_username_token

from fpv_products import settings


# useful for handling different item types with a single interface



class fpv_productsPipeline:
    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings.MONGODB_SERVER)
        db = connection[settings.MONGODB_DB]
        self.collection = db[settings.MONGODB_COLLECTION]

    def process_item(self, item, spider):
        res = self.collection.update_one({'url': item["url"]}, {'$set': dict(item)}, upsert=True)
        return item
