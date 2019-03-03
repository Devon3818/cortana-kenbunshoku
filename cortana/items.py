# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CortanaItem(scrapy.Item):
    # define the fields for your item here like:
    mh_name = scrapy.Field()
    mh_cover = scrapy.Field()
    mh_id = scrapy.Field()
    mh_status = scrapy.Field()
    mh_year = scrapy.Field()
    mh_index = scrapy.Field()
    mh_type = scrapy.Field()
    mh_author = scrapy.Field()
    mh_score = scrapy.Field()
    mh_lately = scrapy.Field()
    mh_chip = scrapy.Field()
    mh_dec = scrapy.Field()
    mh_chapter = scrapy.Field()
    mh_area = scrapy.Field()
    nodata = scrapy.Field()



class ChipItem(scrapy.Item):
    mh_id = scrapy.Field()
    mh_index = scrapy.Field()
    mh_chip = scrapy.Field()
    mh_src = scrapy.Field()
    mh_page = scrapy.Field()

    mh_name = scrapy.Field()
    mh_dec = scrapy.Field()
    mh_cover = scrapy.Field()
    mh_year = scrapy.Field()
    mh_area = scrapy.Field()
    mh_type = scrapy.Field()
    mh_author = scrapy.Field()
    mh_alias = scrapy.Field()
    mh_last = scrapy.Field()
    mh_status = scrapy.Field()
    mh_letter = scrapy.Field()
    mh_update_time = scrapy.Field()
    nodata = scrapy.Field()