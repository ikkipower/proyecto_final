from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings
from scrapy import log
from scrapy import signals
from rssReader.spiders.rssSpider import RssSpider

def stop_reactor():
    
    print "***********"
    reactor.stop() #Stops reactor to prevent script from hanging
 
if __name__ == '__main__':

    spider = RssSpider(domain='elperiodico.com')
    crawler = Crawler(get_project_settings())
    crawler.configure()
    crawler.crawl(spider)
    crawler.signals.connect(stop_reactor,signals.engine_stopped)
    crawler.start()
    
    #Start log and twisted reactor
    log.start()
    reactor.run()		 
