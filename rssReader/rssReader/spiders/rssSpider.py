from scrapy.spider import BaseSpider
from scrapy.selector import XmlXPathSelector
from rssReader.items import RssItem
from bs4 import BeautifulSoup
from datetime import datetime
from scrapy import log

class RssSpider(BaseSpider):
    name = "spiRss"
    start_urls = ["http://www.elperiodico.com/es/rss/rss_portada.xml"]
    allowed_domains = ['elperiodico.com']
    
    def __init__(self, name=None, **kwargs):
        LOG_FILE = "log/%s_%s.log" % (self.name, datetime.now())
        log.log.defaultObserver = log.log.DefaultObserver()
        log.log.defaultObserver.start()
        log.started = False
        log.start(LOG_FILE, loglevel=log.ERROR,logstdout=False)
        super(RssSpider, self).__init__(name, **kwargs)

    
    def parse(self, response):
        xxs = XmlXPathSelector(response)
        cinfo = xxs.select("//channel")   
        iinfo = xxs.select("//channel/item")
        items = []
        
        it = cinfo.select("title/text()").extract()[0].encode('latin-1')
        print len(it)
        if len(it) == 0:
			tituloRss = [""]
        else:
			tituloRss = [it]

        it = cinfo.select("link/text()").extract()[0].encode('latin-1')
        if len(it) == 0:
			linkRss = [""]
        else:
			linkRss = [it]

        it = cinfo.select("description/text()").extract()[0].encode('latin-1')
        if len(it) == 0:
			DescRss = [""]
        else:
			DescRss = [it]

        for site in iinfo:
			aux=[]
			item = RssItem()
			item['titChan'] = tituloRss
			item['descChan'] = linkRss
			item['linkChan'] = DescRss
            
            ################################################
			aux=[]
			it = site.select("title/text()").extract()
			if len(it) == 1:
				aux.append(it[0].encode('latin-1'))
			elif len(it) > 1:
				for aut in it:
					aux.append(aut[i].encode('latin-1'))
			else:
				aux.append("".encode('latin-1'))		
			item['titItem'] = aux              
      
            ################################################
			aux=[]
			it = site.select("description/text()").extract()
			if len(it) == 1:
				aux.append(it[0].encode('latin-1'))
			elif len(it) > 1:
				for aut in it:
					aux.append(aut[i].encode('latin-1'))	
			else:
				aux.append("".encode('latin-1'))				
			item['descItem'] = aux              

            ################################################
			aux=[]
			it = site.select("link/text()").extract()
			if len(it) == 1:
				aux.append(it[0].encode('latin-1'))		
			elif len(it) > 1:
				for aut in it:
					aux.append(aut[i].encode('latin-1'))
			else:
				aux.append("".encode('latin-1'))							
			
			item['linkItem'] = aux                          
            
			items.append(item)
        return items
