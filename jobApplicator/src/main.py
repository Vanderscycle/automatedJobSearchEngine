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
print(pymongoFuncPath)

sys.path.append(pymongoFuncPath)

from postProccessingDataCleaningNLP import (
    _connect_mongo,
    read_mongo,
    update_mongo
)


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
    prompt = None

    def __init__(self):
        super(jobParser, self).__init__()
        pass

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
    query = {"site": "StackOverflow"}
    df = read_mongo(MONGO_DATABASE,MONGO_COLLECTION,query)
    url = 'google.com'
    webbrowser.open_new_tab(url)

