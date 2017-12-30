import dbconfig
import passwordhelper
from user import User
from dbhelper import DBHelper

MOCK_USERS = {'test@example.com': '123456'}

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
                    if user:
                        return User(email, user[0], user[1])
                    else:
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