from dbhelper import DBHelper
import dbconfig

class DBCrime(DBHelper):
    def __init__(self):
        super().__init__(dbconfig.db_user,
                         dbconfig.db_password,
                         'crimemap',
                         'localhost')

    def get_all_inputs(self):
        with self as connection:
            query = "SELECT description FROM crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)
            return cursor.fetchall()
    
    def add_input(self, data):
        with self as connection:
            query = "INSERT INTO crimes (description) VALUES (%s);"
            with connection.cursor() as cursor:
                cursor.execute(query, data)
                connection.commit()

    def clear_all(self):
        with self as connection:
            query = "DELETE FROM crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
