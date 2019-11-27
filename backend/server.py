from flask import Flask
from flask import render_template, make_response, request, json, send_from_directory
import json
import connexion
import database
import datetime
import time
import os
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "dabumts secret key"
CORS(app, supports_credentials=True)
config = None

@app.route('/home', methods=['POST', 'GET'])
def home():
    try:
        # TODO: Check if user is logged in
        if request.cookies['pebune_token']:
            data = database.DB().get_quizzes()
            resp = make_response(render_template('home.html', result=data))
            return resp, 200


        # Check if user just logged in
        username = request.form['username']
        password = request.form['password']

        res = database.DB().login(username, password)
        
        if res == None:
            return render_template('login.html', result=request.form), 403
        
        token, expiration_date = res
        resp = make_response(render_template('home.html', result=request.form))

        resp.set_cookie(key='pebune_token',
            value=token,
            expires=datetime.datetime.strptime(expiration_date, '%Y-%m-%d %H:%M:%S'),
            httponly=False)

        # Compute quizzes
        data = database.DB().get_quizzes()
        resp = make_response(render_template('home.html', result=data))

        return resp, 200
    except Exception as e:
        print(e)
        return render_template('login.html'), 200

    # print(request.form)
    return render_template('home.html', result=request.form)

@app.route('/delete', methods=['POST', 'GET'])
def web_delete():
    try:
        question_id = request.form['question_id']

        database.DB().delete_quiz(question_id)

        data = database.DB().get_quizzes()
        resp = make_response(render_template('home.html', result=data))

        return resp, 200
    except Exception as e:
        print(e)
        return render_template('login.html'), 200

    # print(request.form)
    return render_template('home.html', result=request.form)

@app.route('/add', methods=['POST', 'GET'])
def web_add():
    try:
        question = request.form['question']
        correct_answer = request.form['correct_answer']
        wrong_answer_1 = request.form['wrong_answer_1']
        wrong_answer_2 = request.form['wrong_answer_2']

        database.DB().add_quiz(question, correct_answer, wrong_answer_1, wrong_answer_2)

        data = database.DB().get_quizzes()
        resp = make_response(render_template('home.html', result=data))

        return resp, 200
    except Exception as e:
        print(e)
        return render_template('login.html'), 200

    # print(request.form)
    return render_template('home.html', result=request.form)

@app.route('/login')
def web_login():
    return render_template('login.html')

@app.route('/')
def web_root():
    return render_template('login.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'templates'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/api/register', methods=['POST'])
def register():
    resp = make_response()

    if request == None:
        return resp, 400
    
    if request.json == None:
        return resp, 400

    if 'username' not in request.json \
        or 'password' not in request.json \
        or 'email' not in request.json \
        or 'first_name' not in request.json \
        or 'last_name' not in request.json:
        return resp, 400

    try:
        database.DB().register(request.json['username'],
            request.json['password'],
            request.json['email'],
            request.json['first_name'],
            request.json['last_name'])
        
        database.DB().send_activation_link(request.json['email'])

        return resp, 200
    except Exception as e:
        resp = app.response_class(
            response=json.dumps(
                {
                    'error' : str(e)
                }
            ),
            mimetype='application/json'
        )

        return resp, 400

@app.route('/api/confirm/<token>', methods=['GET'])
def confirm(token):
    resp = make_response()
    
    try:
        result = database.DB().confirm_user(token)
        
        if result:
            return render_template('confirm.html', message='Email confirmed!'), 200
        else:
            return render_template('confirm.html', message='This link is not valid.'), 410

    except Exception as e:
        resp = app.response_class(
            response=json.dumps(
                {
                    'error' : str(e)
                }
            ),
            mimetype='application/json'
        )

        return resp, 404

@app.route('/api/login', methods=['POST'])
def login():
    resp = make_response()

    if request == None:
        return resp, 400
    
    if request.json == None:
        return resp, 400

    if 'username' not in request.json \
        or 'password' not in request.json:
        return resp, 400

    try:
        res = database.DB().login(request.json['username'],
            request.json['password'])
        
        if res == None:
            return resp, 403
        
        token, expiration_date = res

        resp.set_cookie(key='pebune_token',
            value=token,
            expires=datetime.datetime.strptime(expiration_date, '%Y-%m-%d %H:%M:%S'),
            httponly=False)

        return resp, 200
    except Exception as e:
        resp = app.response_class(
            response=json.dumps(
                {
                    'error' : str(e)
                }
            ),
            mimetype='application/json'
        )

        return resp, 400

if __name__ == '__main__':
    try:
        with open('config.json', 'rt') as inputfile:
            config = json.load(inputfile)
    except Exception:
        print('ERROR: Configuration file is missing!')
        exit(-1)

    app.run(host=config['backend']['host'],
            port=config['backend']['port'], debug=True)#, ssl_context='adhoc')
