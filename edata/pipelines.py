# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

# t_market create table t_market (day DATE primary key, shsz UNSIGNED BIG INT, shltsz UNSIGED BIG INT, szsz UNSIGNED BIG INT, szltsz UNSIGNED BIG INT)

class EDataPipeline(object):
    def process_item(self, item, spider):
        self.cursor.execute('select * from t_market where day="%s"' % item['day'])
        if len(self.cursor.fetchall()) == 0:
            self.cursor.execute('insert into t_market (day) values ("%s")' % item['day'])

        if item['type'] == 'sz':
            # 修正单位 元->亿元
            zsz = round(float(item['zsz'])/100000000, 2)
            ltsz = round(float(item['ltsz'])/100000000, 2)
            #self.cursor.execute('update t_market set szzsz=%s, szltsz=%s where day="%s"' % (item['zsz'], item['ltsz'], item['day']))
            self.cursor.execute('update t_market set szzsz=%s, szltsz=%s where day="%s"' % (zsz, ltsz, item['day']))
        elif item['type'] == 'sh':
            self.cursor.execute('update t_market set shzsz=%s, shltsz=%s where day="%s"' % (item['zsz'], item['ltsz'], item['day']))

    def open_spider(self, spider):
        print 'open spider', spider.name
        self.conn = sqlite3.connect('edata.db')
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        print 'close spider', spider.name
        self.cursor.close()
        self.conn.commit()
        self.conn.close()