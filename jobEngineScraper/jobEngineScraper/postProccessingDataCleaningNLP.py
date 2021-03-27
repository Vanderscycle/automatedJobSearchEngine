# access passwords
import os
from dotenv import load_dotenv
# data processing
import pandas as pd
import numpy as np
# accessing the db
import pymongo
#nlp
from collections import Counter
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
load_dotenv()
MONGO_IP = os.getenv('MONGO_IP')
MONGO_PORT = int(os.getenv('MONGO_PORT'))
MONGO_DATABASE = os.getenv('MONGO_DATABASE')
MONGO_COLLECTION = 'stackOverflow'

# taken from
#https://stackoverflow.com/questions/16249736/how-to-import-data-from-mongodb-to-pandas
def _connect_mongo(host, port, db=None, username=None, password=None):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = pymongo.MongoClient(mongo_uri)
    else:
        conn = pymongo.MongoClient(host, port)

    return conn


def read_mongo(db, collection, query={}, host='localhost', port=27017, username=None, password=None, no_id=False):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    conn = _connect_mongo(host=host, port=port, username=username, password=password, db=db)
    db = conn[db]
    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query)

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(iter(cursor))

    # Delete the _id
    if no_id and '_id' in df:
        del df['_id']

    return df


def update_mongo(db, collection,df, host='localhost', port=27017, username=None, password=None, no_id=False):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    conn = _connect_mongo(host=host, port=port, username=username, password=password, db=db)
    db = conn[db]
    # Make a query to the specific DB and Collection
    updates = []

    for _, row in df.iterrows():
        updates.append(pymongo.UpdateOne({'_id': row.get('_id')}, {'$set': {'cleanedDescription': row.get('description')}}, upsert=True))

    db[collection].bulk_write(updates)


def htmlGarbageDeleter(text):
    """ regex to delete pesky \r \n"""
    regex =r'(\\r).*(\\n)|(\\xa0)' 
    words = text.lower().split()
    cleanText = [re.sub(regex, '', w) for w in words]
    return ' '.join(cleanText)


def nltkPreprocess(text):
    # yeah it's not very good because the [] gets captured but since they are later captured by string.punctuation there's no harm
    text = htmlGarbageDeleter(text)
    # lower
    words = text.lower().split()
    # remove punctiuation
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in words]
    #remove stopwords
    stop_words = set(stopwords.words('english'))
    clean = [w for w in stripped if not w in stop_words if w!='' and w.isnumeric()==False and len(w) >2] #len >2 to filter garbage
    # we concatenate all list elements
    return ' '.join(clean)

#otherwise we we do the relative import for the functions it will execute the file which we do not want to
if __name__ == '__main__':
    query = {"site": "ca.indeed"}
    df = read_mongo(MONGO_DATABASE,MONGO_COLLECTION,query)
    df = df[:10]
    print(len(df))
    # df['description'] = df['description'].apply(lambda x:nltkPreprocess(str(x)))
    # update_mongo(MONGO_DATABASE,MONGO_COLLECTION,df)