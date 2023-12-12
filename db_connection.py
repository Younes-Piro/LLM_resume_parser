from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os
_ = load_dotenv(find_dotenv()) # read local .env file

class DB:
    def __init__(self):
        self.client = MongoClient(os.environ['CONNECTION_STRING'])
        self.db = self.client[os.environ['DB']]
        self.collection = self.db[os.environ['COLLECTION']]

    def add_data(self, data):
        self.collection.insert_one(data)

