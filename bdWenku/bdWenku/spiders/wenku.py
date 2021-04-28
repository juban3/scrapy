import scrapy

from bdWenku.bdWenku.data import mysqldb
from bdWenku.bdWenku.items import BdwenkuItem


class WenkuSpider(scrapy.Spider):
    name = 'wenku'
    allowed_domains = ['wenku.baidu.com',]
#    start_urls = ['http://wenku.baidu.com/']
    def start_requests(self):
        books_lists = mysqldb.process_getbook()
        for books_list in books_lists:
            url = 'https://wenku.baidu.com/search?word={}  {}阅读题&ie=utf-8'.format(books_list[0],books_list[1])
            # 交给调度器
            print('url='+url)
            yield scrapy.Request(
                url=url,
                callback=self.parse_getFileUrl
            )

    def parse_getFileUrl(self, response):
        #文件信息
        file_list = response.xpath('''//*[@id="app"]/div/dl''')
        #url_xpath = "//*[@id="app"]/div/dl/dt/p[@class="fl"]/a[1]"
        for dd in file_list:
            # 创建对象'
            item = BdwenkuItem()
            # 文件名
            # 如果不添加extract_first()，会得到一堆列表里面的选择器，但是我们的目标是得到字符串
            item["remark"] = dd.xpath('''./dt/p[@class="fl"]/a[1]/text()''').extract_first().strip()
            # 文件地址
            item["url"] = dd.xpath('''./dt/p[@class="fl"]/a[1]@href''').extract_first().strip()

            # 把爬取的数据交给管道文件pipeline处理
            # 生成器
        yield scrapy.Request(
            url=item["url"],
            callback=self.parse_wgetfile
        )


    def parse_wgetfile(self, response):
        pass