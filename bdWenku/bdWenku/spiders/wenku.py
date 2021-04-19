import scrapy


class WenkuSpider(scrapy.Spider):
    name = 'wenku'
    allowed_domains = ['wenku.baidu.com']
    start_urls = ['http://wenku.baidu.com/']

    def parse(self, response):
        pass
