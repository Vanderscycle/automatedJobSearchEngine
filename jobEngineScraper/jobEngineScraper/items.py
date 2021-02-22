# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from datetime import datetime
def timestampReceival():
    """
    simple timestamp generator to produce a time when an item was scraped
    """
    now = datetime.now()
    return  now.strftime("%m/%d/%Y, %H")

class JobenginescraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    positionName = scrapy.Field()
    site = scrapy.Field()
    remote = scrapy.Field()
    postedWhen = scrapy.Field()
    company = scrapy.Field()
    url = scrapy.Field()
    location = scrapy.Field()
    description = scrapy.Field()
    applied = scrapy.Field()
    filtered = scrapy.Field()
    time = scrapy.Field()
    # https://stackoverflow.com/questions/14390945/suppress-scrapy-item-printed-in-logs-after-pipeline
    def __repr__(self):
        """only print out attr1 after exiting the Pipeline"""
        return repr({
            "positionName": self['positionName'],
            "site": self['site'],
            "company":self['company']
            })