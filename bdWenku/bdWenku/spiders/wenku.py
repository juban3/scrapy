import json
import re

import scrapy

from bdWenku.data.mysqldb import mysqldb
from bdWenku.items import BdwenkuItem


class WenkuSpider(scrapy.Spider):
    name = 'wenku'
    allowed_domains = ['wenku.baidu.com',]
#    start_urls = ['http://wenku.baidu.com/']

    books_lists = mysqldb()
    bdwenku_item = BdwenkuItem()


    def start_requests(self):
        bdwenku_item = self.bdwenku_item
        books_lists = self.books_lists.process_getbook()
        for book_list in books_lists:
            book_list = [' ' if i=='null' else i for i in book_list]
            book = " ".join(book_list[1:-1])
            bdwenku_item["book_id"] = book_list[0]
            bdwenku_item["must"] = book_list[-1]
            for pn in range(1,4):
                url = 'https://wenku.baidu.com/search?word={}阅读题&lm=0&od=0&fr=search&ie=utf-8&pn={} HTTP/1.1'.format(book,pn)
                # 交给调度器
                print(url)
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_getFileUrl,
                    meta=bdwenku_item
            )

    def parse_getFileUrl(self, response):
#        self.logger.debug(response.text)
        self.logger.debug('Status Code: ' + str(response.status))
        bdwenku_item = response.meta
        sel = response.text
        files_url = re.findall(r'http://wenku.baidu.com/view/.*?.html',sel)
        files_url = set(files_url)
        for code in files_url:
            file_code = re.findall('view/(.*?).html',code)
            # 创建对象'
            # 文件名
            #item["remark"] = dd.xpath('''./dt/p[@class="fl"]/a[1]/text()''').extract_first().strip()
            # 文件地址
            bdwenku_item["url"] = code.strip()
            bdwenku_item["file_code"] = file_code


            # 把爬取的数据交给管道文件pipeline处理
            # 生成器
            yield bdwenku_item