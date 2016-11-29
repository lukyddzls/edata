# -*- coding: utf-8 -*-

import datetime
import json
from scrapy.selector import Selector
from scrapy.http import  Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from edata.items import MarketItem

def datelist(start, end):
    start_date = datetime.date(*start)
    end_date = datetime.date(*end)

    result = []
    curr_date = start_date
    while curr_date != end_date:
        result.append("%04d-%02d-%02d" % (curr_date.year, curr_date.month, curr_date.day))
        curr_date += datetime.timedelta(1)
    result.append("%04d-%02d-%02d" % (curr_date.year, curr_date.month, curr_date.day))
    return result

class szSpider(CrawlSpider):
    # name of spiders
    name = 'szSpider'
    allow_domain = ['szse.cn']
    start_urls = [
        'http://www.szse.cn/main/marketdata/tjsj/jbzb/',
    ]

    rules = [
        Rule(LinkExtractor(allow=('http://www.szse.cn/main/marketdata/tjsj/jbzb/')), callback='parse_content', follow=False),
    ]

    def parse_content(self, response):
        sel = Selector(response)
        day = sel.xpath('//span[@class="cls-subtitle"]/text()')
        zsz = sel.xpath(u'//div[@class="index"]//table[@class="cls-data-table"]//td[@class="cls-data-td" and contains(text(), "股票总市值")]/../td[2]/text()')
        ltsz = sel.xpath(u'//div[@class="index"]//table[@class="cls-data-table"]//td[@class="cls-data-td" and contains(text(), "股票流通市值")]/../td[2]/text()')

        if len(zsz) > 0 and len(ltsz) > 0:
            item = MarketItem()
            item['type'] = 'sz'
            item['day'] = day.extract_first()
            item['zsz'] = zsz.extract_first().replace(',', '')
            item['ltsz'] = ltsz.extract_first().replace(',', '')
            yield item

class shSpider(CrawlSpider):
    # name of spiders
    name = 'shSpider'
    allow_domain = ['sse.com.cn']
    start_urls = [
        'http://www.sse.com.cn/market/stockdata/overview/day/',
    ]

    rules = [
        Rule(LinkExtractor(allow=('http://www.sse.com.cn/market/stockdata/overview/day/')), callback='parse_content', follow=False),
    ]

    def parse_content(self, response):
        sel = Selector(response)
        content = sel.xpath('//table[@class="table search_"]/script/text()')

        if len(content) > 0:
            item = MarketItem()
            item['type'] = 'sh'
            item['day'] = content.re_first(r'var searchDate = \'\s*(.*)\';')
            item['zsz'] = content.re_first(r'var marketValueA = \'\s*(.*)\';')
            item['ltsz'] = content.re_first(r'var negotiableValueA = \'\s*(.*)\';')
            yield item

class szHisSpider(CrawlSpider):
    # name of spiders
    name = 'szHisSpider'
    allow_domain = ['szse.cn']
    dates = datelist((2000, 1, 1), (2000, 12, 31))
    start_urls = [
        'http://www.szse.cn/szseWeb/FrontController.szse?randnum=0.45052234100301636&ACTIONID=7&AJAX=AJAX-TRUE&CATALOGID=1803&TABKEY=tab1&REPORT_ACTION=search&txtQueryDate=' + date
        for date in dates
    ]
    rules = []

    def parse(self, response):
        sel = Selector(response)
        day = sel.xpath('//span[@class="cls-subtitle"]/text()')
        zsz = sel.xpath(u'//td[@class="cls-data-td" and contains(text(), "股票总市值")]/../td[2]/text()')
        ltsz = sel.xpath(u'//td[@class="cls-data-td" and contains(text(), "股票流通市值")]/../td[2]/text()')

        if len(zsz) > 0 and len(ltsz) > 0:
            item = MarketItem()
            item['type'] = 'sz'
            item['day'] = day.extract_first()
            item['zsz'] = zsz.extract_first().replace(',', '')
            item['ltsz'] = ltsz.extract_first().replace(',', '')
            yield item

class shHisSpider(CrawlSpider):
    # name of spiders
    name = 'shHisSpider'
    allow_domain = ['sse.com.cn']
    start_urls = [
        'http://www.sse.com.cn/market/stockdata/overview/day/',
    ]

    rules = [
        Rule(LinkExtractor(allow=('http://www.sse.com.cn/market/stockdata/overview/day/')), callback='parse_content', follow=False),
    ]

    def parse_content(self, response):
        sel = Selector(response)
        content = sel.xpath('//table[@class="table search_"]/script/text()')

        if len(content) > 0:
            item = MarketItem()
            item['type'] = 'sh'
            item['day'] = content.re_first(r'var searchDate = \'\s*(.*)\';')
            item['zsz'] = content.re_first(r'var marketValueA = \'\s*(.*)\';')
            item['ltsz'] = content.re_first(r'var negotiableValueA = \'\s*(.*)\';')
            yield item
