import datetime
import config
import dbconfig
import passwordhelper
from user import User
from dbhelper import DBHelper

MOCK_USERS = {'test@example.com': '123456'}
MOCK_TABLES = [
    {
        "_id": passwordhelper.get_hash("1"),
        "name": "1",
        "owner": "test@example.com",
        "url": "mockurl"
    }
]
MOCK_REQUESTS = [
    {
        "_id": "1",
        "table_id": "1",
        "table_name": "1",
        "time": datetime.datetime.now()
    }
]

class MockLoginDB(DBHelper):
    def __init__(self):
        super().__init__(dbconfig.db_user,
                         dbconfig.db_password,
                         dbconfig.db_name,
                         'localhost')

    def get_user(self, email):
        with self as connection:
            query = "SELECT salt, hash FROM users WHERE email=%s;"
            with connection.cursor() as cursor:
                cursor.execute(query, email)
                for user in cursor:
                    return User(email, user[0], user[1])
                return None

    def add_user(self, email, password):
        salt = passwordhelper.get_salt()
        hash = passwordhelper.get_hash(password + salt)
        with self as connection:
            query = f"INSERT INTO users (email, salt, hash)" \
                     "Values (%s, %s, %s);"
            with connection.cursor() as cursor:
                cursor.execute(query, (email, salt, hash))
                connection.commit()
                return True
        return False

    def add_table(self, table_name, owner_id):
        _id = passwordhelper.get_hash(owner_id + table_name)[:5]
        MOCK_TABLES.append({
            "_id": _id,
            "name": table_name,
            "owner": owner_id,
            "url": config.base_url + "newrequest/" + _id
        })
        return _id

    def get_tables(self, owner_id):
        return MOCK_TABLES

    #def update_table(self, table_id, url):
    #    for table in MOCK_TABLES:
    #        if table.get("_id") == table_id:
    #            table["url"] = url
    #            break

    def delete_table(self, table_id):
        for i, table in enumerate(MOCK_TABLES):
            if table["_id"] == table_id:
                del MOCK_TABLES[i]
                return True
        return False

    def add_request(self, table_id, time):
        for table in MOCK_TABLES:
            if table["_id"] == table_id:
                break
        else:
            return False
        for i, req in enumerate(MOCK_REQUESTS):
            if req["table_id"] == table_id:
                del MOCK_REQUESTS[i]
                break
        _id = passwordhelper.get_hash(table_id)[:5]
        MOCK_REQUESTS.append({
            "_id": _id,
            "table_id": table["_id"],
            "table_name": table["name"],
            "time": time
        })
        return True

    def get_requests(self, owner_id):
        return MOCK_REQUESTS

    def delete_request(self, request_id):
        for i, request in enumerate(MOCK_REQUESTS):
            if request["_id"] == request_id:
                del MOCK_REQUESTS[i]
                return True
        return False
