from flask_mysqldb import MySQL
mysql = MySQL()
class Config():
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'zzharrybin219'
    MYSQL_DB = 'demo'
    MYSQL_DATABASE_PORT = 3306