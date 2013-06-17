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
         self.dbobj.connect()
         #como el init solamente se llama una vez obtenemos el dato
         #para evitar repetir la operacion cada vez que insertemos
         #un item nuevo
        
         self.listTitItem = self.dbobj.showTituloItem()
         

    @classmethod
    def from_crawler(cls, crawler):
         pipeline = cls()
         
         crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
         crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
         return pipeline

    def spider_opened(self, spider):
       
        
        print "***********************************************************************"

    def spider_closed(self, spider):
        self.dbobj.disconnect()
        

    def process_item(self, item, spider):
        
        tituloRss = item['titChan'][0].replace("\"","\\\"")
        descripRss = item['descChan'][0].replace("\"","\\\"")
        linkRss = item['linkChan'][0].replace("\"","\\\"")
        tituloItem = item['titItem'][0].replace("\"","\\\"")
        descripItem = item['descItem'][0].replace("\"","\\\"")
        linkItem = item['linkItem'][0].replace("\"","\\\"")
        
        
        
        if self.ifTIExists(tituloItem) == False:
			
			self.dbobj.insData(tituloRss,descripRss,linkRss,tituloItem,descripItem,linkItem)
        else:
			print "***************Entrada ya existente!****************"
       
        return item

    def ifTIExists(self,TR):
        
        #print "******************************** getdata ************************"
        cond = False
        
        for p in self.listTitItem:
			

			if TR == p.replace("\"","\\\""):
				cond = True

				break
			else:

				cond = False

        
        return cond
