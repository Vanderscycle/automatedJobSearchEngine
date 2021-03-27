#the cmd file to turn the script into an CLI program
import cmd
import os
# 
import pandas as pd
import numpy as np
# database module
import pymongo
# rich to make it pretty
from rich.console import Console
from rich import (
    pretty,
    traceback,
    print
)
from subprocess import (call,run)
# website handler
# https://docs.python.org/3/library/webbrowser.html
import webbrowser
# handles passwords
from dotenv import load_dotenv
# used to custom python import
from pathlib import Path
import sys
# importing custom mande pymongo connection function
BASE_DIR = Path(__file__).resolve().parent.parent.parent
pymongoFuncPath = 'jobEngineScraper/jobEngineScraper'
pymongoFuncPath = os.path.join(BASE_DIR,pymongoFuncPath)
sys.path.append(pymongoFuncPath)

from postProccessingDataCleaningNLP import (
    _connect_mongo,
    read_mongo
)

def update_mongo(db, collection,df, host='localhost', port=27017, username=None, password=None, no_id=False):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    conn = _connect_mongo(host=host, port=port, username=username, password=password, db=db)
    db = conn[db]
    # Make a query to the specific DB and Collection
    updates = []

    for _, row in df.iterrows():
        updates.append(pymongo.UpdateOne({'_id': row.get('_id')}, {'$set': {'filtered': row.get('filtered')}}, upsert=True))
        updates.append(pymongo.UpdateOne({'_id': row.get('_id')}, {'$set': {'applied': row.get('applied')}}, upsert=True))

    db[collection].bulk_write(updates)

class jobParser(cmd.Cmd):
    """sudo code
    fetch data from the db
    presents it in the cli
    asks how many job you want to apply to today
    check if you have applied to thet job already (whether that's not interreted or applied)
    asks if you want to apply
    - yes so opens a webpage to the job application, produces a cover letter, and updates the db to 
    - no updates the database and mark it as not interrested
    waits for your next command
    packages cmd/rich/pymongo"""
    intro = 'Welcome to the command line interactive data Structure program.\nType help or ? to list commands.\n'
    prompt = '(job engine) '


    def __init__(self):
        super(jobParser, self).__init__()
        self.console = Console()


    def do_mongoDBInfo(self, arg):
        """
        method where that will return a number of predetermined statistics about the number of job application in the db.
        """
        # types of collections 
        # numbers of job you have yet to apply

        df = read_mongo(MONGO_DATABASE,MONGO_COLLECTION,{}, no_id=True)
        print(f'jobs not yet viewed {len(df[df["applied"].isin([False])])} Jobs viewed {len(df[df["applied"].isin([True])])}')
        print(f'Out of the viewed jobs you rejected (so far): {len(df[df["filtered"].isin(["Rejected"])])} and applied to {len(df[df["filtered"].isin(["Applied"])])} ')


        
    def do_applyToJobs(self,line):
        """
        
        description:
            - method where you will pass an int
        """
        # fun stats
        numberOfApplication,collection = [arg for arg in line.split()]
        print(numberOfApplication,collection)
        applied = 0
        rejected = 0
        if not numberOfApplication or not numberOfApplication.isnumeric():
            print(f'you have entered {numberOfApplication} which is invalid')
            return 
        query = {"$and":[ {"site": 'stackOverflow'},{'applied':False}]} #we we should not filter per collection and instead per applied
        # fetching the info from the df and populating a dataFrame
        df = read_mongo(MONGO_DATABASE,MONGO_COLLECTION,query)
        # since mongo limit requires us to use a different synthax for the querry method it is easier to shrink the df
        df = df[:int(numberOfApplication)]
        for rowIndex, row in df.iterrows():
            print(f'job number: {rowIndex}')
            # printing the information
            for colIndex,col in row.iteritems():

                # we want to skip the unfiltered description
                # we could also drop the column from the df
                if colIndex == 'description':
                    pass

                else:
                    print(colIndex,col)

            answer = input("\nDo you want to apply for this job (y/n)?")
            if answer.lower() in ['y', 'yes']:
                # opens a webpage where job offer is hosted
                webbrowser.open_new_tab(row['url'])
                # need to integrate the cover letter
                df.at[rowIndex,'applied'] = True
                # sometimes it is possible that the spider did not scrape the right item so we must give flexibility to the user
                doubleCheck = input("If the job posting did not fit what you set the spider to do do you want to continue with the job posting (y/n)?")
                if doubleCheck.lower() in ['n', 'no']:
                    df.at[rowIndex,'filtered'] = 'Rejected' 
                    print(f'rejecting the job posting')
                    rejected+=1
                else:
                    df.at[rowIndex,'filtered'] = 'Applied' 
                    applied +=1
                    # git clone 
                    # https://stackoverflow.com/questions/1911109/how-do-i-clone-a-specific-git-branch
                    coverLetterFilePath = os.path.join(BASE_DIR,'Cover-Letter-Generator/') 
                    
                    call(["python", coverLetterFilePath + 'main.py'])
                    # /lowriter --headless --convert-to pdf *.docx
                    call(["lowriter --headless --convert-to pdf *.docx"],cwd= coverLetterFilePath + 'coverLetters/',shell=True)
                    call(["rm *.docx"],cwd= coverLetterFilePath + 'coverLetters/',shell=True)
            # lowriter --headless --convert-to pdf *.docx && rm *.docx
            else:
                print(f'rejecting the job posting')
                rejected+=1
                df.at[rowIndex,'filtered'] = 'Rejected' 
                df.at[rowIndex,'applied'] = True
        # db changes
        print(f'Done with the search. You have applied to {applied} jobs online and ignored {rejected} jobs')
        print('updating mongo database')
        print(df)
        update_mongo(MONGO_DATABASE,MONGO_COLLECTION,df)


    def default(self, line): 
        """
        Allows us to use the app as a normal commandline
        """
        try:
            return exec(line, globals())
        except:
            self.console.print_exception()


    def do_exit(self,arg):
        """
        exits the command line
        """
        exit()

if __name__ == '__main__':
    # setting the rich environment variables
    pretty.install()
    traceback.install()
    # loading the passwords
    load_dotenv()
    MONGO_IP = os.getenv('MONGO_IP')
    MONGO_PORT = int(os.getenv('MONGO_PORT'))
    MONGO_DATABASE = os.getenv('MONGO_DATABASE')
    MONGO_COLLECTION = 'stackOverflow'

    # since we will have multiple website we will scrape from multiple websites we should list them (from the db) and ask 


    # also should check the date when something was posted and then update it postedWhen += (now - (postedWhen + dateScraped))
    jobParser().cmdloop()
