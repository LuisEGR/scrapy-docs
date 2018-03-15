# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DocumentosItem(scrapy.Item):
    UUID = scrapy.Field()
    SITE = scrapy.Field()
    URL = scrapy.Field()
    TITLE = scrapy.Field()
    ARCHIVO = scrapy.Field()
    SH_FILE = scrapy.Field()
    PATH = scrapy.Field()
