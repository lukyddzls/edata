# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class MarketItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    type  = scrapy.Field()
    day   = scrapy.Field()
    zsz   = scrapy.Field()
    ltsz  = scrapy.Field()