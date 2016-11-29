# -*- coding: utf-8 -*-

#%%
import sys
import edata.spiders.edataSpider as edataSpider
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

def run():
    #爬取页面
    settings = get_project_settings()
    configure_logging()
    runner = CrawlerRunner(settings)

    runner.crawl(edataSpider.szSpider)
    runner.crawl(edataSpider.shSpider)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
    print 'run over'

if __name__ == '__main__':
    if len(sys.argv) != 1:
        print 'Usage: python run.py'
        exit(1)

    try:
        run()
    except Exception, e:
        print e