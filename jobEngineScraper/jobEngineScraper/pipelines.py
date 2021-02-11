# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from rich.console import Console
logger = Console()
#let's try the scrapy way with all the info in setting
# https://docs.scrapy.org/en/latest/topics/item-pipeline.html

class MongoPipeline(object):
    """
    Description:
        - class used to handle the spider's output with our database
    input:
        - through a class method we obtain (IP,port,db and collection name) from the spide
    output:
        - outputs in the mongodb
    """
    def __init__(self, mongoIp, mongoPort, mongoDatabase, mongoCollection):
        self.mongoIp = mongoIp
        self.mongoPort = mongoPort
        self.mongoDatabase = mongoDatabase
        self.mongoCollection = mongoCollection


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongoIp=crawler.settings.get('MONGO_IP'),
            mongoPort=crawler.settings.get('MONGO_PORT'),
            mongoDatabase=crawler.settings.get('MONGO_DATABASE', 'items'),
            # from custom settings
            mongoCollection=crawler.settings.get('MONGO_COLLECTION')
        )

    def open_spider(self, spider):
        self.conn = pymongo.MongoClient(self.mongoIp,self.mongoPort)
        self.db = self.conn[self.mongoDatabase]
        self.collection = self.db[self.mongoCollection]

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        #if there's no record
        if not self.collection.count_documents({ 'url': item['url'] }, limit = 1):
            self.collection.insert_one(ItemAdapter(item).asdict())
        # print 
        # for k,v in item.items():
        #     logger.log(f'key/value: {k} : {v}')
        return item

