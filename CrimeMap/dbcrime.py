import datetime
import dbconfig
from dbhelper import DBHelper

class DBCrime(DBHelper):
    def __init__(self):
        super().__init__(dbconfig.db_user,
                         dbconfig.db_password,
                         'crimemap',
                         'localhost')

    def add_crime(self, category, date,
                  latitude, longitude, description):
        with self as connection:
            query = \
              "INSERT INTO crimes (category, date, latitude, longitude, description)" \
              "VALUES (%s, %s, %s, %s, %s)"
            with connection.cursor() as cursor:
                cursor.execute(
                  query,
                  (category, date, latitude, longitude, description)
                )
                connection.commit()

    def get_all_crimes(self):
        cols = ('latitude', 'longitude', 'date', 'category', 'description')
        with self as connection:
            query = "SELECT latitude, longitude, date, category, description FROM crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)
            named_crimes = []
            for crime in cursor:
                named_crime = {col: val for col, val in zip(cols, crime)}
                named_crime['date'] = datetime.datetime.strftime(
                    named_crime['date'], "%Y-%m-%d")
                named_crimes.append(named_crime)
            return named_crimes

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
