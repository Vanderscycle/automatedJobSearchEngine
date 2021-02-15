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
    def __init__(self, mongoIp, mongoPort, mongoDatabase, mongoCollection, username, password, authSource, mode):
        self.conn = pymongo.MongoClient()
        self.mongoIp = mongoIp
        self.mongoPort = mongoPort
        self.mongoDatabase = mongoDatabase
        self.mongoCollection = mongoCollection
        self.mongoUsername = username
        self.mongoUserPassword = password
        self.authSource = authSource
        self.mode = mode


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongoIp=crawler.settings.get('MONGO_IP'),
            mongoPort=crawler.settings.get('MONGO_PORT'),
            mongoDatabase=crawler.settings.get('MONGO_DATABASE', 'items'),
            username=crawler.settings.get('USERNAME'),
            password=crawler.settings.get('USERPASSWORD'),
            authSource=crawler.settings.get('MONGO_COLLECTION'),
            mode=crawler.settings.get('MODE'),
            # from custom settings
            mongoCollection=crawler.settings.get('MONGO_COLLECTION')
        )

    # self.conn = pymongo.MongoClient(host='NoSQLDB',port=27017,username='root',password='password',authSource="admin")
    def _connect_mongo(self,host, port,db=None, username=None, password=None):
        """ A util for making a connection to mongo """

        if username and password:
            mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
            conn = pymongo.MongoClient(mongo_uri)
        else:
            conn = pymongo.MongoClient(host, port)

        return conn

    
    def open_spider(self, spider):
        if self.mode == 'docker':
            self.conn = self._connect_mongo(
                    host=self.mongoIp,
                    port=self.mongoPort,
                    db=self.mongoDatabase,
                    username=self.mongoUsername,
                    password=self.mongoUserPassword
                )
            # self.conn = pymongo.MongoClient(
            #         host=self.mongoIp,
            #         port=self.mongoPort,
            #         username=self.mongoUsername,
            #         password=self.mongoUserPassword,
            #         authSource=self.authSource
            #     )
        else:
            self.mongoIp = '127.0.0.1'
            self.conn = self._connect_mongo(
                    host=self.mongoIp,
                    port=self.mongoPort
                )
            # self
            # self.conn = pymongo.MongoClient(
            #         self.mongoIp,
            #         self.mongoPort
            #     )
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

#! know pipeline issues:
# in docker mode we get massive errors (twisted problems)
# works fine in local mode