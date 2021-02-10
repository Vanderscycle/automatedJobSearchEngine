import scrapy
import re

from rich.console import Console
from rich import (
    pretty,
    traceback,
    print
)
logger = Console()

from ..items import JobenginescraperItem

class flyerSpider(scrapy.Spider):
    # class variable for crawl command
    name = 'SOJobspider'
    
    def start_requests(self): 
        start_url = 'https://stackoverflow.com/jobs'
        yield scrapy.Request(url=start_url, callback=self.pageParser)
    
    def pageParser(self,response):
        """
        goes through all the titles and and creates an array where the subPageParser will scrape from.
        """
        for i in response.css('.stretched-link::text').getall():
            logger.log(f'{i}')
        pass

    def subPageParser(self,response):
        """
        test
        """
        job = JobenginescraperItem()
        pass
# (1) gets you the href of all jobs
# response.css('.stretched-link::attr(href)').getall()
# gets you their titles although only relevant as a way to determine if we should scrape or not
# response.css('.stretched-link::text').getall()

# from (1) we can append the href to stackoverflow.com/(href) and then fetch the page
# gets you the body of the text (description)
# (2) response.css('.mb32.fc-medium div').getall() 
# gives you an array of tags about the technologies used (reliable?)
# response.css('#overview-items :nth-child(3) div a::text').getall()
# (2) may not be good enough and so the statement bellow encompass more, but require filtering
# response.css('#overview-items').getall()

# to loop pages we can see that indexing is done this way:
# /jobs?so_source=JobSearch&so_medium=Internal&pg=2
