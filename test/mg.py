import pymongo

MONGO_URL = f"mongodb://127.0.0.1:27017/"

con = pymongo.MongoClient(MONGO_URL)
db = con['test_mongo']
table = db['record']
table.drop()
