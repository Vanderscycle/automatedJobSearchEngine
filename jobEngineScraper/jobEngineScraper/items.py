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
    company = scrapy.Field()
    url = scrapy.Field()
    location = scrapy.Field()
    description = scrapy.Field()
    applied = scrapy.Field()
    time = scrapy.Field()