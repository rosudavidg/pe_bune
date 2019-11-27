import datetime
import security
import json
import error
import mysql.connector
import email_module

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
        self.db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            database=self.database,
            auth_plugin='mysql_native_password'
        )

    def register(self, username, password, email, first_name, last_name):
        try: 
            cursor = self.db.cursor()
            cursor.callproc('create_user', [username, security.encrypt_password(password), email, first_name, last_name, security.activation_token()])
        except Exception as e:
            print(e)
            raise Exception(error.Error.new(e))
        finally:
            cursor.close()

    def send_activation_link(self, email):
        try:
            cursor = self.db.cursor()
            token = cursor.callproc('get_activation_token', (email, ''))[1]

            email_module.send_activation_link(email, token)
        except Exception as e:
            print(e)
            raise Exception(error.Error.new(e))
        finally:
            cursor.close()
    
    def confirm_user(self, token):
        try:
            cursor = self.db.cursor()

            confirmed = cursor.callproc('confirm_user', (token, ''))[1]
            
            return confirmed
        except Exception as e:
            print(e)
            raise Exception(error.Error.new(e))
        finally:
            cursor.close()
    
    def login(self, username, password):
        try:
            # Verificare existenta user
            cursor = self.db.cursor()
            hashed = cursor.callproc('get_password', (username, ''))[1]
            
            if hashed == None:
                return None

            # Verificare parola
            if not security.check_encrypted_password(password, hashed):
                return None

            # Verificare cont activ
            is_active = cursor.callproc('is_active', (username, ''))[1]

            if not is_active:
                return None

            # Stergere sesiuni vechi
            cursor.callproc('delete_sessions', (username, ))

            # Adaugare sesiune
            token = security.login_token(username)
            expiration_date = cursor.callproc('create_session', (username, token, ''))[2]

            return (token, expiration_date)
        except Exception as e:
            print(e)
            raise Exception(error.Error.new(e))
        finally:
            cursor.close()
