from scrapy.spider import BaseSpider
from scrapy.selector import XmlXPathSelector
from rssReader.items import RssItem
from bs4 import BeautifulSoup
from datetime import datetime
from scrapy import log

class RssSpider(BaseSpider):
    name = "spiRss"
    start_urls = ["http://www.elperiodico.com/es/rss/rss_portada.xml"]
    
    def __init__(self, name=None, **kwargs):
        LOG_FILE = "%s_%s.log" % (self.name, datetime.now())
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
        
        tituloRss = cinfo.select("title/text()").extract()
        linkRss = cinfo.select("link/text()").extract()
        DescRss = cinfo.select("description/text()").extract()
        
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
				aux.append(it[0])		
            elif len(it) > 1:
				for aut in it:
					aux.append(aut[i])		
            print "**********************tititem*************"
            print aux[0]
            print "******************************************"
            item['titItem'] = aux              
       
            ################################################
            aux=[]
            it = site.select("description/text()").extract()
            if len(it) == 1:
				aux.append(it[0])		
            elif len(it) > 1:
				for aut in it:
					aux.append(aut[i])	
            item['descItem'] = aux              

            ################################################
            aux=[]
            it = site.select("link/text()").extract()
            if len(it) == 1:
				aux.append(it[0])		
            elif len(it) > 1:
				for aut in it:
					aux.append(aut[i])		
            item['linkItem'] = aux                          
            
            items.append(item)
        return items
