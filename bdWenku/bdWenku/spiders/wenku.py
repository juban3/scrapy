# -*- coding: utf-8 -*-
import re

import scrapy
from pandas._libs import json

from bdWenku.data.mysqldbConn import mysqldbConn
from bdWenku.items import BdwenkuItem

class WenkuSpider(scrapy.Spider):
    name = 'wenku'
    allowed_domains = ['wenku.baidu.com',]
#    start_urls = ['http://wenku.baidu.com/']
    def start_requests(self):
        sqlconn = mysqldbConn()
        for books_list in sqlconn.process_getbook():
            url = 'https://wenku.baidu.com/search?word={} {}阅读题&usm=3&rsv_idx=2&rsv_page=1&ie=utf-8'.format(books_list[0],books_list[1])
            # 交给调度器
            print('url='+url)
#            header = {'X-Requested-With': 'XMLHttpRequest'}
            yield scrapy.Request(url=url ,callback=self.parse_getFileUrl)

    def parse_getFileUrl(self, response):
        #文件信息//*[@id="app"]/div/dl
#        body = response.body
#        decodeing = re.findall(r' charset=(.*?)">',body)
        body = response.body.decode('gb2312')
#        file_list = body.xpath(r'//span[@title="doc" and @class="ic ic-doc"]')
        file_list = re.findall(r'<p class="fl">(.*?)</p>',body)
        for dd in file_list:
            # 创建对象'
            item = BdwenkuItem()
            # 文件名
            # 如果不添加extract_first()，会得到一堆列表里面的选择器，但是我们的目标是得到字符串#
            item["book_name"] = dd.xpath(r'./div[1]/a/text()').get()
            # 文件地址
            item["url"] = body

            # 把爬取的数据交给管道文件pipeline处理

            # 调用第二网址进行下载
            yield item
            yield scrapy.Request(url=item["url"],callback=self.parse_wgetfile)

    def parse_wgetfile(self, response):
        pass