import scrapy
import sys
from selenium import webdriver
from ..items import CortanaItem
reload(sys)  
sys.setdefaultencoding('utf8')

class MhSpider(scrapy.Spider):
    name = "sl"
    maxLen = 0
    url = ''
    a_href = ''
    a_page = ''
    a_title = ''

    def start_requests(self):
        item = CortanaItem()
        while self.maxLen < 1:
            self.maxLen+=1
            self.url = 'http://www.5qmh.com/7366'
            yield scrapy.Request(url=self.url, callback=self.parse)


    def parse(self, response):
        ul_list = response.css('.chapter-list ul')
        #print ul_list
        #print len(ul_list)
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
                        self.a_href = 'http://www.5qmh.com' + li.css('a::attr(href)').extract_first()
                        self.a_page = li.css('a i::text').extract_first()[:-1]
                        
                        while int(page) < int(self.a_page):
                            page+=1
                            request = scrapy.Request(url=self.a_href+'?p='+str(page), callback=self.parse_page)
                            request.meta['page'] = page
                            request.meta['title'] = self.a_title
                            request.meta['p_index'] = li_index
                            yield request

    def parse_page(self, response):
        filename = 'sl.html'
        img_src = response.css('#manga::attr(src)').extract_first()
        title = response.css('.title h1 a::text').extract_first()
        p = response.css('.title h2::text').extract_first()
        sp = response.css('.title .curPage::text').extract_first()
        
        with open(filename, 'a+') as f:
            f.write('\n')
            f.write(response.meta['title'])
            f.write('\n')
            f.write(str(response.meta['p_index']))
            f.write('\n')
            f.write(title)
            f.write('/')
            f.write(p)
            f.write('/')
            f.write(str(response.meta['page']))
            f.write('/')
            f.write(str(self.a_page))
            f.write('\n')
            f.write(img_src)
            f.write('\n')
            f.write('\n')
            f.write('\n')
            f.write('\n')
            f.close()
            