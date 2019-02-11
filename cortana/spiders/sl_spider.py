import scrapy
import sys
from selenium import webdriver
reload(sys)  
sys.setdefaultencoding('utf8')

class MhSpider(scrapy.Spider):
    name = "sl"
    maxLen = 0
    url = ''

    def start_requests(self):
        while self.maxLen < 40:
            self.maxLen+=1
            self.url = 'http://www.5qmh.com/' + str( self.maxLen )
            yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        filename = 'sl.html'
        with open(filename, 'a+') as f:
            f.write('\n')
            f.write(response.css('.book-btn .btn-read::attr(href)').extract_first())
            f.write('\n')
            f.write(response.css('.book-title h1::text').extract_first())
            f.write('\n')
            f.write('\n')
            f.write('\n')
            f.write('\n')