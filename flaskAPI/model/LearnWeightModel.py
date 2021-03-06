from pymongo import MongoClient

# mongo_uri = "mongodb://username:" + urllib.quote("p@ssword") + "@127.0.0.1:27001/"
mongo_uri = "mongodb://localhost:27017/"
connection = MongoClient(mongo_uri)

# CREATE DATABASE
database = connection['SDN_data']
# CREATE COLLECTION
collection = database['LearnWeightModel']
# print("Database connected")

def is_data_exit(data_search):
    return collection.count_documents({'src': data_search['src'], 'dst': data_search['dst']}, limit=1)

def insert_data(data):
    """
    Insert new data or document in collection
    :param data:
    :return:
    """
    collection.insert(data)
    return

def get_label(src, dest):
    try:
        kq = int(list(collection.find({'src': src, 'dst': dest}))[0]['label'])
    except:
        kq = 0
    return kq

def update_many(data_search, data_update):
    collection.update_many(data_search, {'$set': data_update})
    return 

def insert_n_data(list_data):
    if len(list_data) == 0:
        return
    else:
        collection.insert_many(list_data)


def get_multiple_data():
    """
    get document data by document ID
    :return:
    """
    data = collection.find()
    return list(data)


# CLOSE DATABASE
connection.close()