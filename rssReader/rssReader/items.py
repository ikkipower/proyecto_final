# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class RssItem(Item):
    # define the fields for your item here like:
    # name = Field()
    titChan = Field()
    descChan = Field()
    linkChan = Field()
    titItem = Field()
    descItem = Field()
    linkItem = Field()
