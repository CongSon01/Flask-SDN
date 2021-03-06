from pymongo import MongoClient

# mongo_uri = "mongodb://username:" + urllib.quote("p@ssword") + "@127.0.0.1:27001/"
mongo_uri = "mongodb://localhost:27017/"
connection = MongoClient(mongo_uri)

# CREATE DATABASE
database = connection['SDN_data']
# CREATE COLLECTION
collection = database['Version']
# print("Database connected")

def insert_data(data):
    """
    Insert new data or document in collection
    :param data:
    :return:
    """
    collection.insert(data)
    return

def get_version_max():
    # return collection.find({},{"version":1, "_id":0}).sort("version", -1).limit(1)
    return collection.find_one(sort=[("version", -1)])
    # return collection.find().sort({"version":-1}).limit(1)

def get_version_data(version_max):
    data = collection.find({"version":{ "$gte": version_max }}, {"version":1, "_id":0})
    return list(data)

def get_multiple_data():
    """
    get document data by document ID
    :return:
    """
    data = collection.find()
    return list(data)


# CLOSE DATABASE
connection.close()