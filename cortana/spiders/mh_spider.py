import scrapy
import sys
reload(sys)  
sys.setdefaultencoding('utf8')

class MhSpider(scrapy.Spider):
    name = "mh"
    maxLen = 0
    url = ''

    def start_requests(self):
        while self.maxLen < 35000:
            self.maxLen+=1
            self.url = 'http://www.5qmh.com/' + str( self.maxLen )
            yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        filename = 'manhua.html'
        with open(filename, 'a+') as f:
            f.write('\n')
            f.write('\n')
            f.write('\n')
            f.write('\n')
            f.write('\n')
            f.write('=============================================')
            f.write('\n')
            f.write(response.css('.book-btn .btn-read::attr(href)').extract_first())
            f.write('\n')
            f.write(response.css('.book-title h1::text').extract_first())
            f.write('\n')
            f.write(response.css('#intro-cut p::text').extract_first())
            f.write('\n')
            f.write(response.css('.book-cover .hcover img::attr(src)').extract_first())
            f.write('\n')
            lilist = response.css('.detail-list li')
            for li in lilist:
                spanlist = li.css('span')
                for span in spanlist:
                    if len(span.css('a')) > 1:
                        alist = span.css('a::text')
                        for a in alist:
                            f.write(a.get())
                            f.write('\n')
                    else:
                        f.write(span.css('a::text').extract_first())
        self.log('Saved file %s' % filename)