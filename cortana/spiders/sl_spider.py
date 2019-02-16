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

    mh_name = ''
    mh_dec = ''
    mh_cover = ''
    mh_year = ''
    mh_area = ''
    mh_type = []
    mh_author = ''
    mh_alias = '无'
    mh_last = ''
    mh_status = ''
    mh_letter = ''
    mh_update_time = ''

    id = 1
    pas = '-1'

    def __init__(self, id, pas = '-1'):
        self.id = id
        self.pas = pas


    def start_requests(self):
        self.url = 'http://www.wuqimh.com/' + str(self.id)
        yield scrapy.Request(url=self.url, callback=self.parse)


    def parse(self, response):

        self.mh_name = response.css('.book-title h1::text').extract_first()
        self.mh_dec = response.css('#intro-cut p::text').extract_first()
        self.mh_cover = response.css('.book-cover .hcover img::attr(src)').extract_first()

        lilist = response.css('.detail-list li')

        for li in lilist:
            spanlist = li.css('span')
            for span_index in range(len(spanlist)):
                span = spanlist[span_index]
                if span_index == 1:
                    self.mh_year = span.css('a::text').extract_first()
                if span_index == 2:
                    self.mh_area = span.css('a::text').extract_first()
                if span_index == 3:
                    self.mh_letter = span.css('a::text').extract_first()
                if span_index == 4:
                    if len(span.css('a')) > 1:
                        alist = span.css('a::text')
                        for a in alist:
                            self.mh_type.append(a.get())
                    else:
                        self.mh_type.append(span.css('a::text').extract_first())
                if span_index == 5:
                    self.mh_author = span.css('a::text').extract_first()
                if span_index == 6:
                    if span.css('a::text'):
                        self.mh_alias = span.css('a::text').extract_first()
                if span_index == 7:
                    self.mh_last = span.css('a::text').extract_first()
                    t_span = span.css('span::text')
                    for str_index in range(len(t_span)):
                        if str_index == 1:
                            self.mh_status = t_span[str_index].get()
                        if str_index == 2:
                            self.mh_update_time = t_span[str_index].get()
                pass

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
