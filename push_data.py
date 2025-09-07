import os
import sys
import json
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")

import certifi
ca=certifi.where()
"""
certify-->It is a python package that provide root certificates
It is used by python libraries that need to make a secure http connection
ca is the certified authorities that used to ensure that site we are connecting 
to has a trusted certificate

"""
import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurtiyException
from networksecurity.logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurtiyException(e,sys)
        
    def cv_to_json_converter(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            #data.reset_index(drop=True,inplace=True)

            records=list(json.loads(data.T.to_json()).values())
            """
               .T transposes the DataFrame → swaps rows and columns.
               .to_json() Converts the DataFrame into a JSON string.
            json.loads(...) Converts that JSON string into a Python dictionary:
            Converts the dict values into a list of dictionaries:

            """
            return records
        except Exception as e:
            raise NetworkSecurtiyException(e,sys)

    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            # is what creates the connection to your MongoDB cluster.
            self.database=self.mongo_client[self.database]
            # self.mongo_client → is a MongoClient object that knows how to talk to MongoDB.
            self.collection=self.database[self.collection]
            # self.collection becomes a Collection object inside that database.
            self.collection.insert_many(self.records)
            
            return (len(self.records))
        except Exception as e:
            raise NetworkSecurtiyException(e,sys)


if __name__=='__main__':
    FILE_Path="Network_Data\phisingData.csv"
    DATABASE="Tridib"
    Collection="NetworkData"
    networkobj=NetworkDataExtract()
    records=networkobj.cv_to_json_converter(file_path=FILE_Path)
    print(records)
    no_of_records=networkobj.insert_data_mongodb(records,DATABASE,Collection)
    print(no_of_records)