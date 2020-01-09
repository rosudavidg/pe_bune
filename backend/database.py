import datetime
import security
import json
import error
import mysql.connector
import email_module
from models.user import User

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
            raise Exception(error.Error.new(e))
        finally:
            cursor.close()

    def send_activation_link(self, email):
        try:
            cursor = self.db.cursor()
            token = cursor.callproc('get_activation_token', (email, ''))[1]

            email_module.send_activation_link(email, token)
        except Exception as e:
            raise Exception(error.Error.new(e))
        finally:
            cursor.close()
    
    def confirm_user(self, token):
        try:
            cursor = self.db.cursor()

            confirmed = cursor.callproc('confirm_user', (token, ''))[1]
            
            return confirmed
        except Exception as e:
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
            raise Exception(error.Error.new(e))
        finally:
            cursor.close()

    def get_quizzes(self):
        try:
            cursor = self.db.cursor()
            cursor.callproc('select_quizzes')

            ans = []
            d = {}

            for result in cursor.stored_results():
                ans += result.fetchall()
            
            for a in ans:
                d[a[0]] = {
                    'category' : a[1],
                    'question': a[2],
                    'correct_answer': a[3],
                    'other_answer_1': a[4],
                    'other_answer_2': a[5]
                }

            return d
        except Exception as e:
            raise Exception(error.Error.new(e))
        finally:
            cursor.close()

    def get_leaderboard(self):
        try:
            cursor = self.db.cursor()
            cursor.callproc('get_leaderboard')

            ans = []
            d = {}

            for result in cursor.stored_results():
                ans += result.fetchall()
            
            for a in ans:
                d[a[0]] = {
                    'num' : a[0],
                    'username': a[1],
                    'level': a[2],
                    'experience': a[3]
                }

            return d
        except Exception as e:
            raise Exception(error.Error.new(e))
        finally:
            cursor.close()
        
    def delete_quiz(self, id):
        try:
            cursor = self.db.cursor()
            cursor.callproc('delete_quiz', (id, ))

        except Exception as e:
            raise Exception(error.Error.new(e))
        finally:
            cursor.close()

    def add_quiz(self, category, question, correct_answer, other_answer_1, other_answer_2):
        try:
            cursor = self.db.cursor()
            cursor.callproc('add_quiz', (category, question, correct_answer, other_answer_1, other_answer_2))
        except Exception as e:
            raise Exception(error.Error.new(e))
        finally:
            cursor.close()
    
    def token_is_valid(self, token):
        try:
            cursor = self.db.cursor()
            is_valid = cursor.callproc('check_token', (token, ''))[1]

            if is_valid == True:
                return token.split(':')[0]
            return None
        except Exception as e:
            raise Exception(error.Error.new(e))
        finally:
            cursor.close()

    def is_user_logged_in(self, request):
        if request == None:
            return None
        if request.cookies == None:
            return None
        if 'pebune_token' not in request.cookies:
            return None
        
        token = request.cookies['pebune_token']

        return self.token_is_valid(token)

    def is_user_admin(self, username):
        if username == None:
            return None
        
        try:
            cursor = self.db.cursor()
            return cursor.callproc('is_user_admin', (username, ''))[1]
        except Exception as e:
            raise Exception(error.Error.new(e))
        finally:
            cursor.close()

    def game_exists(self, username):
        if username == None:
            return None
        
        try:
            cursor = self.db.cursor()
            return cursor.callproc('game_exists', (username, ''))[1]
        except Exception as e:
            raise Exception(error.Error.new(e))
        finally:
            cursor.close()
    
    def create_game(self, username):
        if username == None:
            return None
        
        try:
            cursor = self.db.cursor()
            return cursor.callproc('create_game', (username, ''))[1]
        except Exception as e:
            raise Exception(error.Error.new(e))
        finally:
            cursor.close()
    
    def get_game_id(self, username):
        if username == None:
            return None
        
        try:
            cursor = self.db.cursor()
            return cursor.callproc('get_game_id', (username, ''))[1]
        except Exception as e:
            raise Exception(error.Error.new(e))
        finally:
            cursor.close()

    def get_user(self, username):
        cursor = self.db.cursor()

        res = cursor.callproc('get_user', (username, '', '', '', '', ''))
        
        user = User(username, res[2], res[3], res[1], res[4], res[5])
        
        return user

    def get_game_quizzes(self, game_id):
        try:
            cursor = self.db.cursor()
            cursor.callproc('get_game_quizzes', (game_id,))

            ans = []
            d = []

            for result in cursor.stored_results():
                ans += result.fetchall()
            
            for a in ans:
                d.append({
                    'quiz_id' : a[0],
                    'answered': a[1],
                    'correct' : a[2]
                    }
                )

            return d
        except Exception as e:
            raise Exception(error.Error.new(e))
        finally:
            cursor.close()

    def get_category(self, quiz_id):
        try:
            cursor = self.db.cursor()

            return cursor.callproc('get_category', (quiz_id, ''))[1]
        except Exception as e:
            raise Exception(error.Error.new(e))
        finally:
            cursor.close()
    
    def get_quiz(self, quiz_id):
        try:
            cursor = self.db.cursor()

            res = cursor.callproc('get_quiz', (quiz_id, '', '', '', ''))

            d = [res[1],
                {'text':res[2], 'correct': True},
                {'text':res[3], 'correct': False},
                {'text':res[4], 'correct': False}]

            return d
        except Exception as e:
            raise Exception(error.Error.new(e))
        finally:
            cursor.close()
    
    def answer_quiz(self, username, quiz_id, correct, time):
        try:
            cursor = self.db.cursor()

            cursor.callproc('answer_quiz', (quiz_id, username, correct, time))
        except Exception as e:
            raise Exception(error.Error.new(e))
        finally:
            cursor.close()

    def end_game(self, game_id):
        try:
            cursor = self.db.cursor()

            cursor.callproc('end_game', (game_id, ))
        except Exception as e:
            raise Exception(error.Error.new(e))
        finally:
            cursor.close()

    def get_stats(self, username):
        try:
            cursor = self.db.cursor()

            res = cursor.callproc('get_stats', (username, '', '', ''))

            games_played = res[1]
            correct_answers = res[2]
            wrong_answers = res[3]

            return games_played, correct_answers, wrong_answers
        except Exception as e:
            raise Exception(error.Error.new(e))
        finally:
            cursor.close()
    
    def logout(self, username):
        try:
            cursor = self.db.cursor()
            cursor.callproc('logout', (username,))
        except Exception as e:
            raise Exception(error.Error.new(e))
        finally:
            cursor.close()
    