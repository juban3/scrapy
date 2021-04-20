# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BdwenkuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    '''
        设置爬去的数据
        问题
        选项
        答案
        ??
    '''
    question = scrapy.Field()
    option = scrapy.Field()
    #pass
