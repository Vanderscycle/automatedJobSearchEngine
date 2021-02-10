import scrapy
import rich
import re
from rich import (
    pretty,
    traceback,
    print
)

class flyerSpider(scrapy.Spider):
    # class variable for crawl command
    name = 'SOJospider'

    def start_requests(self): 
        start_url = 'https://flyers.smartcanucks.ca/'
        yield scrapy.Request(url=start_url, callback=self.defaultParser)
    
    def defaultParser(self,response):
        """
        test
        """
        pass
