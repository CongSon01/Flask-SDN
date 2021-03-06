from pymongo import MongoClient
import os
def get_database():
    
    # mongo_uri = "mongodb://username:" + urllib.quote("p@ssword") + "@127.0.0.1:27001/"

    # CREATE DATABASE
    database = os.environ.get('DATABASE')
    return database

def get_connect():
    mongo_uri = os.environ.get('MONGO_URL')
    connection = MongoClient(mongo_uri)
    return connection



db.find_one_and_update({"src": "of:0000000000000006",
                        "dst":"of:0000000000000005"}, 
                                 {"linkVersion": 100})