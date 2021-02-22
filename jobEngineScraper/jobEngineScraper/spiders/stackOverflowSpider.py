import scrapy
import re
# used to create random breaks
import time
import random
# to run the spider in a script
# https://docs.scrapy.org/en/latest/topics/practices.html#run-scrapy-from-a-script
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
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

class StackSpider(scrapy.Spider):
    # class variable for crawl command
    name = 'SOJobSpider'
    page = 1
    nextPage = None
    # settings only meant for the spider
    custom_settings = { 
        'MONGO_COLLECTION': 'stackOverflow',
        'DUPEFILTER_CLASS' : 'scrapy.dupefilters.BaseDupeFilter',
        'ITEM_PIPELINES': { 
            'jobEngineScraper.pipelines.MongoPipeline': 300,
        }
    
    }

    
    def start_requests(self):
        """
        Where the spider starts its search
        """ 
        start_url = 'https://stackoverflow.com/jobs'
        yield scrapy.Request(url=start_url, callback=self.pageParser)

    
    def iHazMyIIPChecked(self,response):
        """
        check your ip in the cli
        curl http://icanhazip.com/
        """
        logger.log(f"IP: {response.css('body p::text').get()}")
        yield scrapy.Request(url=StackSpider.nextPage, callback=self.pageParser)
        
        

    def pageParser(self,response):
        """
        goes through all the titles and and creates an array where the subPageParser will scrape from.
        """
        # Console.log(response.meta)
        # logger.log(f'--------short Break 0-5 seconds')
        # time.sleep(random.randint(0, 500))

        logger.log(f" fake user agent used: {response.request.headers['User-Agent']}")
        urlsToVisit = list()
        for title,url in zip(response.css(
            '.stretched-link::text').getall(),
            response.css('.stretched-link::attr(href)').getall()):
            if nltkPreprocess(title) == 'wanted':
                urlsToVisit.append([title,url])
                # logger.log(f'Wanted job: Job title: {title} url: {url}')
            else:
                # logger.log(f'Unwanted job: Job title: {title}')
                pass

        
        # extracting the info
        for title,url in urlsToVisit:
            
            # logger.log(f'Job going to title: {title} url: {url}')
            nextPage = response.urljoin(url)
            yield scrapy.Request(nextPage,callback=self.subPageParser)
            
        # we want the url to the next page
        StackSpider.page += 1
        url = f'?pg={StackSpider.page}'
        if StackSpider.page <= 40: #testing purpose
            # although I can visually see that the max is about 48 pages
            logger.log(f'proceeding to page: {StackSpider.page} url: {url}')
            StackSpider.nextPage = response.urljoin(url)
            # yield scrapy.Request(url='http://icanhazip.com/', callback=self.iHazMyIIPChecked)
            yield scrapy.Request(StackSpider.nextPage,callback=self.pageParser)


    def subPageParser(self,response):
        """
        Description:
            - this is super powerful as we make full use of Scrapy's async capabilities 
            in the event that a there's an error in the response it doesn't crash the spider
        Input:
            - response from the pageParger response
        Output:
            - the dictionary is then sent to the 
            
        """
        logger.log(f"fake user agent used: {response.request.headers['User-Agent']}")

        job = JobenginescraperItem()
        job['positionName'] = response.css('.fc-black-900::text').get()
        job['site'] = 'StackOverflow'
        if response.css('.fc-yellow-500::text').get():
            job['remote'] = True
        else:
            job['remote'] = False
        job['postedWhen'] = response.css('#overview-items .mb24 li::text').get().strip()
        try:
            job['company'] = response.css('.mb4 .fc-black-700::text').get().strip().replace('–\r\n','')
        except Exception as e:
            # message is deprecated
            logger.log(str(e))
            job['company'] = 'Not found'
        # job['company'] = response.css('._up-and-out::text').get() # doesn't always work
        job['url'] = response.url
        job['location'] = response.css('.mr8 .fw-bold::text').get() # can't be bothered with regex at the moment
        # using w3lib to clean the html soup (may have to do a try/except block)
        tempList = list()
        try:
            for i in range(len(response.css('.mb32.fc-medium div').getall())):
                tempList.append(w3lib.html.remove_tags(str(response.css('.mb32.fc-medium div')[i].getall())))
        except Exception as e:
            logger.log(e.message, e.args)
            tempList.append('Description Not Found')

        job['description'] = tempList
        job['applied'] = False
        job['filtered'] = False
        job['time'] = timestampReceival()
        yield job

if __name__ == '__main__':
    process = CrawlerProcess(settings=get_project_settings())
    process.crawl('SOJobspider')
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

            # pause timer if required
            # logger.log(f'--------short Break 0-5 seconds')
            # time.sleep(random.randint(0, 5))