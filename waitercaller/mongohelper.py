import pymongo
import passwordhelper as ph
import config
from bson.objectid import ObjectId
from user import User

class MongoHelper:

    def __init__(self, dbname):
        client = pymongo.MongoClient()
        self.db = client[dbname]
    
    def add_user(self, email, password):
        salt = ph.get_salt()
        hash = ph.get_hash(password + salt)
        try:
            self.db.users.insert({"email": email, "salt": salt, "hash": hash})
            return True
        except pymongo.errors.DuplicateKeyError:
            return False

    def get_user(self, email):
        user = self.db.users.find_one({"email": email})
        if user:
            return User(**user)
        else:
            return None

    def add_table(self, table_name, owner):
        new_id = self.db.tables.insert({
            'name': table_name,
            'owner': owner
        })
        self.db.tables.update(
            {'_id': new_id},
            {"$set": {'url': config.base_url + "newrequest/" + str(new_id)}}
        )

    def get_tables(self, owner):
        return list(self.db.tables.find({'owner': owner}))

    def get_table(self, table_id):
        return self.db.tables.find_one({'_id': ObjectId(table_id)})

    def delete_table(self, table_id):
        self.db.tables.remove({'_id': ObjectId(table_id)})

    def add_request(self, table_id, time):
        table = self.get_table(table_id)
        try:
            self.db.requests.insert(({
                'owner': table['owner'],
                'table_name': table['name'],
                'table_id': table_id,
                'time': time
            }))
            return True
        except pymongo.errors.DuplicateKeyError:
            return False
    
    def get_requests(self, owner):
        return list(self.db.requests.find({'owner': owner}))

    def delete_request(self, request_id):
        self.db.requests.remove({'_id': ObjectId(request_id)})
