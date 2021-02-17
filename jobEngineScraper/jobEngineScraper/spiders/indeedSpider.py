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

class indeedSpider(scrapy.Spider):
    # class variable for crawl command
    name = 'indeedSpider'
    page = 1
    jobtitleIndex = 0
    titlesSearch = ['Data+Scientist','Software+engineer','developer','Data+engineer']
    start_url = 'https://ca.indeed.com/jobs?q={position}&l=Victoria%2C+BC&radius=100'
    # settings only meant for the spider
    custom_settings = { 
        'MONGO_COLLECTION': 'indeed',
        'DUPEFILTER_CLASS' : 'scrapy.dupefilters.BaseDupeFilter'
        # 'ITEM_PIPELINES': { 
        #     'jobEngineScraper.pipelines.MongoPipeline': 300,
        # }


    
    }

    
    def start_requests(self): 
        
        replacePosition = re.findall("\{position\}", indeedSpider.start_url)[0]
        start_url = re.sub(replacePosition , str(indeedSpider.titlesSearch[0]), indeedSpider.start_url)
        logger.log(f'heading to url{start_url}')
        yield scrapy.Request(url=start_url, callback=self.pageParser)
    

    def pageParser(self,response):
        """
        goes through all the titles and and creates an array where the subPageParser will scrape from.
        """
        logger.log(f'response for the url{response}')
        urlsToVisit = list()
        for title, url in zip(
            response.css('#resultsCol .jobsearch-SerpJobCard .title a::attr(title)').getall(),
            response.css('#resultsCol .jobsearch-SerpJobCard h2 a::attr(href)').getall()):
            if nltkPreprocess(title) == 'wanted':
                urlsToVisit.append([title,url])
                logger.log(f'Wanted job: Job title: {title} url: {url[:10]}')
            else:
                logger.log(f'Unwanted job: Job title: {title} url: {url[:10]}')
                pass
        for title,url in urlsToVisit:
            # logger.log(f'Job going to title: {title} url: {url}')
            nextPage = response.urljoin(url)
            # I will have to ignore robots.txt so that means I need a proxy otherwise its ban time
            yield scrapy.Request(nextPage,callback=self.subPageParser)   

        # next page format 
        # 'https://ca.indeed.com/jobs?q={position}&l=Victoria%2C+BC&radius=100&start=10'
        # we need to change the start with to index the page
        urlPgJoin = f'&start={indeedSpider.page*10}'
        if indeedSpider.page <= 2: #testing purpose

            replacePosition = re.findall("\{position\}", indeedSpider.start_url)[0]
            nextPage = re.sub(replacePosition , str(indeedSpider.titlesSearch[0]), indeedSpider.start_url) + urlPgJoin
            logger.log(f'proceeding to page: {indeedSpider.page} url: {nextPage}')
            indeedSpider.page += 1
            yield scrapy.Request(nextPage,callback=self.pageParser)

    def subPageParser(self,response):
        """
        scrapes all the data
        """
        job = JobenginescraperItem()
        job['positionName'] = response.css('.jobsearch-JobInfoHeader-title-container h1::text').get()
        job['site'] = 'ca.indeed'
        job['remote'] = False # can't find a good hook
        job['postedWhen'] = response.css('.jobsearch-JobMetadataFooter div::text').get()
        job['company'] = response.css('.jobsearch-CompanyInfoWithoutHeaderImage div::text').get()
        job['url'] = response.url
        job['location'] = scrapy.Field()
        job['description'] = w3lib.html.remove_tags(str(response.css('.jobsearch-JobComponent-description').get()))
        job['applied'] = False
        job['filtered'] = False
        job['time'] = timestampReceival()
        yield job
# https://ca.indeed.com/jobs?q={position}&l=Victoria%2C+BC&radius=100
# cool thing with indeed is that the we can do multiple job search using the url items e.g. q=Data+engineer
# wh
# using splash fetch('http://localhost:8050/render.html?url=https://ca.indeed.com/jobs?q=developer&l=Victoria,%20BC&radius=100')
# get the job title 
# response.css('#resultsCol .jobsearch-SerpJobCard .title a::attr(title)')[0].getall()
# the href of the job
# response.css('#resultsCol .jobsearch-SerpJobCard h2 a::attr(href)')[0].getall()

