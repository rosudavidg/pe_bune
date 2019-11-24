import pymysql
import datetime
import security
import json
import error

class DB():
    def __init__(self):
        config = None

        try:
            with open('config.json', 'rt') as inputfile:
                config = json.load(inputfile)
        except Exception:
            print('ERROR: Configuration file is missing!')
            exit(-1)

        self.host = config['database']['host']
        self.database = config['database']['database']
        self.user = config['database']['user']
        self.password = config['database']['password']
        self.connect()

    def connect(self):
        self.db = pymysql.connect(
            self.host,
            self.user,
            self.password,
            self.database
        )

    def query(self, sql):
        cursor = self.db.cursor()
        cursor.execute(sql)

        return cursor

    def register(self, username, password, email, first_name, last_name):
        try:
            cursor = self.db.cursor(pymysql.cursors.DictCursor)
            cursor.callproc('create_new_user', [username, security.encrypt_password(password), email, first_name, last_name])
        except Exception as e:
            raise Exception(error.Error.new(e))
        finally:
            cursor.close()
