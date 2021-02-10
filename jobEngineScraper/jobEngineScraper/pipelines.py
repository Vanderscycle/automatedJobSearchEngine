# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

#let's try the scrapy way with all the info in setting
# https://docs.scrapy.org/en/latest/topics/item-pipeline.html
class JobenginescraperPipeline:

    def __init__(self):
        # requires two arguments
        self.conn = pymongo.MongoClient(
            '127.0.0.1',27017)
        

        dbnames = self.conn.list_database_names()
        if 'jobSearch' not in dbnames:
            # creating the database
            # mongodb doesn't take capitilization
            self.db = self.conn['jobSearch']

        #the database already exists
        else:
            # we acces the db

            self.db = self.conn.jobSearch

        dbCollectionNames = self.db.list_collection_names()
        if 'amazonWholeFood' not in dbCollectionNames:
            self.collection = self.db['amazonWholeFood']
        
        else:
            # we acces the db collection
            self.collection = self.db.amazonWholeFood

    def process_item(self, item, spider):


        try:
            # insert Many requires a dict of dict. i
            self.collection.insert_one(dict(item))
            # self.collection.update(dict(item),{ 'upsert': 'true' })
        
        except Exception as e:
            print('\n','--- ERROR ---',e,'\n')
        # in the future 

        for k,v in item.items():
            print(f'key/value: {k} : {v}')
        return item
