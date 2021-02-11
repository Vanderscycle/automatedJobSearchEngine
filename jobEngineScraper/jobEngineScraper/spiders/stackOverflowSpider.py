import scrapy
import re
# used to create random breaks
import time
import random
# scrapy.utils.markup is deprecated.
import w3lib.html
# making the terminal outputs clearers
from rich.console import Console
from rich import (
    pretty,
    traceback,
    print
)

logger = Console()
# importing the required 
from ..items import JobenginescraperItem,timestampReceival
#importing the NLP preprocessor
from ..preProcessingNLP import nltkPreprocess

class flyerSpider(scrapy.Spider):
    # class variable for crawl command
    name = 'SOJobspider'
    page = 1
    # settings only meant for the spider
    custom_settings = { 
        'MONGO_COLLECTION': 'stackOverflow',
        'DUPEFILTER_DEBUG' : True,#allows the spider to not stop over duplicates 
        'ITEM_PIPELINES': { 
            'jobEngineScraper.pipelines.MongoPipeline': 300,
        }
    
    }

    
    def start_requests(self): 
        start_url = 'https://stackoverflow.com/jobs'
        yield scrapy.Request(url=start_url, callback=self.pageParser)
    
    def pageParser(self,response):
        """
        goes through all the titles and and creates an array where the subPageParser will scrape from.
        """
        urlsToVisit = list()
        for title,url in zip(response.css('.stretched-link::text').getall(),response.css('.stretched-link::attr(href)').getall()):
            if nltkPreprocess(title) == 'wanted':
                urlsToVisit.append([title,url])
                # logger.log(f'Wanted job: Job title: {title} url: {url}')
            else:
                # logger.log(f'Unwanted job: Job title: {title}')
                pass

        
        # extracting the info
        for title,url in urlsToVisit:

            # logger.log(f'--------short Break 0-5 seconds')
            # time.sleep(random.randint(0, 5))
            
            logger.log(f'Job going to title: {title} url: {url}')
            nextPage = response.urljoin(url)
            yield scrapy.Request(nextPage,callback=self.subPageParser)
            
        # we want the url to the next page
        flyerSpider.page += 1
        url = f'?pg={flyerSpider.page}'
        if flyerSpider.page <= 2: #testing purpose
            # although I can visually see that the max is about 48 pages
            logger.log(f'proceeding to page: {flyerSpider.page} url: {url}')
            nextPage = response.urljoin(url)
            yield scrapy.Request(nextPage,callback=self.pageParser)


    def subPageParser(self,response):
        """
        test
        """
        job = JobenginescraperItem()
        job['positionName'] = response.css('.fc-black-900::text').get()
        job['site'] = 'StackOverflow'
        job['company'] = response.css('.fs-body3 .fc-black-500::text').get().strip().replace('–\r\n','')
        # job['company'] = response.css('._up-and-out::text').get() # doesn't always work
        job['url'] = response.url
        job['location'] = response.css('.mr8 .fw-bold::text').get() # can't be bothered with regex at the moment
        # using w3lib to clean the html soup
        tempList = list()
        for i in range(len(response.css('.mb32.fc-medium div').getall())):
            tempList.append(w3lib.html.remove_tags(str(response.css('.mb32.fc-medium div')[i].getall())))
        job['description'] = tempList
        job['applied'] = False
        job['time'] = timestampReceival()
        yield job

if __name__ == "__main__":
    
    process = CrawlerProcess()
    process.crawl(MySpider)
    process.start() 
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

# will have to explore this scrapy hub
# https://stackoverflow.com/questions/30345623/scraping-dynamic-content-using-python-scrapy
# for indeed (will have to do it manually)
# response.css('#resultsCol .jobsearch-SerpJobCard .title')[0].getall()