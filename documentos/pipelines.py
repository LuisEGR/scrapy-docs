# -*- coding: utf-8 -*-
import json
import datetime
import sys
import traceback
import pymongo
from scrapy.settings import Settings

class MongoDBPipeline(object):
    collection_name = 'scrapy_docs'

    def __init__(self, mongo_host, mongo_port, mongo_db):
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_host=crawler.settings.get('MONGODB_SERVER'),
            mongo_port=crawler.settings.get('MONGODB_PORT'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_host, self.mongo_port)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        exist = self.db[self.collection_name].find(
            {'MD5': item['MD5']}).count() > 0
        print("Existente:" + str(exist))
        if not exist:            
            self.db[self.collection_name].insert_one(dict(item))
        return item
