import scrapy
import sys
from selenium import webdriver
from ..items import ChipItem
reload(sys)  
sys.setdefaultencoding('utf8')

class MhSpider(scrapy.Spider):
    name = "5q"
    url = ''
    a_href = ''
    a_page = ''
    a_title = ''
    id = 1
    pas = '-1'

    def __init__(self, id, pas = '-1'):
        self.id = id
        self.pas = pas


    def start_requests(self):
        self.url = 'http://www.wuqimh.com/' + str(self.id)
        yield scrapy.Request(url=self.url, callback=self.parse)


    def parse(self, response):
        ul_list = response.css('.chapter-list ul')
        if len(ul_list) > 0 :
            for ul in ul_list:
                li_list = ul.css('li')
                if len(li_list) > 0 :
                    li_index = 0
                    li_list.reverse()
                    for li in li_list:
                        li_index+=1
                        page = 0
                        self.a_title = li.css('a::attr(title)').extract_first()
                        
                        if self.pas != '-1' and self.pas != self.a_title:
                            continue
                        else:
                            self.pas = '-1'
                            self.a_href = 'http://www.wuqimh.com' + li.css('a::attr(href)').extract_first()
                            self.a_page = li.css('a i::text').extract_first()[:-1]

                            while int(page) < int(self.a_page):
                                page+=1
                                request = scrapy.Request(url=self.a_href+'?p='+str(page), callback=self.parse_page)
                                request.meta['page'] = page
                                request.meta['title'] = self.a_title
                                request.meta['id'] = str(self.id)
                                request.meta['p_index'] = li_index
                                yield request                        


    def parse_page(self, response):
        item = ChipItem()
        item['mh_id'] = response.meta['id']
        item['mh_index'] = response.meta['p_index']
        item['mh_chip'] = response.meta['title']
        item['mh_page'] = response.meta['page']
        item['mh_src'] = response.css('#manga::attr(src)').extract_first()
        
        yield item
