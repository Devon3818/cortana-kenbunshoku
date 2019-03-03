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
    mh_alias = []
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

        # get mh info data
        self.mh_name = response.css('.book-title h1::text').extract_first()
        self.mh_dec = response.css('#intro-cut p::text').extract_first()
        self.mh_cover = response.css('.book-cover .hcover img::attr(src)').extract_first()

        lilist = response.css('.detail-list li')

        for li_index in range(len(lilist)):
            spanlist = lilist[li_index].css('span')
            if li_index == 0:
                for span_index in range(len(spanlist)):
                    span = spanlist[span_index]
                    if span_index == 0:
                        self.mh_year = span.css('a::text').extract_first()
                        print 'year:'+self.mh_year
                    if span_index == 1:
                        self.mh_area = span.css('a::text').extract_first()
                        print 'area:'+self.mh_area
                    if span_index == 2:
                        self.mh_letter = span.css('a::text').extract_first()
                        print 'letter:'+self.mh_letter
            if li_index == 1:
                spanlist = lilist[li_index].css('span')
                for span_index in range(len(spanlist)):
                    span = spanlist[span_index]
                    if span_index == 0:
                        a_list = span.css('a')
                        for a in range(len(a_list)):
                            a_type = a_list[a].css('a::text').extract_first()
                            print a_type
                            self.mh_type.append(a_type)
                            print self.mh_type
                    if span_index == 1:
                        self.mh_author = span.css('a::text').extract_first()
                        print 'author:'+self.mh_author
            if li_index == 2:
                for span_index in range(len(spanlist)):
                    span = spanlist[span_index]
                    if span_index == 0:
                        al = span.css('a::text').extract_first()
                        self.mh_alias.append( al )
                        print 'alias:'+al
            if li_index == 3:
                spanlist = lilist[li_index].css('span')
                a_last = lilist[li_index].css('a::text').extract_first()
                self.mh_last = a_last
                print 'last:'+a_last
                for span_index in range(len(spanlist)):
                    span = spanlist[span_index]
                    print len(spanlist)
                    if span_index == 1:
                        st = span.css('span::text').extract_first()
                        self.mh_status = st
                        print 'status:'+st
                    if span_index == 2:
                        ut = span.css('span::text').extract_first()
                        self.mh_update_time = ut
                        print 'update_time:'+ut

        # get mh chip list data
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
