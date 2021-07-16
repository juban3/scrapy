import scrapy

from bdWenku.data.mysqldb import mysqldb
from bdWenku.items import BdwenkuItem


class WenkuSpider(scrapy.Spider):
    name = 'wenku'
    allowed_domains = ['wenku.baidu.com',]
#    start_urls = ['http://wenku.baidu.com/']

    books_lists = mysqldb()
    def start_requests(self):
        books_lists = self.books_lists.process_getbook()
#        books_lists = books_lists.replace('null',' ')
        for book_list in books_lists:
            book_list = [' ' if i=='null' else i for i in book_list]
            book = " ".join(book_list[1:])
            url = 'https://wenku.baidu.com/search?word={}阅读题&ie=utf-8'.format(book)
            # 交给调度器
            print('url='+url)
            yield scrapy.Request(
                url=url,
                callback=self.parse_getFileUrl
                #ua ip
            )

    def parse_getFileUrl(self, response):
        self.logger.debug(response.text)
        self.logger.debug('Status Code: ' + str(response.status))
        bdwenku_item = BdwenkuItem()
        #文件信息
        file_list = response.xpath('''//*[@id="app"]/div/dl''')
        #url_xpath = "//*[@id="app"]/div/dl/dt/p[@class="fl"]/a[1]"
        for dd in file_list:
            # 创建对象'
            # 文件名
            # 如果不添加extract_first()，会得到一堆列表里面的选择器，但是我们的目标是得到字符串
            #item["remark"] = dd.xpath('''./dt/p[@class="fl"]/a[1]/text()''').extract_first().strip()
            # 文件地址
            bdwenku_item["url"] = dd.xpath('''./dt/p[@class="fl"]/a[1]@href''').extract_first().strip()
            # 把爬取的数据交给管道文件pipeline处理
            # 生成器
            yield bdwenku_item
        '''
        yield scrapy.Request(
            url=bdwenku_item["file_url"],
            callback=self.parse_wgetfile
        )
        '''

    def parse_wgetfile(self, response):
        pass