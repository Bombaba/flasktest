import pymysql
import dbconfig

connection = pymysql.connect(host='localhost',
                             user=dbconfig.db_user,
                             passwd=dbconfig.db_password)

try:
    with connection.cursor() as  cursor:
        sql = f"CREATE DATABASE IF NOT EXISTS {dbconfig.db_name}"
        cursor.execute(sql)
        sql = f"""CREATE TABLE IF NOT EXISTS {dbconfig.db_name}.{dbconfig.db_table} (
id int NOT NULL AUTO_INCREMENT,
email VARCHAR(254),
salt VARCHAR(28),
hash VARCHAR(128),
updated_at TIMESTAMP,
PRIMARY KEY (id)
)"""
        cursor.execute(sql)
    connection.commit()
finally:
    connection.close()