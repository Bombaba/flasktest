import pymongo
import config
client = pymongo.MongoClient()
c = client[config.DB_NAME]
print(c.users.create_index('email', unique=True))
print(c.requests.create_index('table_id', unique=True))
