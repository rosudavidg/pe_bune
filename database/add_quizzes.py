# import datetime
import json
import mysql.connector


INPUT_FILENAME = 'quizzes.json'


class DB():
    def __init__(self):
        config = None

        try:
            with open('../backend/config.json', 'rt') as inputfile:
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

    def add_quiz(self, category, question, correct_answer, wrong_answer_1, wrong_answer_2):
        try: 
            cursor = self.db.cursor()
            cursor.callproc('add_quiz', [category, question, correct_answer, wrong_answer_1, wrong_answer_2])
        except Exception as e:
            raise Exception('Cannot add quiz!')
        finally:
            cursor.close()


def read_input_data():
    # Read input data
    with open(INPUT_FILENAME, 'rt', encoding="utf-8-sig") as f:
        return json.load(f)


def add_quiz(db, quiz):
    # Parse quiz
    question = quiz['question']
    correct_answer = quiz['correct_answer']
    wrong_answer_1 = quiz['wrong_answer_1']
    wrong_answer_2 = quiz['wrong_answer_2']
    category = quiz['category']

    db.add_quiz(category, question, correct_answer, wrong_answer_1, wrong_answer_2)


if __name__ == '__main__':
    # Read input data
    quizzes = read_input_data()
     
    # Create connection to database
    db = DB()

    # Add quizzes
    for quiz in quizzes:
        add_quiz(db, quiz)
