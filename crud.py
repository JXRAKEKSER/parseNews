import pymongo;
from pymongo import MongoClient

client = MongoClient('localhost', 27017);

db = client['news'];

collection = db['parseNews'];

def insertData(collection, data):
    return collection.insert_one(data)

def findData(collection, data):
    return collection.find_one(data);