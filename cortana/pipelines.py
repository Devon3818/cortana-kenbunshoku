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

        if spider.name == '5q':
			data = {
				'mh_id': item['mh_id'],
				'mh_index': item['mh_index'],
				'mh_chip': item['mh_chip'],
				'mh_src': item['mh_src'],
				'mh_page': item['mh_page'],
			}
			self.mhpost['chip'].insert_one(data)
        if item['nodata'] == 1:
            data = {
                'mh_id': item['mh_id'],
                'mh_name': item['mh_name'],
                'mh_dec': item['mh_dec'],
                'mh_cover': item['mh_cover'],
                'mh_year': item['mh_year'],
                'mh_area': item['mh_area'],
                'mh_type': item['mh_type'],
                'mh_author': item['mh_author'],
                'mh_alias': item['mh_alias'],
                'mh_last': item['mh_last'],
                'mh_status': item['mh_status'],
                'mh_letter': item['mh_letter'],
                'mh_update_time': item['mh_update_time'],
                'nodata': item['nodata']
            }
            print 'nodatamh'
            self.mhpost['mh'].insert_one(data)

        return item

    def close_spider(self, spider):
        self.client.close()
