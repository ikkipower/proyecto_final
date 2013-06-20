#  Copyright 2013 Sergio Morlans <https://github.com/ikkipower/proyecto_final>
#       
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#       
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#       
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

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
         
         crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
         return pipeline


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
			     
        return item

    def ifTIExists(self,TR):
      
        cond = False    
        for p in self.listTitItem:		

			if TR == p.replace("\"","\\\""):
				cond = True
				break
			else:
				cond = False
        
        return cond
