# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from scrapy.conf import settings

class CortanaPipeline(object):

    def __init__(self):
        try:
            self.client = MongoClient(settings['MONGO_HOST'],settings['MONGO_PORT'])
            self.mhpost = self.client[settings['MONGO_DB']]
            self.mhpost.authenticate(settings['MONGO_USER'],settings['MONGO_PWD'])
            print("MonoDB connection established...")
        except Exception as e:
            print("An exception occurred when try to connect to MongoDB: "+str(e))

        
    def process_item(self, item, spider):
        return item

    def close_spider(self, spider):
        self.client.close()
