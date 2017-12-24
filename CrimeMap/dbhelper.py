import pymysql

class DBHelper:
    def __init__(self, user, passwd, dbname, host='localhost'):
        self.user = user
        self.passwd = passwd
        self.dbname = dbname
        self.host = host
        self.connection = None

    def connect(self):
        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd,
            db=self.dbname
        )
        return self.connection

    def close_db(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_db()
        if exc_type:
            print(exc_value)
        return True
    