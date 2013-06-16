# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import json
from scrapy import signals
from scrapy.contrib.exporter import XmlItemExporter

#class JsonWriterPipeline(object):

#    def __init__(self):
#        self.file = open('rssfeeds.jl', 'wb')

#    def process_item(self, item, spider):
		
#        line = json.dumps(dict(item)) + "\n"
#        self.file.write(line)
#        return item
####################################################################
###################### Mysql Pipeline ############################## 
####################################################################

from dbclass import Dbclass

class MySqlPipeline(object):

    def __init__(self):
         self.dbobj = Dbclass('RSSdata','rssuser','rss')
         self.i=0 #se ha de borrar
         

    @classmethod
    def from_crawler(cls, crawler):
         pipeline = cls()
         
         crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
         crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
         return pipeline

    def spider_opened(self, spider):
        print "****************************** opened *********************************"
        self.dbobj.connect()
        print "***********************************************************************"

    def spider_closed(self, spider):
        self.dbobj.disconnect()
        print "*** closed ***"
        

    def process_item(self, item, spider):
        print "******************************** process ************************"
        print(type(item['titItem'][0]))
        print item['titItem'][0]
        print(type(item['descItem'][0]))
        print item['descItem'][0]
        print(type(item['linkItem'][0]))
        print item['linkItem'][0]
        print "******************************** insdata ************************"
        self.dbobj.insData("ddd","jjj","http://www.marca.com",item['titItem'][0],item['descItem'][0],"ss")
        #if len(item['tag'])>0:
			#self.exporter.export_item(item)
        return item


