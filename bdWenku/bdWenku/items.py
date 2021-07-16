# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BdwenkuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    '''
        文件名
        文件链接

    '''
    file_name = scrapy.Field()
    url = scrapy.Field()
    book_id = scrapy.Field()
