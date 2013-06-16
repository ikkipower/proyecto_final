# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import json
from scrapy import signals

class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open('rssfeeds.jl', 'wb')

    def process_item(self, item, spider):
		
        line = json.dumps(dict(item),encoding="utf-8",ensure_ascii=False ) + "\n"
        self.file.write(line)
        return item
